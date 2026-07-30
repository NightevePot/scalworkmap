# SCAL BS Demo 页面样式工作手册

> 最后更新：2026-07-27  
> 适用范围：所有 BS (Web MES) 字段血缘演示页面

---

## ⚠️ 核心铁律

> **1. 严禁编造不存在的功能。** 每一个 demo 必须有对应的原始窗体源码（.cshtml / .aspx / .cs），基于实际窗体的字段、布局、业务逻辑来改建。
>
> **2. 生成后自检。** 每次生成页面后必须打开检查，至少不能出现格式混乱（行列错排、标签换行、空数据填充等基础问题）。
>
> **3. 回顾上轮对话。** 每次生成后重新回顾上一轮要求，确保没有遗漏。之前刚纠正过的问题，不允许在新需求中重犯。
>
> **4. 不确定时先查源码。** 当功能不确定时，第一件事是去以下文件夹查逻辑：`E:\code\scal-mes`（BS）、`E:\code\scal-mes-client`（CS）、`E:\code\scal-pda-f\scal-wms-app`（PDA 前端）、`E:\code\scal-pda-b`（PDA 后端）、`E:\code\xxaedatabase`（数据库脚本）。
>
> 具体禁止行为：
> - 不允许凭空捏造页面结构（如表格式、按钮、Tab、列名）
> - 不允许将多个不相关页面的功能合并到一个 demo
> - 不允许猜测数据库表名、BLL 类名、API 名称
> - 不允许使用"看起来像"的字段名代替真实字段名
> - 做之前必须先找到并阅读原始源码文件，确认其真实存在

---

## 1. 页面整体结构

```html
<body>
  <div class="demo-main">
    <header class="bar">...</header>       <!-- 绿色顶部导航栏 -->
    <div class="sub-tabs">...</div>        <!-- ⚠️ 子标签入口（必做！见 §2.4） -->
    <div class="toolbar">...</div>         <!-- 查询/操作工具栏 -->
    <div class="content">                  <!-- 主内容区 -->
      <!-- datagrid / 表单 / 工作区 -->
    </div>
    <aside class="card" id="card">...</aside>  <!-- 浮动血缘卡片 -->
  </div>
  <div class="stats-panel">...</div>       <!-- 右侧调用统计面板 -->
</body>
```

### 1.1 布局要求
- `body`：`display:flex; justify-content:center; gap:16px; padding:12px`
- `demo-main`：`flex:1; max-width:1050px; min-width:0`
- `stats-panel`：`width:280px; flex-shrink:0; position:sticky; top:12px`

---

## 2. 绿色顶部栏 `.bar`

### 2.1 CSS 规范
```css
.bar{height:50px;display:flex;color:#fff;background:var(--green)}
.brand{width:215px;display:grid;place-items:center;border-right:1px solid rgba(0,0,0,.12);font-size:20px;font-weight:700}
.nav{display:flex;flex:0 0 auto}
.nav span{width:70px;display:grid;place-items:center;border-right:1px solid rgba(0,0,0,.12);font-weight:700;font-size:12px}
.nav span.active{background:rgba(0,0,0,.16);box-shadow:inset 0 -3px 0 #fff}
.bar-info{display:flex;align-items:center;padding:0 16px;font-weight:700;font-size:11px;white-space:nowrap;gap:8px;margin-left:auto}
.bar-badge{background:rgba(255,255,255,.2);padding:2px 8px;border-radius:10px}
```

### 2.2 导航项（固定 9 项，不可省略）
```
工艺流程 | 企业架构 | 生产模型 | 查询管理 | 工作流程 | 质量控制 | 仓库作业 | 计划任务 | 批次工具
```
- 当前所在模块添加 `class="active"`
- 颜色：`--green: #00a65a`

### 2.3 页面标题格式
```
BS · Web MES | {页面中文名} · 字段血缘演示
```
示例：`BS · Web MES | 条码申请 · 字段血缘演示`

### 2.4 ⚠️ 子标签入口（必做）

