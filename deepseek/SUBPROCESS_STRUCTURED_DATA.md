# SCAL 子流程结构化数据

> 工作方法第③步：为每个子流程记录前驱/后继/参与系统/实现证据/数据实体/可选 Demo 目标
> 后续第④步将基于此文档建模为 JSON，驱动 HTML 地图生成

---

## 阶段一：采购 (Procurement)

### 1.1 采购单创建

| 属性              | 值                                                   |
| ----------------- | ---------------------------------------------------- |
| **阶段**          | 采购                                                 |
| **序号**          | 1.1                                                  |
| **前驱**          | —（流程起点）                                        |
| **后继**          | 1.2 条码申请                                         |
| **主导系统**      | Web MES (BS)                                         |
| **参与系统**      | BS                                                   |
| **BS 入口**       | `CKZY_LotApplyBLL.GetPurchaseOrderListByPage()`      |
| **BS Controller** | `CKZY_LotApplyController` (Areas/WarehouseOperation) |
| **BS DAL**        | `CKZY_LotApplyDAL`                                   |
| **数据库表**      | `PurchaseOrder`, `PurchaseOrderDetail`               |
| **Demo**          | `business/sample.html`                               |

### 1.2 条码申请

| 属性               | 值                                                   |
| ------------------ | ---------------------------------------------------- |
| **阶段**           | 采购                                                 |
| **序号**           | 1.2                                                  |
| **前驱**           | 1.1 采购单创建                                       |
| **后继**           | 1.3 标签分发                                         |
| **主导系统**       | Web MES (BS)                                         |
| **参与系统**       | BS, PDA后端, CS(补打)                                |
| **BS 入口**        | `CKZY_LotApplyBLL` — 物料编号/DateCode/标签定义下拉  |
| **BS Controller**  | `CKZY_LotApplyController`                            |
| **PDA 后端 BLL**   | `BarCodeDefBll` — 条码定义 CRUD                      |
| **PDA 后端 Model** | `BarCodeDef`, `BarCodeDefForTran`                    |
| **CS 补打**        | `frmME_LotReprint`                                   |
| **BS 补打**        | `CKZY_LotApplyReprintBLL`, `CKZY_LotBatchRePrintBLL` |
| **数据库表**       | `BarCodeDef`, `PurchaseOrderLotApply`                |
| **Demo**           | `business/sample.html`                               |

### 1.3 标签分发

| 属性              | 值                                                          |
| ----------------- | ----------------------------------------------------------- |
| **阶段**          | 采购                                                        |
| **序号**          | 1.3                                                         |
| **前驱**          | 1.2 条码申请                                                |
| **后继**          | 2.1 PDA扫码入库                                             |
| **主导系统**      | Web MES (BS)                                                |
| **参与系统**      | BS                                                          |
| **BS 入口**       | `SendLabelQueryBLL` — 标签查询分发                          |
| **BS Controller** | `SendLabelQueryController`                                  |
| **数据库表**      | `PurchaseOrderLotApply` → 标签打印/分发记录                 |
| **备注**          | ⚠️ 标签分发的完整数据流待验证（申请→生成→打印→分发状态变更） |

---

## 阶段二：入库 (Receiving)

### 2.1 PDA扫码入库

| 属性             | 值                                                                 |
| ---------------- | ------------------------------------------------------------------ |
| **阶段**         | 入库                                                               |
| **序号**         | 2.1                                                                |
| **前驱**         | 1.3 标签分发                                                       |
| **后继**         | 2.2 入库单生成                                                     |
| **主导系统**     | PDA 前端 + PDA 后端                                                |
| **参与系统**     | PDA前端, PDA后端, DB                                               |
| **PDA Fragment** | `JieShouFramgnet_A.java`, `JieShouFramgnet_B.java`                 |
| **PDA Thread**   | `ScanReceiveThread.java` → WCF `GetProductInWarehouseOrderSumInfo` |
| **PDA Thread**   | `SaoMiaoJieShouThread.java` — 扫描入库确认                         |
| **PDA Thread**   | `AddRukuDanThread.java` → WCF `AddProductInWarehouseOrder`         |
| **PDA Thread**   | `RukuThread.java`, `RukuThread2.java`, `RuKuThreadNew.java`        |
| **PDA Fragment** | `RuKuFramgnet_A.java`, `RuKuFramgnet_B.java`                       |
| **WCF 接口**     | `GetProductInWarehouseOrderSumInfo` — 入库单汇总                   |
| **WCF 接口**     | `CheckInWHQty` — 入库数量校验                                      |
| **数据库 SP**    | `Pro_PDA_MfgInWHOrder_Add`                                         |
| **数据库表**     | `MfgInWHOrder`, `InWH`, `InWHOrder`, `InWHDetail`, `Package`       |

