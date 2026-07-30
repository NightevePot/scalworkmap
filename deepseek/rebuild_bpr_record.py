#!/usr/bin/env python3
"""Rebuild demo-cs-bpr-record.html from frmME_BPRRecord source."""

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-bpr-record.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══ Identity ═══
html = html.replace('<title>报废单 · CS客户端</title>', '<title>BPR作业 · CS客户端</title>')
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">BPR作业</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">BPR作业</div>')

# ═══ Form content ═══
old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'
form_end_marker = '    <div class="stats">'
pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

new_form = r'''            <!-- ═══════ frmME_BPRRecord · BPR作业 1588×918 ═══════ -->

            <!-- panel1: 顶部工具栏 1567×50 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px 6px 2px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- BPR作业 <span style="font-weight:400;color:#888;font-size:8pt">frmME_BPRRecord 1588×918</span><span style="float:right;font-size:8pt;color:#888">Text="BPR作业" · 3 DataGridView</span></div>
              <div class="blk-bd" style="padding:6px 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                <label style="font:9pt '微软雅黑';color:red">*</label>
                <label style="font:9pt '微软雅黑'">工单：</label>
                <input data-k="MfgOrderNMTextBox" value="MO-SO251206750-02" style="width:200px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px">
                <label style="font:9pt '微软雅黑';margin-left:8px">工艺版本：</label>
                <span data-k="lblGYVersion" style="font:9pt '微软雅黑';color:#1a3a5c">01.01</span>
                <label style="font:9pt '微软雅黑';margin-left:8px">设备名：</label>
                <select data-k="cboDevice" style="width:126px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0">
                  <option>QDZY-10007</option><option>QDZY-10006</option>
                </select>
                <button class="btn" data-k="btnProcessSwitch" style="font:9pt '微软雅黑';width:138px;height:35px">工艺设备切换</button>
                <button class="btn primary" data-k="btnStartNoProcess" style="font:9pt '微软雅黑';width:138px;height:35px">无工艺启动</button>
              </div>
            </div>

            <!-- BPRRecord_MfgorderListPanel: 工单详情 + 规格详情 两栏 -->
            <div style="display:flex;gap:4px;margin:2px 6px">
              <div class="blk" style="flex:1;border:1px solid #C0C0C0;background:#FAFBFC;min-width:0">
                <div class="blk-hd" style="background:#E8F0FE">工单详情 <span style="font-size:8pt;color:#888">BPRRecord_MfgOrderDetailList · 7列</span></div>
                <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:140px">
                  <table class="grid">
                    <thead><tr><th>WIP</th><th>工单数量</th><th>规格描述</th><th>物料编号</th><th>生产批号</th><th>LabelDefld</th><th>DataCode</th></tr></thead>
                    <tbody><tr><td data-k="MOD_WIP">—</td><td data-k="MOD_MOQty">50.00</td><td data-k="MOD_Description">25kg/桶</td><td data-k="MOD_ProductNM">2969344</td><td data-k="MOD_MFGBatch">B20260729-001</td><td data-k="MOD_LableDefId">LBL-001</td><td data-k="MOD_DateCode">20260729</td></tr></tbody>
                  </table>
                </div></div>
              </div>
              <div class="blk" style="flex:1;border:1px solid #C0C0C0;background:#FAFBFC;min-width:0">
                <div class="blk-hd" style="background:#E8F0FE">规格详情 <span style="font-size:8pt;color:#888">BPRRecord_SpecDetailList · 8列</span></div>
                <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:140px">
                  <table class="grid">
                    <thead><tr><th>项次</th><th>项目名称</th><th>规格描述</th><th>检验方法</th><th>内控标准</th><th>结果</th><th>ProcessSpecId</th><th>Info</th></tr></thead>
                    <tbody><tr><td data-k="SDL_Item">1</td><td data-k="SDL_PSDNM">外观检查</td><td data-k="SDL_Description">无异物</td><td data-k="SDL_Method">目视</td><td data-k="SDL_Standard">澄清透明</td><td data-k="SDL_Result">合格</td><td data-k="SDL_ProcessSpecId">PS-001</td><td data-k="SDL_Info">—</td></tr></tbody>
                  </table>
                </div></div>
              </div>
            </div>

            <!-- BPRRecord_ProcessStepPanel: 工艺步骤明细 (大表 23列) -->
            <div class="blk" style="border:1px solid #C0C0C0;margin:4px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:#E8F0FE">工艺步骤明细 <span style="font-size:8pt;color:#888">BPRRecord_StepDetailList · 23列</span></div>
              <div class="blk-bd" style="padding:0"><div class="grid-wrap" style="max-height:200px">
                <table class="grid">
                  <thead><tr>
                    <th>步骤</th><th>项次</th><th>步骤名称</th><th>物料编号</th><th>规格描述</th><th>值</th><th>结果</th><th>标准值</th><th>单位</th><th>最大值</th><th>最小值</th><th>可跳过</th><th>数据采集项</th><th>读值方式</th><th>设备名称</th><th>启动按钮</th><th>开始作业</th><th>开始作业时间</th><th>下一步</th>
                  </tr></thead>
                  <tbody><tr>
                    <td data-k="SDL_SN">1</td><td data-k="SDL_StepItem">1</td><td data-k="SDL_StepNM">投料步骤</td><td data-k="SDL_StepProductNM">2969344</td><td data-k="SDL_StepDescription">投入原料A</td><td data-k="SDL_Value">50.15</td><td data-k="SDL_StepResult">合格</td><td data-k="SDL_StandardValue">50.00</td><td data-k="SDL_UOMNM">kg</td><td data-k="SDL_MaxValue">50.50</td><td data-k="SDL_MinValue">49.50</td><td data-k="SDL_IsSkipable">否</td><td data-k="SDL_DataCollectNM">重量采集</td><td data-k="SDL_DataMethod">OPC</td><td data-k="SDL_AddEquipmentNM">QDZY-10007</td><td data-k="SDL_AddEquipmentStatus">已启动</td><td data-k="SDL_AddWorkStatus">作业中</td><td data-k="SDL_AddStartWorkTime">2026-07-29 14:30</td><td data-k="SDL_AddNextStepStatus">—</td>
                  </tr></tbody>
                </table>
              </div></div>
            </div>

            <!-- TextPanel: 操作输入区 1567×482 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:4px 6px 6px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 步骤操作 <span style="font-weight:400;color:#888;font-size:8pt">TextPanel 1567×482</span></div>
              <div class="blk-bd" style="padding:6px 8px;display:flex;gap:12px">
                <!-- 左: 当前步骤信息网格 -->
                <div style="flex:1;display:grid;grid-template-columns:100px 1fr 100px 1fr;gap:4px 8px;align-items:center;font:9pt '微软雅黑'">
                  <label>当前步骤：</label><input data-k="txtCurrentStep" value="1" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0;width:80px" title="ReadOnly">
                  <label>总步骤：</label><input data-k="txtTotalStep" value="5" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0;width:80px" title="ReadOnly">
                  <label>当前项次：</label><input data-k="txtCurrentItem" value="1" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0;width:80px" title="ReadOnly">
                  <label>规格描述：</label><input data-k="txtDescription" value="投入原料A" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>最小值：</label><input data-k="txtMinValue" value="49.50" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>标准值：</label><input data-k="txtStandardValue" value="50.00" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>最大值：</label><input data-k="txtMaxValue" value="50.50" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>单位：</label><input data-k="txtUomNM" value="kg" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>重量：</label><input data-k="txtWeight" value="50.15" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;font-weight:bold;font-size:12pt;color:green" title="可手输/OPC自动采集">
                  <label>实时值：</label><input data-k="txtValueBox" value="50.15" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;font-weight:bold" title="当前OPC实时读数">
                  <label>数据采集项：</label><input data-k="txtDataCollectNM" value="重量采集" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>结果：</label><input data-k="txtResult" value="合格" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;color:green">
                  <label>设备名：</label><input data-k="TextArea_EquipmentNM" value="QDZY-10007" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>开始时间：</label><input data-k="txtStartTime" value="2026-07-29 14:30:00" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                  <label>计时器：</label><span data-k="txtTimer" style="font:14pt '微软雅黑';font-weight:700;color:#1a3a5c;cursor:pointer">00:05:23</span>
                  <label></label><span data-k="EquipmentLabel" style="font:9pt;color:#888">设备状态: 运行中</span>
                  <label>读值方式：</label><span data-k="ValueLabel" style="font:9pt">OPC</span>
                  <label></label><label data-k="lblzdTime" style="font:8pt;color:#888">最后更新时间: 14:30:15</label>
                </div>
                <!-- 中: 按钮列 -->
                <div style="flex:0 0 140px;display:flex;flex-direction:column;gap:8px;align-items:center">
                  <button class="btn primary" data-k="TextArea_Start" style="width:122px;height:47px;font:12pt '微软雅黑'">启动</button>
                  <button class="btn primary" data-k="TextArea_BtnStartWorking" style="width:122px;height:47px;font:12pt '微软雅黑'">开始作业</button>
                  <button class="btn" data-k="TextArea_BtnNextStep" style="width:122px;height:47px;font:12pt '微软雅黑'">下一步</button>
                  <div style="margin-top:8px;font-size:8pt">
                    <label><input type="checkbox" data-k="cbIsAniseed"> 大料</label><br>
                    <label><input type="checkbox" data-k="CheckBox_Skip"> 允许跳过</label>
                  </div>
                </div>
                <!-- 右: 附录字段 -->
                <div style="flex:0 0 180px;display:flex;flex-direction:column;gap:4px;font:9pt '微软雅黑'">
                  <label>步进重量:</label><input data-k="tbBBWeight" value="0.00" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                  <label>解析工艺:</label><input data-k="txtIsParsing" value="否" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="Visible=false">
                  <label>按钮编号:</label><input data-k="txtBtnNumber" value="BTN-01" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                  <button class="btn" data-k="btnTransmission" style="width:100px;height:30px;font:9pt '微软雅黑';margin-top:4px">传输</button>
                  <button class="btn" data-k="ClearValueText" style="width:100px;height:30px;font:9pt '微软雅黑'">清零</button>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">'''

