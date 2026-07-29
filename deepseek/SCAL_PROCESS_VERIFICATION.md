# SCAL 流程验证报告

> 日期：2026-07-24
> 基于：SCAL_SOURCE_INVENTORY_V2.md 盘点结果
> 方法：对照 5 个源码库，逐阶段阅读关键源码验证子流程

---

## 架构关键发现

PDA 后端 (`SZ_WCFService`) 的大多数业务操作是**存储过程的薄封装**：

```
PDA前端 (Android) → WCF (JSON) → 存储过程 (Pro_PDA_*) → 数据库
```

Web MES (BS) 和桌面 MES (CS) 通过 BLL→DAL→EF 走标准三层架构。

---

## 第一阶段：采购 (Procurement)

### 已验证子流程

```
采购单创建 → 条码申请 → 标签分发
```

### 1.1 采购单创建

| 维度          | 证据                                                             |
| ------------- | ---------------------------------------------------------------- |
| **执行系统**  | Web MES (BS)                                                     |
| **BLL**       | `CKZY_LotApplyBLL.GetPurchaseOrderListByPage()` — 采购单下拉列表 |
| **DAL**       | `CKZY_LotApplyDAL`                                               |
| **数据库表**  | `PurchaseOrder`, `PurchaseOrderDetail`（DOC 文档确认）           |
| **Demo 页面** | `business/sample.html`                                           |

### 1.2 条码申请

| 维度               | 证据                                                                    |
| ------------------ | ----------------------------------------------------------------------- |
| **执行系统**       | Web MES (BS) + PDA 后端                                                 |
| **BS BLL**         | `CKZY_LotApplyBLL` — 提供采购单号、物料编号、DateCode、标签定义下拉列表 |
| **BS Controller**  | `CKZY_LotApplyController` (Areas/WarehouseOperation)                    |
| **PDA 后端 BLL**   | `BarCodeDefBll` — 条码定义的 CRUD                                       |
| **PDA 后端 Model** | `BarCodeDef` / `BarCodeDefForTran`                                      |
| **数据库表**       | `BarCodeDef`, `PurchaseOrderLotApply`（DOC 文档确认）                   |
| **关联 BS 模块**   | `CKZY_LotApplyReprint`（标签补打）, `CKZY_LotBatchRePrint`（批量补打）  |

**流程说明**：
1. Web MES 端根据采购单号查询采购明细
2. 选择物料后进入条码申请页面
3. 系统生成标签申请记录 (`PurchaseOrderLotApply`)
4. PDA 后端 `BarCodeDefBll` 管理条码定义配置
5. CS 端可通过 `frmME_LotReprint` 补打标签

### 1.3 标签分发

| 维度              | 证据                                             |
| ----------------- | ------------------------------------------------ |
| **执行系统**      | Web MES (BS)                                     |
| **BS BLL**        | `SendLabelQueryBLL` — 标签分发查询               |
| **BS Controller** | `SendLabelQueryController`                       |
| **数据库表**      | 从 `PurchaseOrderLotApply` 关联标签打印/分发记录 |

> ⚠️ **待验证**：标签分发的完整数据流（申请→生成→打印→分发状态变更）

---

## 第二阶段：入库 (Receiving)

### 已验证子流程

```
PDA扫码入库 → 入库单生成
```

> 入库流程存在两个入口：PDA 扫码入库（主）和 Web MES 端操作（辅）。

### 2.1 PDA 扫码入库