### 2.2 入库单生成

| 属性             | 值                                                                       |
| ---------------- | ------------------------------------------------------------------------ |
| **阶段**         | 入库                                                                     |
| **序号**         | 2.2                                                                      |
| **前驱**         | 2.1 PDA扫码入库                                                          |
| **后继**         | 2.3 暂收入库 / 3.1 抽样标签                                              |
| **主导系统**     | PDA 后端                                                                 |
| **参与系统**     | PDA后端, DB                                                              |
| **WCF 接口**     | `AddProductInWarehouseOrderDetail` → SP `Pro_PDA_MfgInWHOrder_AddDetail` |
| **WCF 接口**     | `DoInWH` — 执行入库                                                      |
| **WCF 接口**     | `CompliteProductInWarehouseOrder` / `CompliteProductInWarehouseOrderNew` |
| **PDA 后端 BLL** | `InWHBll` — 入库 CRUD                                                    |
| **PDA 后端 DAL** | `InWHDal`                                                                |
| **数据库表**     | `InWH`, `InWHOrder`, `InWHDetail`, `CheckInHistory`                      |

### 2.3 暂收入库

| 属性             | 值                                                                  |
| ---------------- | ------------------------------------------------------------------- |
| **阶段**         | 入库                                                                |
| **序号**         | 2.3（与 2.2 并列，可选路径）                                        |
| **前驱**         | 2.1 PDA扫码入库                                                     |
| **后继**         | 2.2 入库单生成 / 3.1 抽样标签                                       |
| **主导系统**     | PDA 前端 + PDA 后端                                                 |
| **参与系统**     | PDA前端, PDA后端, DB                                                |
| **PDA Fragment** | `ZanShouFramgnet_A.java`, `ZanShouFramgnet_B.java`                  |
| **PDA Thread**   | `ZanShouThread.java`, `ZanShouMingXiThread.java`                    |
| **WCF 接口**     | `AddTemporaryReceiptOrder` → SP `Pro_PDA_TemporaryReceiptOrder_Add` |
| **WCF 接口**     | `AddTemporaryReceiptOrderDetail`                                    |
| **WCF 接口**     | `CompliteTemporaryReceipt`                                          |
| **数据库表**     | `TemporaryReceiptOrder`, `TemporaryReceiptOrderDetail`              |

### 2.4 入库查询(BS端)

| 属性         | 值                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| **阶段**     | 入库                                                                                                   |
| **序号**     | 2.4（辅助，非必经）                                                                                    |
| **前驱**     | 2.2 入库单生成                                                                                         |
| **后继**     | —                                                                                                      |
| **主导系统** | Web MES (BS)                                                                                           |
| **参与系统** | BS                                                                                                     |
| **BS 入口**  | `CKZY_RecieveMaterialQueryBLL`                                                                         |
| **BS 入口**  | `CKZY_TemporaryReceiptOrderBLL`, `CKZY_UnfinishedTempReceiptBLL`, `CKZY_UnfinishedWarehouseReceiptBLL` |
| **数据库表** | `InWH`, `InWHOrder`, `TemporaryReceiptOrder`                                                           |

---

## 阶段三：质检 (Quality Inspection)

### 3.1 抽样标签

