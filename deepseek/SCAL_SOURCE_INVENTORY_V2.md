# SCAL 源码盘点 V2

> 盘点日期：2026-07-24
> 范围：PDA前端、PDA后端、Web MES、桌面MES客户端、数据库
> 状态：**源码结构盘点完成，待进入流程验证阶段**

---

## 1. PDA 前端 — `E:\code\scal-pda-f\scal-wms-app`

**技术栈**：Android Gradle 项目（Java）

### 1.1 目录结构

```
app/src/main/java/
├── com/chanham/chmesandroid/     ← 主业务模块
│   ├── fragment/     (60+ Fragment)    ← 页面碎片
│   ├── thread/       (70+ Thread)      ← 后台API调用线程
│   ├── newactivity/  (80+ Activity)    ← 页面容器
│   ├── adapter/      (40+ Adapter)     ← 列表适配器
│   ├── bean/         (45+ Bean)        ← 数据传输对象
│   ├── model/        (2 个)            ← 数据模型接口
│   ├── views/        (5 个)            ← 自定义视图
│   ├── util/         (11 个)           ← 工具类(蓝牙打印/网络等)
│   ├── service/      (1 个)            ← MyService
│   ├── ab/           (2 个)            ← FragmentAB/FunctionAB
│   ├── br/                             ← BroadcastReceiver
│   └── crash/                          ← 崩溃处理
├── com/example/xxxmesandroidclient/wcf/  ← WCF客户端代理
├── com/mining/app/                       ← 第三方SDK入口
├── inters/                               ← 业务回调接口(3个)
└── zpSDK/zpSDK/                          ←  zpSDK(打印相关)
```

### 1.2 核心业务模块（按 Fragment 分类）

| 业务域           | Fragment 文件                                                                             | 对应 Thread                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **收货/入库**    | `JieShouFramgnet_A/B`, `RuKuFramgnet_A/B`, `ZanShouFramgnet_A/B`                          | `ScanReceiveThread`, `AddRukuDanThread`, `JieShouThread`, `SaoMiaoJieShouThread`, `ZanShouThread`, `RukuThread` 等 |
| **仓库作业**     | `CangKuFragment`, `SongKuFramgnet_A/B`, `Fragment_Stack_A/B/C`, `Fragment_UporDown_a/b/c` | `SongKuThread`, `SaoMiaoSongKuThread`, `DanPiThread`, `DuopiThread` 等                                             |
| **工单投料**     | `Fragment_GongDanTouLiao_A/B/C`                                                           | `FaLiaoThread`, `B_FaLiaoThread`, `TouLiaoItemThread`, `TouLiaoPiciHaoThread` 等                                   |
| **工单领料**     | `GongDanLingLiaoFragment_A/B/C`, `GongDanLingLiaoFragment_*_New`                          | `GongDanLingLiaoThread`, `GongDanLingLiaoQueRenThread`                                                             |
| **调料理库**     | `DiaoLiaoFramgnet_A`                                                                      | `JieLiaoThread`                                                                                                    |
| **产出**         | `Fragment_Output_a/b`, `Fragment_Collect_a/b/c/d`                                         | `YesThread`, `YesThreadNew`, `TotalThread`                                                                         |
| **产线退料**     | `ProductionLineReturnSelectNewFragment_A/B/C`                                             | `ProductLineReturnThread`, `ReturnSelectThreadNew`                                                                 |
| **退货**         | `ReturnFramgnet_A/B`, `ReturnApplyFramgnet_A/B/C`                                         | `ReturnThread`, `ReturnApplyThread`, `ReturnDetailThread`                                                          |
| **发货**         | `FinishProductShipment_A/B`                                                               | `FinishShipThread`, `FinishProductSaveThread`                                                                      |
| **成品产出入库** | `ChanChuPingRuKuNewFragment_A/B/C`                                                        | `RuKuThreadNew`, `RuKuMingXiNewThread`                                                                             |
| **不良产出**     | `BuLiangChanXianChanChuFragment_A/B`                                                      | —                                                                                                                  |
| **盘点**         | `ShengChanFragment`（含盘点布局`fragment_pandian*.xml`）                                  | `PlopThread`, `PlopMingXiThread`                                                                                   |
| **库存查询**     | —（独立 Activity）                                                                        | `KunCunChaXunThread`, `GetStockNMThread`                                                                           |
| **有效期**       | `Fragment_youxiaoqi_info`                                                                 | `YouXiaoQiThread`                                                                                                  |
| **序列号拆分**   | `FragmentSerial_SerialNumberSplit_A/B`                                                    | `SerialNumberSplitThread`                                                                                          |
| **上架**         | 独立 Activity `ShangJiaActivity`                                                          | —                                                                                                                  |
| **滞留/放行**    | 独立 Activity `FragmentHoldReleaseActivity`                                               | —                                                                                                                  |

