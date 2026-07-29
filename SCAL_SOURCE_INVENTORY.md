# SCAL Source Inventory

## Status

Completed on 2026-07-24. This is a source and evidence inventory, not yet a verified business-flow map. File names and table names below are candidates for the next validation stage.

## Source Map

| Source | Technology and structure | Role in the research |
| --- | --- | --- |
| PDA frontend | Android Gradle application at `E:\code\scal-pda-f\scal-wms-app` | Mobile screens, scan operations, print actions, and PDA-to-service calls. |
| PDA backend | .NET/WCF solution at `E:\code\scal-pda-b\scal-mes-pda-services` | PDA service contract, service implementation, business logic, data access, and data models. |
| Web MES (BS) | .NET solution at `E:\code\scal-mes`, with `Apps.Web`, `Apps.WebApi`, `Apps.BLL`, `Apps.DAL`, and `Apps.Models` | Browser-side business entry points, APIs, and core MES business/data-access logic. |
| Manufacturing MES client (CS) | .NET Windows client at `E:\code\scal-mes-client`, with `WinClient` | Desktop manufacturing forms, printing, weighing, material issue, equipment, and output workflows. |
| Database snapshot | `E:\code\xxaedatabase\db-scripts` | Versioned database change and backup scripts, including stored-procedure sources and history-query artifacts. |
| Documentation and demos | `E:\code\scal-mes（副本）\TEMPS\DOC` | Database table/field documentation and business-page demos used to explain selected workflow steps. |

## Confirmed Documentation Assets

- `main.html` is the current table-documentation index.
- `tables` contains 621 current HTML table pages.
- `data/state.json` is an additional metadata export. It is not currently parseable by PowerShell's JSON parser, so table HTML pages remain the dependable source for this research.
- `business` contains three pages: `index.html`, `sample.html`, and `sampling-label.html`.
- `business/sampling-label.html` explicitly presents this incoming-material sequence:

  ```text
  采购单采购 -> 条码申请 -> 标签分发 -> 扫码入库 -> 抽样标签 -> 质检判定
  ```

- The sampling-label demo also exposes field-level data lineage, including `Product`, `Lot`, `MfgOrder`, `SampleLot`, and printer/label configuration information.

## Candidate Evidence by Main Stage

These are discovery leads only. The next stage must read their implementation and establish actual order, conditions, and cross-system handoffs.

| Main stage | Candidate artifacts discovered |
| --- | --- |
| Procurement | DOC table pages: `PurchaseOrder`, `PurchaseOrderDetail`, `PurchaseOrderLotApply`, `BarCodeDef`; PDA backend: `BarCodeDefBll`, `InWHOrderPurchase`; demo: `business/sample.html`. |
| Receiving | DOC table pages: `del_InWH`, `del_InWHOrder`, `del_InWHOrderPurchase`, `CheckInHistory`, `MfgInWHOrder`; PDA frontend: `ScanReceiveThread`, `AddRukuDanThread`, receiving fragments; PDA backend: `InWHDal`, stock-search services. |
| Quality inspection | DOC table pages: `SampleLot`, `SampleLotDetail`, `InspectionHistory`, inspection-detail tables; Web MES: `SamplingLabelQueriesDAL`, `SampleLabelQueryDAL`, inspection BLL/DAL classes; demo: `business/sampling-label.html`. |
| Material loading | DOC table pages: `BPRLoadMaterial`, `ProductLineLoadMaterialHistory`, `V_ResourceLoadMaterial`; PDA frontend: `Fragment_GongDanTouLiao_*`, material-issue threads; PDA backend: `LoadMaterialBll`, `ResourceLoadedMaterial2Bll`; CS: `frmME_IssueMaterial`. |
| Weighing | DOC table pages: `WeightingEquipmentContentList`, `WeightingEquipmentHanderList`; CS: `frmME_IssueMaterial_Weighting`, `frmME_WeightingTest`. |
| Formula output | DOC table pages: `Recipe`, `SpecRecipe`, `ProductRecipeAndWorkersSetting*`, `ProductLineOutputHistory`; PDA backend: `RecipeBll`; CS: `frmME_EquipmentConfigOut`, `frmME_BCPOutput`. |
| Case closure | DOC table pages: `BPRHistory*`, `BPRTimeHistory*`, `BPRWorkLog`, `BPRLockHistory`; CS: `frmME_CleanBPREnd`. The precise definition of “结案” remains to be verified. |

## Cross-System Evidence Points

- PDA frontend contains receive, scan, warehouse, material-issue, production-output, and printing-related classes; it is an Android client, not a web frontend.
- PDA backend is a WCF service solution with separate service, BLL, DAL, model, and interface projects. Its visible process candidates include barcode definition, receiving, stock, material loading, recipe, manufacturing-order start, and production operations.
- Web MES contains the server-side BLL/DAL and web/API layers. Candidate modules include send labels, sampling labels, inspection, stock, traceability, and production-component control.
- CS contains desktop implementation candidates for material issue, material weighing, equipment configuration output, production output, and BPR completion.
- The database snapshot holds selected versioned procedures, including material-in-stock and history-query procedures. The DOC table pages are currently the broader schema reference.

## Inventory Limits

- The seven-stage chain has not yet been treated as confirmed implementation behavior.
- A matching file or table name is not proof of a direct process transition.
- The relationship between each business demo and production code will be validated before it becomes a clickable link in the final map.
- “Case closure” needs an explicit business definition and a verified technical endpoint.

## Next Step

Read the candidate implementations, beginning with the proven incoming-material chain in the sampling-label demo, to verify subprocess order, state changes, interfaces, and database entities.
