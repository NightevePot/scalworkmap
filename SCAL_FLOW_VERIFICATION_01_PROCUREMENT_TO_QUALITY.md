# Flow Verification 01: Procurement to Quality Inspection

## Scope and Confidence

This document verifies the first researched branch of the planned SCAL process map:

```text
采购单采购 -> 条码申请 -> 标签分发 -> 扫码入库 -> 抽样标签 -> 质检判定
```

System-side label generation is verified, but the separate operational handoff represented by "label distribution" has not yet been located. The quality-decision evidence is complete for the sample workflow; original inventory-lot state changes are implemented as separately traceable operations, but an automatic writeback from the sample decision to `Lot.QCState` is still unverified.

## Verified Data Lineage

```text
PurchaseOrder / PurchaseOrderDetail
  -> PurchaseOrderLotApply (LotNM, BasicLotId, ParentId, Level, Qty)
  -> TemporaryReceiptOrder / TemporaryReceiptOrderDetail (scanned LotNM)
  -> Lot (LotNM, Level = '000', Qty > 0, QCState = -1)
  -> SampleLot / SampleLotDetail
  -> InspectionHistory (SampleLotId, SampleLotNM)
```

`LotNM` is the verified business identifier crossing barcode application, PDA temporary receipt, received lot, sampling, and inspection history.

## Node Verification

| Node | Status | Verified implementation and data behavior |
| --- | --- | --- |
| Procurement order | Verified as source context | Barcode application reads the selected purchase order and detail through `Pro_LotApply_GetPurchaseOrderDetailList_New`, with purchase order, product, supplier part number, user, and customer-order parameters. |
| Barcode application | Verified | `CKZY_LotApplyController.AddPurchaseOrderLotApplyOutPackage` calls BLL/DAL, which executes `Pro_LotApply_AddPurchaseOrderLotApplyOutPackage`. The procedure writes one or more `PurchaseOrderLotApply` records, including `PurchaseOrderId`, `Item`, `DateCode`, `BasicLotId`, `ParentId`, `LotNM`, `Level`, and `Qty`. |
| Label generation and distribution | Partially verified | Barcode application creates the application/package records that support label generation. The DOC demo presents a separate distribution node after application. A similarly named send-label query module exists (`Pro_Send_Query`), but its role has not yet been proven to be the operational handoff represented by the demo, and no independent distribution log has been located. |
| Purchase receiving / scan receiving | Verified | PDA temporary receipt creates a receipt header, scans an outer-package `LotNM` into a temporary receipt detail, then completes the receipt. The scan procedure verifies that the lot exists in `PurchaseOrderLotApply`, is an outer package (`Level = '001'`), and does not already exist in `Lot`. Completion aggregates the package records, updates purchase-detail received quantity, and invokes the lot-start procedure. That procedure inserts `Lot` with `Status = 3` and `QCState = -1`, which matches the sampling module's raw-material eligibility filter. |
| Sampling label | Verified | `ZLKZ_SamplingLabelDAL` queries received lots with `Pro_CreateSample_GetReceivedLotList_New` and creates samples with `Pro_CreateSampleLot_New`. The creation procedure writes `SampleLot` and `SampleLotDetail` records in a transaction. |
| Quality inspection | Verified at sample-workflow level | `MESZLKZ_InspectionDAL` invokes the inspection procedures for submit, completion, approval, and rejection. `Pro_Inspection_SendApprove_New` moves a completed sample from status `0` to `1` and writes submitter/time. `Pro_Inspection_Approve_New` moves an approved sample to status `2` and writes approver/time. `Pro_Inspection_Reject` writes the caller-supplied sample status, rejection reason, person, and time. `InspectionHistory` stores both `SampleLotId` and `SampleLotNM`. Original-lot state changes are separately traceable, but no direct `Lot.QCState` update was found in these sample-decision procedures. |

## System Ownership

| Concern | Current owner | Evidence |
| --- | --- | --- |
| Purchase barcode application | Web MES (BS) | `Apps.WebApi/Areas/WarehouseOperation/Controllers/CKZY_LotApplyController.cs`; `Apps.DAL/MES/WarehouseOperation/CKZY_LotApplyDAL.cs`. |
| Sampling label | Web MES (BS) | `Apps.DAL/MES/QualityControl/ZLKZ_SamplingLabelDAL.cs`; `Apps.WebApi/Areas/QualityControl/Controllers/ZLKZ_SamplingLabelController.cs`. |
| Schema and procedures | Database | `E:\code\scal-mes\存储过程清单` and DOC table pages. |
| Incoming-material demonstration | DOC business demo | `E:\code\scal-mes（副本）\TEMPS\DOC\business\sample.html` and `sampling-label.html`. |