html = html[:pos_start] + new_form + html[pos_end + len(form_end_marker):]

# ═══ Stats panel ═══
html = html.replace(
    '      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">CS&#xB7;报废单</span></div>',
    '      <div class="sh">&#x1F4CA; 代码分析<span class="tag tag-form" style="margin-left:4px">BPR作业 frmME_BPRRecord</span></div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div>\n          <div style="font-size:7pt;color:DimGray">DataGridView</div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div>\n          <div style="font-size:7pt;color:DimGray">DAL/BLL</div>')

old_t = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderHead</span> <span
              class="tag tag-tbl">报废单表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderList</span> <span
              class="tag tag-tbl">报废单明细</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MfgOrder</span> <span
              class="tag tag-tbl">工单</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ProductLine</span> <span
              class="tag tag-tbl">产线</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>
          </div>'''
new_t = r'''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">BPRRecord_StepDetailList</span> <span class="tag tag-tbl">工艺步骤明细 19列</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">BPRRecord_SpecDetailList</span> <span class="tag tag-tbl">规格详情 8列</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">BPRRecord_MfgOrderDetailList</span> <span class="tag tag-tbl">工单详情 7列</span></div>'''
html = html.replace(old_t, new_t)

old_d = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_ScrapOrderDAL</span> <span
              class="tag tag-bll">报废单</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetScrapOrderHeaderListByPage / GetScrapOrderListByPage
            / DelScrapOrder / DelScrapOrderHead / SendApproveScrapOrder</div>
          <div style="margin-top:2px"><span
              style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_InnerPackagingDAL</span> <span
              class="tag tag-bll">内包装</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetProductLine &#x2192; 产线下拉数据源</div>
          <div style="margin-top:2px"><span
              style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_SurplusMaterialDAL</span> <span
              class="tag tag-bll">余料</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetMfgOrderNM &#x2192; 工单号下拉数据源</div>
          <div style="margin-top:2px"><span
              style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZA_WIPLotSplitDAL</span> <span
              class="tag tag-bll">WIP拆分</span></div>'''
new_d = r'''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_BPRRecordBLL</span> <span class="tag tag-bll">BPR业务逻辑</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">bprBLL → BPR业务逻辑层</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_BPRRecordDAL</span> <span class="tag tag-bll">BPR数据访问</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">BPRDAL → BPR数据操作</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_IssueMaterialDAL</span> <span class="tag tag-bll">发料数据</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">IMDAL → 发料称重关联数据</div>'''
html = html.replace(old_d, new_d)

