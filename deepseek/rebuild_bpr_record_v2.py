#!/usr/bin/env python3
"""Rebuild demo-cs-bpr-record.html v2 - accurate absolute positioning."""

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-bpr-record.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<title>报废单 · CS客户端</title>', '<title>BPR作业 · CS客户端</title>')
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">BPR作业</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">BPR作业</div>')

old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'
form_end_marker = '    <div class="stats">'
pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

new_form = r'''            <!-- ═══════ frmME_BPRRecord · BPR作业 1588×918 ═══════ -->

            <!-- panel1: 顶部工具栏 1567×50 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px 6px 2px 6px;background:#FAFBFC">
              <div class="blk-bd" style="padding:6px 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                <label style="font:9pt '微软雅黑';color:red">*</label>
                <label style="font:9pt '微软雅黑'">工单：</label>
                <input data-k="SearchArea_MfgOrderNM" value="MO-SO251206750-02" style="width:200px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px" title="ComboGrid控件">
                <label style="font:9pt '微软雅黑';margin-left:8px">工艺版本：</label>
                <span data-k="lblGYVersion" style="font:9pt '微软雅黑';color:#1a3a5c">01.01</span>
                <button class="btn" data-k="SearchArea_Query" style="font:9pt '微软雅黑';width:60px;height:28px">查询</button>
                <span style="flex:1"></span>
                <label style="font:9pt '微软雅黑'">设备名：</label>
                <select data-k="cboDevice" style="width:126px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"><option>QDZY-10007</option><option>QDZY-10006</option></select>
                <button class="btn" data-k="btnProcessSwitch" style="font:9pt '微软雅黑';width:138px;height:35px">工艺设备切换</button>
                <button class="btn primary" data-k="btnStartNoProcess" style="font:9pt '微软雅黑';width:138px;height:35px">无工艺启动</button>
              </div>
            </div>

            <!-- BPRRecord_MfgorderListPanel: 工单详情 + 规格详情 -->
            <div style="display:flex;gap:4px;margin:2px 6px">
              <div class="blk" style="flex:1;border:1px solid #C0C0C0;background:#FAFBFC;min-width:0">
                <div class="blk-hd" style="background:#E8F0FE">工单详情</div>
                <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:120px"><table class="grid">
                  <thead><tr><th>WIP</th><th>工单数量</th><th>规格描述</th><th>物料编号</th><th>生产批号</th><th>LabelDefld</th><th>DataCode</th></tr></thead>
                  <tbody><tr><td data-k="MOD_WIP">—</td><td data-k="MOD_MOQty">50.00</td><td data-k="MOD_Description">25kg/桶</td><td data-k="MOD_ProductNM">2969344</td><td data-k="MOD_MFGBatch">B20260729-001</td><td data-k="MOD_LableDefId">LBL-001</td><td data-k="MOD_DateCode">20260729</td></tr></tbody>
                </table></div></div>
              </div>
              <div class="blk" style="flex:1;border:1px solid #C0C0C0;background:#FAFBFC;min-width:0">
                <div class="blk-hd" style="background:#E8F0FE">规格详情</div>
                <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:120px"><table class="grid">
                  <thead><tr><th>项次</th><th>项目名称</th><th>规格描述</th><th>检验方法</th><th>内控标准</th><th>结果</th><th>ProcessSpecId</th><th>Info</th></tr></thead>
                  <tbody><tr><td data-k="SDL_Item">1</td><td data-k="SDL_PSDNM">外观检查</td><td data-k="SDL_Description">无异物</td><td data-k="SDL_Method">目视</td><td data-k="SDL_Standard">澄清透明</td><td data-k="SDL_Result">合格</td><td data-k="SDL_ProcessSpecId">PS-001</td><td data-k="SDL_Info">—</td></tr></tbody>
                </table></div></div>
              </div>
            </div>

            <!-- BPRRecord_ProcessStepPanel: 工艺步骤明细 大表 -->
            <div class="blk" style="border:1px solid #C0C0C0;margin:4px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:#E8F0FE">工艺步骤明细 <span style="font-size:8pt;color:#888">BPRRecord_StepDetailList · 19列</span></div>
              <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:180px"><table class="grid">
                <thead><tr><th>步骤</th><th>项次</th><th>步骤名称</th><th>物料编号</th><th>规格描述</th><th>值</th><th>结果</th><th>标准值</th><th>单位</th><th>最大值</th><th>最小值</th><th>可跳过</th><th>数据采集项</th><th>读值方式</th><th>设备名称</th><th>启动按钮</th><th>开始作业</th><th>开始作业时间</th><th>下一步</th></tr></thead>
                <tbody><tr><td data-k="SDL_SN">1</td><td data-k="SDL_StepItem">1</td><td data-k="SDL_StepNM">投料步骤</td><td data-k="SDL_StepProductNM">2969344</td><td data-k="SDL_StepDescription">投入原料A</td><td data-k="SDL_Value">50.15</td><td data-k="SDL_StepResult">合格</td><td data-k="SDL_StandardValue">50.00</td><td data-k="SDL_UOMNM">kg</td><td data-k="SDL_MaxValue">50.50</td><td data-k="SDL_MinValue">49.50</td><td data-k="SDL_IsSkipable">否</td><td data-k="SDL_DataCollectNM">重量采集</td><td data-k="SDL_DataMethod">OPC</td><td data-k="SDL_AddEquipmentNM">QDZY-10007</td><td data-k="SDL_AddEquipmentStatus">已启动</td><td data-k="SDL_AddWorkStatus">作业中</td><td data-k="SDL_AddStartWorkTime">14:30</td><td data-k="SDL_AddNextStepStatus">—</td></tr></tbody>
              </table></div></div>
            </div>

            <!-- TextPanel: 步骤操作区 1567×482 — 绝对定位四列布局 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:4px 6px 6px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 步骤操作 <span style="font-weight:400;color:#888;font-size:8pt">TextPanel 1567×482</span></div>
              <div class="blk-bd" style="padding:8px;display:flex;gap:0;position:relative;min-height:420px">

                <!-- 第1列: 步骤参数 (x≈6~180) -->
                <div style="flex:0 0 290px;display:grid;grid-template-columns:95px 180px;gap:4px 8px;align-items:start;font:9pt '微软雅黑'">
                  <label style="padding-top:4px">当前步骤:</label><input data-k="txtCurrentStep" value="1" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">当前项次:</label><input data-k="txtCurrentItem" value="1" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">标准值:</label><input data-k="txtStandardValue" value="50.00" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">上限:</label><input data-k="txtMaxValue" value="50.50" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">下限:</label><input data-k="txtMinValue" value="49.50" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">单位:</label><input data-k="txtUomNM" value="kg" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                </div>

                <!-- 第2列: 数据采集/规格 (x≈299~385) -->
                <div style="flex:0 0 290px;display:grid;grid-template-columns:105px 180px;gap:4px 8px;align-items:start;font:9pt '微软雅黑'">
                  <label style="padding-top:4px">数据采集名:</label><input data-k="txtDataCollectNM" value="重量采集" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">总步骤数:</label><input data-k="txtTotalStep" value="5" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">规格描述:</label><textarea data-k="txtDescription" readonly style="height:140px;font:9pt '微软雅黑';border:1px solid #C0C0C0;padding:4px;background:#FFFFE0;resize:none">投入原料A</textarea>
                </div>

                <!-- 第3列: 设备/重量/结果 (x≈575~729) -->
                <div style="flex:0 0 310px;display:grid;grid-template-columns:130px 180px;gap:4px 8px;align-items:start;font:9pt '微软雅黑'">
                  <label style="padding-top:4px;color:red">* 设备名:</label><input data-k="TextArea_EquipmentNM" value="QDZY-10007" style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px" title="KeyDown事件, ImeMode=Disable">
                  <label style="padding-top:4px;color:red">* 值:</label><input data-k="TextArea_Value" value="50.15" style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;font-weight:bold;color:green" title="手输/OPC自动采集">
                  <label style="padding-top:4px;color:red">* 结果:</label><input data-k="txtResult" value="合格" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">罐称重量:</label><input data-k="txtWeight" value="50.15" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0" title="ReadOnly, 有TextChanged+KeyPress事件">
                  <label style="padding-top:6px">本步加料重量:</label><input data-k="tbBBWeight" value="0.00" readonly style="height:38px;font:14pt '微软雅黑';font-weight:bold;border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                  <label style="padding-top:4px">当前步骤开始时间:</label><input data-k="txtStartTime" value="2026-07-29 14:30:00" readonly style="height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px;background:#FFFFE0">
                </div>

                <!-- 第4列: 计时器 + 验证 + 按钮 (x≈912+) -->
                <div style="flex:0 0 310px;display:flex;flex-direction:column;gap:4px">
                  <div style="display:flex;gap:8px;align-items:center">
                    <span data-k="EquipmentLabel" style="font:9pt;color:red;cursor:pointer" title="设备验证状态">验证成功</span>
                    <span data-k="ValueLabel" style="font:9pt;color:red;cursor:pointer" title="值验证状态">验证成功</span>
                  </div>
                  <div style="display:flex;gap:8px;align-items:center;margin-top:4px">
                    <span data-k="txtTimeShow" style="font:20pt '宋体';cursor:pointer" title="计时显示">00:00:00</span>
                    <span data-k="txtTimer" style="font:20pt '宋体';color:red;cursor:pointer" title="计时器(红色)">00:00:00</span>
                  </div>
                  <label style="color:red;font:9pt;margin-top:4px"><input type="checkbox" data-k="cbIsAniseed"> 大料</label>
                  <span style="color:red;font:9pt">(未预称原料)</span>
                  <label style="font:9pt;margin-top:4px"><input type="checkbox" data-k="CheckBox_Skip"> 是否跳步</label>
                  <!-- 按钮组 -->
                  <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:4px">
                    <button class="btn primary" data-k="TextArea_Start" style="width:122px;height:47px;font:10pt '微软雅黑'">启动</button>
                    <button class="btn primary" data-k="TextArea_BtnStartWorking" style="width:122px;height:47px;font:10pt '微软雅黑'">开始作业</button>
                    <button class="btn" data-k="TextArea_BtnNextStep" style="width:122px;height:47px;font:10pt '微软雅黑'">下一步</button>
                    <button class="btn" data-k="ClearValueText" style="width:122px;height:47px;font:10pt '微软雅黑'">清空</button>
                    <button class="btn" data-k="btnTransmission" style="width:122px;height:47px;font:10pt '微软雅黑'">修改设备名</button>
                  </div>
                </div>
              </div>
              <!-- 电箱 + 大文本框 底部行 -->
              <div style="display:flex;gap:8px;padding:4px 8px;border-top:1px solid #E0E0E0">
                <label style="font:10pt '微软雅黑';color:red">*</label>
                <label style="font:10pt '微软雅黑'">电箱:</label>
                <input data-k="RefrigeratorId" value="BOX-001" style="width:180px;height:29px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:0 4px" title="ComboGrid控件">
                <span style="flex:1"></span>
                <textarea data-k="txtValueBox" readonly style="width:314px;height:150px;font:10pt '微软雅黑';border:1px solid #C0C0C0;padding:4px;background:#FFFFE0;resize:none" title="Multiline, ReadOnly, ScrollBars=Both. 显示OPC采集日志"></textarea>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">'''