每个 BS demo 必须在绿色导航栏下方显示**子标签入口**，体现该页面在 MES 中的导航路径。

```css
.sub-tabs{height:32px;display:flex;align-items:center;padding:0 12px;background:#f7f7f7;border-bottom:1px solid #cfd4d7;gap:4px;font-size:11px}
.sub-tab{padding:4px 12px;border:1px solid #d5d9dc;border-bottom:0;color:#4e5d67;background:#fff;border-radius:3px 3px 0 0;cursor:default;white-space:nowrap}
.sub-tab.active{border-top:3px solid var(--green);color:#173f5f;font-weight:700}
.sub-arr{color:#94a3b8;font-size:10px}
```

```html
<div class="sub-tabs">
<span class="sub-tab">{所属模块}</span><span class="sub-arr">▸</span><span class="sub-tab active">{当前页面}</span>
</div>
```

**各页面入口对照：**

| Demo 页面    | 子标签                    |
| ------------ | ------------------------- |
| 条码申请     | `仓库作业 ▸ 条码申请`     |
| 抽样标签     | `质量控制 ▸ 抽样标签`     |
| 检验         | `质量控制 ▸ 检验`         |
| 质检结果判定 | `质量控制 ▸ 质检结果判定` |
| 放行/滞留    | `质量控制 ▸ 放行/滞留`    |

---

## 3. 工具栏 `.toolbar`

```css
.toolbar{background:var(--soft);padding:8px 16px;border-bottom:1px solid var(--line)}
.toolbar table{width:100%}
.toolbar th{text-align:right;font-size:12px;font-weight:600;padding:3px 6px}
.toolbar td{padding:3px 12px 3px 4px}
.toolbar input,.toolbar select{padding:4px 8px;border:1px solid var(--line);border-radius:3px;font-size:12px;outline:none}
```

### 3.1 按钮规范
```css
.btn{border:none;border-radius:3px;font-size:12px;font-weight:700;cursor:pointer;padding:5px 14px}
.btn-pri{background:var(--blue);color:#fff}        /* 主按钮（查询等） */
.btn-sec{background:#fff;color:#17232d;border:1px solid var(--line)}  /* 次按钮（重置/导出） */
```

### 3.2 表单字段必须加 `data-k` 属性
```html
<input value="RE2026070008" data-k="purchaseOrderInput">
```
用于字段血缘追踪点击。

---

## 4. 主内容区 `.content`

### 4.1 数据表格 `.dg`
```css
.dg{background:#fff;border:1px solid var(--line);margin-bottom:8px}
.dg table{width:100%;border-collapse:collapse;font-size:11px}
.dg th{background:var(--soft);padding:5px 8px;text-align:left;border-right:1px solid var(--line);border-bottom:1px solid var(--line);font-size:10px;font-weight:700}
.dg td{padding:4px 8px;border-right:1px solid #f0f0f0;border-bottom:1px solid #f0f0f0;cursor:pointer}
.dg td[data-k]:hover{background:#eff6ff}
```

### 4.2 原始窗体还原原则
- **必须参照原始 `.cshtml` 源码**还原字段布局
- 保留原始页面的字段顺序、分组、必填标记（`*`）
- 内外包装分两个独立区块展示
- 设备信息独立一节

---

## 5. 浮动血缘卡片 `.card`

### 5.1 CSS 规范
```css
.card{position:fixed;z-index:5;right:24px;bottom:24px;width:620px;min-height:300px;max-height:calc(100vh-40px);overflow:auto;border:1px solid #b7c9d2;border-radius:6px;background:#fff;box-shadow:0 15px 36px rgba(24,53,70,.26);opacity:0;visibility:hidden;transform:scale(.98);transition:.16s}
.card.show{opacity:1;visibility:visible;transform:scale(1)}
.card-head{display:flex;align-items:center;justify-content:space-between;min-height:50px;padding:0 17px;color:#fff;background:#245f84;cursor:move}
```