### 1.3 PDA 调用后端的模式

- 所有网络请求通过 `AppVolley.java`（基于 Volley 库）
- 后端地址为 WCF 服务（`SZ_PDAService`），接口定义在 `ISZ_WCFService.cs`
- Bean 类承载请求/响应数据
- Thread 类封装每个业务操作的 API 调用逻辑

### 1.4 布局文件

`res/layout/` 下有 **200+** 个 XML 布局文件，涵盖所有业务页面。

---

## 2. PDA 后端 — `E:\code\scal-pda-b\scal-mes-pda-services`

**技术栈**：.NET Framework WCF 服务

### 2.1 项目结构

```
scal-mes-pda-services/
├── SZ_PDAService/           ← WCF 服务端点
│   ├── ISZ_WCFService.cs    ← 服务契约接口（100+ 方法）
│   └── SZ_WCFService.svc    ← 服务实现
├── XXXMES.Bll/              ← 业务逻辑层
├── XXXMES.Dal/              ← 数据访问层
├── XXXMES.Interface/        ← 接口定义
├── XXXMES.Model/            ← 数据模型
├── XXXMES.Service2/         ← 服务辅助类
└── XXXMES.Common/           ← 公共工具
```

### 2.2 BLL（业务逻辑）模块

| 子模块          | 类文件                                                                                                                                                                          | 业务领域                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **WMS**         | `FeedOrderBll`, `StorageLocationBll`                                                                                                                                            | 仓库作业                                      |
| **Transaction** | `InWHBll`, `LoadMaterialBll`, `MfgOrderStartBll`, `MfgOrderStartLotBll`, `ResourceLoadedMaterial2Bll`, `MfgOrderHistoryBll`, `LotMove/`, `LotStart/`, `LotTools/`, `LotTrans2/` | 入库、投料、工单启动、批次移动/拆分/合并      |
| **Product**     | `BarCodeDefBll`, `BOMBll`, `ProductBll`, `ProductFamilyBll`, `DataCollectBll` 等 16 个                                                                                          | 产品主数据、条码、BOM、数据采集、Hold/Release |
| **PlanAndTask** | `MfgOrderBll`, `SalesOrderBll`, `ShpOrderBll`, `ShopFlowScheduleBll` 等                                                                                                         | 工单、销售订单、排程                          |
| **IPQC**        | `IPQCCheckBll`, `IPQCCheckDetailBll`, `IPQCCheckMasterBll`, 异常/评分 等 9 个                                                                                                   | 过程质量控制                                  |
| **WorkFlow**    | `RecipeBll`, `SpecBll`, `ProcessSpecBll`, `WorkflowBll`, `OperationBll`                                                                                                         | 配方、工艺规范、工作流                        |
| **Enterprise**  | —                                                                                                                                                                               | 企业组织架构                                  |
| **ICCard**      | —                                                                                                                                                                               | IC卡管理                                      |

### 2.3 DAL（数据访问）模块