| 维度             | 证据                                                                              |
| ---------------- | --------------------------------------------------------------------------------- |
| **执行系统**     | PDA 前端 + PDA 后端                                                               |
| **PDA Fragment** | `JieShouFramgnet_A.java` / `JieShouFramgnet_B.java` — 入库扫描界面                |
| **PDA Thread**   | `ScanReceiveThread.java` — 调用 `GetProductInWarehouseOrderSumInfo`               |
| **PDA Thread**   | `SaoMiaoJieShouThread.java` — 扫描入库确认                                        |
| **PDA Thread**   | `AddRukuDanThread.java` — 调用 `AddProductInWarehouseOrder` 创建入库单            |
| **PDA Thread**   | `RukuThread.java` / `RukuThread2.java` / `RuKuThreadNew.java`                     |
| **PDA Fragment** | `RuKuFramgnet_A.java` / `RuKuFramgnet_B.java` — 入库操作界面                      |
| **PDA Fragment** | `ZanShouFramgnet_A.java` / `ZanShouFramgnet_B.java` — 暂收界面                    |
| **WCF 接口**     | `AddProductInWarehouseOrder` → 调用 SP `Pro_PDA_MfgInWHOrder_Add`                 |
| **WCF 接口**     | `AddProductInWarehouseOrderDetail` → 调用 SP `Pro_PDA_MfgInWHOrder_AddDetail`     |
| **WCF 接口**     | `DoInWH` — 执行入库                                                               |
| **WCF 接口**     | `CheckInWHQty` — 校验入库数量                                                     |
| **WCF 接口**     | `GetProductInWarehouseOrderSumInfo` — 获取入库单汇总信息                          |
| **PDA 后端 BLL** | `InWHBll` — 入库业务逻辑（Add/Delete/GetModel）                                   |
| **PDA 后端 DAL** | `InWHDal` — 入库数据访问                                                          |
| **数据库表**     | `InWH`, `InWHOrder` (含 `InWHOrderNM`), `InWHDetail`, `CheckInHistory`, `Package` |

### 2.2 暂收流程

| 维度             | 证据                                                                            |
| ---------------- | ------------------------------------------------------------------------------- |
| **PDA Fragment** | `ZanShouFramgnet_A/B`                                                           |
| **PDA Thread**   | `ZanShouThread.java`, `ZanShouMingXiThread.java`                                |
| **WCF 接口**     | `AddTemporaryReceiptOrder` → SP `Pro_PDA_TemporaryReceiptOrder_Add`             |
| **WCF 接口**     | `AddTemporaryReceiptOrderDetail` → SP `Pro_PDA_TemporaryReceiptOrder_AddDetail` |
| **WCF 接口**     | `CompliteTemporaryReceipt` — 完成暂收                                           |

### 2.3 Web MES 端入库查询

| 维度              | 证据                                                                                |
| ----------------- | ----------------------------------------------------------------------------------- |
| **BS BLL**        | `CKZY_RecieveMaterialQueryBLL` — 入库查询                                           |
| **BS Controller** | `CKZY_RecieveMaterialQueryController`                                               |
| **BS BLL**        | `CKZY_TemporaryReceiptOrderBLL` — 临时入库单                                        |
| **BS BLL**        | `CKZY_UnfinishedTempReceiptBLL` / `CKZY_UnfinishedWarehouseReceiptBLL` — 未完成入库 |

### 2.4 入库-质检的衔接点

**扫码入库后会触发抽样标签流程**：
- PDA 入库完成后，系统产生入库批次
- Web MES `SamplingLabelQueriesBLL` 可查询待抽样的批次
- 对应 `business/sampling-label.html` Demo 中的「扫码入库 → 抽样标签」

---

## 第三阶段：质检 (Quality Inspection)

### 已验证子流程

```
抽样标签 → 送检 → 检验判定 → 放行/滞留
```

### 3.1 抽样标签

| 维度              | 证据                                                                           |
| ----------------- | ------------------------------------------------------------------------------ |
| **执行系统**      | Web MES (BS)                                                                   |
| **BS BLL**        | `SamplingLabelQueriesBLL` — 抽样标签查询                                       |
| **BS Controller** | `SamplingLabelQueriesController`                                               |
| **BS BLL**        | `ZLKZ_SamplingLabelBLL` — 抽样标签管理（物料类别、已收料列表、已申请样品批次） |
| **BS BLL**        | `ZLKZ_BCPSamplingLabelBLL` — 半成品抽样标签                                    |
| **BS BLL**        | `ZLKZ_GZSamplingLabelBLL` — 罐装抽样标签                                       |
| **BS BLL**        | `ZLKZ_PZSamplingLabelBLL` — 配制抽样标签                                       |
| **BS BLL**        | `ZLKZ_ProductRetentionSampleLabelBLL` — 产品留样标签                           |
| **数据库表**      | `SampleLot`, `SampleLotDetail`（DOC 文档确认）                                 |
| **Demo 页面**     | `business/sampling-label.html` — 完整展示了「扫码入库 → 抽样标签 → 质检判定」  |

**`sampling-label.html` Demo 确认的来料流程链**：
```
采购单采购 → 条码申请 → 标签分发 → 扫码入库 → 抽样标签 → 质检判定
```