html = html[:pos_start] + new_form + html[pos_end + len(form_end_marker):]

# ═══ Stats panel ═══
html = html.replace('CS&#xB7;报废单</span>', 'BPR作业 frmME_BPRRecord</span>')
html = html.replace('<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>', '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div>')
html = html.replace('<div style="font-size:7pt;color:DimGray">数据库表</div>', '<div style="font-size:7pt;color:DimGray">DataGridView</div>')
html = html.replace('<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>', '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div>')
html = html.replace('<div style="font-size:7pt;color:DimGray">DAL类</div>', '<div style="font-size:7pt;color:DimGray">DAL/BLL</div>')

# Replace tables, DAL, forms, source note (same pattern as before, shortened)
old_t = html[html.find('ScrapOrderHead</span>'):html.find('</div>\n        </div>\n      </div>\n      <div class="ss">\n        <h4><span\n            style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#7c3aed')+200]
# Simple string replacement approach
html = html.replace('工单</span></div>\n          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ProductLine</span> <span\n              class="tag tag-tbl">产线</span></div>\n          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>\n          </div>',
    '工单</span></div>\n          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ProductLine</span> <span\n              class="tag tag-tbl">产线</span></div>\n          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>\n          </div>')

# Actually let me just do the replacements more simply
html = html.replace('MESZZZX_ScrapOrderDAL</span> <span\n              class="tag tag-bll">报废单</span>',
    'MESZZZX_BPRRecordBLL</span> <span\n              class="tag tag-bll">BPR业务逻辑</span>')