| 属性              | 值                                                             |
| ----------------- | -------------------------------------------------------------- |
| **阶段**          | 质检                                                           |
| **序号**          | 3.1                                                            |
| **前驱**          | 2.2/2.3 入库完成                                               |
| **后继**          | 3.2 送检                                                       |
| **主导系统**      | Web MES (BS)                                                   |
| **参与系统**      | BS                                                             |
| **BS 入口**       | `SamplingLabelQueriesBLL.GetSamplingLabelPage()`               |
| **BS Controller** | `SamplingLabelQueriesController`                               |
| **BS BLL**        | `ZLKZ_SamplingLabelBLL` — 物料类别、已收料列表、已申请样品批次 |
| **BS BLL**        | `ZLKZ_BCPSamplingLabelBLL` — 半成品抽样                        |
| **BS BLL**        | `ZLKZ_GZSamplingLabelBLL` — 罐装抽样                           |
| **BS BLL**        | `ZLKZ_PZSamplingLabelBLL` — 配制抽样                           |
| **BS BLL**        | `ZLKZ_ProductRetentionSampleLabelBLL` — 留样                   |
| **数据库表**      | `SampleLot`, `SampleLotDetail`                                 |
| **Demo**          | `business/sampling-label.html` ✅ 已验证                        |

### 3.2 送检

| 属性         | 值                                                           |
| ------------ | ------------------------------------------------------------ |
| **阶段**     | 质检                                                         |
| **序号**     | 3.2                                                          |
| **前驱**     | 3.1 抽样标签                                                 |
| **后继**     | 3.3 检验判定                                                 |
| **主导系统** | Web MES (BS)                                                 |
| **参与系统** | BS                                                           |
| **BS 入口**  | `ZLKZ_SendBLL` — 流水号验证、数据采集区域、物料/上料回车事件 |
| **数据库表** | `SampleLot` → 送检状态变更                                   |

### 3.3 检验判定

| 属性         | 值                                                     |
| ------------ | ------------------------------------------------------ |
| **阶段**     | 质检                                                   |
| **序号**     | 3.3                                                    |
| **前驱**     | 3.2 送检                                               |
| **后继**     | 3.4 放行/滞留                                          |
| **主导系统** | Web MES (BS)                                           |
| **参与系统** | BS                                                     |
| **BS 入口**  | `MESZLKZ_InspectionBLL` — 检验管理                     |
| **BS 子类**  | `MESZLKZ_InspectionCPBLL` — 成品检验                   |
| **BS 子类**  | `MESZLKZ_FinalInspectionBLL` — 终检                    |
| **BS 子类**  | `MESZLKZ_ReInspecBLL` — 复检                           |
| **BS 子类**  | `MESZLKZ_InspectionExemptionBLL` — 检验豁免            |
| **BS 辅助**  | `ZLKZ_AQLSamplePlanBLL`, `ZLKZ_AQLCalculatorBLL` — AQL |
| **数据库表** | `InspectionHistory`, 检验明细表                        |

### 3.4 放行/滞留

| 属性              | 值                                              |
| ----------------- | ----------------------------------------------- |
| **阶段**          | 质检                                            |
| **序号**          | 3.4                                             |
| **前驱**          | 3.3 检验判定                                    |
| **后继**          | 4.1 投前称重确认                                |
| **主导系统**      | Web MES (BS) + PDA 后端                         |
| **参与系统**      | BS, PDA后端, PDA前端                            |
| **BS 入口**       | `MESZLKZ_ReleaseHoldBLL`                        |
| **BS BLL**        | `HoldReleaseHistoryBLL`                         |
| **BS Controller** | `HoldReleaseHistoryController`                  |
| **PDA 后端 WCF**  | `DoHoldOrRelease` — PDA 端滞留/放行             |
| **PDA 前端**      | `FragmentHoldReleaseActivity`                   |
| **数据库表**      | `HoldReleaseHistory`                            |
| **BS 废号**       | `ZLKZ_AbolishLotNMBLL` — 批次号作废（极端场景） |

### 3.5 IPQC 在线检测（产中质检）