### 5.2 智能避让定位（必须实现）
```javascript
function show(k, n) {
  // ... 填充数据 ...
  
  // 智能定位：卡片不遮挡点击位置
  const r = n ? n.getBoundingClientRect() : null;
  const midX = window.innerWidth / 2, midY = window.innerHeight / 2;
  card.style.left = ''; card.style.top = ''; card.style.right = ''; card.style.bottom = '';
  
  if (!r) {
    // 无点击目标（按钮调用）→ 默认右下角
    card.style.right = '24px'; card.style.bottom = '24px';
  } else {
    // 根据点击象限，卡片出现在对角
    if (r.left + r.width / 2 < midX) card.style.right = '24px';
    else card.style.left = '24px';
    if (r.top + r.height / 2 < midY) card.style.bottom = '24px';
    else card.style.top = '24px';
  }
  card.classList.add('show');
}
```

### 5.3 拖拽支持（必须实现）
```javascript
let drag = null;
const head = card.querySelector('.card-head');
head.onpointerdown = e => {
  if (e.target.closest('.close') || !card.classList.contains('show')) return;
  const r = card.getBoundingClientRect();
  drag = { x: e.clientX - r.left, y: e.clientY - r.top };
  head.setPointerCapture(e.pointerId);
};
head.onpointermove = e => {
  if (!drag) return;
  card.style.left = `${Math.max(8, Math.min(innerWidth - card.offsetWidth - 8, e.clientX - drag.x))}px`;
  card.style.top = `${Math.max(8, Math.min(innerHeight - card.offsetHeight - 8, e.clientY - drag.y))}px`;
};
head.onpointerup = () => drag = null;
```

### 5.4 点击外部关闭
```javascript
document.addEventListener('click', e => {
  if (card.classList.contains('show') && !card.contains(e.target) && !e.target.closest('[data-k]')) {
    card.classList.remove('show');
  }
});
```

---

## 6. 右侧调用统计面板 `.stats-panel`

### 6.1 ⚠️ 关键 CSS（多次踩坑总结）

```css
.stats-panel {
  width: 280px;                    /* 不要窄于 280px */
  background: #fff;
  border-radius: 8px;
  flex-shrink: 0;
  position: sticky;
  top: 12px;
  max-height: calc(100vh - 24px);
  display: flex;                   /* flex列布局，标题固定 */
  flex-direction: column;
}
.stats-panel .sh {
  flex-shrink: 0;                  /* 标题不随内容滚动 */
}
.stats-body {
  flex: 1;
  overflow-y: auto;                /* 只有内容区滚动 */
  overflow-x: hidden;
}
```

### 6.2 `.sn`（英文表名）样式铁律

```css
.stats-panel .si .sn {
  flex: 1 1 auto;                  /* 按内容自适应宽度 */
  font-family: Consolas, monospace;
  font-size: 9px;
  line-height: 1.35;
  word-break: normal;              /* ✓ 正常断词 */
  overflow-wrap: break-word;       /* ✓ 超长单词才换行 */
}
```

### 🚫 绝对禁止的 CSS 组合（已踩坑验证）

| 错误写法                                              | 后果                              |
| ----------------------------------------------------- | --------------------------------- |
| `word-break: break-all`                               | 中英文字符全部逐字断开竖排        |
| `overflow-wrap: break-word` + `word-break: keep-all`  | 英文无空格时仍逐字断开            |
| `overflow: hidden; white-space: nowrap; min-width: 0` | flex 子元素缩到 0px，文字完全消失 |
| `overflow: hidden; text-overflow: ellipsis`           | 表名被截断只显示一半              |

### 6.3 `.st`（中文标签）规范
```css
.stats-panel .st {
  font-size: 8px;
  padding: 0 3px;
  border-radius: 2px;
  font-weight: 600;
  flex-shrink: 0;
  white-space: nowrap;             /* 标签不换行 */
}
```

### 6.4 `.si`（每行条目）规范
```css
.stats-panel .si {
  display: flex;
  flex-wrap: wrap;                 /* 标签可折到下行，给表名腾空间 */
  align-items: baseline;
  gap: 3px;
  padding: 2px 4px;
}
```