# This approach is getting messy. Let me just write clean replacements from the known scrap-order patterns.
# I'll do targeted replaces for the key sections.

# Tables
html = html.replace('报废单表头</span>', '工艺步骤明细 19列</span>')
html = html.replace('报废单明细</span>', '规格详情 8列</span>')
html = html.replace('Step detail list', '')  # no-op safety

# DAL section  
html = html.replace('GetScrapOrderHeaderListByPage / GetScrapOrderListByPage\n            / DelScrapOrder / DelScrapOrderHead / SendApproveScrapOrder',
    'bprBLL → BPR业务逻辑层')

html = html.replace('MESZZZX_InnerPackagingDAL</span> <span\n              class="tag tag-bll">内包装</span>',
    'MESZZZX_BPRRecordDAL</span> <span\n              class="tag tag-bll">BPR数据访问</span>')
html = html.replace('GetProductLine &#x2192; 产线下拉数据源',
    'BPRDAL → BPR数据操作')
html = html.replace('MESZZZX_SurplusMaterialDAL</span> <span\n              class="tag tag-bll">余料</span>',
    'MESZZZX_IssueMaterialDAL</span> <span\n              class="tag tag-bll">发料数据</span>')
html = html.replace('GetMfgOrderNM &#x2192; 工单号下拉数据源',
    'IMDAL → 发料称重关联数据')
