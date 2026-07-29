# Flow Verification 04: Preparation Output and Work-Order Closure

## Scope and Conclusion

This document verifies the last two macro stages of the planned SCAL map: `配置产出 -> 结案`.

The verified implementation uses two distinct workflows:

```text
配置产出
  -> CS/BS PZOutput selects an open MfgOrder and preparation tank
  -> records gross, tare, net, batch, date code, label and expiry
  -> Pro_PZOutput_Packing_New
  -> output Lot + CurrentStatus + START / InStock histories
  -> MfgInWHOrder and MfgInWHOrderDetail (配制产出入库单)

工单结案
  -> BS CKZY_WorkOrder calls Pro_MfgOrder_Close_Check
  -> normal close, forced-close prompt, or blocking result
  -> Pro_MfgOrder_Close
  -> CloseMO transaction + MfgOrder.MOStatus = 2 + completed quantity
  -> line-side material archival/deduction and optional ERP interface queue
```

`配置产出` is a real production-output and stock-entry transaction, rather than a recipe-maintenance screen. Its first persistent result is an output `Lot` associated with the manufacturing order and a preparation tank. `结案` is a separate, guarded work-order state transition. It cannot be drawn as an automatic side effect of output.

## Primary Flow

```text
Weighed/configured production context
  -> choose open MfgOrder, TankNO, preparation tank, date code and label style
  -> enter gross/tare; system derives and validates net weight
  -> Pro_PZOutput_Packing_New
  -> new output Lot / CurrentStatus
  -> HistoryMainLine + StartHistory (START)
  -> HistoryMainLine + WareHouseHistory (InStock)
  -> MfgInWHOrder / Detail, status completed
  -> output label and production-output lot list
  -> product sent/received by warehouse as required
  -> close check
  -> Pro_MfgOrder_Close
  -> MfgOrder MOStatus = 2 (closed)
```

`MfgOrderId`, `MfgOrderNM`, `MFGBatch`, `LotNM`, and the production quantity are the principal traceability keys across these stages. `TankNO`/`PreparationTank` identify the configuration vessel; the output lot's `CurrentStatus.EquipmentNM` stores the selected tank number.

## Configuration Output

### UI and Service Path

The CS form `frmME_PZOutput` selects a manufacturing order, a tank and a local printer. It calls the PZ-output DAL for:

- output work-order/load data and unused tank list;
- gross/tare/net-weight calculation;
- output-lot list and label-print information;
- output submission, removal, and reprint.

The DAL's `Output` method submits the work order, gross/tare/net weight, manufacturing batch, station, user/time, date code, tank, label definition, printer style, preparation tank, and expiry date to `Pro_PZOutput_Packing` / current `Pro_PZOutput_Packing_New` variants. The procedure returns the newly generated lot number for label handling.

### Preconditions and Controls

`Pro_PZOutput_Packing_New` enforces these conditions before creating output:

1. `NetWeight` must equal `GrossWeight - SkinWeight`.
2. A work order must be selected and its `MOStatus` must not be `2` (already closed).
3. The output lot must have a configured label definition and printer style.
4. `DateCode`, manufacturing batch, and preparation-tank number are required. The submitted batch must equal the work order's `MFGBatch`.
5. A customer configured for validity control requires an expiry date.
6. The selected tank cannot already be in use by another lot of the same work order. If it is new, the procedure creates the equipment and equipment-current-status records; otherwise it updates the equipment tare weight.
7. The procedure calculates existing work-in-process/output quantity and blocks a result beyond its configured work-order threshold.

The procedure documentation says `配制产出`. It emits the action text `PZOutput` / `配制产出` in its transaction call.

### Persistent Output Results

The output procedure creates a production lot tied to the work order. The inserted `Lot` includes the output product, quantity, unit, work-order ID, manufacturing batch, date code, warehouse/location, QC state, level, lot estate, gross/tare weights, basic/parent lot, preparation tank, and making date. It creates its `CurrentStatus` with the tank number as `EquipmentNM` and the calculated expiry date.