old_f = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_AddScrapOrder</span> <span
              class="tag tag-form">报废单主页</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_ScrapOrder</span> <span
              class="tag tag-form">添加/编辑表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EditScrapOrder</span> <span
              class="tag tag-form">添加/编辑明细</span></div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">ESignature</span> <span
              class="tag tag-form">电子签名(送审)</span></div>'''
new_f = r'''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_BPRRecord</span> <span class="tag tag-form">BPR作业 1588×918</span></div>
          <div style="margin-top:3px;font-size:8pt">├─ 启动 → 开始作业 → 下一步 (按步骤执行)<br>
          ├─ 工艺设备切换 → 无工艺启动<br>
          ├─ OPC实时读值 → 重量/数据采集项<br>
          └─ 指纹采集: ESignature (授权验证)</div>'''
html = html.replace(old_f, new_f)

old_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_AddScrapOrder.cs /
        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确</div>'''
new_src = r'''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_BPRRecord.cs / .Designer.cs<br>
        1588×918 · 3 DataGridView: StepDetailList(19列) · SpecDetailList(8列) · MfgOrderDetailList(7列)<br>
        DAL: MESZZZX_BPRRecordBLL · MESZZZX_BPRRecordDAL · MESZZZX_IssueMaterialDAL</div>'''