### 3.2 送检

| 维度              | 证据                                                                     |
| ----------------- | ------------------------------------------------------------------------ |
| **执行系统**      | Web MES (BS)                                                             |
| **BS BLL**        | `ZLKZ_SendBLL` — 送检管理（流水号验证、数据采集区域、物料/上料回车事件） |
| **BS Controller** | `ZLKZ_SendController` (推断)                                             |

### 3.3 检验判定

| 维度              | 证据                                                                           |
| ----------------- | ------------------------------------------------------------------------------ |
| **执行系统**      | Web MES (BS)                                                                   |
| **BS BLL**        | `MESZLKZ_InspectionBLL` — 检验管理（供应商查询、规格明细、批次列表、附件管理） |
| **BS Controller** | `MESZLKZ_InspectionController`                                                 |
| **BS BLL**        | `MESZLKZ_InspectionCPBLL` — 成品检验                                           |
| **BS BLL**        | `MESZLKZ_FinalInspectionBLL` — 终检                                            |
| **BS BLL**        | `MESZLKZ_ReInspecBLL` — 复检                                                   |
| **BS BLL**        | `MESZLKZ_InspectionExemptionBLL` — 检验豁免                                    |
| **BS BLL**        | `ZLKZ_AQLSamplePlanBLL` / `ZLKZ_AQLCalculatorBLL` — AQL 抽样方案               |
| **数据库表**      | `InspectionHistory`, 各类检验明细表（DOC 确认）                                |

### 3.4 放行/滞留

| 维度              | 证据                                              |
| ----------------- | ------------------------------------------------- |
| **执行系统**      | Web MES (BS) + PDA 后端                           |
| **BS BLL**        | `MESZLKZ_ReleaseHoldBLL` — 放行/滞留              |
| **BS BLL**        | `HoldReleaseHistoryBLL`（根 BLL）                 |
| **BS Controller** | `HoldReleaseHistoryController`                    |
| **PDA 后端 WCF**  | `DoHoldOrRelease` — PDA 端滞留/放行操作           |
| **PDA 前端**      | `FragmentHoldReleaseActivity` — PDA 滞留/放行页面 |
| **数据库表**      | `HoldReleaseHistory`                              |
| **BS BLL**        | `ZLKZ_AbolishLotNMBLL` — 批次号作废（极端场景）   |

### 3.5 IPQC 在线检测（产中质检，共 23+ 种）

全部在 Web MES (BS) 端：

| 检测类型   | BLL 类                                            |
| ---------- | ------------------------------------------------- |
| 首检       | `MESZLKZ_PAD_IPQC_FirstCheckBLL`                  |
| 外观检验   | `MESZLKZ_PAD_IPQC_OnLineAppearanceInspectionBLL`  |
| 密封检查   | `MESZLKZ_PAD_IPQC_OnLineSealingCheckFormBLL`      |
| 密封泄漏   | `MESZLKZ_PAD_IPQC_OnLineSealLeakageCheckBLL`      |
| 密封宽度   | `MESZLKZ_PAD_IPQC_OnLineSealWidthCheckBLL`        |
| 扭矩控制   | `MESZLKZ_PAD_IPQC_OnLineTorqueControlBLL`         |
| 热罐检查   | `MESZLKZ_PAD_IPQC_HotTankCheckBLL`                |
| 压漏检查   | `MESZLKZ_PAD_IPQC_OnLinePressureLeakageCheckBLL`  |
| 标签检查   | `MESZLKZ_PAD_IPQC_OnLineLableCheckBLL`            |
| 长度检查   | `MESZLKZ_PAD_IPQC_OnLineLengthCheckCheckBLL`      |
| 码日期检查 | `MESZLKZ_PAD_IPQC_OnLineCodeDateBLL`              |
| STM高度    | `MESZLKZ_PAD_IPQC_OnLineSTMHeightCheckBLL`        |
| TAMU检查   | `MESZLKZ_PAD_IPQC_OnLineTAMUCheckBLL`             |
| 条码扫描   | `MESZLKZ_PAD_IPQC_OnLineBarCodeScanFoamBLL`       |
| Crimp真空  | `MESZLKZ_PAD_IPQC_OnLineCrimpVacuumCheckBLL`      |
| 活化检查   | `MESZLKZ_PAD_IPQC_OnLineActivationCheckBLL`       |
| 包材变更   | `MESZLKZ_PAD_IPQC_PackageMaterialChangeBLL`       |
| 包材计划   | `MESZLKZ_PAD_IPQC_PackingMaterialPlanBLL`         |
| 产前准备   | `MESZLKZ_PAD_IPQC_PreparationBeforeProductionBLL` |
| 设备调整   | `MESZLKZ_PAD_IPQC_EquipmentAjustingBLL`           |
| 测试报告   | `MESZLKZ_PAD_IPQC_TestReportBLL`                  |
| 称重设备   | `MESZLKZ_PAD_IPQC_WeightingEquipmentFoamBLL`      |
| 复查       | `MESZLKZ_PAD_IPQC_CheckAgainBLL`                  |

