# Flow Verification 02: Material Loading

## Scope and Conclusion

This document verifies the fourth macro stage of the planned SCAL map: `上料`.

The implementation distinguishes four related operations. They must not be shown as one indistinguishable "material issue" box:

```text
工单 / 发料单
  -> PDA 扫码发料
  -> 领料确认
  -> PDA 产线实际上料
  -> 产线已装料记录与上料历史

旧版资源挂料
  -> ResourceLoadedMaterial2

CS 原料称重
  -> 称料阶段（下一宏观阶段，不属于本上料主线）
```

The verified modern route is `发料 -> 领料确认 -> 产线上料`. A material cannot be loaded through `Pro_PDA_ProductLineLoadMaterial_DoLoad` until it has an eligible, confirmed dispatch record. The legacy resource-loading route remains in the PDA backend and should be rendered as a version/site-specific branch.

## Primary Flow

```text
Released inventory Lot
  -> DispatchMaterialOrder (MfgOrderNM, ProductNM, Qty)
  -> PDA selects dispatch order and scans LotNM
  -> Pro_PDA_DispatcheOrder_DispatchLot
  -> CurrentStatus2 / dispatch quantity / DispatchState
  -> dispatch confirmation recorded in DispatchHistory
  -> PDA scans LotNM for a production line and MfgOrder
  -> Pro_PDA_ProductLineLoadMaterial_DoLoad
  -> ProductLineLoadedMaterial (State = 0)
  -> LotLoadHistory + ProductLineLoadMaterialHistory (TxnId = LOADMA)
```

`LotNM` remains the cross-system business identifier. `MfgOrderNM` binds both the dispatch and physical loading records to the manufacturing order; `ProductLineNM` and `ResourceNM` bind the second operation to its execution location.

## Node Verification

| Node | Status | Verified behavior |
| --- | --- | --- |
| Manufacturing order and dispatch order | Verified as operational context | `MfgOrder` stores the manufacturing order and production batch. `DispatchMaterialOrder` stores `DispatchMaterialOrderNM`, `Item`, `MfgOrderNM`, `ProductNM`, and requested quantity. |
| Dispatch-order selection | Verified | PDA `FaLiaoDanXuanZe` calls `/GetDispatchOrderList2` with resource, user, dispatch-order, manufacturing-order, date, and order type filters. |
| Suggested lot selection | Verified | PDA `FaLiaoThread` calls `/GetSuggestLot` with `NeedQty`, `Item`, and `DispatchOrderNM`, receiving candidate `LotNM`, quantity, demand quantity, unit, and storage location. |
| PDA scan dispatch | Verified | PDA `B_FaLiaoThread` calls `/DoDispatchLot` with transaction/stock type, resource, user, dispatch order, product, item, scanned `LotNM`, and an optional suggested-lot check. The service executes `Pro_PDA_DispatcheOrder_DispatchLot`. |
| Dispatch state and quantity movement | Verified | On successful dispatch, the procedure creates a `CurrentStatus2` record through `Pro_GSB_SInsertCurrentStatus2`, invokes `Pro_Tran_ChangeQty` to deduct material, updates `PurchaseOrderLotApply.DispatchState`, and aggregates dispatch quantity. `DispatchState` is a material-issue flag, not a procurement-label distribution flag. |
| Receipt/dispatch confirmation | Required precondition, implementation evidence | The production-line loading procedure requires a current `DispatchHistory` row for the same `LotId` and `MfgOrderNM`, with a dispatch-confirmation reference. It rejects a lot that is not confirmed or has no dispatch history. The confirmation action must remain a distinct node between dispatch and loading. |
| Production-line loading | Verified | PDA calls `/DoProductLineLoadMaterialLoad`; the backend invokes `Pro_PDA_ProductLineLoadMaterial_DoLoad` with `ProductLineNM`, `MfgOrderNM`, `LotNM`, `Qty`, `ResourceNM`, and `UserNM`. |
| Loaded-material state | Verified | The loading procedure inserts `ProductLineLoadedMaterial` with product-line, manufacturing-order, lot, quantity, resource, user, and `State = 0`. It rejects a repeated active load of the same lot for the same manufacturing order. |
| Loading traceability | Verified | The procedure writes `HistoryMainLine` and `LotLoadHistory`, then `ProductLineHistoryMainLine` and `ProductLineLoadMaterialHistory`, all with `TxnId = LOADMA`. It changes the lot's warehouse/location to the mapped production-line workshop and changes `CurrentStatus.LastRevTxnId` to `LOADMA`. |
| Unload | Verified | `/DoProductLineLoadMaterialUnLoad` invokes the corresponding unload procedure. It records an unload row and histories with `TxnId = UNLOADMA`, and updates the lot's current-status revision marker. |
| Legacy resource loading | Verified as separate branch | The older `/DoLoadMaterial` API attaches a compatible lot to `ResourceLoadedMaterial2`, keyed by resource, manufacturing order, manufacturing-order-start lot, and material lot. It prevents concurrent loading of a different lot for the same material. This is not the same persistence model as `ProductLineLoadedMaterial`. |

