#!/usr/bin/env python3
"""Rebuild demo-cs-weighing-test.html from frmME_WeightingTest source."""

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-weighing-test.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══ Identity ═══
html = html.replace('<title>报废单 · CS客户端</title>', '<title>称重调试 · CS客户端</title>')
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">称重调试</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">称重调试</div>')

# ═══ Form content ═══
old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'
form_end_marker = '    <div class="stats">'
pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

new_form = '''            <!-- ═══════ frmME_WeightingTest · 称重调试 1497×643 ═══════ -->
            <!-- 源码: this.Text="称重调试", 无DataGridView -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 称重调试 <span style="font-weight:400;color:#888;font-size:8pt">frmME_WeightingTest 1497×643</span><span style="float:right;font-size:8pt;color:#888">Text="称重调试" · DAL: MESZZZX_GetEquipmentDAL</span></div>
              <div class="blk-bd" style="padding:8px">
                <!-- ═══ 顶部: 设备号输入区 ═══ -->
                <div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;padding:6px 8px;background:#F5F5F5;border:1px dashed #C0C0C0;border-radius:2px">
                  <label style="font:12pt '微软雅黑';font-weight:700">设备号:</label>
                  <input data-k="textBox1" placeholder="输入设备号后回车..." value="QDZY-10007" style="width:285px;height:38px;font:16pt '宋体';border:1px solid #C0C0C0;border-radius:2px;padding:0 8px" title="源码: textBox1, 宋体16.2pt, KeyDown→Enter→EquipmentInfo(equipmentNMTemp)→Start()">
                  <span style="font-size:8pt;color:#888">按 Enter → EquipmentInfo → 连接TCP + 初始化串口</span>
                </div>
                <!-- ═══ 主体: 三列布局 ═══ -->
                <div style="display:flex;gap:8px;align-items:flex-start">
                  <!-- 左列: 选择称重机 + 选择语音 -->
                  <div style="flex:0 0 340px;display:flex;flex-direction:column;gap:8px">
                    <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                      <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择称重机 <span style="font-weight:400;color:#888;font-size:8pt">groupBox3 328×125</span></legend>
                      <select data-k="cmbEquipList" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:12px" title="源码: DropDownList, 设备号回车后填充EquipmentInfo结果">
                        <option>QDZY-10007</option><option>QDZY-10006</option><option>QDZY-10008</option><option>QDZY-11005</option><option>QDZY-30001</option><option>QDZY-10094</option>
                      </select>
                    </fieldset>
                    <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                      <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择语音 <span style="font-weight:400;color:#888;font-size:8pt">groupBox4 328×125</span></legend>
                      <select data-k="cmbVoice" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:12px" title="源码: SpeechSynthesizer.GetInstalledVoices()">
                        <option>Microsoft Huihui Desktop</option><option>Microsoft Zira Desktop</option>
                      </select>
                    </fieldset>
                  </div>
                  <!-- 中列: 皮重 + 净重 GroupBox -->
                  <div style="flex:1;display:flex;flex-direction:column;gap:8px;min-width:810px">
                    <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:123px">
                      <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">皮重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox1 798×123</span></legend>
                      <div style="display:flex;align-items:center;gap:8px;height:80px">
                        <label style="font:21pt '微软雅黑';font-weight:700;width:80px">皮重:</label>
                        <input data-k="SkinWeight" value="1.50" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px" title="源码: SkinWeightTextBox, Courier New 36pt Bold. SkinWeightButton_Click → readWeight(串口)→SkinWeight.Text">
                        <button class="btn primary" data-k="SkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="SkinWeightButton_Click: this.SkinWeight.Text = readWeight; SpeakInfo('皮重X千克')">皮重称重</button>
                        <button class="btn" data-k="RemoveSkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="RemoveSkinWeightButton_Click: SkinWeight.Text='0.00'">去皮重</button>
                      </div>
                    </fieldset>
                    <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:222px">
                      <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">净重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox2 798×222</span></legend>
                      <div style="display:flex;align-items:center;gap:8px;height:80px">
                        <label style="font:21pt '微软雅黑';font-weight:700;width:80px;color:green">净重:</label>
                        <input data-k="NetWeight" value="50.15" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;color:green" title="源码: NetWeightTextBox, Courier New 36pt Bold, ForeColor=Green. WeightButton_Click → readWeight→NetWeight, GrossWeight=皮重+净重">
                        <button class="btn primary" data-k="WeightButton" style="width:142px;height:77px;font:15pt '宋体'" title="WeightButton_Click: NetWeight=readWeight, GrossWeight=皮重+净重, SpeakInfo('净重X千克')">净重称重</button>
                        <button class="btn" data-k="btnRefresh" style="width:142px;height:77px;font:15pt '宋体'" title="btnRefresh_Click">刷新</button>
                        <span data-k="WeightLabel" style="font:30pt '微软雅黑';font-weight:700;color:#1a3a5c;cursor:pointer" title="源码: timer2_Tick→TCP readWeight→WeightLabel.Text 30pt 微软雅黑">0.00</span>
                      </div>
                      <div style="display:flex;align-items:center;gap:8px;height:80px;margin-top:8px">
                        <label style="font:21pt '微软雅黑';font-weight:700;width:80px">毛重:</label>
                        <input data-k="GrossWeight" value="51.65" readonly style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;background:#FFFFE0;color:#B8860B" title="源码: ReadOnly=True, ForeColor=Yellow. GrossWeight.Text = SkinWeight + NetWeight">
                        <span style="font:9pt '微软雅黑';color:#888">[自动: 皮重+净重]</span>
                      </div>
                    </fieldset>
                  </div>
                  <!-- 右列: WeightBar 垂直进度条 -->
                  <div style="width:180px;flex-shrink:0;display:flex;flex-direction:column;align-items:center">
                    <div data-k="MaxValueLabel" style="font:9pt '微软雅黑';cursor:pointer" title="源码: frmME_WeightingTest_Load→MaxValueLabel.Text=MaxValue">0.00</div>
                    <div style="font:8pt;color:#888">上限 MaxValue</div>
                    <div style="width:163px;height:8px;background:#000;margin:2px 0" title="button3: 分隔条, Enabled=false"></div>
                    <div style="flex:1;width:163px;background:linear-gradient(to top,#0f0,#ff0,#f00);border:1px solid #C0C0C0;border-radius:2px;min-height:180px;position:relative" title="WeightBar: VerticalProgressBar, Maximum=10000">
                      <div id="wbarFill" style="position:absolute;bottom:0;width:100%;background:rgba(0,0,0,0.15);height:50%;transition:height 0.3s"></div>
                    </div>
                    <div style="width:163px;height:8px;background:#000;margin:2px 0" title="button2: 分隔条, Enabled=false"></div>
                    <div data-k="StdValueLabel" style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c;cursor:pointer" title="源码: StdValueLabel, 微软雅黑12pt">0.00</div>
                    <div style="font:8pt;color:#888">标准 StdValue</div>
                    <div style="width:163px;height:8px;background:#000;margin:4px 0 2px 0" title="button1: 分隔条, Enabled=false"></div>
                    <div data-k="MinValueLabel" style="font:9pt '微软雅黑';cursor:pointer" title="源码: MinValueLabel.Text=MinValue">0.00</div>
                    <div style="font:8pt;color:#888">下限 MinValue</div>
                  </div>
                </div>
                <!-- ═══ 底部: 调试输出 textBox2 ═══ -->
                <div style="margin-top:8px;padding:4px 8px;background:#F5F5F5;border:1px dashed #C0C0C0;border-radius:2px;font-size:8pt;color:#666">
                  <b>调试输出 textBox2</b> (1006×34, 宋体13.8pt): 
                  <span data-k="textBox2" style="font:12pt '宋体';color:#333;cursor:pointer" title="源码: textBox2.Font=宋体13.8pt, 1006×34. 显示TCP连接状态/调试信息">TCP已连接 192.168.5.213:4196 | readWeight=50.15 | timer2运行中</span>
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
    '      <div class="sh">&#x1F4CA; 代码分析<span class="tag tag-form" style="margin-left:4px">称重调试 frmME_WeightingTest</span></div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">0</div>\n          <div style="font-size:7pt;color:DimGray">DataGridView</div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">1</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>')

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
html = html.replace(old_t, '''          <div style="font-size:8pt;color:#888;padding:2px 4px">无DataGridView<br>数据来源: TCP串口读取秤重硬件</div>''')

old_sp = '''        <div style="font-size:8pt;color:#888;padding:2px 4px">通过 DAL&#x2192;WebAPI 直接操作，未使用独立存储过程</div>'''
html = html.replace(old_sp, '''        <div style="font-size:8pt;color:#888;padding:2px 4px">无存储过程. MESZZZX_GetEquipmentDAL→WebAPI获取设备IP→TCP连接</div>''')

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
html = html.replace(old_d, '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_GetEquipmentDAL</span> <span class="tag tag-bll">设备查询</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetEquipmentInfo(body, grid) → 返回ServerNM(IP地址)</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">BaseMethod</span> <span class="tag tag-bll">通用方法</span></div>''')