It then writes two traceability sets:

```text
output Lot -> HistoryMainLine(TxnId = START) -> StartHistory
output Lot -> HistoryMainLine(TxnId = InStock) -> WareHouseHistory
```

The procedure also creates a completed manufacturing stock-entry document:

```text
MfgInWHOrder
  IQCOrderNM = 配制产出入库单
  Status = 1
  Type = 0

MfgInWHOrderDetail
  MfgOrderId, LotId, LotNM, Qty, Product, MFGBatch,
  production/expiry date, quality state, source preparation tank
  Status = 2
```

`BPRStartHistory` is updated when the first output changes the relevant start state. These are concrete output and stock-entry records, so the map should give this macro block a solid transition from production preparation to a produced, traceable lot.

## Work-Order Closure

### Entry and Result States

The BS work-order page calls these API/DAL operations in sequence:

```text
CloseCheck -> Pro_MfgOrder_Close_Check
CloseButton -> Pro_MfgOrder_Close
UnCloseButton -> Pro_MfgOrder_UnClose_New  [controlled correction branch]
```

Both close calls carry `MfgOrderId`, `MfgOrderNM`, completion quantity, user, BS station identifier, and `closetype` (`0` normal, `1` forced). `Pro_MfgOrder_Close_Check` explicitly distinguishes its results:

- `code = 200`: can proceed;
- `code = 998`: an operator may choose forced closure; and
- `code = 999`: closure is blocked.

### Close Preconditions

The verified close check blocks or warns on these conditions:

| Check | Result |
| --- | --- |
| Work order already has `MOStatus = 2` | Block. |
| Output/line-side lot remains and has not completed warehouse send/receipt | Block until send scan and warehouse acceptance. |
| Dispatched material receipt is not confirmed | Block. |
| Recently created preparation output is less than two minutes old | Block for the wait period. |
| Production-return application or warehouse-return receipt is unfinished | Block, or prompt for forced close for the applicable customer/product configuration. |
| Latest `MfgOrderStart` record remains active (`State = 0`) | Block until its production line is closed. |
| Completion quantity is zero while material has been issued | Warn as a forced-close decision. |
| Actual issued material deviates from BOM-scaled requirement by at least 5 percent | Warn as a forced-close decision. |

The check aggregates `DispatchHistory` and confirmed returns to calculate actual consumption. It gives the final process map a strong, code-enforced connection from output/warehouse and line-return completion to the closing decision.

### Closure Effects

On success, `Pro_MfgOrder_Close`:

1. Writes a close transaction through `Pro_Tran_OpenCloseMO` with `TxnId = CloseMO`.
2. Updates `MfgOrder.MOStatus` to `2`, records the closing user/time, and saves `CompliteQty`.
3. Writes back sample quantity calculated from `SampleLotDetail` and `ProductRetentionSampleLabel`.
4. Updates `MfgOrderBOM` actual issued quantity, issued manufacturing batches, and standard loss rate from dispatch history where the ERP flow is enabled.
5. Transfers applicable line-side (`LotEstate = 10`) material data to `LotDeduction` as part of the close/archive handling, then removes the corresponding active line-side lot data according to department/product rules.
6. When ERP integration is enabled, queues consumption and work-order-close interface transactions in `InterfaceBusiness`; the map should render ERP as an optional external integration, not as a local completion prerequisite unless the target site requires it.

Once `MOStatus = 2`, the independently verified dispatch, loading, output, return, sampling, and weighing procedures reject further normal operations on the work order. This is the stable end state of the seven-stage macro chain.

### Reopen Branch

The BS API offers `UnCloseButton`, which invokes `Pro_MfgOrder_UnClose_New`. Render this as a controlled administrative correction branch from `工单已结案` back to the work-order state; do not show it as a normal forward subprocess.

## Node Verification