---

## 第四阶段：称重 (Weighing)

### 已验证子流程

```
投前称重确认 → 称重测试 → 余料称重
```

> **称重是投料的前置阶段**。物料在投入产线/设备之前，必须先进行精确称重以确认数量。余料退回时也需要称重记录。

| 维度              | 证据                                                                                                                        |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **执行系统**      | 桌面 MES (CS) 为主，BS 端辅助                                                                                               |
| **CS 窗体**       | `frmME_IssueMaterial_Weighting.cs` — **投前称重确认**                                                                       |
| **CS 窗体**       | `frmME_WeightingTest.cs` — **称重测试**                                                                                     |
| **CS 窗体**       | `frmME_SurplusMaterial.cs` / `frmME_SurplusMaterialGZ.cs` — 余料称重                                                        |
| **BS BLL**        | `CKZY_MaterialWeighingBLL` — 物料称重查询                                                                                   |
| **BS Controller** | `CKZY_MaterialWeighingController`                                                                                           |
| **BS BLL**        | `MESZZZX_SurplusMaterialBLL` — 余料称重（BS端）                                                                             |
| **数据库表**      | `WeightingEquipmentContentList`, `WeightingEquipmentHanderList`, `WeightingEquipmentValueView` 等（DOC + Apps.Models 确认） |

---

## 第五阶段：投料 (Material Loading)

### 已验证子流程

```
工单领料 → 发料/投料
```

> 称重确认完成后，物料正式投入产线/设备。注意区分：
> - **领料** = PDA 端从仓库领出物料
> - **投料** = CS 端将已称重的物料投入设备/产线端口

### 5.1 工单领料（PDA端）

| 维度             | 证据                                                                       |
| ---------------- | -------------------------------------------------------------------------- |
| **执行系统**     | PDA 前端 + PDA 后端                                                        |
| **PDA Fragment** | `GongDanLingLiaoFragment_A.java` / `_B` / `_C`（及 `_New` 版本）— 工单领料 |
| **PDA Fragment** | `Fragment_GongDanTouLiao_A.java` / `_B` / `_C` — 工单投料                  |
| **PDA Thread**   | `GongDanLingLiaoThread.java` — 领料                                        |
| **PDA Thread**   | `GongDanLingLiaoQueRenThread.java` — 领料确认                              |
| **PDA Thread**   | `FaLiaoThread.java` — 发料（扫描物料→调用 WCF）                            |
| **PDA Thread**   | `B_FaLiaoThread.java` — 发料（B版本）                                      |
| **PDA Thread**   | `TouLiaoItemThread.java` / `TouLiaoItemThread2.java` — 投料明细            |
| **PDA Thread**   | `TouLiaoPiciHaoThread.java` — 投料批次号                                   |
| **PDA Thread**   | `YiFaLiaoMingXiThread.java` — 已发料明细                                   |

### 5.2 工单发料/投料（CS端 + BS端）

