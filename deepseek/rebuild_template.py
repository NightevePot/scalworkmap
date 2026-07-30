#!/usr/bin/env python3
"""Rebuild demo-cs-template.html (原料称重) from demo-cs-scrap-order.html."""

import re

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-template.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. Title ──
html = html.replace('<title>报废单 · CS客户端</title>', '<title>原料称重 · CS客户端</title>')

# ── 2. Sidebar & Tab ──
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">原料称重</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">原料称重</div>')

# ── 3. Replace form content (Block ① → ③) with 原料称重 GroupBox layout ──
# Find the content area: from <div class="content"> to the closing </div> before <div class="stats">
# Strategy: replace everything between <!-- ═══════ Block ②: 报废单表头区... --> marker and the </div></div></div> before stats

old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'

# Find the end of the form area (before stats)
# Look for pattern: </div>\n        </div>\n      </div>\n    </div>\n    <div class="stats">
form_end_marker = '    <div class="stats">'

# Find positions
pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

if pos_start == -1 or pos_end == -1:
    print(f"ERROR: pos_start={pos_start}, pos_end={pos_end}")
else:
    new_form = '''            <!-- ═══════ 原料称重: 4个GroupBox + 垂直进度条 ═══════ -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 原料称重信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">frmME_IssueMaterial_Weighting 1497×396</span></div>
              <div class="blk-bd" style="padding:8px;display:flex;gap:8px">
                <div style="flex:0 0 360px;display:flex;flex-direction:column;gap:8px">
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择称重机</legend>
                    <select data-k="cmbEquipList" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:8px">
                      <option>电子秤-01</option><option>电子秤-02</option><option>电子秤-03</option>
                    </select>
                  </fieldset>
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:125px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">选择语音</legend>
                    <select data-k="cmbVoice" style="width:295px;height:35px;font:10pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;margin-top:8px">
                      <option>开启</option><option>关闭</option>
                    </select>
                  </fieldset>
                </div>
                <div style="flex:1;display:flex;flex-direction:column;gap:8px">
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:123px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">皮重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox1 798×123</span></legend>
                    <div style="display:flex;align-items:center;gap:8px;height:80px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px">皮重:</label>
                      <input data-k="SkinWeight" value="1.50" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px">
                      <button class="btn primary" data-k="SkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'">皮重称重</button>
                      <button class="btn" data-k="RemoveSkinWeightButton" style="width:142px;height:77px;font:15pt '宋体'">去皮重</button>
                    </div>
                  </fieldset>
                  <fieldset style="border:1px solid #C0C0C0;border-radius:3px;padding:8px 12px;height:222px">
                    <legend style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">净重信息 <span style="font-weight:400;color:#888;font-size:8pt">groupBox2 798×222</span></legend>
                    <div style="display:flex;align-items:center;gap:8px;height:80px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px;color:green">净重:</label>
                      <input data-k="NetWeight" value="50.15" style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;color:green">
                      <button class="btn primary" data-k="WeightButton" style="width:142px;height:77px;font:15pt '宋体'">净重称重</button>
                      <button class="btn" data-k="btnRefresh" style="width:142px;height:77px;font:15pt '宋体'">刷新</button>
                      <span style="font:30pt '微软雅黑';font-weight:700;color:#1a3a5c">0.00</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;height:80px;margin-top:8px">
                      <label style="font:21pt '微软雅黑';font-weight:700;width:80px">毛重:</label>
                      <input data-k="GrossWeight" value="51.65" readonly style="width:280px;height:75px;font:36pt 'Courier New';font-weight:bold;border:1px solid #C0C0C0;border-radius:3px;text-align:right;padding:0 8px;background:#FFFFE0;color:#B8860B">
                      <span style="font:9pt '微软雅黑';color:#888">[自动]</span>
                    </div>
                  </fieldset>
                </div>
                <div style="width:180px;flex-shrink:0;display:flex;flex-direction:column;align-items:center">
                  <div style="font:9pt '微软雅黑';color:#888">上限</div>
                  <div data-k="MaxValueLabel" style="font:9pt '微软雅黑'">50.50</div>
                  <div style="width:163px;height:6px;background:#333;margin:2px 0"></div>
                  <div style="flex:1;width:163px;background:linear-gradient(to top,#0f0,#ff0,#f00);border:1px solid #C0C0C0;border-radius:2px;min-height:180px;position:relative">
                    <div style="position:absolute;top:50%;width:100%;border-top:2px dashed #333"></div>
                  </div>
                  <div style="width:163px;height:6px;background:#333;margin:2px 0"></div>
                  <div data-k="StdValueLabel" style="font:12pt '微软雅黑';font-weight:700;color:#1a3a5c">50.00</div>
                  <div style="font:9pt '微软雅黑';color:#888">标准值</div>
                  <div style="width:163px;height:6px;background:#333;margin:4px 0 2px 0"></div>
                  <div data-k="MinValueLabel" style="font:9pt '微软雅黑'">49.50</div>
                  <div style="font:9pt '微软雅黑';color:#888">下限</div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">'''

    html = html[:pos_start] + new_form + html[pos_end + len(form_end_marker):]

# ── 4. Replace stats panel content ──
old_stats = '''      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">CS&#xB7;报废单</span></div>'''

new_stats_title = '''      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">CS&#xB7;原料称重</span></div>'''

