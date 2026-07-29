# Flow Verification 03: Material Weighing

## Scope and Conclusion

This document verifies the fifth macro stage of the planned SCAL map: `称料`.

There are two modules with similar names, but they are not one end-to-end process:

```text
Warehouse "收料称重"
  -> product and pending-lot query only in the verified web API surface

Manufacturing "原料称重"
  -> dispatched, line-side Lot
  -> physical weighing or exempt weighing
  -> W-suffixed weighed Lot split
  -> WeighingHistory and weighed-label output
  -> optional independent review
  -> report / BPR consumption traceability
```

The production workflow is implemented by the CS `IssueMaterial` module and the `Pro_IssueMaterial_Confirm*_News` procedure family. It only accepts a lot that has a matching manufacturing-order dispatch record and `LotEstate = 10` (the procedure's line-side-material condition). It creates a new weighed lot whose number begins with the original `LotNM + "W"`, keeps a weighing-history row for both the new and residual original lot, and splits the dispatch trace to the new lot.

The map may place `称料` after `上料` because that is the requested business macro sequence. The code does **not** make PDA physical loading (`ProductLineLoadedMaterial` / `LOADMA`) a prerequisite for the weighing procedure. Its enforced predecessor is `发料到工单 + 在线边仓`; the physical-loading and weighing routes must therefore be shown as related production operations, not as a hard program-enforced serial dependency.

## Primary Flow

```text
Lot dispatched to MfgOrder
  + LotEstate = 10 (line-side material)
  -> CS selects MfgOrder and scans original LotNM
  -> process-spec step, unit, container, station, scale weight
  -> limit / unit-conversion / authorization validation
  -> Pro_IssueMaterial_Confirm_News (physical weighing)
     or Pro_IssueMaterial_Confirm2_News (exempt weighing)
  -> Pro_Tran_WeightingSplitIssueMaterial
  -> original Lot residual + new LotNM-Wxxx
  -> Pro_Tran_Weighing_News, twice
  -> WeighingHistory: original Status = 0; new Status = 1
  -> Pro_STD_Tran_DispatchSplit
  -> weighed-label printing and downstream BPR/report query

Optional, independently configured review:
  scan weighed label -> e-signature / optional dual check
  -> update WeighingHistory.CheckEquipmentNM, CheckUserNM, CheckDate, Remark
```

`LotNM` and `MfgOrderNM` remain the principal join keys. `ProcessSpecStepId` connects the measured quantity to the recipe/BPR requirement. `WeighingHistoryId` is the review record key.

## Node Verification

| Node | Status | Verified behavior |
| --- | --- | --- |
| Warehouse receipt weighing | Separate query-only surface | `CKZY_MaterialWeighingController` exposes only product lookup and `GetWeighingList`; its BLL/DAL call `Pro_MaterialWeighing_GetWeighingList_New`. Do not render it as the manufacturing split-and-trace workflow without further evidence. |
| Manufacturing weighing UI | Verified | CS `frmME_IssueMaterial` opens `frmME_IssueMaterial_Weighting`. The weight form reads a scale value, records tare, net, and gross weight, and initializes the weighing-device connection. |
| Manufacturing-order and lot entry | Verified | `Pro_IssueMaterial_Confirm_News` rejects an empty manufacturing order, unit, lot number, or physical net weight. The UI/DAL submits the manufacturing order, station, process-spec step, equipment, container, user, weight values, and timestamp fields. |
| Dispatched and line-side prerequisites | System-enforced | The confirm procedure requires a matching active `DispatchHistory` row for the same `LotNM` and `MfgOrderNM`, rejects zero dispatched quantity, and rejects a lot whose `LotEstate` is not `10`. |
| Unit and recipe controls | System-enforced | The procedure resolves the process-step unit, requires a configured unit conversion where needed, aggregates prior active `WeighingHistory` quantity by product, manufacturing order, and process-spec step, and compares it to the configured maximum. |
| Over-limit authorization | System-enforced | Over-limit weighing requires a supervisor account, password, and reason. The procedure verifies the account and supervisor privilege before continuing. |
| Physical weighing submit | Verified | Shared CS DAL `Confirm` calls `Pro_IssueMaterial_Confirm_News`; it supplies physical net/tare/gross values and returns the generated lot number. |
| Exempt weighing submit | Verified | Shared CS DAL `ConfirmPass` calls `Pro_IssueMaterial_Confirm2_News`. This route derives the weight from the original lot but follows the same split-and-history model. |
| Weighed lot split | System-enforced | The physical route sets split reason `配制称重`, generates a unique `LotNM + W...` barcode, and calls `Pro_Tran_WeightingSplitIssueMaterial` with weight, unit, resource, user, verifier, equipment, container, expiry, and manufacturing-order context. |
| Weighing history | System-enforced | The confirm procedure calls `Pro_Tran_Weighing_News` for the new weighed lot with `Status = 1`, then for the original residual lot with `Status = 0`. The history table documents this status meaning directly. |
| Dispatch trace handoff | System-enforced | After splitting, the confirm procedure calls `Pro_STD_Tran_DispatchSplit` with original lot, new weighed lot, quantity, user, and station. This transfers the manufacturing-order dispatch trace to the weighed lot. |
| Review / recheck | Optional configurable control | `frmME_IssueMaterialCheck` checks `ESignatureValid("IssueMaterialCheck", "Confirm")` and its double-check setting. On success it writes review equipment, reviewer, time, and remark back to the selected `WeighingHistory` row. |
| Cancellation | Verified as controlled reversal route | `frmME_IssueMaterial` first calls `CheckCancel`, can require an `IssueMaterial/Cancel` electronic signature, then invokes its cancel data-access operation. The database scripts include `Pro_IssueMaterial_Cancel` and `UndoWeighingHistory`; the final map should show this as a guarded correction/reversal branch rather than a normal forward node. |
| Reporting / BPR use | Verified | `Pro_Report_GetWeighingListByMfgOrderNMQuery_New` reads active (`Status = 1`) weighing records together with process-step, operator, verifier, and weight fields. BPR procedures also query `WeighingHistory` for material-weight validation and material information. |

## Enforced Validation and Split Effects

`Pro_IssueMaterial_Confirm_News` applies the following rules before writing data:

1. A manufacturing order, unit, scanned source lot, and non-zero net weight are required.
2. `DispatchHistory` must show the source lot has been issued to that same manufacturing order; its issued quantity must be positive.
3. The source lot must have `LotEstate = 10`, described by the procedure as material at the line-side warehouse.
4. The requested unit must match the process-spec unit or have a configured conversion.
5. Previously active weighing amounts for the same product, manufacturing order, and process-spec step are accumulated and compared to the recipe maximum.
6. An over-limit result requires a valid supervisor credential and an over-limit reason.

On success it uses `GetTableNextMaxIdByTableName2` to create a new number under `originalLotNM + "W"`, for example `originalLotNMW001`. `Pro_Tran_WeightingSplitIssueMaterial` performs the inventory/lot split. The caller then records the two views of the operation:

```text
new W lot:  TxnId = PreWeighing, Status = 1, MfgOrderNM populated,
            measured net/gross/tare, equipment, container, operator/verifier,
            process-spec step and pre-weigh expiry

original lot: TxnId = PreWeighing, Status = 0, residual weights,
              source-lot trace retained
```

Finally, `Pro_STD_Tran_DispatchSplit` writes the corresponding dispatch split. This is the code-level bridge from the issued source material to the newly weighed material label, rather than a mere print-label operation.

## Review, Signatures, and Audit Boundary

The main confirmation payload includes `VerifyUserCode` and a confirmation time, and `WeighingHistory` has `VerifyPersonNM` and `IssueMaterialdoubleCheckerTime` fields. In addition, the separate `frmME_IssueMaterialCheck` workflow provides later review:

```text
scan weighed LotNM
  -> IssueMaterialCheckDAL reads WeighingHistory
  -> configured ESignature
  -> optional ESignatrueVerify dual check
  -> EditWeighingHistoryCheckInfo
  -> CheckEquipmentNM / CheckUserNM / CheckDate / Remark
```

Electronic signature and dual check are configuration-dependent. They should be rendered as a guarded optional control node, not as an unconditional gate on every weighing result. The cancellation action is separately configurable for electronic signature and audit trail; it should connect to an `UndoWeighingHistory` correction branch.

## Traceability Records

The documented `WeighingHistory` schema contains the complete evidence set needed by the interactive map:

- transaction/history identifiers and transaction station/user;
- manufacturing order, product, production batch, lot ID, and `LotNM`;
- net, gross, tare, unit, weighing person, verifier, equipment, container, and expiry;
- process-spec step, over-limit supervisor/reason, precision, and BPR identifier;
- `Status` (`0` original lot, `1` new lot), weighing time, confirmation time, flag; and
- recheck equipment, reviewer, remark, and recheck time.

This makes `WeighingHistory` the main record opened by the `称料` macro-node. `Lot`, `DispatchHistory`, dispatch-split records, `HistoryMainLine`, and BPR/report procedures are linked evidence rather than substitutes for it.

## Relationship to Material Loading

The previously verified physical-loading route requires a confirmed dispatch record and persists `ProductLineLoadedMaterial` plus `LOADMA` histories. The weighing route independently requires a dispatched lot in line-side status and persists a split lot plus `PreWeighing` histories.

Therefore render the map as follows:

```text
发料 / 领料确认
  -> 产线上料 (PDA LOADMA)                 [physical attachment route]
  -> 原料称重 (CS PreWeighing)             [weighed-material preparation route]

原料称重 -> W 称量批次 -> 配置/生产记录
```

At the macro level, display `上料 -> 称料` as the selected business sequence. At the detailed level, mark the link `业务主流程假设` unless a factory-specific SOP confirms that every `LOADMA` must precede every `PreWeighing`; the source code only proves the dispatch and line-side prerequisites above.

## Source Map

| Layer | Main evidence |
| --- | --- |
| Web MES | `CKZY_MaterialWeighingController`, BLL, DAL, and `CKZY_MaterialWeighing` view. |
| Desktop MES | `frmME_IssueMaterial`, `frmME_IssueMaterial_Weighting`, `frmME_IssueMaterialCheck`, and `MESZZZX_IssueMaterialDAL`. |
| Database | `Pro_IssueMaterial_Confirm_News`, `Pro_IssueMaterial_Confirm2_News`, `Pro_Tran_WeightingSplitIssueMaterial`, `Pro_Tran_Weighing_News`, `Pro_STD_Tran_DispatchSplit`, and `Pro_IssueMaterial_Cancel`. |
| DOC table pages | `WeighingHistory`, `UndoWeighingHistory`, `Lot`, `DispatchHistory`, `HistoryMainLine`, and BPR/report-related tables. |

## Map Rendering Guidance

Render solid links for the verified manufacturing route:

```text
已发料在线边仓批次 -> 扫描原批次 / 选择工单
扫描原批次 -> 读取工艺步骤与称量设备 -> 实称或免称
实称或免称 -> W 称量批次拆分 -> WeighingHistory（原批次 / 新批次）
W 称量批次 -> 发料记录拆分 -> 称量标签 / BPR 称量报表
```

Render these as guarded branches:

```text
累计超量 -> 主管授权 + 原因 -> 提交
称量标签 -> 电子签名复核 / 可选双人复核 -> WeighingHistory 复核字段
称量记录 -> 取消前校验 + 电子签名 / 审计追踪 -> UndoWeighingHistory
```

Render warehouse `收料称重` as a separate small node under procurement/receipt support, labelled `待称批次查询（已验证）`; do not join it to the manufacturing W-lot split flow.

## Remaining Verification Work

1. Verify the exact configuration records that decide whether `IssueMaterial` confirmation itself requires electronic signature or dual check.
2. Verify which downstream configuration/production-output operation consumes the W-suffixed lot at each target site.
3. Confirm the final cancellation procedure's full inventory and dispatch restoration behavior before presenting it as an automatically reversible operation.