| 属性           | 值                                                                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **阶段**       | 质检                                                                                                                                                         |
| **序号**       | 3.5（与来料质检并列，覆盖生产过程）                                                                                                                          |
| **前驱**       | 6.1 工单启动后                                                                                                                                               |
| **后继**       | —（贯穿生产全程）                                                                                                                                            |
| **主导系统**   | Web MES (BS)                                                                                                                                                 |
| **参与系统**   | BS                                                                                                                                                           |
| **23+ 检测项** | 首检、外观、密封、扭矩、热罐、压漏、标签、长度、码日期、STM高度、TAMU、条码、Crimp真空、活化、包材变更/计划、产前准备、设备调整、测试报告、称重设备、复查 等 |
| **BS 入口**    | `MESZLKZ_PAD_IPQC_*BLL` 系列 (23+ 个)                                                                                                                        |
| **数据库表**   | `IPQCCheck`, `IPQCCheckDetail`, `IPQCCheckMaster`                                                                                                            |

---

## 阶段四：称料 (Weighing)

### 4.1 投前称重确认

| 属性              | 值                                                              |
| ----------------- | --------------------------------------------------------------- |
| **阶段**          | 称料                                                            |
| **序号**          | 4.1                                                             |
| **前驱**          | 3.4 放行/滞留（质检通过）                                       |
| **后继**          | 4.2 称重测试 / 5.1 工单领料                                     |
| **主导系统**      | 桌面 MES (CS)                                                   |
| **参与系统**      | CS, BS(查询)                                                    |
| **CS 窗体**       | `frmME_IssueMaterial_Weighting.cs` — 投前称重确认               |
| **BS 查询**       | `CKZY_MaterialWeighingBLL`                                      |
| **BS Controller** | `CKZY_MaterialWeighingController`                               |
| **数据库表**      | `WeightingEquipmentContentList`, `WeightingEquipmentHanderList` |
| **备注**          | 物料在上料前必须先称重确认数量，是上料的**前置条件**            |

### 4.2 称重测试

| 属性         | 值                               |
| ------------ | -------------------------------- |
| **阶段**     | 称料                             |
| **序号**     | 4.2（与 4.1 并列）               |
| **前驱**     | 4.1 投前称重确认                 |
| **后继**     | 4.3 余料称重                     |
| **主导系统** | 桌面 MES (CS)                    |
| **参与系统** | CS                               |
| **CS 窗体**  | `frmME_WeightingTest.cs`         |
| **数据库表** | `WeightingEquipmentValueView` 等 |

### 4.3 余料称重

| 属性         | 值                                                       |
| ------------ | -------------------------------------------------------- |
| **阶段**     | 称料                                                     |
| **序号**     | 4.3                                                      |
| **前驱**     | 5.2 上料完成后（上料后剩余物料退回称重）                 |
| **后继**     | —                                                        |
| **主导系统** | 桌面 MES (CS) + Web MES (BS)                             |
| **参与系统** | CS, BS                                                   |
| **CS 窗体**  | `frmME_SurplusMaterial.cs`, `frmME_SurplusMaterialGZ.cs` |
| **BS BLL**   | `MESZZZX_SurplusMaterialBLL` — 余料称重确认              |
| **数据库表** | 称重相关表                                               |

---

## 阶段五：上料 (Material Loading)

### 5.1 工单领料（PDA端）

| 属性             | 值                                                  |
| ---------------- | --------------------------------------------------- |
| **阶段**         | 上料                                                |
| **序号**         | 5.1                                                 |
| **前驱**         | 4.1 称重确认完成                                    |
| **后继**         | 5.2 发料/上料(CS端)                                 |
| **主导系统**     | PDA 前端 + PDA 后端                                 |
| **参与系统**     | PDA前端, PDA后端                                    |
| **PDA Fragment** | `GongDanLingLiaoFragment_A/B/C`（及 `_New` 版本）   |
| **PDA Fragment** | `Fragment_GongDanTouLiao_A/B/C`                     |
| **PDA Thread**   | `GongDanLingLiaoThread.java`                        |
| **PDA Thread**   | `GongDanLingLiaoQueRenThread.java`                  |
| **PDA Thread**   | `FaLiaoThread.java`, `B_FaLiaoThread.java`          |
| **PDA Thread**   | `TouLiaoItemThread.java`, `TouLiaoItemThread2.java` |
| **PDA Thread**   | `TouLiaoPiciHaoThread.java`                         |
| **PDA Thread**   | `YiFaLiaoMingXiThread.java`                         |
| **PDA Fragment** | `DiaoLiaoFramgnet_A.java`                           |
| **PDA Thread**   | `JieLiaoThread.java`                                |