html = html.replace(old_stats, new_stats_title)

# ── 5. Replace stats detail blocks ──
# Count boxes
html = html.replace('<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>',
                    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">2</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>')
html = html.replace('<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>',
                    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">1</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>')

# Database tables section
old_tables = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderHead</span> <span
              class="tag tag-tbl">报废单表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ScrapOrderList</span> <span
              class="tag tag-tbl">报废单明细</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MfgOrder</span> <span
              class="tag tag-tbl">工单</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">ProductLine</span> <span
              class="tag tag-tbl">产线</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>
          </div>'''

new_tables = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">DispatchHistory</span> <span
              class="tag tag-tbl">发料历史</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span>
          </div>'''

html = html.replace(old_tables, new_tables)

# DAL section
old_dal = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_ScrapOrderDAL</span> <span
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

new_dal = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_WeighingDAL</span> <span
              class="tag tag-bll">称重DAL</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">GetWeight / SaveWeight / GetDispatchHistoryByPage</div>'''

html = html.replace(old_dal, new_dal)

# Forms section
old_forms = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_AddScrapOrder</span> <span
              class="tag tag-form">报废单主页</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_ScrapOrder</span> <span
              class="tag tag-form">添加/编辑表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EditScrapOrder</span> <span
              class="tag tag-form">添加/编辑明细</span></div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">ESignature</span> <span
              class="tag tag-form">电子签名(送审)</span></div>'''

new_forms = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_IssueMaterial_Weighting</span> <span
              class="tag tag-form">原料称重 1497×396</span></div>'''

html = html.replace(old_forms, new_forms)

# Source note
old_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_AddScrapOrder.cs /
        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确</div>'''

new_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_IssueMaterial_Weighting.cs / .Designer.cs<br>groupBox1(皮重) · groupBox2(净重) · groupBox3(称重机) · groupBox4(语音) · WeightBar</div>'''

html = html.replace(old_src, new_src)

# ── 6. Remove modals (scrap-order dialogs) ──
# Remove from <!-- ═══════ Modal: frmME_ScrapOrder to the end of the last modal -->
modal_start = html.find('<!-- ═══════ Modal: frmME_ScrapOrder')
script_start = html.find('<script>')

if modal_start != -1 and script_start != -1:
    # Keep only the script section
    html = html[:modal_start] + '\n  ' + html[script_start:]

# ── 7. Replace JavaScript field lineage map ──
# Find the map block: from "const map = {" to the matching "};"
map_start = html.find('const map = {')
if map_start != -1:
    # Count braces to find matching closing brace
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
                map_end = i + 1  # include the }
                break
    
    if map_end != -1:
        new_js_map = """    // ═══════ 字段血缘 Map (原料称重) ═══════
    const map = {
      // === 称重机选择 ===
      cmbEquipList: ['称重机', 'EquipmentList', 'ComboBox 295×35', ['Equipment→cmbEquipList']],
      // === 语音选择 ===
      cmbVoice: ['语音', '(本地设置)', 'ComboBox 295×35', ['VoiceConfig→cmbVoice']],
      // === 皮重信息 groupBox1 ===
      SkinWeight: ['皮重值', 'Weighing.SkinWeight', 'TextBox 280×75', ['电子秤→SkinWeight'], '[自动]'],
      SkinWeightButton: ['皮重称重按钮', 'Button.Click→ReadScale()', 'Button 142×77', ['WeightingForm→SkinWeightButton']],
      RemoveSkinWeightButton: ['去皮重按钮', 'Button.Click→ClearSkin()', 'Button 142×77', ['WeightingForm→RemoveSkinWeightButton']],
      // === 净重信息 groupBox2 ===
      NetWeight: ['净重值', 'Weighing.NetWeight', 'TextBox 280×75', ['电子秤→NetWeight'], '[自动]'],
      GrossWeight: ['毛重值', 'SkinWeight + NetWeight', 'TextBox(ReadOnly) 280×75', ['计算: 皮重+净重'], '[自动]'],
      WeightButton: ['净重称重按钮', 'Button.Click→ReadScale()', 'Button 142×77', ['WeightingForm→WeightButton']],
      btnRefresh: ['刷新按钮', 'Button.Click→Refresh()', 'Button 142×77', ['WeightingForm→btnRefresh']],
      // === 进度条标签 ===
      MaxValueLabel: ['上限值', 'Weighing.UpperLimit', 'Label', ['WeighingConfig→MaxValueLabel'], '[自动]'],
      StdValueLabel: ['标准值', 'Weighing.StdValue', 'Label', ['WeighingConfig→StdValueLabel'], '[自动]'],
      MinValueLabel: ['下限值', 'Weighing.LowerLimit', 'Label', ['WeighingConfig→MinValueLabel'], '[自动]'],
    };"""
        html = html[:map_start] + new_js_map + html[map_end:]
        print(f"  Map replaced: {map_start} → {map_end}")
    else:
        print("  WARNING: Could not find map closing brace")
else:
    print("  WARNING: Could not find 'const map = {'")

# ── 8. Update toast interaction messages ──
html = html.replace("'数据已保存 (报废单)'", "'数据已保存 (原料称重)'")
html = html.replace("'报废单查询成功！'", "'称重数据读取成功！'")

# ── Write output ──
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-template.html rebuilt successfully!")
print(f"   File size: {len(html)} bytes")