## Dispatch Validations and Effects

`Pro_PDA_DispatcheOrder_DispatchLot` validates the scanned label before writing a dispatch result.

- It reads a received `Lot` or an eligible package record from `PurchaseOrderLotApply`.
- It rejects empty quantity, invalid package hierarchy, and outer packages that have already been split into child packages.
- It rejects material whose quality state is not eligible; the procedure reports the lot as defective or waiting inspection when `QCState` is not the permitted value.
- It calculates already-issued quantity from `CurrentStatus2` by dispatch order and product, and can enforce the suggested-lot list.
- For a package still represented only by the barcode-application table, it first creates the required `Lot` record before dispatch.

On a successful dispatch, `Pro_GSB_SInsertCurrentStatus2` copies the lot's active status into `CurrentStatus2`, including `DispatchMaterialOrder` and quantity, then calls `Pro_Tran_ChangeQty` with the `发料` action. The enclosing dispatch procedure marks package records as dispatched and reduces related parent/child lot quantities where applicable.

`DispatchHistory` is the durable bridge to downstream production work. Its schema captures the lot, quality state, manufacturing order, dispatch quantity, source stock order, resource, and a `DispatchConfirmHistoryId`. `DispatchConfirmHistory` records the separate confirmation actor, time, manufacturing order, lot, quantity, and result.

## Production-Line Loading Preconditions

`Pro_PDA_ProductLineLoadMaterial_DoLoad` is explicitly described as `PDA-上料`. It rejects the loading operation when any of the following is true:

1. The lot does not exist.
2. The manufacturing order has been closed.
3. The lot has expired or passed its reinspection date.
4. The loading quantity is not positive or exceeds the lot quantity.
5. The lot has not reached the required receipt/dispatch-confirmed state (`LotEstate = 10` in this route).
6. The lot has no matching confirmed `DispatchHistory` row for the manufacturing order.
7. The lot already has an active `ProductLineLoadedMaterial` record for that manufacturing order.

This produces a strong, system-enforced connection from the preceding dispatch-confirmation step to physical production-line loading.

## Legacy Route and Adjacent Operations

### Legacy resource loading

The legacy PDA API follows a different lifecycle:

```text
PDA DoLoadMaterial(ResourceNM, LotNM)
  -> LoadMaterialBll / LoadMaterialDal
  -> ResourceLoadedMaterial2(ResourceId, MfgOrderId, MfgOrderStartLotId, MLotId)
```

It identifies the resource from the PDA device name and records the material-lot attachment. The API name and UI result say "上料成功", but its persistent state is `ResourceLoadedMaterial2`, not `ProductLineLoadedMaterial`. The final interactive map should show it as a collapsed alternative branch until the target site/version is known.

### CS material weighing belongs to the next stage