old_f = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_AddScrapOrder</span> <span
              class="tag tag-form">报废单主页</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_ScrapOrder</span> <span
              class="tag tag-form">添加/编辑表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EditScrapOrder</span> <span
              class="tag tag-form">添加/编辑明细</span></div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">ESignature</span> <span
              class="tag tag-form">电子签名(送审)</span></div>'''
html = html.replace(old_f, '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_WeightingTest</span> <span class="tag tag-form">称重调试 1497×643</span></div>
          <div style="margin-top:3px;font-size:8pt"><b>通信:</b> SuperSocket TCP → 秤重设备<br>
          <b>语音:</b> SpeechSynthesizer<br>
          <b>定时器:</b> timer2 (实时更新 WeightBar + WeightLabel)<br>
          <b>调试:</b> textBox1输入设备号回车→EquipmentInfo→TCP连接→textBox2输出状态</div>''')

old_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_AddScrapOrder.cs /
        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确</div>'''
html = html.replace(old_src, '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_WeightingTest.cs / .Designer.cs<br>
        1497×643 · 4 GroupBox + WeightBar + textBox1(设备号) + textBox2(调试输出)<br>
        DAL: MESZZZX_GetEquipmentDAL · timer2 · SpeechSynthesizer · AsyncTcpSession</div>''')

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
        new_map = '''    // ═══════ 字段血缘 Map (称重调试 · frmME_WeightingTest) ═══════
    const map = {
      // === 设备号输入 ===
      textBox1: ['设备号输入', '用户输入, KeyDown→Enter', 'TextBox 285×38, 宋体16.2pt', ['textBox1_KeyDown→EquipmentInfo(equipmentNMTemp)→Start()']],
      // === groupBox3: 选择称重机 ===
      cmbEquipList: ['称重机', 'EquipmentInfo→WebAPI返回', 'ComboBox(DropDownList) 295×35', ['textBox1_KeyDown→GetEquipmentDAL.GetEquipmentInfo']],
      // === groupBox4: 选择语音 ===
      cmbVoice: ['语音', 'SpeechSynthesizer.GetInstalledVoices()', 'ComboBox(DropDownList) 295×35', ['frmME_WeightingTest_Load→speechs.GetInstalledVoices()']],
      // === groupBox1: 皮重信息 ===
      SkinWeight: ['皮重值', '串口→readWeight', 'TextBox 280×75 Courier New 36pt Bold', ['SkinWeightButton_Click→this.SkinWeight.Text=readWeight, SpeakInfo("皮重X千克")'], '[硬件读取]'],
      SkinWeightButton: ['皮重称重', 'Button.Click→SkinWeightButton_Click', 'Button 142×77 宋体15pt', ['readWeight→SkinWeight.Text, SpeakInfo语音播报']],
      RemoveSkinWeightButton: ['去皮重', 'Button.Click→RemoveSkinWeightButton_Click', 'Button 142×77 宋体15pt', ['SkinWeight.Text="0.00"']],
      // === groupBox2: 净重信息 ===
      NetWeight: ['净重值', '串口→readWeight→NetWeight.Text', 'TextBox 280×75 Courier New 36pt Bold, ForeColor=Green', ['WeightButton_Click→NetWeight=readWeight, GrossWeight=皮重+净重, SpeakInfo("净重X千克")'], '[硬件读取]'],
      WeightButton: ['净重称重', 'Button.Click→WeightButton_Click', 'Button 142×77 宋体15pt', ['readWeight→NetWeight, GrossWeight=皮重+净重, SpeakInfo语音播报']],
      btnRefresh: ['刷新', 'Button.Click→btnRefresh_Click', 'Button 142×77 宋体15pt', ['btnRefresh_Click']],
      GrossWeight: ['毛重值', 'SkinWeight + NetWeight', 'TextBox(ReadOnly) 280×75, ForeColor=Yellow', ['WeightButton_Click→GrossWeight.Text = 皮重+净重'], '[自动计算]'],
      WeightLabel: ['实时读数', 'timer2_Tick→TCP→readWeight', 'Label 30pt 微软雅黑', ['timer2→TCP AsyncTcpSession→readWeight→WeightLabel.Text'], '[硬件实时]'],
      // === 右列: WeightBar + 标签 ===
      MaxValueLabel: ['上限', 'frmME_WeightingTest_Load→MaxValue', 'Label', ['外部SetMaxValue→MaxValueLabel.Text']],
      StdValueLabel: ['标准值', 'frmME_WeightingTest_Load→StdValue', 'Label 微软雅黑12pt', ['外部SetStdValue→StdValueLabel.Text']],
      MinValueLabel: ['下限', 'frmME_WeightingTest_Load→MinValue', 'Label', ['外部SetMinValue→MinValueLabel.Text']],
      // === 底部调试 ===
      textBox2: ['调试输出', 'TCP连接状态/readWeight', 'TextBox 1006×34, 宋体13.8pt', ['textBox1_KeyDown→textBox2.Text=test, timer2实时更新']],
    };'''
        html = html[:map_start] + new_map + html[map_end:]

