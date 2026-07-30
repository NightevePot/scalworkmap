#!/usr/bin/env python3
"""Rebuild demo-cs-template.html from frmME_IssueMaterial_Weighting source code.
Based on actual Designer.cs + .cs code-behind. No fabrication."""

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-template.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════ Step 1: Basic identity ═══════
html = html.replace('<title>报废单 · CS客户端</title>', '<title>称重 · CS客户端</title>')
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">称重</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">称重</div>')

# ═══════ Step 2: Replace form content - accurate from Designer.cs ═══════
old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'
form_end_marker = '    <div class="stats">'

pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

# Scale relative positions to fit the demo (form is 1497×396, but demo content area is ~1100px wide)
# We'll use the exact Designer.cs values but fit them in flex layout
new_form = '''            <!-- ═══════ 称重窗体: frmME_IssueMaterial_Weighting ═══════ -->
            <!-- 源码: 1497×396, 4 GroupBox + WeightBar + 3分隔条 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 称重 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">frmME_IssueMaterial_Weighting 1497×396</span><span style="float:right;font-size:8pt;color:#888">Text="称重"</span></div>
              <div class="blk-bd" style="padding:8px;display:flex;gap:8px;align-items:flex-start">
                <!-- 左列: 选择称重机 + 选择语音 -->
                <div style="flex:0 0 340px;display:flex;flex-direction:column;gap:8px">
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择称重机 <span style="font-weight:400;color:#888;font-size:8pt">groupBox3 328×125</span></legend>
                    <select data-k="cmbEquipList" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:12px">
                      <option>QDZY-10007</option><option>QDZY-10006</option><option>QDZY-10008</option><option>QDZY-11005</option><option>QDZY-30001</option><option>QDZY-10094</option>
                    </select>
                    <div style="font-size:7pt;color:#888;margin-top:4px">源码: Config.ini → PRINT/PRINT2/PRINT4/PRINT7 节</div>
                  </fieldset>
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择语音 <span style="font-weight:400;color:#888;font-size:8pt">groupBox4 328×125</span></legend>
                    <select data-k="cmbVoice" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:12px">
                      <option>Microsoft Huihui Desktop</option><option>Microsoft Zira Desktop</option>
                    </select>
                    <div style="font-size:7pt;color:#888;margin-top:4px">源码: SpeechSynthesizer.GetInstalledVoices()</div>
                  </fieldset>
                </div>
                <!-- 中列: 皮重 + 净重 GroupBox -->
                <div style="flex:1;display:flex;flex-direction:column;gap:8px;min-width:810px">
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:123px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">皮重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox1 798×123</span></legend>
                    <div style="display:flex;align-items:center;gap:8px;height:80px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px">皮重:</label>
                      <input data-k="SkinWeight" value="1.50" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px">
                      <button class="btn primary" data-k="SkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="SkinWeightButton_Click: 读取readWeight→SkinWeight.Text, 语音播报">皮重称重</button>
                      <button class="btn" data-k="RemoveSkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="RemoveSkinWeightButton_Click: SkinWeight.Text='0.00'">去皮重</button>
                    </div>
                  </fieldset>
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:222px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">净重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox2 798×222</span></legend>
                    <div style="display:flex;align-items:center;gap:8px;height:80px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px;color:green">净重:</label>
                      <input data-k="NetWeight" value="50.15" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;color:green" title="ForeColor=Green">
                      <button class="btn primary" data-k="WeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="WeightButton_Click: readWeight→NetWeight, GrossWeight=皮重+净重, 语音播报">净重称重</button>
                      <button class="btn" data-k="btnRefresh" style="width:142px;height:77px;font:15pt '宋体'" title="btnRefresh_Click">刷新</button>
                      <span data-k="WeightLabel" style="font:30pt '微软雅黑';font-weight:700;color:#1a3a5c">0.00</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;height:80px;margin-top:8px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px">毛重:</label>
                      <input data-k="GrossWeight" value="51.65" readonly style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;background:#FFFFE0;color:#B8860B" title="ReadOnly=True, ForeColor=Yellow, =SkinWeight+NetWeight">
                      <span style="font:9pt '微软雅黑';color:#888">[自动: 皮重+净重]</span>
                    </div>
                  </fieldset>
                </div>
                <!-- 右列: WeightBar 垂直进度条 -->
                <div style="width:180px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;position:relative">
                  <div data-k="MaxValueLabel" style="font:9pt '微软雅黑'">0.00</div>
                  <div style="font:8pt;color:#888">上限 MaxValue</div>
                  <div style="width:163px;height:8px;background:#000;margin:2px 0" title="button3: 分割条, Enabled=false"></div>
                  <div style="flex:1;width:163px;background:linear-gradient(to top,#0f0,#ff0,#f00);border:1px solid #C0C0C0;border-radius:2px;min-height:180px;position:relative" title="WeightBar: VerticalProgressBar, Maximum=10000">
                    <div style="position:absolute;top:30%;width:100%;border-top:2px dashed rgba(0,0,0,0.3)"></div>
                  </div>
                  <div style="width:163px;height:8px;background:#000;margin:2px 0" title="button2: 分割条, Enabled=false"></div>
                  <div data-k="StdValueLabel" style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">0.00</div>
                  <div style="font:8pt;color:#888">标准 StdValue</div>
                  <div style="width:163px;height:8px;background:#000;margin:4px 0 2px 0" title="button1: 分割条, Enabled=false"></div>
                  <div data-k="MinValueLabel" style="font:9pt '微软雅黑'">0.00</div>
                  <div style="font:8pt;color:#888">下限 MinValue</div>
                </div>
              </div>
              <!-- 实时读数区 (timer1_Tick) -->
              <div style="margin:4px 12px;padding:4px 8px;background:#F5F5F5;border:1px dashed #C0C0C0;border-radius:2px;font-size:8pt;color:#666">
                <b>timer1_Tick</b>: 每间隔从TCP读取 readWeight → 更新 WeightLabel 和 WeightBar.Value（范围: minimum~maximum）。<br>
                公式: maximum = MaxValue²/StdValue×1000, minimum = MinValue²/StdValue×1000
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">'''