`SQLServer2005DAL/` 下有 **100+** 个 DAL 类，覆盖：
- 收货入库：`InWHDal`, `CheckInHistoryDal`
- 投料：`LoadMaterialDal`, `ResourceLoadedMaterial2Dal`
- 批次管理：`LotDal`, `LotMoveDal`, `LotStartDal`, `LotSplitDal` 等
- 工单：`MfgOrderDal`, `MfgOrderStartDal`, `MfgOrderHistoryDal`
- 历史追踪：`HistoryMainLineDal`, `IssueHistoryDal`, `ShipmentHistoryDal` 等
- 设备/资源：`ResourceDal`, `ResourceMonitorDal`
- 配方/工艺：`RecipeDal`, `ProcessSpecDal`
- IPQC：`IPQCCheckDal`, `IPQCCheckDetailDal`, `IPQCCheckMasterDal`
- 仓库：`FeedOrderDal`, `StorageLocationDal`

### 2.4 WCF 服务接口（ISZ_WCFService）主要方法分类

| 业务类别      | 代表方法                                                                                                    |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| **收货入库**  | `DoInWH`, `CheckInWHQty`, `AddProductInWarehouseOrder`, `CompliteProductInWarehouseOrder`                   |
| **工单启动**  | `AddMfgOrderStart`, `CheckThisResourceIsStarting`, `DoMfgOrderStartStart`                                   |
| **投料**      | `DoLoadMaterial`, `CompliteLoadMaterial`, `CompliteLoadSMTMaterial`, `DoProductLineLoadMaterialLoad/UnLoad` |
| **发料/派工** | `DoDispatchLot`, `DoDisptachLot`, `DoProductLineDispatchConfirm`                                            |
| **产出**      | `DoOutput`, `DoProductLineOutPut`, `DoProductLineExcutionOutPut`                                            |
| **产线退料**  | `AddProductLineReturnOrder`, `CompliteProductLineReturn`, `AddProductLineReturnApplyOrder`                  |
| **批次移动**  | `DoLotMove`                                                                                                 |
| **发货**      | `AddShipBill`, `CheckShipBillLot`, `CompleteOneShipBill`                                                    |
| **转库**      | `AddStockTansferOrder`, `CompliteStockTansferOrder`                                                         |
| **滞留/放行** | `DoHoldOrRelease`                                                                                           |
| **产线质检**  | `DoProductLineQC`                                                                                           |
| **盘点**      | `DoPI`（Physical Inventory）                                                                                |
| **设备/人员** | `DoMachineBegain/Leave`, `DoProductLineSpecLoadEquipment/Worker`                                            |
| **临时收货**  | `AddTemporaryReceiptOrder`, `CompliteTemporaryReceipt`                                                      |

---

## 3. Web MES (BS端) — `E:\code\scal-mes`

**技术栈**：.NET Framework，ASP.NET MVC + Web API + Entity Framework

### 3.1 解决方案结构

```
SZ-QDMES.sln
├── Apps.Web/          ← MES Web 前端（MVC）
├── Apps.WebApi/       ← Web API 层
│   ├── Controllers/   ← 120+ API 控制器
│   ├── Areas/
│   │   ├── ManufacturingExecution/Controllers/ (23个)
│   │   ├── WarehouseOperation/Controllers/ (33个)
│   │   ├── QualityControl/Controllers/
│   │   ├── BatchTool/Controllers/
│   │   ├── CPReport/Controllers/
│   │   ├── ESignature/Controllers/
│   │   └── TechnologicalProcess/Controllers/
│   └── MES/upload/
├── Apps.BLL/          ← 业务逻辑层
│   ├── MES/
│   │   ├── ManufacturingExecution/ (22 个 BLL)
│   │   ├── WarehouseOperation/ (34 个 BLL)
│   │   ├── QualityControl/ (50+ 个 BLL)
│   │   ├── BatchTool/
│   │   ├── CPReport/
│   │   ├── ElectronicSignature/
│   │   ├── EnterpriseArchitecture/
│   │   ├── ProductionModel/
│   │   └── TechnologicalProcess/
│   └── (根目录 70+ 其他 BLL)
├── Apps.DAL/          ← 数据访问层
│   ├── MES/（同上模块结构，含 ManufacturingExecution 22个、WarehouseOperation 34个）
│   ├── SCALDbContext.cs
│   └── SZDbContext.cs
├── Apps.Models/       ← 200+ 视图模型 + EF 自动生成实体
│   ├── MES/
│   │   ├── ManufacturingExecution/ (15+ 子目录)
│   │   ├── WarehouseOperation/ (30+ 子目录)
│   │   ├── Quality Control/ (30+ 子目录)
│   │   ├── BatchTool/
│   │   ├── CPReport/
│   │   ├── ElectronicSignature/
│   │   ├── EnterpriseArchitecture/
│   │   ├── ProductionModel/
│   │   └── TechnologicalProcess/
│   └── DB.edmx / DB.Context.tt ← EF 数据模型
├── Apps.IBLL/         ← BLL 接口
├── Apps.IDAL/         ← DAL 接口
├── Apps.Common/       ← 公共工具
├── Apps.Core/         ← 核心基础
├── Apps.Jobs/         ← 后台任务
└── Apps.Locale/       ← 国际化
```