| 维度               | 证据                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| **执行系统**       | 桌面 MES (CS) + Web MES (BS)                                                                           |
| **CS 窗体**        | `frmME_IssueMaterial.cs` — **发料/投料主界面**                                                         |
| **CS 窗体**        | `frmME_IssueMaterialCheck.cs` — 投料校验                                                               |
| **BS BLL**         | `MESZZZX_IssueMaterialBLL` — 发料业务（工单列表、BPR列表、已发料列表、流水号验证）                     |
| **BS Controller**  | `MESZZZX_IssueMaterialController`                                                                      |
| **PDA 后端 WCF**   | `DoLoadMaterial` — PDA端投料                                                                           |
| **PDA 后端 WCF**   | `CompliteLoadMaterial` — 完成投料                                                                      |
| **PDA 后端 WCF**   | `CompliteLoadSMTMaterial` — 完成SMT投料                                                                |
| **PDA 后端 WCF**   | `DoProductLineLoadMaterialLoad` / `UnLoad` — 产线投料加载/卸载                                         |
| **PDA 后端 WCF**   | `DoDispatchLot` — 发料扫描                                                                             |
| **PDA 后端 WCF**   | `DoDisptachLot` — 派工发料                                                                             |
| **PDA 后端 WCF**   | `DoProductLineDispatchConfirm` — 产线派工确认                                                          |
| **PDA 后端 BLL**   | `LoadMaterialBll` — 投料业务（AddOBA/AddOQC/AddPackage/AddShip/CompliteLoad）                          |
| **PDA 后端 DAL**   | `LoadMaterialDal`, `ResourceLoadedMaterial2Dal`                                                        |
| **PDA 后端 Model** | `LoadMaterial`, `ResourceLoadedMaterial2`, `CompltedLoadInfo`                                          |
| **数据库表**       | `BPRLoadMaterial`, `ProductLineLoadMaterialHistory`, `V_ResourceLoadMaterial`, `DispatchMaterialOrder` |

**流程说明**：
1. PDA 端执行工单领料（`GongDanLingLiaoFragment`）
2. CS 端 `frmME_IssueMaterial` 执行发料/投料（称重后物料投入产线/设备）
3. BS 端 `MESZZZX_IssueMaterialBLL` 可与 CS 端并行的 Web 版发料
4. 投料完成后 → 进入第六阶段：配方产出

## 第六阶段：配方产出 (Formula Output)

### 已验证子流程

```
工单启动 → 设备启动 → 配方执行 → 产出
```

### 6.1 工单启动

| 维度             | 证据                                                       |
| ---------------- | ---------------------------------------------------------- |
| **执行系统**     | PDA 前端 + PDA 后端                                        |
| **PDA Activity** | `StartMfgOrder.java`, `StartMfgOrderLists.java` — 工单启动 |
| **PDA 后端 WCF** | `AddMfgOrderStart` — 添加工单启动                          |
| **PDA 后端 WCF** | `DoMfgOrderStartStart` — 执行工单启动                      |
| **PDA 后端 WCF** | `CheckThisResourceIsStarting` — 检查资源是否已启动         |
| **PDA 后端 BLL** | `MfgOrderStartBll` — 工单启动业务                          |
| **PDA 后端 BLL** | `MfgOrderStartLotBll` — 工单启动批次                       |
| **数据库表**     | `MfgOrderStart`, `ResourceCurrentMfgOrderStartLot`         |

### 6.2 设备启动

| 维度             | 证据                                                  |
| ---------------- | ----------------------------------------------------- |
| **执行系统**     | 桌面 MES (CS)                                         |
| **CS 窗体**      | `frmME_EquipmentStart.cs` — 设备启动                  |
| **CS 窗体**      | `frmME_StorageTankEquipmentStart.cs` — 储罐设备启动   |
| **CS 窗体**      | `frmME_SteelTankEquipmentStart.cs` — 钢罐设备启动     |
| **CS 窗体**      | `frmME_PreplanTankEquipmentStart.cs` — 预排罐设备启动 |
| **CS 窗体**      | `frmME_TicketStart.cs` — 票据启动                     |
| **CS 窗体**      | `frmME_EquipmentStopHistory.cs` — 设备停机历史        |
| **PDA 后端 WCF** | `DoMachineBegain` / `DoMachineLeave` — 人员设备上下机 |

### 6.3 配方管理

| 维度              | 证据                                                                |
| ----------------- | ------------------------------------------------------------------- |
| **执行系统**      | PDA 后端 + Web MES (BS)                                             |
| **PDA 后端 BLL**  | `RecipeBll` — 配方 CRUD（AddRecipe/DeleteRecipe/GetRecipeBySpecId） |
| **PDA 后端 DAL**  | `RecipeDal`                                                         |
| **BS BLL**        | `MESGYLC_RecipeBLL` (推断: MESGYLC_RecipeController 存在)           |
| **BS Controller** | `MESGYLC_RecipeController`                                          |
| **数据库表**      | `Recipe`, `SpecRecipe`, `ProductRecipeAndWorkersSetting*`           |