### 6.5 统计面板 HTML 结构
```html
<div class="stats-panel">
  <div class="sh">📊 调用统计<span class="badge">BS·页面名</span></div>
  <div class="stats-body">
    <div class="stats-count-row">...</div>
    <div class="ss">
      <h4>📊 数据库表</h4>
      <div class="si"><span class="sn" title="完整表名">TableName</span><span class="st tbl">中文名</span></div>
      ...
    </div>
  </div>
</div>
```

### 6.6 标签颜色规范
| 类型       | class     | 背景色    | 文字色    |
| ---------- | --------- | --------- | --------- |
| 数据库表   | `.st.tbl` | `#d1fae5` | `#065f46` |
| 存储过程   | `.st.sp`  | `#ede9fe` | `#6d28d9` |
| BLL 业务层 | `.st.bll` | `#fef3c7` | `#92400e` |

---

## 7. 字段血缘数据规范

### 7.1 map 对象结构
```javascript
const map = {
  fieldKey: [
    '字段显示名',        // [0] 中文标签
    '数据库来源',         // [1] Table.Column 或 SP 名
    '数据类型',           // [2] nvarchar(50) / decimal 等
    '查询过程简述',       // [3] BLL/SP 描述
    '所属阶段',           // [4] 用于流程高亮
    ['路径节点1','路径节点2']  // [5] 血缘路径数组
  ]
};
```

### 7.2 按钮动作描述规范

按钮动作描述必须包含真实方法名（如 `IM_Button_Confirm_Click`），禁止使用模糊描述。

---

# CS (WinForms 客户端) Demo 页面制作规范

> 最后更新：2026-07-29  
> 适用范围：所有 CS (WinForms 桌面客户端) 字段血缘演示页面  
> 参考模板：`demo-cs-template.html`

---

## ⚠️ 核心铁律（同 BS 规范 §核心铁律，补充 CS 专项）