html = html.replace(old_src, new_src)

# ═══ Remove modals + add card ═══
modal_start = html.find('<!-- ═══════ Modal: frmME_ScrapOrder')
script_start = html.find('<script>')
if modal_start != -1 and script_start != -1:
    card_html = '''  <aside class="card" id="card">
    <div class="card-hd"><div><small>FIELD DATA LINEAGE</small><h3 id="title"></h3></div><button onclick="cl()" style="border:none;background:none;font-size:16px;cursor:pointer;color:DimGray">✕</button></div>
    <div class="card-bd"><div class="path" id="pth"></div><dl><dt>字段名</dt><dd id="label"></dd></dl><dl><dt>数据来源</dt><dd id="source"></dd></dl><dl><dt>控件类型</dt><dd id="type"></dd></dl><dl><dt>调用链路</dt><dd id="formula"></dd></dl><dl><dt>备注</dt><dd id="note" style="color:#059669"></dd></dl></div>
  </aside>\n  '''
    html = html[:modal_start] + card_html + html[script_start:]

# ═══ Replace JS map ═══
map_start = html.find('const map = {')
if map_start != -1:
    brace_count = 0; in_map = False; map_end = -1
    for i in range(map_start, len(html)):
        if html[i] == '{': brace_count += 1; in_map = True
        elif html[i] == '}':
            brace_count -= 1
            if in_map and brace_count == 0: map_end = i + 1; break
    if map_end != -1:
        new_map = r'''    // ═══════ 字段血缘 Map (BPR作业 · frmME_BPRRecord) ═══════
    const map = {
      // === 顶部工具栏 ===
      MfgOrderNMTextBox: ['工单号', 'MfgOrder.MfgOrderNM', 'ComboGrid', ['BindMfgOrderNM→工单下拉']],
      lblGYVersion: ['工艺版本', 'BPR.ProcessSpecVersion', 'Label', ['查询工单→工艺版本']],
      cboDevice: ['设备名', 'Config.ini', 'ComboBox', ['frmME_BPRRecord_Load→设备列表']],
      btnProcessSwitch: ['工艺设备切换', 'Button.Click', 'Button 138×35', ['btnProcessSwitch_Click→切换工艺/设备']],
      btnStartNoProcess: ['无工艺启动', 'Button.Click', 'Button 138×35', ['btnStartNoProcess_Click→无BPR启动']],
      // === MfgOrderDetailList 工单详情 ===
      MOD_WIP: ['WIP', 'MfgOrder.WIP', 'DataGridView col', ['MfgOrderDetailList→dtMfgOrderNM']],
      MOD_MOQty: ['工单数量', 'MfgOrder.MOQty', 'DataGridView col', ['MfgOrderDetailList→dtMfgOrderNM']],
      MOD_Description: ['规格描述', 'MfgOrder.Description', 'DataGridView col', ['MfgOrderDetailList→dtMfgOrderNM']],
      MOD_ProductNM: ['物料编号', 'Product.ProductNM', 'DataGridView col', ['MfgOrderDetailList→dtMfgOrderNM']],
      MOD_MFGBatch: ['生产批号', 'MfgOrder.MFGBatch', 'DataGridView col', ['MfgOrderDetailList→dtMfgOrderNM']],
      // === SpecDetailList 规格详情 ===
      SDL_Item: ['项次', 'SpecDetail.Item', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      SDL_PSDNM: ['项目名称', 'SpecDetail.PSDNM', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      SDL_Description: ['规格描述', 'SpecDetail.Description', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      SDL_Method: ['检验方法', 'SpecDetail.Method', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      SDL_Standard: ['内控标准', 'SpecDetail.Standard', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      SDL_Result: ['结果', 'SpecDetail.Result', 'DataGridView col', ['SpecDetailList→BPRRecordDAL']],
      // === StepDetailList 工艺步骤 ===
      SDL_SN: ['步骤', 'StepDetail.SN', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_StepItem: ['项次', 'StepDetail.Item', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_StepNM: ['步骤名称', 'StepDetail.StepNM', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_Value: ['值', 'StepDetail.Value', 'DataGridView col', ['StepDetailList→BPRRecordDAL/OPC采集']],
      SDL_StepResult: ['结果', 'StepDetail.Result', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_StandardValue: ['标准值', 'StepDetail.StandardValue', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_UOMNM: ['单位', 'UOM.UOMNM', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_MaxValue: ['最大值', 'StepDetail.MaxValue', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_MinValue: ['最小值', 'StepDetail.MinValue', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_DataCollectNM: ['数据采集项', 'StepDetail.DataCollectNM', 'DataGridView col', ['StepDetailList→BPRRecordDAL']],
      SDL_DataMethod: ['读值方式', 'StepDetail.DataMethod', 'DataGridView col', ['StepDetailList→BPRRecordDAL(OPC/手动)']],
      // === 步骤操作区 ===
      txtCurrentStep: ['当前步骤', 'currentStep', 'TextBox(ReadOnly)', ['BPR记录→currentStep'], '[自动]'],
      txtTotalStep: ['总步骤', 'TotalStep', 'TextBox(ReadOnly)', ['BPR记录→TotalStep'], '[自动]'],
      txtCurrentItem: ['当前项次', 'currentSpec', 'TextBox(ReadOnly)', ['BPR记录→currentSpec'], '[自动]'],
      txtMinValue: ['最小值', 'StepDetail.MinValue', 'TextBox(ReadOnly)', ['StepDetailList选中行→MinValue'], '[自动]'],
      txtStandardValue: ['标准值', 'StepDetail.StandardValue', 'TextBox(ReadOnly)', ['StepDetailList选中行→StandardValue'], '[自动]'],
      txtMaxValue: ['最大值', 'StepDetail.MaxValue', 'TextBox(ReadOnly)', ['StepDetailList选中行→MaxValue'], '[自动]'],
      txtWeight: ['重量', 'OPC采集/手输', 'TextBox', ['OPC→_weight 或 手动输入'], '[手输/自动]'],
      txtValueBox: ['实时值', 'OPC实时读数', 'TextBox', ['OPC→valueOpc→txtValueBox.Text'], '[OPC实时]'],
      txtResult: ['结果', 'OPC采集/手输', 'TextBox', ['OPC→_result 或 手动输入→合格/不合格']],
      txtTimer: ['计时器', 'System.Timer→CountDown/CountUp', 'Label 14pt', ['timer→txtTimer.Text=HH:mm:ss'], '[实时]'],
      TextArea_Start: ['启动按钮', 'Button.Click→启动步骤', 'Button 122×47', ['TextArea_Start_Click→启动当前步骤']],
      TextArea_BtnStartWorking: ['开始作业', 'Button.Click→开始作业', 'Button 122×47', ['TextArea_BtnStartWorking_Click→workState=true']],
      TextArea_BtnNextStep: ['下一步', 'Button.Click→下一项次', 'Button 122×47', ['TextArea_BtnNextStep_Click→currentSpec++']],
      cbIsAniseed: ['大料标记', 'CheckBox.Checked', 'CheckBox', ['cbIsAniseed→标记大料']],
      CheckBox_Skip: ['允许跳过', 'CheckBox.Checked', 'CheckBox', ['CheckBox_Skip→skip标志']],
    };'''
        html = html[:map_start] + new_map + html[map_end:]