### 6.4 产出（多类型）

| 产出类型           | CS 窗体                                           | BS BLL                                                                              | WCF 接口                                                                 |
| ------------------ | ------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **BCP 半成品产出** | `frmME_BCPOutput`                                 | `MESZZZX_BCPOutputBLL`                                                              | —                                                                        |
| **PZ 配置产出**    | `frmME_PZOutput` / `frmME_PZoutputTKBD`           | `MESZZZX_PZOutputBLL`                                                               | —                                                                        |
| **设备配置产出**   | `frmME_EquipmentConfigOut`                        | `MESZZZX_EquipmentConfigOutBLL`                                                     | —                                                                        |
| **PDA 产出**       | `Fragment_Output_a/b`, `Fragment_Collect_a/b/c/d` | —                                                                                   | `DoOutput`, `DoProductLineOutPut`, `DoProductLineExcutionOutPut`         |
| **成品包装**       | `frmME_CPPackage` / `frmME_NZBPackaging`          | `MESZZZX_CPPackageBLL` / `MESZZZX_InnerPackagingBLL` / `MESZZZX_PalletPackagingBLL` | —                                                                        |
| **成品入库**       | —                                                 | —                                                                                   | `CompliteProductInWarehouseOrder` / `CompliteProductInWarehouseOrderNew` |

**PDA 产出相关**：
| 维度             | 证据                                                               |
| ---------------- | ------------------------------------------------------------------ |
| **PDA Fragment** | `Fragment_Output_a.java` / `_b` — 产出扫描                         |
| **PDA Fragment** | `Fragment_Collect_a.java` / `_b` / `_c` / `_d` — 数据采集          |
| **PDA Thread**   | `YesThread.java` — `DoOutput` 产出确认                             |
| **PDA Thread**   | `YesThreadNew.java` — 新版本产出确认                               |
| **PDA Thread**   | `TotalThread.java` — `GetProductSendWarehouseSentLotList` 产出汇总 |
| **PDA Fragment** | `ChanChuPingRuKuNewFragment_A/B/C` — 成品产出入库                  |

**成品产出入库 WCF 接口**：
| WCF 方法                                     | 对应 SP                                     |
| -------------------------------------------- | ------------------------------------------- |
| `CheckProductInWarehouseLotInfo`             | PDA 成品入库批次校验                        |
| `CheckProductSendWarehouseLotInfo`           | PDA 产线送仓批次校验                        |
| `AddProductLineSendWarehouseOrder`           | `Pro_PDA_ProductLineSendWarehouseOrder_Add` |
| `DoProductSendWarehouseOrderComplete`        | 产线送仓完成                                |
| `DoProductLineSendWarehouseOrderSendLot`     | 产线送仓发送批次                            |
| `CompliteProductInWarehouseOrder` / `...New` | 成品入库完成                                |

### 6.5 批次拆分（产出阶段辅助操作）

| 维度               | 证据                                                      |
| ------------------ | --------------------------------------------------------- |
| **PDA Fragment**   | `FragmentSerial_SerialNumberSplit_A/B` — 序列号拆分       |
| **PDA Fragment**   | `Fragment_Stack_A/B/C` — 堆栈拆分                         |
| **CS 窗体**        | `frmME_WIPLotSplit.cs` — 在制品批次拆分                   |
| **BS BLL**         | `CKZY_LotSplitBLL` — 批次拆分                             |
| **BS BLL**         | `MESZZZX_WIPLotSplitBLL` — 在制品拆分                     |
| **PDA 后端 WCF**   | `DoLotMove` — 批次移动（拆分的底层操作）                  |
| **PDA 后端 Model** | `SplitHistory`, `SplitHistoryDetails`, `SplitPartHistory` |
| **数据库表**       | `SplitHistory*`, `LotSplit` 相关表                        |

---

## 第七阶段：结案 (Case Closure)

### 已验证入口