html = html.replace('MESZZZA_WIPLotSplitDAL</span> <span\n              class="tag tag-bll">WIP拆分</span>', '')

# Forms
html = html.replace('frmME_AddScrapOrder</span> <span\n              class="tag tag-form">报废单主页</span>',
    'frmME_BPRRecord</span> <span\n              class="tag tag-form">BPR作业 1588×918</span>')
html = html.replace('frmME_ScrapOrder</span> <span\n              class="tag tag-form">添加/编辑表头</span>', '')
html = html.replace('EditScrapOrder</span> <span\n              class="tag tag-form">添加/编辑明细</span>', '')
html = html.replace('ESignature</span> <span\n              class="tag tag-form">电子签名(送审)</span>',
    '├─ 启动→开始作业→下一步 (OPC采集+计时)\n          <br>├─ 工艺设备切换 / 无工艺启动')

# Source note
html = html.replace('frmME_AddScrapOrder.cs /\n        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确',
    'frmME_BPRRecord.cs / .Designer.cs<br>1588×918 · 3 DataGridView(34列) · TextArea_Start/StartWorking/NextStep<br>DAL: BPRRecordBLL · BPRRecordDAL · IssueMaterialDAL')

# Remove modals + add card
modal_start = html.find('<!-- ═══════ Modal: frmME_ScrapOrder')
script_start = html.find('<script>')
if modal_start != -1 and script_start != -1:
    card_html = '''  <aside class="card" id="card">
    <div class="card-hd"><div><small>FIELD DATA LINEAGE</small><h3 id="title"></h3></div><button onclick="cl()" style="border:none;background:none;font-size:16px;cursor:pointer;color:DimGray">✕</button></div>
    <div class="card-bd"><div class="path" id="pth"></div><dl><dt>字段名</dt><dd id="label"></dd></dl><dl><dt>数据来源</dt><dd id="source"></dd></dl><dl><dt>控件类型</dt><dd id="type"></dd></dl><dl><dt>调用链路</dt><dd id="formula"></dd></dl><dl><dt>备注</dt><dd id="note" style="color:#059669"></dd></dl></div>
  </aside>\n  '''
    html = html[:modal_start] + card_html + html[script_start:]