### 3.2 核心业务模块速览

#### 制造执行（ManufacturingExecution）— BS端
| 子模块                                                                                | 说明            | 关联 CS 端                 |
| ------------------------------------------------------------------------------------- | --------------- | -------------------------- |
| `IssueMaterial`                                                                       | 发料/投料       | `frmME_IssueMaterial`      |
| `BCPOutput`                                                                           | BCP 产出        | `frmME_BCPOutput`          |
| `PZOutput` / `PZoutputTKBD`                                                           | 配置产出        | `frmME_PZOutput`           |
| `EquipmentConfigOut`                                                                  | 设备配置产出    | `frmME_EquipmentConfigOut` |
| `EquipmentStart`                                                                      | 设备启动        | `frmME_EquipmentStart`     |
| `EquipmentMove`                                                                       | 设备移动        | `frmME_EquipmentMove`      |
| `EquipmentSaveInput/Output`                                                           | 设备存取        | `frmME_EquipmentSave*`     |
| `BPRRecord`                                                                           | 批次生产记录    | `frmME_BPRRecord`          |
| `SurplusMaterial`                                                                     | 余料管理        | `frmME_SurplusMaterial`    |
| `WIPLotSplit`                                                                         | 在制品批次拆分  | `frmME_WIPLotSplit`        |
| `CPPackage`                                                                           | 成品包装        | `frmME_CPPackage`          |
| `InnerPackaging` / `PalletPackaging`                                                  | 内包装/托盘包装 | `frmME_NZBPackaging`       |
| `ReworkRecord`                                                                        | 返工记录        | `ReworkRecord/`            |
| `ScrapOrder`                                                                          | 报废单          | `frmME_ScrapOrder`         |
| `TicketStart`                                                                         | 票据启动        | `frmME_TicketStart`        |
| `StorageTankEquipmentStart` / `SteelTankEquipmentStart` / `PreplanTankEquipmentStart` | 罐体设备启动    | 对应 CS 同名字段           |