# ═══ Replace button JS ═══
old_btn = r'''    // ═══════ 按钮交互 ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        // 查询
        if (k === 'btnQueryHead') { toast('🔍 正在查询：线号+工单号+报废日期 → 加载报废单表头及明细'); return }
        // 送审
        if (k === 'btnSendApprove') { if (!confirm('确认送审该报废单？\n送审后将进入审核流程，不可编辑。')) return; toast('📤 报废单已提交审核（模拟）'); return }
        // 添加表头 → 打开 frmME_ScrapOrder
        if (k === 'btnAddHead') { document.getElementById('modalHeadTitle').textContent = '添加报废单表头 — frmME_ScrapOrder'; openModal('modalHead'); return }
        // 编辑表头
        if (k === 'btnEditHead') { if (!document.querySelector('#headGrid tbody tr.sel-row')) { toast('⚠️ 请先在表头表格中选中一条记录'); return } document.getElementById('modalHeadTitle').textContent = '编辑报废单表头 — frmME_ScrapOrder (isEdit=1)'; openModal('modalHead'); return }
        // 删除表头
        if (k === 'btnDelHead') { if (!document.querySelector('#headGrid tbody tr.sel-row')) { toast('⚠️ 请先选中一条表头记录'); return } if (!confirm('确认删除选中的报废单表头？')) return; toast('🗑️ 报废单表头已删除（模拟）'); return }
        // 添加明细 → 打开 EditScrapOrder
        if (k === 'btnAddList') { document.getElementById('modalListTitle').textContent = '添加报废单明细 — EditScrapOrder'; openModal('modalList'); return }
        // 编辑明细
        if (k === 'btnEditList') { if (!document.querySelector('#listGrid tbody tr.sel-row')) { toast('⚠️ 请先在明细表格中选中一条记录'); return } document.getElementById('modalListTitle').textContent = '编辑报废单明细 — EditScrapOrder (isEdit=1)'; openModal('modalList'); return }
        // 删除明细
        if (k === 'btnDelList') { if (!document.querySelector('#listGrid tbody tr.sel-row')) { toast('⚠️ 请先选中一条明细记录'); return } if (!confirm('确认删除选中的报废单明细？')) return; toast('🗑️ 报废单明细已删除（模拟）'); return }
        // 显示字段血缘
        show(k);
      })
    });'''