html = html[:pos_start] + new_form + html[pos_end + len(form_end_marker):]

# ═══════ Step 3: Replace stats panel - accurate from .cs code ═══════
old_stats_title = '      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">CS&#xB7;报废单</span></div>'
new_stats_title = '      <div class="sh">&#x1F4CA; 代码分析<span class="tag tag-form" style="margin-left:4px">称重 frmME_IssueMaterial_Weighting</span></div>'
html = html.replace(old_stats_title, new_stats_title)

# Count boxes: replace 5 tables→0 tables (no DB), 0 stored procs stays, 4 DAL→1 DAL
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">0</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">1</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>')

# Replace tables section
old_tables_block = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderHead</span> <span
              class="tag tag-tbl">报废单表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderList</span> <span
              class="tag tag-tbl">报废单明细</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MfgOrder</span> <span
              class="tag tag-tbl">工单</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ProductLine</span> <span
              class="tag tag-tbl">产线</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>
          </div>'''
new_tables_block = '''          <div style="font-size:8pt;color:#888;padding:2px 4px">此窗体无数据库表操作<br>数据来源: 串口/TCP 实时读取秤重硬件</div>'''
html = html.replace(old_tables_block, new_tables_block)

# Replace stored proc section
old_sp_block = '''        <div style="font-size:8pt;color:#888;padding:2px 4px">通过 DAL&#x2192;WebAPI 直接操作，未使用独立存储过程</div>'''
new_sp_block = '''        <div style="font-size:8pt;color:#888;padding:2px 4px">无存储过程，数据直接从硬件串口读取</div>'''
html = html.replace(old_sp_block, new_sp_block)

# Replace DAL section
old_dal_block = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_ScrapOrderDAL</span> <span
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
new_dal_block = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EquipmentDAL</span> <span
              class="tag tag-bll">设备DAL</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetLoadData(equipmentNM) → 仅在非预定义设备时调用</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">BaseMethod</span> <span
              class="tag tag-bll">通用方法</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetAppCurrentPath / IniFile.GetINI → 读取Config.ini设备配置</div>'''
html = html.replace(old_dal_block, new_dal_block)

# Replace forms section
old_forms_block = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_AddScrapOrder</span> <span
              class="tag tag-form">报废单主页</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_ScrapOrder</span> <span
              class="tag tag-form">添加/编辑表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EditScrapOrder</span> <span
              class="tag tag-form">添加/编辑明细</span></div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">ESignature</span> <span
              class="tag tag-form">电子签名(送审)</span></div>'''