#### 仓库作业（WarehouseOperation）— BS端
| 子模块                                                                           | 说明                   |
| -------------------------------------------------------------------------------- | ---------------------- |
| `Warehouse`                                                                      | 仓库管理               |
| `LotApply` / `LotApplyReprint` / `LotBatchRePrint`                               | 标签申请/补打/批量补打 |
| `PrintSLLabel`                                                                   | 打印抽样标签           |
| `LotSplit`                                                                       | 批次拆分               |
| `PackageSplit`                                                                   | 包装拆分               |
| `ChangeQty`                                                                      | 数量变更               |
| `CombineStockOrder`                                                              | 合并库存单             |
| `FIFOAdjust`                                                                     | 先进先出调整           |
| `MaterialWeighing`                                                               | 物料称重               |
| `MaterialTraceability`                                                           | 物料追溯               |
| `StorageLocation` / `StorageLocationKanBan`                                      | 库位/看板              |
| `TemporaryReceiptOrder` / `UnfinishedTempReceipt` / `UnfinishedWarehouseReceipt` | 临时收货               |
| `WorkOrder` / `BPRStartQuery`                                                    | 工单/批次生产记录查询  |
| `DensityQuery`                                                                   | 密度查询               |
| `RecieveMaterialQuery`                                                           | 收货查询               |
| `ReturnMaterial` / `ReturnReceipt`                                               | 退料/退货              |
| `ShippingList` / `SalesStockingQuiry`                                            | 发货清单/销售备货      |
| `OutStockQuery`                                                                  | 出库查询               |
| `PLReturnQuery`                                                                  | 产线退料查询           |
| `InspectionLotNM`                                                                | 检验批次号             |
| `WorkloadAccount`                                                                | 工作量统计             |
| `ProductionPick`                                                                 | 生产领料               |
| `InspectionHistoryDataQuery`                                                     | 检验历史数据查询       |
| `IQCReportQuery`                                                                 | 来料检验报告查询       |
| `QualityTraceabilityQuery`                                                       | 质量追溯查询           |
| `ReleaseDetentionHistoryQuery`                                                   | 放行/滞留历史查询      |

#### 质量控制（QualityControl）— BS端
| 子模块                                                                                                       | 说明                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `SamplingLabel` / `BCPSamplingLabel` / `GZSamplingLabel` / `PZSamplingLabel` / `ProductRetentionSampleLabel` | 各类抽样标签（半成品/罐装/配置/留样）                                                                                                        |
| `Send`                                                                                                       | 送检                                                                                                                                         |
| `Inspection` / `InspectionCP` / `FinalInspection` / `ReInspec`                                               | 检验/成品检验/终检/复检                                                                                                                      |
| `InspectionExemption`                                                                                        | 检验豁免                                                                                                                                     |
| `InspectionMethod`                                                                                           | 检验方法                                                                                                                                     |
| `AQLSamplePlan` / `AQLCalculator`                                                                            | AQL抽样方案/计算器                                                                                                                           |
| `ReleaseHold`                                                                                                | 放行/滞留                                                                                                                                    |
| `AbolishLotNM`                                                                                               | 批次号作废                                                                                                                                   |
| `ChangeQADate`                                                                                               | 修改QA日期                                                                                                                                   |
| `CPReportSet`                                                                                                | 成品检验报告设置                                                                                                                             |
| `YYBatch`                                                                                                    | 原料批次                                                                                                                                     |
| `Reason` / `ReportVersion`                                                                                   | 原因代码/报告版本                                                                                                                            |
| **IPQC 在线检测（PAD_IPQC_*）**                                                                              | 首检、外观、密封、扭矩、热罐、压漏、标签、长度、码日期、STM高度、TAMU、 CrimpVacuum、包材变更/计划、产前准备、称重设备 等 **23+** 种在线检测 |
| `MPMSMaintain` / `MPMSMainHZ`                                                                                | MPMS维护/汇总                                                                                                                                |
| `QCProcessSpec` / `QCProcessSpecApprove`                                                                     | 质量控制工艺规范/审批                                                                                                                        |
| `QualityItems`                                                                                               | 质量项目                                                                                                                                     |
| `TSZTechnologyExplain`                                                                                       | 技术说明                                                                                                                                     |
| `MfgOrderLaserCodeHistory`                                                                                   | 工单激光码历史                                                                                                                               |

---

## 4. 桌面 MES 客户端 (CS端) — `E:\code\scal-mes-client`

**技术栈**：.NET WinForms

### 4.1 结构