# Replace JS map
map_start = html.find('const map = {')
if map_start != -1:
    brace_count = 0; in_map = False; map_end = -1
    for i in range(map_start, len(html)):
        if html[i] == '{': brace_count += 1; in_map = True
        elif html[i] == '}':
            brace_count -= 1
            if in_map and brace_count == 0: map_end = i + 1; break
    if map_end != -1:
        new_map = r'''    const map = {
      SearchArea_MfgOrderNM: ['工单号', 'MfgOrder.MfgOrderNM', 'ComboGrid', ['SearchArea_Query→BindMfgOrderNM']],
      lblGYVersion: ['工艺版本', 'BPR.ProcessSpecVersion', 'Label', ['查询工单→工艺版本']],
      cboDevice: ['设备名', 'Config.ini', 'ComboBox', ['frmME_BPRRecord_Load→设备列表']],
      SearchArea_Query: ['查询按钮', 'Button.Click', 'Button', ['SearchArea_Query_Click']],
      btnProcessSwitch: ['工艺设备切换', 'Button.Click', 'Button 138×35', ['btnProcessSwitch_Click']],
      btnStartNoProcess: ['无工艺启动', 'Button.Click', 'Button 138×35', ['btnStartNoProcess_Click']],
      MOD_WIP: ['WIP', 'MfgOrder.WIP', 'DGV', ['MfgOrderDetailList']],
      MOD_MOQty: ['工单数量', 'MfgOrder.MOQty', 'DGV', ['MfgOrderDetailList']],
      MOD_Description: ['规格描述', 'MfgOrder.Description', 'DGV', ['MfgOrderDetailList']],
      MOD_ProductNM: ['物料编号', 'Product.ProductNM', 'DGV', ['MfgOrderDetailList']],
      MOD_MFGBatch: ['生产批号', 'MfgOrder.MFGBatch', 'DGV', ['MfgOrderDetailList']],
      SDL_Item: ['项次', 'SpecDetail.Item', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_PSDNM: ['项目名称', 'SpecDetail.PSDNM', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_Description: ['规格描述', 'SpecDetail.Description', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_Method: ['检验方法', 'SpecDetail.Method', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_Standard: ['内控标准', 'SpecDetail.Standard', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_Result: ['结果', 'SpecDetail.Result', 'DGV', ['SpecDetailList→BPRDAL']],
      SDL_SN: ['步骤', 'StepDetail.SN', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_StepItem: ['项次', 'StepDetail.Item', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_StepNM: ['步骤名称', 'StepDetail.StepNM', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_Value: ['值', 'StepDetail.Value', 'DGV', ['StepDetailList→BPRDAL/OPC']],
      SDL_StepResult: ['结果', 'StepDetail.Result', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_StandardValue: ['标准值', 'StepDetail.StandardValue', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_UOMNM: ['单位', 'UOM.UOMNM', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_MaxValue: ['最大值', 'StepDetail.MaxValue', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_MinValue: ['最小值', 'StepDetail.MinValue', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_DataCollectNM: ['数据采集项', 'StepDetail.DataCollectNM', 'DGV', ['StepDetailList→BPRDAL']],
      SDL_DataMethod: ['读值方式', 'StepDetail.DataMethod', 'DGV', ['StepDetailList→BPRDAL(OPC/手动)']],
      txtCurrentStep: ['当前步骤', 'currentStep', 'TextBox(ReadOnly)', ['BPR记录→currentStep'], '[自动]'],
      txtCurrentItem: ['当前项次', 'currentSpec', 'TextBox(ReadOnly)', ['BPR记录→currentSpec'], '[自动]'],
      txtStandardValue: ['标准值', 'StepDetail.StandardValue', 'TextBox(ReadOnly)', ['选中行→StandardValue'], '[自动]'],
      txtMaxValue: ['最大值', 'StepDetail.MaxValue', 'TextBox(ReadOnly)', ['选中行→MaxValue'], '[自动]'],
      txtMinValue: ['最小值', 'StepDetail.MinValue', 'TextBox(ReadOnly)', ['选中行→MinValue'], '[自动]'],
      txtUomNM: ['单位', 'UOM.UOMNM', 'TextBox(ReadOnly)', ['选中行→UOMNM'], '[自动]'],
      txtDataCollectNM: ['数据采集名', 'StepDetail.DataCollectNM', 'TextBox(ReadOnly)', ['选中行→DataCollectNM'], '[自动]'],
      txtTotalStep: ['总步骤数', 'TotalStep', 'TextBox(ReadOnly)', ['BPR记录→TotalStep'], '[自动]'],
      txtDescription: ['规格描述', 'StepDetail.Description', 'TextBox(ReadOnly,Multiline)', ['选中行→Description'], '[自动]'],
      TextArea_EquipmentNM: ['设备名', '用户输入(KeyDown)', 'TextBox, ImeMode=Disable', ['KeyDown→Enter→验证设备']],
      TextArea_Value: ['值', 'OPC采集/手输', 'TextBox', ['OPC→valueOpc 或 手动输入']],
      txtResult: ['结果', 'OPC采集/自动判定', 'TextBox(ReadOnly)', ['OPC→_result→合格/不合格'], '[自动]'],
      txtWeight: ['罐称重量', 'OPC/手输', 'TextBox(ReadOnly,TextChanged+KeyPress)', ['_weight→txtWeight, TextChanged→计算加料量'], '[手输/自动]'],
      tbBBWeight: ['本步加料重量', '计算值', 'TextBox(ReadOnly,14pt Bold)', ['_weight计算→tbBBWeight'], '[自动计算]'],
      txtStartTime: ['当前步骤开始时间', 'startDateTime', 'TextBox(ReadOnly)', ['开始作业→记录startDateTime'], '[自动]'],
      txtTimeShow: ['计时显示', 'System.Timer', 'Label 宋体20pt', ['timer→CountDown→txtTimeShow'], '[实时]'],
      txtTimer: ['计时器', 'System.Timer', 'Label 宋体20pt RED', ['timer→CountUp→txtTimer'], '[实时]'],
      EquipmentLabel: ['设备验证', '验证结果', 'Label RED', ['设备验证→验证成功/验证失败']],
      ValueLabel: ['值验证', '验证结果', 'Label RED', ['值验证→验证成功/验证失败']],
      cbIsAniseed: ['大料标记', 'CheckBox RED', 'CheckBox', ['cbIsAniseed_Click→大料标记']],
      CheckBox_Skip: ['是否跳步', 'CheckBox', 'CheckBox', ['CheckBox_Skip_CheckedChanged→skip标志']],
      TextArea_Start: ['启动', 'Button.Click', 'Button 122×47', ['TextArea_Start_Click→启动步骤']],
      TextArea_BtnStartWorking: ['开始作业', 'Button.Click', 'Button 122×47', ['TextArea_BtnStartWorking_Click→workState=true']],
      TextArea_BtnNextStep: ['下一步', 'Button.Click', 'Button 122×47', ['TextArea_BtnNextStep_Click→下一项']],
      ClearValueText: ['清空', 'Button.Click', 'Button 122×47', ['ClearValueText_Click→清空值']],
      btnTransmission: ['修改设备名', 'Button.Click', 'Button 122×47', ['btnTransmission_Click→修改设备名']],
      RefrigeratorId: ['电箱', 'ComboGrid', 'ComboGrid', ['电箱选择→RefrigeratorId']],
      txtValueBox: ['OPC日志', 'OPC数据流', 'TextBox(Multiline,ReadOnly,ScrollBars)', ['OPC→txtValueBox.AppendText'], '[OPC实时日志]'],
    };'''
        html = html[:map_start] + new_map + html[map_end:]