### 5.2 发料/上料（CS端 + BS端）

| 属性               | 值                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| **阶段**           | 上料                                                                                                   |
| **序号**           | 5.2                                                                                                    |
| **前驱**           | 5.1 工单领料                                                                                           |
| **后继**           | 4.3 余料称重 / 6.1 工单启动                                                                            |
| **主导系统**       | 桌面 MES (CS)                                                                                          |
| **参与系统**       | CS, BS, PDA后端                                                                                        |
| **CS 窗体**        | `frmME_IssueMaterial.cs` — 发料/上料主界面                                                             |
| **CS 窗体**        | `frmME_IssueMaterialCheck.cs` — 上料校验                                                               |
| **BS BLL**         | `MESZZZX_IssueMaterialBLL` — 工单列表/BPR列表/已发料列表/流水号验证                                    |
| **BS Controller**  | `MESZZZX_IssueMaterialController`                                                                      |
| **PDA 后端 WCF**   | `DoLoadMaterial` — PDA端上料                                                                           |
| **PDA 后端 WCF**   | `CompliteLoadMaterial` — 完成上料                                                                      |
| **PDA 后端 WCF**   | `CompliteLoadSMTMaterial` — 完成 SMT 上料                                                              |
| **PDA 后端 WCF**   | `DoProductLineLoadMaterialLoad` / `UnLoad`                                                             |
| **PDA 后端 WCF**   | `DoDispatchLot` / `DoDisptachLot` — 发料扫描/派工发料                                                  |
| **PDA 后端 WCF**   | `DoProductLineDispatchConfirm` — 产线派工确认                                                          |
| **PDA 后端 BLL**   | `LoadMaterialBll`                                                                                      |
| **PDA 后端 DAL**   | `LoadMaterialDal`, `ResourceLoadedMaterial2Dal`                                                        |
| **PDA 后端 Model** | `LoadMaterial`, `ResourceLoadedMaterial2`, `CompltedLoadInfo`                                          |
| **数据库表**       | `BPRLoadMaterial`, `ProductLineLoadMaterialHistory`, `V_ResourceLoadMaterial`, `DispatchMaterialOrder` |

---

## 阶段六：配置产出 (Formula Output)

### 6.1 工单启动

| 属性             | 值                                                 |
| ---------------- | -------------------------------------------------- |
| **阶段**         | 配置产出                                           |
| **序号**         | 6.1                                                |
| **前驱**         | 5.2 上料完成                                       |
| **后继**         | 6.2 设备启动 / 3.5 IPQC在线检测开始                |
| **主导系统**     | PDA 前端 + PDA 后端                                |
| **参与系统**     | PDA前端, PDA后端, DB                               |
| **PDA Activity** | `StartMfgOrder.java`, `StartMfgOrderLists.java`    |
| **PDA 后端 WCF** | `AddMfgOrderStart` — 添加工单启动                  |
| **PDA 后端 WCF** | `DoMfgOrderStartStart` — 执行工单启动              |
| **PDA 后端 WCF** | `CheckThisResourceIsStarting`                      |
| **PDA 后端 BLL** | `MfgOrderStartBll`, `MfgOrderStartLotBll`          |
| **数据库表**     | `MfgOrderStart`, `ResourceCurrentMfgOrderStartLot` |

### 6.2 设备启动

| 属性             | 值                                                    |
| ---------------- | ----------------------------------------------------- |
| **阶段**         | 配置产出                                              |
| **序号**         | 6.2                                                   |
| **前驱**         | 6.1 工单启动                                          |
| **后继**         | 6.3 配方执行                                          |
| **主导系统**     | 桌面 MES (CS)                                         |
| **参与系统**     | CS, PDA后端                                           |
| **CS 窗体**      | `frmME_EquipmentStart.cs`                             |
| **CS 窗体**      | `frmME_StorageTankEquipmentStart.cs` — 储罐启动       |
| **CS 窗体**      | `frmME_SteelTankEquipmentStart.cs` — 钢罐启动         |
| **CS 窗体**      | `frmME_PreplanTankEquipmentStart.cs` — 预排罐启动     |
| **CS 窗体**      | `frmME_TicketStart.cs` — 票据启动                     |
| **CS 窗体**      | `frmME_EquipmentStopHistory.cs` — 停机历史            |
| **PDA 后端 WCF** | `DoMachineBegain` / `DoMachineLeave` — 人员设备上下机 |