```
WinClient/
├── MES/
│   ├── ManufacturingExecution/  ← 制造执行（核心，40+ 窗体）
│   ├── Preparation/             ← 生产准备（无配方启动）
│   ├── BatchTool/               ← 批次工具（标签补打）
│   ├── Debugging/               ← 调试
│   └── FingerprintCollection/   ← 指纹采集
├── Controls/                    ← 自定义控件
├── Content/                     ← 静态资源
├── ZPLHelper/                   ← ZPL标签打印
├── frmLogin.cs / MainForm.cs    ← 登录和主窗体
└── Program.cs                   ← 入口
```

### 4.2 制造执行窗体一览（ManufacturingExecution/）

| 窗体                                                  | 功能                 |
| ----------------------------------------------------- | -------------------- |
| `frmME_MfgOrder`                                      | 工单管理             |
| `frmME_IssueMaterial`                                 | 发料/投料            |
| `frmME_IssueMaterialCheck`                            | 投料校验             |
| `frmME_IssueMaterial_Weighting`                       | 投料称重             |
| `frmME_WeightingTest`                                 | 称重测试             |
| `frmME_BCPOutput`                                     | BCP 产出             |
| `frmME_PZOutput` / `frmME_PZoutputTKBD`               | 配置产出             |
| `frmME_EquipmentConfigOut`                            | 设备配置产出         |
| `frmME_EquipmentStart`                                | 设备启动             |
| `frmME_EquipmentStopHistory`                          | 设备停机历史         |
| `frmME_EquipmentMove`                                 | 设备移动             |
| `frmME_EquipmentSaveInput/Output`                     | 设备存取             |
| `frmME_EquipmentDataCollectList`                      | 设备数据采集列表     |
| `frmME_EquipmentDataCollectHistory`                   | 设备数据采集历史     |
| `frmME_EquipmentDataCollectTimeCollection`            | 设备数据采集时间汇总 |
| `frmME_BPRRecord` / `frmME_BPRRecordEdit`             | 批次生产记录         |
| `frmME_CleanBPREnd`                                   | **结案清理**         |
| `frmME_CPPackage`                                     | 成品包装             |
| `frmME_NZBPackaging`                                  | 内包装               |
| `frmME_SurplusMaterial` / `frmME_SurplusMaterialGZ`   | 余料管理             |
| `frmME_WIPLotSplit`                                   | 在制品拆分           |
| `frmME_EditExpirationDate`                            | 修改有效期           |
| `frmME_EditMfgBatch`                                  | 修改生产批次         |
| `frmME_EditPackageQty`                                | 修改包装数量         |
| `frmME_PZClearCheck`                                  | 配置清洁检查         |
| `frmME_PZIMEICheck`                                   | 配置 IMEI 检查       |
| `frmME_TicketStart` / `frmME_TicketStartEquipmentAdd` | 票据启动             |
| `frmME_PreplanTankEquipmentStart`                     | 预排罐设备启动       |
| `frmME_SteelTankEquipmentStart`                       | 钢罐设备启动         |
| `frmME_StorageTankEquipmentStart`                     | 储罐设备启动         |
| `frmME_OnLinePackCountCheckFoam/`                     | 在线包装数量检查     |
| `PreproductionLineCheckList/`                         | 产前检查清单         |
| `ProductionPerformanceInput/`                         | 生产绩效录入         |
| `ReworkRecord/`                                       | 返工记录             |
| `ScrapOrder/`                                         | 报废单               |
| `DeviceInformation`                                   | 设备信息             |
| `ChangePassWord`                                      | 修改密码             |

---

## 5. 数据库 — `E:\code\xxaedatabase`

### 5.1 结构

```
db-scripts/
├── backups/                              ← 版本备份
│   ├── 2026-06-30_original/             ← 原始备份
│   ├── 2026-07-06_original/
│   ├── 2026-07-08_original/
│   ├── 2026-07-10-original/
│   └── 2026-07-14_centerline-coordinate-repair_before/
└── changes/                              ← 增量变更
    ├── 2026-06-30_changed/              ← 审计追踪-数据链 SP
    ├── 2026-07-06_changed/
    ├── 2026-07-08_changed/
    ├── 2026-07-13_changed/
    └── 2026-07-14_changed/              ← Centerline 坐标修复 SP
```