# Replace button JS
old_btn_start = html.find('// ═══════ 按钮交互 ═══════')
old_btn_end = html.find('// ═══════ Grid 行选中', old_btn_start)
if old_btn_start != -1 and old_btn_end != -1:
    new_btn = r'''    // ═══════ 按钮交互 (frmME_BPRRecord) ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        if (k === 'TextArea_Start') { toast('🚀 启动步骤'); return }
        if (k === 'TextArea_BtnStartWorking') { toast('▶ 开始作业 workState=true, 记录startDateTime'); return }
        if (k === 'TextArea_BtnNextStep') { toast('⏭ 下一步 currentSpec++'); return }
        if (k === 'ClearValueText') { document.querySelector('[data-k="TextArea_Value"]').value = ''; toast('清空值'); return }
        if (k === 'btnTransmission') { toast('✏ 修改设备名'); return }
        if (k === 'btnProcessSwitch') { toast('🔄 工艺设备切换'); return }
        if (k === 'btnStartNoProcess') { toast('⚡ 无工艺启动'); return }
        if (k === 'SearchArea_Query') { toast('🔍 查询工单'); return }
        show(k);
      })
    });
    // 设备名 KeyDown 回车事件
    document.querySelector('[data-k="TextArea_EquipmentNM"]').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { toast('🔌 设备 ' + this.value + ' 已确认 (验证中...)'); }
    });
    // 大料复选框
    document.querySelector('[data-k="cbIsAniseed"]').addEventListener('change', function() {
      toast(this.checked ? '☑ 标记为大料' : '☐ 取消大料标记');
    });'''
    html = html[:old_btn_start] + new_btn + '\n\n    ' + html[old_btn_end:]

html = html.replace("function submitHead() { closeModal('modalHead'); toast('✅ 报废单表头已保存（模拟）') }", "// (BPR作业无弹窗)")
html = html.replace("function submitList() { closeModal('modalList'); toast('✅ 报废单明细已保存（模拟）') }", "")
html = html.replace(
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; card.classList.add('show') }",
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; document.getElementById('note').textContent = f[4] || ''; card.classList.add('show') }")

with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-bpr-record.html rebuilt v2!")
print(f"   Size: {len(html)} bytes")