new_forms_block = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_IssueMaterial_Weighting</span> <span
              class="tag tag-form">称重 1497×396</span></div>
          <div style="margin-top:4px;font-size:8pt;line-height:1.6">
            <b>通信:</b> SuperSocket TCP (AsyncTcpSession) → 秤重设备<br>
            <b>语音:</b> System.Speech.Synthesis.SpeechSynthesizer<br>
            <b>定时器:</b> timer1 (实时更新 WeightBar + WeightLabel)<br>
            <b>设备列表:</b> QDZY-10007/10006/10008/11005/30001/10094<br>
            <b>配置:</b> Config.ini → PRINT/PRINT2/PRINT4/PRINT7 节
          </div>'''
html = html.replace(old_forms_block, new_forms_block)

# Replace source note
old_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_AddScrapOrder.cs /
        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确</div>'''
new_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_IssueMaterial_Weighting.cs / .Designer.cs<br>
        groupBox1(皮重 798×123) · groupBox2(净重 798×222) · groupBox3(称重机 328×125) · groupBox4(语音 328×125)<br>
        WeightBar(VerticalProgressBar 163×361) · timer1 · SpeechSynthesizer · AsyncTcpSession</div>'''
html = html.replace(old_src, new_src)

# ═══════ Step 4: Remove modals (not applicable to weighing form) ═══════
modal_start = html.find('<!-- ═══════ Modal: frmME_ScrapOrder')
script_start = html.find('<script>')
if modal_start != -1 and script_start != -1:
    html = html[:modal_start] + '\n  ' + html[script_start:]

# ═══════ Step 5: Replace JavaScript map ═══════
map_start = html.find('const map = {')
if map_start != -1:
    brace_count = 0
    in_map = False
    map_end = -1
    for i in range(map_start, len(html)):
        if html[i] == '{':
            brace_count += 1
            in_map = True
        elif html[i] == '}':
            brace_count -= 1
            if in_map and brace_count == 0:
                map_end = i + 1
                break
    
    if map_end != -1:
        new_js_map = '''    // ═══════ 字段血缘 Map (称重 · frmME_IssueMaterial_Weighting) ═══════
    const map = {
      // === groupBox3: 选择称重机 ===
      cmbEquipList: ['称重机', 'Config.ini→cmbEquipList.Items.Add', 'ComboBox(DropDownList) 295×35', ['initCZJSerialPort()→PRINT/PRINT2/PRINT4/PRINT7节']],
      // === groupBox4: 选择语音 ===
      cmbVoice: ['语音', 'SpeechSynthesizer.GetInstalledVoices()', 'ComboBox(DropDownList) 295×35', ['frmME_IssueMaterial_Weighting_Load→speech.GetInstalledVoices()']],
      // === groupBox1: 皮重信息 ===
      SkinWeight: ['皮重值', 'ReadScale→SkinWeight.Text', 'TextBox 280×75 Courier New 36pt Bold', ['SkinWeightButton_Click→readWeight(串口)'], '[硬件读取]'],
      SkinWeightButton: ['皮重称重', 'Button.Click→SkinWeightButton_Click', 'Button 142×77 宋体 15pt', ['readWeight→Math.Abs→SkinWeight.Text, SpeakInfo("皮重X千克")']],
      RemoveSkinWeightButton: ['去皮重', 'Button.Click→RemoveSkinWeightButton_Click', 'Button 142×77 宋体 15pt', ['SkinWeight.Text="0.00"']],
      // === groupBox2: 净重信息 ===
      NetWeight: ['净重值', 'ReadScale→NetWeight.Text', 'TextBox 280×75 Courier New 36pt Bold, ForeColor=Green', ['WeightButton_Click→readWeight→NetWeight.Text'], '[硬件读取]'],
      WeightButton: ['净重称重', 'Button.Click→WeightButton_Click', 'Button 142×77 宋体 15pt', ['readWeight→NetWeight, GrossWeight=皮重+净重, SpeakInfo("净重X千克")']],
      btnRefresh: ['刷新', 'Button.Click→btnRefresh_Click', 'Button 142×77 宋体 15pt', ['btnRefresh_Click']],
      GrossWeight: ['毛重值', 'SkinWeight+NetWeight', 'TextBox(ReadOnly) 280×75, ForeColor=Yellow', ['WeightButton_Click→GrossWeight.Text=皮重+净重'], '[自动计算]'],
      WeightLabel: ['实时读数', 'timer1_Tick→readWeight', 'Label 30pt 微软雅黑', ['timer1→TCP→readWeight→WeightLabel.Text'], '[硬件实时]'],
      // === 右列: WeightBar + 标签 ===
      MaxValueLabel: ['上限值', 'frmME_IssueMaterial_Weighting_Load→MaxValue', 'Label', ['外部SetMaxValue属性→MaxValueLabel.Text']],
      StdValueLabel: ['标准值', 'frmME_IssueMaterial_Weighting_Load→StdValue', 'Label 微软雅黑 12pt', ['外部SetStdValue属性→StdValueLabel.Text']],
      MinValueLabel: ['下限值', 'frmME_IssueMaterial_Weighting_Load→MinValue', 'Label', ['外部SetMinValue属性→MinValueLabel.Text']],
      WeightBar: ['垂直进度条', 'timer1_Tick→WeightBar.Value', 'VerticalProgressBar 163×361, Maximum=10000', ['timer1→readWeight→(值-minimum)/(maximum-minimum)'], '[硬件实时]'],
    };'''
        html = html[:map_start] + new_js_map + html[map_end:]

# ═══════ Step 6: Update button JS logic ═══════
# Remove old scrap-order button handlers - find and replace the button interaction block
old_btn_block_start = '''    // ═══════ 按钮交互 ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        // 查询
        if (k === 'btnQueryHead') { toast('🔍 正在查询：线号+工单号+报废日期 → 加载报废单表头及明细'); return }
        // 送审
        if (k === 'btnSendApprove') { if (!confirm('确认送审该报废单？\\n送审后将进入审核流程，不可编辑。')) return; toast('📤 报废单已提交审核（模拟）'); return }
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