### 5.2 已确认的存储过程

| 来源       | 存储过程                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-30 | `Pro_HistoryQuery_ALL`, `Pro_HistoryQuery_GetLotHistoryMainLineInfoByLotId`, `Pro_HistoryQuery_GetLotInfo`                       |
| 2026-07-14 | `Pro_CenterlineEntry_ChangeLodData`, `Pro_CenterlineEntry_ChangeSave`, `Pro_CenterlineEntry_Check`, `Pro_CenterlineEntry_Insert` |

> **注意**：完整 schema（621 张表）来自文档 HTML 页面，而非此目录。此目录仅含版本化的变更脚本，不是全量 schema 导出。

---

## 6. 文档与 Demo — `E:\code\scal-mes（副本）\TEMPS\DOC`

### 6.1 文档资产

| 资产                           | 说明                                            |
| ------------------------------ | ----------------------------------------------- |
| `main.html`                    | 表文档索引页                                    |
| `tables/`                      | 621 张表的 HTML 文档页面                        |
| `data/state.json`              | 元数据导出（但 PowerShell JSON 解析器无法解析） |
| `business/index.html`          | 业务 Demo 索引                                  |
| `business/sample.html`         | 业务 Demo 示例                                  |
| `business/sampling-label.html` | **抽样标签 Demo（已验证的来料流程链）**         |

### 6.2 sampling-label.html 确认的来料流程链

```
采购单采购 → 条码申请 → 标签分发 → 扫码入库 → 抽样标签 → 质检判定
```

该 Demo 还暴露了字段级数据血缘：`Product`, `Lot`, `MfgOrder`, `SampleLot`，以及打印机/标签配置信息。

---

## 7. 跨系统关联矩阵