| Node | Status | Verified behavior |
| --- | --- | --- |
| Configuration-output form | Verified | CS `frmME_PZOutput` supplies work-order, tank, preparation tank, weights, batch, date code, label/printer and expiry data. It supports print, reprint, and removal paths. |
| Output transaction | Verified | `MESZZZX_PZOutputDAL.Output` calls the PZ output packing procedure and receives the generated lot number. |
| Output lot and tank trace | Verified | `Pro_PZOutput_Packing_New` inserts `Lot` and `CurrentStatus`; the latter stores `EquipmentNM = TankNO`, while the lot stores `PreparationTank`. |
| Output / stock histories | Verified | The procedure creates `START` and `InStock` history-main-line records, plus `StartHistory` and `WareHouseHistory`. |
| Output stock-entry order | Verified | The procedure creates `MfgInWHOrder` titled `配制产出入库单` and a completed `MfgInWHOrderDetail`. |
| Closure precheck | Verified | Web `CKZY_WorkOrder` DAL calls `Pro_MfgOrder_Close_Check` before the close button. The procedure returns allow/forced/block codes. |
| Work-order closure | Verified | Web close button calls `Pro_MfgOrder_Close`; it calls `Pro_Tran_OpenCloseMO` and updates `MfgOrder.MOStatus = 2` and `CompliteQty`. |
| Material and sample reconciliation | Verified | Closure derives sample quantity from product/sample records, aggregates dispatch/return consumption, and updates material-use/BOM data in the relevant path. |
| Line-side cleanup | Verified | Closure moves applicable line-side material to `LotDeduction` and removes active line-side material records according to configured department/product logic. |
| Reopen | Verified as correction route | BS invokes `Pro_MfgOrder_UnClose_New`; it is a distinct reversal action. |

## Source Map

| Layer | Main evidence |
| --- | --- |
| Web MES | `CKZY_WorkOrder` view, API controller, BLL/DAL; `MESZZZX_PZOutputController`, BLL/DAL. |
| Desktop MES | `frmME_PZOutput`, `MESZZZX_PZOutputDAL`, label/reprint/removal actions. |
| Database | `Pro_PZOutput_Packing_New`, `Pro_MfgOrder_Close_Check`, `Pro_MfgOrder_Close`, `Pro_MfgOrder_UnClose_New`, `Pro_Tran_OpenCloseMO`. |
| DOC table pages | `Lot`, `CurrentStatus`, `HistoryMainLine`, `StartHistory`, `WareHouseHistory`, `MfgInWHOrder`, `MfgInWHOrderDetail`, `MfgOrder`, `MfgOrderBOM`, `MfgOrderStart`, `LotDeduction`, and `InterfaceBusiness`. |

## Map Rendering Guidance

Render these as the solid end-of-chain path:

```text
称量/配制上下文 -> 选择工单与配制罐 -> 称量产出
称量产出 -> 产出批次 Lot -> 配制产出入库单
产出批次 -> 送库扫描 / 仓库接收 -> 工单结案前检查
结案前检查 -> 正常结案或强制结案 -> MfgOrder.MOStatus = 2
```

Render these as guarded side paths:

```text
产出超量 / 标签或批次资料缺失 / 罐占用 -> 阻断产出
线边批次未送库、收料未确认、退料未接收、产线未关 -> 阻断结案
产出为零但有发料、耗用偏差 >= 5% -> 强制结案确认
已结案 -> 结案还原 [受控修正]
结案 -> ERP 耗料单 / 关单接口队列 [部署可选]
```

Do not attach `结案` directly to a single output label. The verified completion gate is the work-order-level reconciliation performed by `Pro_MfgOrder_Close_Check`.

## Remaining Verification Work

1. Confirm which customer/product configurations allow forced closure and whether user permissions further restrict it.
2. Verify the factory-specific post-output warehouse send/receive UI path that satisfies the close check's `送库扫描与送库接收` condition.
3. During HTML implementation, link `配置产出` to the `PZOutput` demo/source node and `结案` to the `CKZY_WorkOrder` close-check source node; no matching HTML demo page was verified in the DOC folder during this pass.