The Web/desktop `IssueMaterial` module is a weighing and confirmation workflow, not evidence that a material was physically loaded on a line.

- Its list sources include the manufacturing order, BPR material requirements, and dispatched materials.
- `Pro_IssueMaterial_Confirm_New` is described as raw-material weighing. It requires a manufacturing order, package `LotNM`, net weight, and a matching dispatch history for that manufacturing order.
- The confirmation procedures create a split, weighed lot and call `Pro_Tran_Weighing_News`; the `Confirm2_News` route also updates `WeighingHistory.WeighFlag` and splits the dispatch record to the new weighed lot.
- The CS form is `frmME_IssueMaterial`; it supports weighing, label printing, electronic signature/double check, cancellation, and audit history.

This is the evidence basis for the subsequent `称料` macro stage. Draw it after the material becomes available to the manufacturing order, but do not make it the completion event of the physical `上料` route without site-specific confirmation.

### BPR material record is traceability, not proof of physical loading

`Pro_BPRRecord_RecordMaterialLot` inserts `BPRLoadMaterial` rows from a provided lot list. Each row records manufacturing order, process specification/step, `LotNM`, quantity, unit, station, user, product, and manufacturing batch. This is a BPR execution record at a process step. It can be linked as a traceability node or a later production record, but the procedure alone does not replace the PDA `LOADMA` operation.

## Source Map

| Layer | Main evidence |
| --- | --- |
| PDA frontend | `FaLiaoDanXuanZe`, `FaLiaoThread`, `B_FaLiaoThread`; product-line loading call sites in `DatasModel` and `Fragment_UporDown_a`. |
| PDA backend | `SZ_WCFService.svc.cs` endpoints `DoDispatchLot`, `DoLoadMaterial`, `DoProductLineLoadMaterialLoad`, and `DoProductLineLoadMaterialUnLoad`; `LoadMaterialBll` / `LoadMaterialDal`. |
| Web MES | `MESZZZX_IssueMaterialController`, BLL, and DAL. |
| Desktop MES | `frmME_IssueMaterial`, `frmME_IssueMaterialCheck`, `frmME_IssueMaterial_Weighting`, and the shared issue-material DAL. |
| Database | `Pro_PDA_DispatcheOrder_DispatchLot`, `Pro_GSB_SInsertCurrentStatus2`, `Pro_PDA_ProductLineLoadMaterial_DoLoad`, `Pro_PDA_ProductLineLoadMaterial_DoUnLoad`, and the `Pro_IssueMaterial_Confirm*` family. |
| DOC table pages | `DispatchMaterialOrder`, `CurrentStatus2`, `DispatchHistory`, `DispatchConfirmHistory`, `ProductLineLoadedMaterial`, `ProductLineLoadMaterialHistory`, `ResourceLoadedMaterial2`, and `BPRLoadMaterial`. |

## Map Rendering Guidance

Render this verified modern chain as solid links:

```text
工单 / 发料单 -> PDA 选择发料单 -> 推荐批次 -> 扫描发料
扫描发料 -> 发料记录 / CurrentStatus2 -> 领料确认
领料确认 -> PDA 扫描上料 -> ProductLineLoadedMaterial (active)
产线上料 -> LOADMA 历史 / 产线仓位更新
产线上料 -> 下料 (UNLOADMA) [optional reverse operation]
```

Render the following as a collapsed alternative branch, not as a duplicate modern route:

```text
PDA 旧版上料 -> ResourceLoadedMaterial2
```

Render `CS 原料称重 / WeighingHistory / 称重标签` as the handoff into the next macro stage. Render BPR material recording as an evidence/traceability attachment to a process step, not as the physical-loading completion node.

## Remaining Verification Work

1. Locate the exact UI/API implementation of the intermediate `DispatchConfirmHistory` action and verify which site uses it.
2. Confirm which SCAL factory/version uses the modern product-line route versus the legacy `ResourceLoadedMaterial2` route.
3. During the next stage, verify how weighed split lots are selected by configuration/production-output operations.