# ═══ Replace button JS ═══
old_btn = '''    // ═══════ 按钮交互 ═══════
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

new_btn = '''    // ═══════ 按钮交互 (frmME_WeightingTest 实际事件) ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        // 皮重称重 → SkinWeightButton_Click: this.SkinWeight.Text = readWeight
        if (k === 'SkinWeightButton') {
          var v = (Math.random() * 5 + 0.5).toFixed(2);
          document.querySelector('[data-k="SkinWeight"]').value = v;
          updateGrossWeight();
          toast('🔊 语音: 皮重 ' + v + ' 千克');
          return;
        }
        // 去皮重 → RemoveSkinWeightButton_Click
        if (k === 'RemoveSkinWeightButton') {
          document.querySelector('[data-k="SkinWeight"]').value = '0.00';
          updateGrossWeight();
          toast('皮重已清零');
          return;
        }
        // 净重称重 → WeightButton_Click
        if (k === 'WeightButton') {
          var nw = (Math.random() * 50 + 20).toFixed(2);
          document.querySelector('[data-k="NetWeight"]').value = nw;
          updateGrossWeight();
          toast('🔊 语音: 净重 ' + nw + ' 千克');
          return;
        }
        // 刷新 → btnRefresh_Click
        if (k === 'btnRefresh') {
          document.querySelector('[data-k="WeightLabel"]').textContent = (Math.random() * 50).toFixed(2);
          toast('🔄 刷新实时读数 (模拟 timer2_Tick)');
          return;
        }
        show(k);
      })
    });
    // 毛重 = 皮重 + 净重
    function updateGrossWeight() {
      var sk = parseFloat(document.querySelector('[data-k="SkinWeight"]').value) || 0;
      var nw = parseFloat(document.querySelector('[data-k="NetWeight"]').value) || 0;
      document.querySelector('[data-k="GrossWeight"]').value = (sk + nw).toFixed(2);
    }
    // 设备号回车 → textBox1_KeyDown
    document.querySelector('[data-k="textBox1"]').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var eq = this.value;
        document.querySelector('[data-k="textBox2"]').textContent = 'TCP已连接 ' + eq + ' | readWeight=50.15 | timer2运行中';
        toast('🔌 设备 ' + eq + ' 已连接 (模拟 EquipmentInfo→TCP)');
      }
    });'''

html = html.replace(old_btn, new_btn)
html = html.replace("function submitHead() { closeModal('modalHead'); toast('✅ 报废单表头已保存（模拟）') }", "// (称重调试无弹窗)")
html = html.replace("function submitList() { closeModal('modalList'); toast('✅ 报废单明细已保存（模拟）') }", "")

# ═══ Update show() to include note ═══
html = html.replace(
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; card.classList.add('show') }",
    "function show(k) { const f = map[k]; if (!f) return; document.getElementById('title').textContent = f[0]; document.getElementById('label').textContent = f[0]; document.getElementById('source').textContent = f[1]; document.getElementById('type').textContent = f[2]; document.getElementById('formula').textContent = f[3]; document.getElementById('note').textContent = f[4] || ''; card.classList.add('show') }")

# ═══ Write ═══
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-weighing-test.html rebuilt from frmME_WeightingTest source!")
print(f"   Size: {len(html)} bytes")
print("   Layout: textBox1(设备号)→groupBox3/4(左)+groupBox1/2(中)+WeightBar(右)+textBox2(底)")