| 业务阶段      | PDA前端                                                  | PDA后端                                                              | Web MES(BS)                                                           | 桌面MES(CS)                                                     | 数据库                                                 |
| ------------- | -------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------ |
| **条码申请**  | —                                                        | `BarCodeDefBll`                                                      | `CKZY_LotApply*`, `SendLabelQuery`                                    | `frmME_LotReprint`                                              | `BarCodeDef` 表                                        |
| **标签分发**  | —                                                        | —                                                                    | `SendLabelQuery`, `PrintSLLabel`                                      | —                                                               | —                                                      |
| **扫码收货**  | `JieShouFramgnet_*`, `RuKuFramgnet_*`                    | `InWHBll`, `DoInWH`                                                  | `CKZY_RecieveMaterialQuery`, `TemporaryReceiptOrder`                  | —                                                               | `InWH`, `CheckInHistory` 表                            |
| **抽样标签**  | —                                                        | —                                                                    | `SamplingLabelQueries`, `ZLKZ_SamplingLabel`                          | —                                                               | `SampleLot`, `SampleLotDetail` 表                      |
| **质检判定**  | —                                                        | `IPQCCheckBll`                                                       | `MESZLKZ_Inspection*`, `PAD_IPQC_*` 23+ 检测                          | —                                                               | `InspectionHistory` 表                                 |
| **工单投料**  | `Fragment_GongDanTouLiao_*`                              | `LoadMaterialBll`, `DoLoadMaterial`, `DoProductLineLoadMaterialLoad` | `MESZZZX_IssueMaterial`                                               | `frmME_IssueMaterial`                                           | `BPRLoadMaterial`, `ProductLineLoadMaterialHistory` 表 |
| **投料称重**  | —                                                        | —                                                                    | `CKZY_MaterialWeighing`                                               | `frmME_IssueMaterial_Weighting`, `frmME_WeightingTest`          | `WeightingEquipment*` 表                               |
| **工单领料**  | `GongDanLingLiaoFragment_*`                              | —                                                                    | —                                                                     | —                                                               | —                                                      |
| **产出**      | `Fragment_Output_*`, `Fragment_Collect_*`                | `DoOutput`, `DoProductLineOutPut`                                    | `MESZZZX_BCPOutput`, `MESZZZX_PZOutput`, `MESZZZX_EquipmentConfigOut` | `frmME_BCPOutput`, `frmME_PZOutput`, `frmME_EquipmentConfigOut` | `ProductLineOutputHistory` 表                          |
| **成品入库**  | `ChanChuPingRuKuNewFragment_*`                           | `CompliteProductInWarehouseOrder`                                    | —                                                                     | —                                                               | —                                                      |
| **产线退料**  | `ReturnFramgnet_*`, `ReturnApplyFramgnet_*`              | `AddProductLineReturnOrder`, `CompliteProductLineReturn`             | `CKZY_ReturnMaterial`, `CKZY_PLReturnQuery`                           | —                                                               | —                                                      |
| **发货**      | `FinishProductShipment_*`                                | `AddShipBill`, `CompleteOneShipBill`                                 | `CKZY_ShippingList`, `CKZY_SalesStockingQuiry`                        | —                                                               | `Shipment`, `ShipmentHistory` 表                       |
| **批次拆分**  | `FragmentSerial_SerialNumberSplit_*`, `Fragment_Stack_*` | `DoLotMove`                                                          | `CKZY_LotSplit`                                                       | `frmME_WIPLotSplit`                                             | `SplitHistory` 表                                      |
| **滞留/放行** | `FragmentHoldReleaseActivity`                            | `DoHoldOrRelease`                                                    | `MESZLKZ_ReleaseHold`                                                 | —                                                               | `HoldReleaseHistory` 表                                |
| **盘点**      | `ShengChanFragment` (pandian)                            | `DoPI`                                                               | —                                                                     | —                                                               | —                                                      |
| **结案**      | —                                                        | —                                                                    | —                                                                     | **`frmME_CleanBPREnd`**                                         | `BPRHistory*`, `BPRLockHistory` 表                     |
| **库存查询**  | `KuCunChaXunActivity` 1-4                                | —                                                                    | `CKZY_OutStockQuery`                                                  | —                                                               | —                                                      |
| **库位查询**  | `KuWeiChaXunActivity`                                    | —                                                                    | `CKZY_StorageLocation`                                                | —                                                               | —                                                      |
| **BPR记录**   | —                                                        | —                                                                    | `MESZZZX_BPRRecord`                                                   | `frmME_BPRRecord`                                               | `BPRHistory*` 表                                       |

---

## 8. 盘点限制与假设

1. **7 阶段流程尚未验证**：文件/表名匹配 ≠ 实际流程衔接关系。
2. **BS vs CS 分工待确认**：哪些流程在 Web 端、哪些在桌面端、哪些两者都涉及。
3. **跨系统状态变更的"真相来源"**：每个交接点的标识符和状态字段需要读代码确认。
4. **Demo 页面与生产代码的关系**：需验证后再作为可点击链接。
5. **"结案"定义待明确**：`frmME_CleanBPREnd` 是唯一发现的相关入口，但准确的业务定义和完整的技术链路需验证。
6. **数据库完整 schema 依赖 DOC 文档**：`db-scripts/` 只有增量变更脚本，全量表结构需对照 `tables/` 下的 HTML 文档。
7. **PDA 盘点功能**：根据 `fragment_pandian*.xml` 布局和 `DoPI`（Physical Inventory）接口确认存在盘点功能，但具体实现细节待验证。

---

## 9. 下一步

按 `SCAL_PROCESS_MAP_REQUIREMENTS.md` 的工作方法第 2 步：

> **验证每个阶段的确切子流程及其顺序**

从已验证的来料流程链开始（sampling-label.html）：

```
采购单采购 → 条码申请 → 标签分发 → 扫码入库 → 抽样标签 → 质检判定
```

逐一阅读源码确认：
- 子流程的精确顺序
- 状态变更点
- 系统间接口调用
- 数据库实体读写

然后扩展到全部 7 个阶段：**采购 → 收货 → 质检 → 投料 → 称重 → 配方产出 → 结案**。