new_btn = r'''    // ═══════ 按钮交互 (frmME_BPRRecord 实际事件) ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        if (k === 'TextArea_Start') { toast('🚀 启动步骤: currentStep=' + document.querySelector('[data-k="txtCurrentStep"]').value); return }
        if (k === 'TextArea_BtnStartWorking') { toast('▶ 开始作业 workState=true'); return }
        if (k === 'TextArea_BtnNextStep') { toast('⏭ 下一步 currentSpec++'); return }
        if (k === 'btnProcessSwitch') { toast('🔄 工艺设备切换'); return }
        if (k === 'btnStartNoProcess') { toast('⚡ 无工艺启动模式'); return }
        if (k === 'btnTransmission') { toast('📡 传输数据'); return }
        if (k === 'ClearValueText') { document.querySelector('[data-k="txtValueBox"]').value = '0.00'; toast('清零'); return }
        show(k);
      })
    });'''

html = html.replace(old_btn, new_btn)
html = html.replace("function submitHead() { closeModal('modalHead'); toast('✅ 报废单表头已保存（模拟）') }", "// (BPR作业无弹窗)")
html = html.replace("function submitList() { closeModal('modalList'); toast('✅ 报废单明细已保存（模拟）') }", "")

# ═══ Fix show() to include note ═══
html = html.replace(
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; card.classList.add('show') }",
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; document.getElementById('note').textContent = f[4] || ''; card.classList.add('show') }")

# ═══ Write ═══
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-bpr-record.html rebuilt from frmME_BPRRecord source!")
print(f"   Size: {len(html)} bytes")
print("   3 DataGridViews: StepDetailList(19) · SpecDetailList(8) · MfgOrderDetailList(7)")