### 6.3 配方管理

| 属性              | 值                                                        |
| ----------------- | --------------------------------------------------------- |
| **阶段**          | 配置产出                                                  |
| **序号**          | 6.3                                                       |
| **前驱**          | 6.2 设备启动                                              |
| **后继**          | 6.4 产出                                                  |
| **主导系统**      | PDA 后端 + Web MES (BS)                                   |
| **参与系统**      | PDA后端, BS                                               |
| **PDA 后端 BLL**  | `RecipeBll` — 配方 CRUD                                   |
| **PDA 后端 DAL**  | `RecipeDal`                                               |
| **BS Controller** | `MESGYLC_RecipeController`                                |
| **数据库表**      | `Recipe`, `SpecRecipe`, `ProductRecipeAndWorkersSetting*` |

### 6.4 产出（多类型）

| 属性         | 值                                      |
| ------------ | --------------------------------------- |
| **阶段**     | 配置产出                                |
| **序号**     | 6.4                                     |
| **前驱**     | 6.3 配方执行                            |
| **后继**     | 6.5 成品入库                            |
| **主导系统** | 桌面 MES (CS) + Web MES (BS) + PDA 前端 |
| **参与系统** | CS, BS, PDA前端, PDA后端                |

| 产出类型       | CS 窗体                                 | BS BLL                          | PDA 入口                   |
| -------------- | --------------------------------------- | ------------------------------- | -------------------------- |
| BCP 半成品产出 | `frmME_BCPOutput`                       | `MESZZZX_BCPOutputBLL`          | `Fragment_Output_a/b`      |
| PZ 配置产出    | `frmME_PZOutput` / `frmME_PZoutputTKBD` | `MESZZZX_PZOutputBLL`           | —                          |
| 设备配置产出   | `frmME_EquipmentConfigOut`              | `MESZZZX_EquipmentConfigOutBLL` | —                          |
| PDA 数据采集   | —                                       | —                               | `Fragment_Collect_a/b/c/d` |

| **PDA 产出 WCF** | `DoOutput`, `DoProductLineOutPut`, `DoProductLineExcutionOutPut`                  |
| ---------------- | --------------------------------------------------------------------------------- |
| **PDA Thread**   | `YesThread.java`, `YesThreadNew.java`, `TotalThread.java`                         |
| **成品包装 CS**  | `frmME_CPPackage`, `frmME_NZBPackaging`                                           |
| **成品包装 BS**  | `MESZZZX_CPPackageBLL`, `MESZZZX_InnerPackagingBLL`, `MESZZZX_PalletPackagingBLL` |
| **数据库表**     | `ProductLineOutputHistory`                                                        |

### 6.5 成品入库

| 属性             | 值                                                                       |
| ---------------- | ------------------------------------------------------------------------ |
| **阶段**         | 配置产出                                                                 |
| **序号**         | 6.5                                                                      |
| **前驱**         | 6.4 产出                                                                 |
| **后继**         | 7.1 BPR记录                                                              |
| **主导系统**     | PDA 前端 + PDA 后端                                                      |
| **参与系统**     | PDA前端, PDA后端, DB                                                     |
| **PDA Fragment** | `ChanChuPingRuKuNewFragment_A/B/C`                                       |
| **WCF 接口**     | `CompliteProductInWarehouseOrder` / `CompliteProductInWarehouseOrderNew` |
| **WCF 接口**     | `AddProductLineSendWarehouseOrder`                                       |
| **WCF 接口**     | `DoProductSendWarehouseOrderComplete`                                    |
| **WCF 接口**     | `DoProductLineSendWarehouseOrderSendLot`                                 |
| **数据库表**     | `ProductLineSendWarehouseOrder`                                          |

### 6.6 批次拆分（辅助操作）