new_btn_block = '''    // ═══════ 按钮交互 (基于 frmME_IssueMaterial_Weighting.cs 实际事件) ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        // 皮重称重 → SkinWeightButton_Click
        if (k === 'SkinWeightButton') { 
          var v = (Math.random() * 10).toFixed(2);
          document.querySelector('[data-k="SkinWeight"]').value = v;
          toast('🔊 语音播报: 皮重 ' + v + ' 千克 (模拟TCP读数)');
          return;
        }
        // 去皮重 → RemoveSkinWeightButton_Click
        if (k === 'RemoveSkinWeightButton') {
          document.querySelector('[data-k="SkinWeight"]').value = '0.00';
          toast('皮重已清零');
          return;
        }
        // 净重称重 → WeightButton_Click
        if (k === 'WeightButton') {
          var nw = (Math.random() * 50 + 20).toFixed(2);
          document.querySelector('[data-k="NetWeight"]').value = nw;
          var sk = parseFloat(document.querySelector('[data-k="SkinWeight"]').value) || 0;
          var gw = (sk + parseFloat(nw)).toFixed(2);
          document.querySelector('[data-k="GrossWeight"]').value = gw;
          toast('🔊 语音播报: 净重 ' + nw + ' 千克, 毛重=' + gw);
          return;
        }
        // 刷新 → btnRefresh_Click
        if (k === 'btnRefresh') {
          document.querySelector('[data-k="WeightLabel"]').textContent = (Math.random() * 50).toFixed(2);
          toast('🔄 刷新实时读数');
          return;
        }
        // 显示字段血缘
        show(k);
      })
    });'''

html = html.replace(old_btn_block_start, new_btn_block)

# Also replace the old submit functions (no modals needed)
html = html.replace(
    "function submitHead() { closeModal('modalHead'); toast('✅ 报废单表头已保存（模拟）') }",
    "// (称重窗体无模态弹窗)")
html = html.replace(
    "function submitList() { closeModal('modalList'); toast('✅ 报废单明细已保存（模拟）') }",
    "")

# Step 7: Update toast messages  
html = html.replace("'数据已保存 (报废单)'", "'数据已保存 (称重)'")

# ═══════ Write ═══════
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-template.html rebuilt from actual source code!")
print(f"   Size: {len(html)} bytes")
print("   Based on: frmME_IssueMaterial_Weighting.cs + .Designer.cs")