| 维度              | 证据                                                                        |
| ----------------- | --------------------------------------------------------------------------- |
| **执行系统**      | 桌面 MES (CS)                                                               |
| **CS 窗体**       | `frmME_CleanBPREnd.cs` — **结案清理（唯一确认入口）**                       |
| **CS BPR相关**    | `frmME_BPRRecord.cs` / `frmME_BPRRecordEdit.cs` — BPR记录编辑               |
| **BS BLL**        | `MESZZZX_BPRRecordBLL` — BPR记录（工单列表、规格明细、步骤查看、设备检验）  |
| **BS Controller** | `MESZZZX_BPRRecordController`                                               |
| **BS BLL**        | `CKZY_BPRStartQueryBLL` — BPR启动查询                                       |
| **数据库表**      | `BPRHistory*`, `BPRTimeHistory*`, `BPRWorkLog`, `BPRLockHistory`（DOC确认） |

> ⚠️ **待验证**：
> - 「结案」的准确定义（关闭工单？关闭BPR？关闭批次？）
> - `frmME_CleanBPREnd` 的实际操作逻辑
> - BS端是否有对应的结案操作
> - 结案的前置条件（所有产出完成？质检通过？）

---

## 跨阶段关联汇总

### 完整流程链（基于已有证据）

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│ 1. 采购       │    │ 2. 入库       │    │ 3. 质检           │
│              │    │              │    │                  │
│ 采购单创建 ──►│───►│ 扫码入库 ────►│───►│ 抽样标签         │
│ 条码申请      │    │ 入库单生成    │    │ 送检 → 检验判定   │
│ 标签分发      │    │              │    │ 放行/滞留         │
└──────────────┘    └──────────────┘    └──────────────────┘
                                                  │
                                                  ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│ 6. 配置产出   │    │ 5. 上料       │    │ 4. 称料           │
│              │    │              │    │                  │
│ 工单启动      │◄───│ 工单领料      │◄───│ 投前称重确认     │
│ 设备启动      │    │ 发料/上料     │    │ 称重测试         │
│ 配方执行→产出 │    │              │    │ 余料称重         │
└──────┬───────┘    └──────────────┘    └──────────────────┘
       │
       ▼
┌──────────────┐
│ 7. 结案       │
│              │
│ BPR记录       │
│ 结案清理      │
└──────────────┘
```

### 系统参与度矩阵

| 阶段     | PDA前端    | PDA后端   | Web MES(BS)  | 桌面MES(CS)  | 主导系统      |
| -------- | ---------- | --------- | ------------ | ------------ | ------------- |
| 采购     | —          | 条码定义  | ✅ 主         | 标签补打     | **BS**        |
| 入库     | ✅ 主       | ✅ 主      | 查询         | —            | **PDA**       |
| 质检     | —          | 滞留/放行 | ✅ 主         | —            | **BS**        |
| 称料     | —          | —         | 查询         | ✅ 主         | **CS**        |
| 上料     | ✅ 领料     | ✅ 上料    | ✅ 发料查询   | ✅ 发料/上料  | **CS+PDA**    |
| 配置产出 | ✅ 产出扫描 | ✅ 产出    | ✅ 多类型产出 | ✅ 多类型产出 | **CS+BS+PDA** |
| 结案     | —          | —         | BPR查询      | ✅ 主         | **CS**        |

### 关键存储过程（PDA后端直调）

所有 PDA WCF 方法都通过以下模式调用数据库：

```
WCF Method → CommonBll.PageQueryForReportForSP("exec Pro_PDA_xxx ...")
```

已确认的 SP 前缀：
- `Pro_PDA_MfgInWHOrder_*` — 入库单
- `Pro_PDA_ProductLineReturnApplyOrder_*` — 产线退料申请
- `Pro_PDA_ProductLineReturnOrder_*` — 产线退料
- `Pro_PDA_ProductLineSendWarehouseOrder_*` — 产线送仓
- `Pro_PDA_StockTansferOrder_*` — 转库
- `Pro_PDA_TemporaryReceiptOrder_*` — 临时入库
- `Pro_PDA_ShipBill_*` — 发货

---

## 待验证项

1. **标签分发**的完整数据流（申请→生成→打印→分发状态）
2. **"结案"**的准确定义和技术实现逻辑
3. **配方产出**的多种产出类型之间的区别和触发条件
4. 每个阶段的前置条件和状态流转规则
5. **PDA 盘点**功能（`DoPI`）在整体流程中的位置
6. 产线退料（`ProductLineReturn*`）与入库/退货的区别

---

## 下一步

按 `SCAL_PROCESS_MAP_REQUIREMENTS.md` 工作方法第 3 步：

> **为每个子流程记录前驱/后继/参与系统/实现证据/数据实体/可选 Demo 目标**