| 属性             | 值                                                             |
| ---------------- | -------------------------------------------------------------- |
| **阶段**         | 配置产出                                                       |
| **序号**         | 6.6（产出阶段辅助）                                            |
| **前驱**         | 6.1 工单启动后                                                 |
| **后继**         | —（产出过程中按需）                                            |
| **主导系统**     | CS + BS + PDA                                                  |
| **参与系统**     | CS, BS, PDA前端, PDA后端                                       |
| **PDA Fragment** | `FragmentSerial_SerialNumberSplit_A/B`, `Fragment_Stack_A/B/C` |
| **CS 窗体**      | `frmME_WIPLotSplit.cs`                                         |
| **BS BLL**       | `CKZY_LotSplitBLL`, `MESZZZX_WIPLotSplitBLL`                   |
| **PDA 后端 WCF** | `DoLotMove` — 批次移动                                         |
| **数据库表**     | `SplitHistory`, `SplitHistoryDetails`, `SplitPartHistory`      |

---

## 阶段七：结案 (Case Closure)

### 7.1 BPR记录

| 属性              | 值                                                           |
| ----------------- | ------------------------------------------------------------ |
| **阶段**          | 结案                                                         |
| **序号**          | 7.1                                                          |
| **前驱**          | 6.5 成品入库                                                 |
| **后继**          | 7.2 结案清理                                                 |
| **主导系统**      | 桌面 MES (CS) + Web MES (BS)                                 |
| **参与系统**      | CS, BS                                                       |
| **CS 窗体**       | `frmME_BPRRecord.cs`, `frmME_BPRRecordEdit.cs`               |
| **BS BLL**        | `MESZZZX_BPRRecordBLL` — 工单/BPR/规格明细/步骤查看/设备检验 |
| **BS Controller** | `MESZZZX_BPRRecordController`                                |
| **BS BLL**        | `CKZY_BPRStartQueryBLL`                                      |
| **数据库表**      | `BPRHistory*`, `BPRTimeHistory*`, `BPRWorkLog`               |

### 7.2 结案清理

| 属性         | 值                                                      |
| ------------ | ------------------------------------------------------- |
| **阶段**     | 结案                                                    |
| **序号**     | 7.2                                                     |
| **前驱**     | 7.1 BPR记录                                             |
| **后继**     | —（流程终点）                                           |
| **主导系统** | 桌面 MES (CS)                                           |
| **参与系统** | CS                                                      |
| **CS 窗体**  | `frmME_CleanBPREnd.cs` — **唯一确认结案入口**           |
| **数据库表** | `BPRLockHistory`                                        |
| **备注**     | ⚠️ 结案的确切定义待验证（关闭工单？关闭BPR？关闭批次？） |

---

## 衔接关系总表

| 衔接点                    | 阶段间过渡                |
| ------------------------- | ------------------------- |
| 标签分发 → PDA扫码入库    | 采购(1.3) → 入库(2.1)     |
| 入库完成 → 抽样标签       | 入库(2.2/2.3) → 质检(3.1) |
| 放行通过 → 投前称重       | 质检(3.4) → 称料(4.1)     |
| 称重确认 → 工单领料       | 称料(4.1) → 上料(5.1)     |
| 上料完成 → 余料称重(退回) | 上料(5.2) → 称料(4.3)     |
| 上料完成 → 工单启动       | 上料(5.2) → 配置产出(6.1) |
| 成品入库 → BPR记录        | 配置产出(6.5) → 结案(7.1) |
| BPR记录 → 结案清理        | 结案(7.1) → 结案(7.2)     |

---

## 跨系统 ID 与状态追踪点

| 实体           | 传递路径               | 关键字段                               |
| -------------- | ---------------------- | -------------------------------------- |
| 采购单号       | 采购 → 入库            | `PurchaseOrderNM`                      |
| 入库单号       | 入库 → 质检            | `InWHOrderNM`, `MfgInWHOrderNM`        |
| 批次号 (LotNM) | 贯穿全部               | `LotNM` — 收货/检验/上料/产出/结案共用 |
| 工单号         | 上料 → 配置产出 → 结案 | `MfgOrderNM`                           |
| BPR号          | 配置产出 → 结案        | `BPRId`                                |
| 资源号         | 上料/设备启动          | `ResourceNM`                           |