- **必须先读源码再动手。** CS 源码路径：`E:\code\scal-mes-client\WinClient\`
- **优先读 `.Designer.cs`**（控件声明、坐标、大小、字体、颜色），再读 `.cs`（运行时逻辑）
- **版本号必须来自真实文件。** 读 `WinClient\UpdateList.xml` 获取 `<Version>`，或直接问用户实际运行版本
- **实际运行界面 > 源码。** 源码仓库可能不是最新部署版本，用户看到的界面为准

---

## 1. CS 整体结构（MainForm 外壳）

CS 客户端启动后进入 `MainForm`，其结构为：

```
┌──────────────────────────────────────────────┐
│  panelTop (82px, #BCDCF4)                      │  ← 顶栏
│  logo | 日期 | 时间 | 星期 | 系统连接 | 版本 | 用户 │
├────────┬─────────────────────────────────────┤
│panelLeft│  kkTab1 (TabControl, OwnerDrawFixed) │
│179px   │  ┌──────────────────────────────┐   │
│tvMenu  │  │ Tab: 首页 | 原料称重 | 余料称重...│   │
│WhiteSmk│  ├──────────────────────────────┤   │
│        │  │  子窗体内容 (Dock=Fill)       │   │
│        │  │                              │   │
└────────┴──────────────────────────────────────┘
```

### 1.1 源码关键行号

| 属性                | 值                                                | 源码位置                  |
| ------------------- | ------------------------------------------------- | ------------------------- |
| panelTop.BackColor  | `#BCDCF4` (188,220,244)                           | MainForm.Designer.cs L245 |
| panelTop.Height     | 82px                                              | MainForm.Designer.cs L248 |
| tvMenu.BackColor    | `WhiteSmoke`                                      | MainForm.Designer.cs L225 |
| tvMenu.GroupBgColor | `#5FA2D3` (95,162,211)                            | MainForm.Designer.cs L229 |
| tvMenu.Width        | 179px                                             | MainForm.Designer.cs L205 |
| 字体                | 微软雅黑 9F                                       | MainForm.Designer.cs L228 |
| 用户名              | 微软雅黑 15F Bold Black                           | MainForm.Designer.cs L287 |
| 版本号来源          | `frmLogin.version` ← `UpdateList.xml` `<Version>` | frmLogin.cs L28 + L83     |

---

## 2. 子窗体结构（以 frmME_IssueMaterial 原料称重为例）

### 2.1 面板 Dock=Top 层叠顺序

WinForms `Dock=Top` 规则：**最后加入 Controls 的面板在最上面。** 读取 Designer.cs 中 `panelMain.Controls.Add()` 的顺序（从下到上）：

```
panelMain.Controls.Add(panel7);              // ⑦ 操作区 (最底部)
panelMain.Controls.Add(panelDetail);          // ⑥ 已发料明细+称重记录
panelMain.Controls.Add(panelBPRList);         // ⑤ BPR配方明细
panelMain.Controls.Add(panelIssueMaterialTitle); // ④ 称重信息标题
panelMain.Controls.Add(panelWorkOrderList);   // ③ 工单列表
panelMain.Controls.Add(panelWorkOrder);       // ② 搜索栏
panelMain.Controls.Add(panelBasicInfoTitle);  // ① 基础信息标题 (最顶部)
```

### 2.2 可折叠面板

- `panelBasicInfoTitle` 点击 → 切换 `panelWorkOrder` + `panelWorkOrderList` 显隐
- `panelIssueMaterialTitle` 点击 → 切换 `panelBPRList` + `panelDetail` 显隐
- 标题栏：`labelBasicInfoTitle.Text = "-"` / `"+"`  表示展开/折叠
- **面板背景色不是灰色！** `BackColor = SystemColors.GradientActiveCaption`（浅蓝渐变）

### 2.3 子窗体标题颜色

```css
/* 对应 SystemColors.GradientActiveCaption */
.sec-hdr {
  background: linear-gradient(180deg, #E8F4FD, #BCDCF4);
  height: 28px;
  /* L1700 panelBasicInfoTitle, L1411 panelIssueMaterialTitle */
}
```

---

## 3. CS 专用配色方案

| 用途              | 色值                                | 来源                               |
| ----------------- | ----------------------------------- | ---------------------------------- |
| 顶栏 / 高亮字段   | `#BCDCF4`                           | MainForm.Designer.cs L245          |
| 树菜单分组标题    | `#5FA2D3`                           | MainForm.Designer.cs L229          |
| 树菜单背景        | `WhiteSmoke`                        | MainForm.Designer.cs L225          |
| 折叠标题栏        | `linear-gradient(#E8F4FD, #BCDCF4)` | SystemColors.GradientActiveCaption |
| 内容区背景        | `#F0F0F0` (SystemColors.Control)    | WinForms 默认                      |
| DataGridView 表头 | `#E8F0FE`                           | WinForms 默认                      |
| 必填标记          | `Color.Red` (`*`)                   | L1672 label42                      |
| 批号高亮          | `#BCDCF4` (同顶栏)                  | L94 txt_mfgBatch                   |

---

## 4. CS 字体规范

| 场景              | 字体              | 来源                 |
| ----------------- | ----------------- | -------------------- |
| 一般标签/Label    | 微软雅黑 10F      | Designer 多处        |
| 树菜单            | 微软雅黑 9F       | L228                 |
| DataGridView      | **宋体 9F**       | L868 IM_DispatchList |
| 用户名            | 微软雅黑 15F Bold | L287 lblOperName     |
| 物料编号 / 标准值 | 微软雅黑 **20F**  | L70-71, L92          |
| 操作按钮          | 微软雅黑 12F      | L107-112             |

---

## 5. CS 按钮尺寸精确值

| 按钮文字         | 尺寸   | 字号 | 来源                      |
| ---------------- | ------ | ---- | ------------------------- |
| 查询             | 132×37 | 12F  | L1675 QueryButton         |
| 调料             | 183×46 | 12F  | L107 IM_Button_ToMfgOrder |
| 已发料明细重印   | 183×46 | 12F  | L108                      |
| 原料称重明细重印 | 183×46 | 12F  | L108                      |
| 免称             | 100×48 | 12F  | L110                      |
| 称重             | 100×48 | 12F  | L111                      |
| 确认             | 100×48 | 12F  | L112                      |
| 取消称重         | 245×48 | 12F  | L126                      |

---

## 6. DataGridView 列名（必须来自源码）

**禁止编造列名。** 列名来自 Designer.cs 中的 `HeaderText` 属性：

```
// 示例：IM_DispatchList (已发料明细)
IM_DispatchList_SN.HeaderText = "#"
IM_DispatchList_MFGBatch.HeaderText = "原料批号"
IM_DispatchList_ExpirationDate.HeaderText = "有效期"
IM_DispatchList_LotNM.HeaderText = "流水号"
IM_DispatchList_DispatchQty.HeaderText = "发料数量"
IM_DispatchList_WipQty.HeaderText = "线边数量"
IM_DispatchList_UOMNM.HeaderText = "单位"
IM_DispatchList_DispatchStatus.HeaderText = "发料状态"
IM_DispatchList_Info.HeaderText = "其他信息"
```

---

## 7. 左侧菜单（全部 35 项，来自 MainForm.cs TreeMenuName switch）

菜单项从数据库权限动态加载（`dal.GetCSMenuAuthority`），但 switch 中定义了所有可能的模块：

工单启动、内栈板包装、不锈钢清洗消毒、原料称重、原料称重复核、工单、返工记录表、成品包装、配制罐清洗启动、余料称重、配制罐输出、报废单、半成品产出、预配罐清洗启动、BPR作业、BPR作业修改、配制设备检查记录、配制区域生产前清场记录、储罐输入、生产前生产线清场检查表、中心线输入、储罐清洗启动、配制后清洗、储罐输出、在线产品装箱重量检查表、生产线分批、设备清洗消毒、配制产出TK绑定、批号重印、设备停机记录、罐装退料、配制产出、称重调试、天平调试、生产实绩录入

---

## 8. data-k 标注铁律

**所有可见数据字段必须有 `data-k` 属性**，无一例外。包括但不限于：
- 搜索框 / 下拉框
- DataGridView 所有列的单元格
- 操作区所有 TextBox / Label 值
- 所有按钮
- 顶栏的日期/时间/用户/版本

每个 `data-k` 必须在 JS `map` 对象中有对应条目，格式：
```javascript
key:['字段中文名','数据库来源.字段名','控件类型·尺寸','调用链路','源码位置',['路径节点']]
```

---

## 9. CS Demo HTML 模板结构

```html
<body>
  <div style="display:flex;gap:8px">        <!-- 左右布局 -->
    <div class="win">                         <!-- CS 窗口外壳 -->
      <div class="topbar">...</div>           <!-- panelTop 82px #BCDCF4 -->
      <div class="body">                      <!-- flex row -->
        <div class="left">...</div>           <!-- 179px 树菜单 -->
        <div class="right">                   <!-- 主内容区 -->
          <div class="tabs">...</div>         <!-- Tab 页签 -->
          <div class="content">               <!-- 子窗体内容 -->
            <div class="sec-hdr">− 基础信息</div>   <!-- 可折叠标题 -->
            <!-- 搜索栏 -->
            <!-- DataGridView × N -->
            <div class="sec-hdr">− 原料称重</div>   <!-- 可折叠标题 -->
            <!-- DataGridView × N -->
            <!-- 操作区 (最后,不可折叠) -->
          </div>
        </div>
      </div>
    </div>
    <div class="stats">...</div>              <!-- 右侧统计面板 -->
  </div>
  <aside class="card">...</aside>             <!-- 血缘卡片 -->
</body>
```

---

## 10. CS Demo 创建检查清单

- [ ] 已读取目标窗体的 `.Designer.cs`，确认所有控件名/坐标/大小/颜色
- [ ] 已读取 `.cs` 代码文件，确认运行时逻辑（折叠面板/数据绑定/按钮事件）
- [ ] 顶栏正确：`#BCDCF4`, 82px, 日期/时间/星期/版本/用户
- [ ] 左侧菜单包含全部 35 个模块（来自 MainForm.cs TreeMenuName switch）
- [ ] 面板按 Dock=Top 倒序排列（最下面加入的最先 display）
- [ ] 可折叠面板使用 `GradientActiveCaption` 渐变背景，28px 高
- [ ] DataGridView 使用宋体 9F，表头 `#E8F0FE`，所有列名来自真实 HeaderText
- [ ] 按钮尺寸精确匹配：查询 132×37，调料 183×46，免称/称重/确认 100×48
- [ ] 所有可见数据字段都有 `data-k`，JS map 中有对应条目
- [ ] 版本号来自 UpdateList.xml 或用户实际运行版本（禁止编造）
- [ ] 已打开页面自检，无格式混乱或空白数据

- 必须写明**目标写入表名**（不能写"传送到下一步"这种模糊描述）
- 格式：`方法名() → 目标表名 → 作用说明`
- 示例：`FI_Move_DZQM() → dtFinalInspection → FinalInspectionReason表 → MES主流程TravelDoc读取决定放行/滞留`

### 7.3 `data-k` 属性规范
- 所有可点击字段必须添加 `data-k="keyName"`
- 表头 `<th>` 也应可点击（加 `onclick` 或 `data-k`）
- 按钮加 `data-k`（如 `data-k="btnQuery"`）

---

## 8. CSS 变量定义

```css
:root {
  --green: #00a65a;     /* BS 主色调 */
  --deep: #287460;       /* 深绿 */
  --line: #d3dce1;       /* 边框线 */
  --soft: #f5f8f9;       /* 浅灰背景 */
  --blue: #1688ca;       /* 蓝色（按钮/链接） */
}
```

---

## 9. 自检清单

每完成一个 BS demo 页面，必须逐项检查：

- [ ] 绿色顶部栏 9 项导航完整，当前模块高亮
- [ ] ⚠️ 子标签入口：显示 `模块 ▸ 页面名` 路径
- [ ] 工具栏使用标准 `.toolbar` 样式
- [ ] 所有字段有 `data-k` 属性
- [ ] 浮动卡片支持智能避让定位 + 拖拽
- [ ] 统计面板表名**完整显示**（不截断、不竖排）
- [ ] 统计面板标题固定不随滚动消失
- [ ] 字段 map 中按钮动作写明**具体表名**
- [ ] 页面布局参照原始 `.cshtml` 源码
- [ ] 标签颜色使用规定 class（tbl/sp/bll）

---

## 10. 已知 BS 页面与源码对照

| Demo 文件                    | BS 源码页面                            | 所属模块                |
| ---------------------------- | -------------------------------------- | ----------------------- |
| `demo-barcode-apply.html`    | `CKZY_LotApply/Index.cshtml`           | 仓库作业 → 条码申请     |
| `sampling-label.html`        | `ZLKZ_SamplingLabel`                   | 质量控制 → 抽样标签     |
| `demo-inspection-check.html` | `MESZLKZ_Inspection/Index.cshtml`      | 质量控制 → 检验         |
| `demo-inspection.html`       | `MESZLKZ_FinalInspection/Index.cshtml` | 质量控制 → 质检结果判定 |

---

## 附录：踩坑记录

### A1. Flex `min-width: 0` 陷阱
Flex 子元素默认 `min-width: auto`（等于内容宽度）。设置 `min-width: 0` 可允许收缩，但配合 `overflow: hidden` 会导致元素缩到 **0px**，文字完全消失。

**正确做法**：要么设 `min-width: 4em` 保底，要么不用 `overflow: hidden`。

### A2. 中英文混排断词
- `word-break: break-all` → 中英文全部逐字断开 ❌
- `word-break: keep-all` → 中文不断但英文长单词溢出 ❌
- `overflow-wrap: break-word` + `word-break: normal` → 中文正常，英文只在必要时断 ✅

### A3. 统计面板滚动
标题和内容必须分离：标题在 flex 容器外（`flex-shrink: 0`），内容在 `overflow-y: auto` 子容器内。