## PDA Temporary-Receipt Branch

The procurement receiving branch is implemented in the PDA temporary-receipt screens:

```text
PDA AddTemporaryReceiptOrder
  -> Pro_PDA_TemporaryReceiptOrder_Add
PDA AddTemporaryReceiptOrderDetail (TemporaryReceiptOrderNM, LotNM)
  -> Pro_PDA_TemporaryReceiptOrder_AddDetail
PDA CompliteTemporaryReceipt
  -> Pro_PDA_TemporaryReceiptOrder_Complite
  -> Pro_PDA_Tran_TemporaryReceiptLotStart_Basic
  -> Lot / CurrentStatus creation
```

`ZanShouFramgnet_A` submits the scanned `LotNM` with a temporary receipt order number. `ZanShouFramgnet_B` completes the receipt order. The database procedure explicitly describes this as "PDA temporary receipt - completion (purchase receipt/purchase receiving, sales return, other receipt)".

The PDA also has a separate `MfgInWHOrder` product-receipt branch. It remains separate from this procurement-receipt chain.

## Important Database Evidence

### Barcode application

- `Pro_LotApply_AddPurchaseOrderLotApplyOutPackage` resolves `PurchaseOrderId` from `PurchaseOrderNM`.
- It inserts a basic `PurchaseOrderLotApply` record, then package-level child records as needed.
- The generated `LotNM`, parent relationship, packaging level, and quantity are stored with the application record.

### Receiving to sampling eligibility

- `Pro_PDA_TemporaryReceiptOrder_AddDetail` reads the scanned `LotNM` from `PurchaseOrderLotApply`; it rejects a missing barcode-application record, an already-created `Lot`, and non-outer-package labels.
- `Pro_PDA_TemporaryReceiptOrder_Complite` aggregates scanned package records by their basic lot, updates `PurchaseOrderDetail.RecievedQty` and `UnReceivedQty`, then starts the basic lot.
- `Pro_PDA_Tran_TemporaryReceiptLotStart_Basic` inserts both `Lot` and `CurrentStatus`. It initializes the received lot with `Status = 3` (waiting inspection) and `QCState = -1` (under inspection).
- `Pro_CreateSample_GetReceivedLotList_New` dispatches raw material and packaging material to `Pro_CreateSample_GetReceivedLotList_YL_New`.
- The YL procedure selects candidate `Lot` rows where `Level = '000'`, `Qty > 0`, and `QCState = -1`.
- It joins the candidate lot to `PurchaseOrder`, `PurchaseOrderDetail`, and `PurchaseOrderLotApply` using the purchase identifiers and `LotNM`.

### Sample generation and inspection handoff

- `Pro_CreateSampleLot_New` receives an original `LotNM` and optional subitem lot number.
- It writes `SampleLot` with `BasicLotId`, `BasicLotNM`, `LotNM`, `LotId`, quantity, sample count, label copies, product, warehouse, and manufacturing-batch values.
- It writes `SampleLotDetail` with the generated `SampleLotNM`, sample quantity, unit, and quality-related fields.
- `InspectionHistory` contains `SampleLotId` and `SampleLotNM`, making the inspection record traceable to the sample record.

### Quality decision state machine

- `MESZLKZ_InspectionController` exposes the Web MES inspection workflow, backed by `MESZLKZ_InspectionDAL`.
- `Pro_Inspection_SendApprove_New` requires `SampleLotDetail.SampleLotStatus = 0`, then sets it to `1` and records submission person/time.
- `Pro_Inspection_Approve_New` sets `SampleLotStatus = 2` and records approval person/time.
- `Pro_Inspection_Reject` sets the provided `SampleLotStatus` and records rejection reason, person, and time.
- The current evidence describes the sample-review state machine. A separate verification is still needed to identify the procedure that changes the original `Lot.QCState` after an approval, rejection, hold, or exemption.

## Closed-Gap Results

### `PurchaseOrderLotApply.DispatchState` is a material-issue flag

`PurchaseOrderLotApply.DispatchState` is documented as "调度状态" and defaults to `0`. It is not a record of procurement-label distribution.

- `Pro_GSB_SWritLotDispatchState` recursively sets `DispatchState = 1` on a scanned application-label record and its package children.
- `Pro_PDA_DispatcheOrder_DispatchLot` invokes that procedure only after its dispatch transaction reports "发料成功"; its inline comment explicitly says that it changes the application-table batch issue state.
- The related PDA query procedures select only `DispatchState = 0` application labels when preparing a material-dispatch operation.

Therefore, the state belongs to the later material-loading/issue branch. It must not be used as evidence that the label created during procurement barcode application was physically distributed to receiving staff. `Pro_Send_Query` is likewise a sample/quality-send query and does not close that handoff.

### Sample inspection and original-lot status are two explicit operations

The original-lot quality status has a confirmed Web MES operator entry point:

```text
StockQueryQualityHold/Index
  -> POST /api/MESZLKZ_ReleaseHold/CheckAction
  -> optional electronic signature
  -> POST /api/MESZLKZ_ReleaseHold/QualityChangeStatus
  -> MESZLKZ_ReleaseHoldController
  -> BLL / DAL
  -> Pro_HoldRelease_QualityChangeStatus_New
  -> Lot.Status and Lot.QCState
```

The page is a stock-query quality release/hold screen. An operator selects original `Lot` records, provides a reason, and chooses one of `放行` (`0`), `扣留` (`1`), or `不合格` (`2`). The request carries the original lot numbers, product, manufacturing batch, old/new usage status, station, reason, and user; it does not carry a `SampleLotId`.

`Pro_HoldRelease_QualityChangeStatus_New` records the request in `HoldRelease_log`, rejects a target status of `3` (waiting inspection), and updates the selected `Lot` as follows:

- `Lot.Status = HoldStatusNew`.
- `Lot.QCState = 0` when the target status is `2`; otherwise `Lot.QCState = 1`.
- Eligible child lots are traversed and updated as part of the same operation. ERP interface work is also recorded when that integration is enabled.

The caller inventory contains only the release/hold page, controller, BLL, DAL, and this procedure. In contrast, the inspection approval path calls `Pro_Inspection_SendApprove_New`, `Pro_Inspection_Complete_New`, `Pro_Inspection_Approve_New`, and `Pro_Inspection_Reject`; it does not call `QualityChangeStatus`. The link from sample approval/rejection to release/hold is therefore a required business/operator handoff, not a verified automatic callback.

## Demo Mapping

| Demo page | Confirmed value |
| --- | --- |
| `business/sample.html` | Demonstrates barcode application from a purchase order. Its field lineage cites `Pro_LotApply_GetPurchaseOrderDetailList_New` and `Pro_LotApply_AddPurchaseOrderLotApplyOutPackage`. |
| `business/sampling-label.html` | Demonstrates the received-lot list, sample creation, and sample-label printing. Its field lineage cites `Pro_CreateSampleLot_New`. |

## Remaining Verification Work

1. Confirm the real-world owner and evidence, if any, for physical label distribution after printing; no system record has been located.
2. Confirm the operating rule that maps sample approval, rejection, hold, or exemption to the release/hold choice. The code proves the two operations, but not an automatic relationship between them.
3. Determine whether the DOC demo represents one production configuration or a generic, cross-site process model.

## Map Rendering Guidance

Render the following as solid evidence links:

```text
采购单 -> 条码申请 -> 采购条码申请记录 -> PDA 暂收扫码
PDA 暂收扫码 -> 采购收料完成 -> 待检 Lot (QCState = -1)
待检 Lot -> 抽样标签 -> SampleLot / SampleLotDetail -> InspectionHistory
SampleLotDetail (0) -> 送审 (1) -> 核准 (2) 或退回（调用方状态）
库存查询-质量放行/扣留 -> QualityChangeStatus -> Lot.Status / Lot.QCState
```

Render the following as a dashed, "pending verification" link:

```text
条码申请 -> 标签分发 -> PDA 暂收扫码
质检样品判定 -> 原始 Lot 库存状态自动回写
```

Represent the independently traceable original-lot status change as its own operational node until the invoking workflow is verified.

Keep the PDA manufacturing/product-receipt branch visually separate from the procurement temporary-receipt branch.
