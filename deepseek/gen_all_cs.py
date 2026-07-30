import os, re

base_cs = r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution'
base_out = r'E:\code\scal-pda-f\workspace\deepseek'
tpl_path = os.path.join(base_out, 'demo-cs-scrap-order.html')

with open(tpl_path, 'r', encoding='utf-8') as f:
    tpl = f.read()

css = tpl[tpl.find('<style>'):tpl.find('</style>')+len('</style>')]
nav_start = tpl.find('<div class="left">')
nav_end = tpl.find('</div>', tpl.find('<div class="right">'))
sidebar = tpl[nav_start:tpl.find('</div>', nav_end)+6]
toast_start = tpl.find('<!-- ═══════ Toast -->')
card_script = tpl[toast_start:]

def parse_designer(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    result = {}
    m = re.search(r'this\.ClientSize\s*=\s*new\s+System\.Drawing\.Size\s*\((\d+)\s*,\s*(\d+)\)', c)
    result['size'] = f"{m.group(1)}\u00d7{m.group(2)}" if m else '?'
    docks = {}
    for m in re.finditer(r'this\.(\w+)\.Dock\s*=\s*System\.Windows\.Forms\.DockStyle\.(\w+)', c):
        docks[m.group(1)] = m.group(2)
    result['has_dock'] = len(docks) > 0
    sizes = {}
    for m in re.finditer(r'this\.(\w+)\.Size\s*=\s*new\s+System\.Drawing\.Size\s*\((\d+)\s*,\s*(\d+)\)', c):
        sizes[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    locs = {}
    for m in re.finditer(r'this\.(\w+)\.Location\s*=\s*new\s+System\.Drawing\.Point\s*\((\d+)\s*,\s*(\d+)\)', c):
        locs[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    ctors = {}
    for m in re.finditer(r'this\.(\w+)\s*=\s*new\s+(\S+)\s*\(\)', c):
        ctors[m.group(1)] = m.group(2).split('.')[-1]
    texts = {}
    for m in re.finditer(r'this\.(\w+)\.Text\s*=\s*"([^"]*)"', c):
        texts[m.group(1)] = m.group(2)
    readonly = set()
    for m in re.finditer(r'this\.(\w+)\.ReadOnly\s*=\s*true', c):
        readonly.add(m.group(1))
    headers = {}
    for m in re.finditer(r'this\.(\w+)\.HeaderText\s*=\s*"([^"]*)"', c):
        headers[m.group(1)] = m.group(2)
    hierarchy = {}
    for m in re.finditer(r'this\.(\w+)\.Controls\.Add\(this\.(\w+)\)', c):
        parent, child = m.groups()
        if parent not in hierarchy: hierarchy[parent] = []
        hierarchy[parent].append(child)
    result['docks'] = docks; result['sizes'] = sizes; result['locs'] = locs
    result['ctors'] = ctors; result['texts'] = texts; result['readonly'] = readonly
    result['headers'] = headers; result['hierarchy'] = hierarchy
    cols_by_grid = {}
    for m in re.finditer(r'this\.(\w+)\.Columns\.AddRange\(new\s+System\.Windows\.Forms\.DataGridViewColumn\[\]\s*\{(.*?)\}\)', c, re.DOTALL):
        grid_name = m.group(1)
        col_names = re.findall(r'this\.(\w+)', m.group(2))
        cols = [{'name': cn, 'header': headers.get(cn, cn.replace(grid_name+'_', ''))} for cn in col_names]
        if cols: cols_by_grid[grid_name] = cols
    result['grids'] = cols_by_grid
    buttons = []
    for name, ctype in ctors.items():
        if 'Button' in ctype:
            l = locs.get(name, (0,0)); s = sizes.get(name, (0,0)); txt = texts.get(name, '')
            if txt: buttons.append({'name': name, 'text': txt, 'loc': l, 'size': s})
    result['buttons'] = sorted(buttons, key=lambda b: (b['loc'][1], b['loc'][0]))
    fields = []
    for name, ctype in ctors.items():
        if any(t in ctype for t in ['TextBox', 'Combo', 'DateTime', 'ComboGrid']):
            l = locs.get(name, (0,0)); s = sizes.get(name, (0,0))
            fields.append({'name': name, 'type': ctype, 'loc': l, 'size': s, 'readonly': name in readonly})
    result['fields'] = sorted(fields, key=lambda f: (f['loc'][1], f['loc'][0]))
    return result, locs, ctors, texts, readonly

def find_label(field, locs, ctors, texts):
    fx, fy = field['loc']
    for name, (lx, ly) in locs.items():
        if 'Label' in ctors.get(name,'') and abs(ly - fy) <= 5 and lx < fx:
            return texts.get(name, '')
    return field['name'].replace('TextArea_','').replace('SearchArea_','').replace('txt','').replace('_',' ')

def input_html(f, locs, ctors, texts, w_override=0):
    lbl = find_label(f, locs, ctors, texts)
    ro = f['readonly']
    tag = '[自动]' if ro else '[输入]'
    tc = '#888' if ro else '#2563eb'
    bg = 'background:#F5F5F5' if ro else ''
    ra = 'readonly' if ro else ''
    w = w_override if w_override else (f['size'][0] if f['size'][0] > 0 else 180)
    h = f['size'][1] if f['size'][1] > 0 else 28
    hs = f'height:{h}px' if h != 28 else 'height:28px'
    return f'<label style="font:9pt \'微软雅黑\';white-space:nowrap">{lbl}：<span style="font-size:7pt;color:{tc}">{tag}</span></label>\n<input data-k="{f["name"]}" {ra} style="width:{w}px;{hs};font:9pt \'微软雅黑\';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px;{bg}">'

def build_page(data, locs, ctors, texts, readonly, pinfo):
    h = ''
    has_dock = data['has_dock']
    
    if has_dock:
        tc = None
        for n, d in data['docks'].items():
            if d == 'Fill' and data['sizes'].get(n, (0,0))[0] > 1000: tc = n; break
        if not tc and data['docks']: tc = list(data['docks'].keys())[0]
        topp = data['hierarchy'].get(tc, []) if tc else []
        
        sp = None
        for pn in topp:
            ch = data['hierarchy'].get(pn, [])
            if any('Button' in data['ctors'].get(c,'') for c in ch) and any(any(t in data['ctors'].get(c,'') for t in ['TextBox','Combo']) for c in ch):
                sp = pn; break
        
        def all_children(name):
            r = []
            for c in data['hierarchy'].get(name, []):
                r.append(c); r.extend(all_children(c))
            return r
        
        for pn in topp:
            dock = data['docks'].get(pn, 'None')
            if dock != 'Top': continue
            sz = data['sizes'].get(pn, (0,0))
            ac = all_children(pn)
            pb = [b for b in data['buttons'] if b['name'] in ac]
            pf = [f for f in data['fields'] if f['name'] in ac]
            pg = [g for g in data['grids'] if g in ac]
            
            if pn == sp:
                h += f'<div class="blk"><div class="blk-hd">查询 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">{pn} {sz[0]}x{sz[1]}</span></div>'
                h += '<div class="blk-bd" style="padding:4px 8px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">'
                for f in pf: h += input_html(f, locs, ctors, texts)
                for b in pb:
                    pr = b['text'] in ['查询','启动','产出','称重','确认','开始作业','下一步','结案']
                    cl = 'btn primary' if pr else 'btn'
                    h += f'<button class="{cl}" data-k="{b["name"]}" style="width:{b["size"][0]}px;height:{b["size"][1]}px;font:12pt \'微软雅黑\'">{b["text"]}</button>'
                h += '</div></div>'
            elif pg:
                for gn in pg:
                    cols = data['grids'][gn]
                    h += f'<div class="blk"><div class="blk-hd">列表 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">{gn} {sz[0]}x{sz[1]}, {len(cols)}列</span></div>'
                    h += '<div class="grid-wrap" style="min-height:60px;max-height:250px"><table class="grid"><thead><tr>'
                    for col in cols: h += f'<th>{col["header"]}</th>'
                    h += '</tr></thead><tbody><tr>'
                    for col in cols: h += f'<td data-k="g_{col["name"]}">\u2014</td>'
                    h += '</tr></tbody></table></div></div>'
            elif pf:
                h += f'<div class="blk"><div class="blk-hd">详细信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">{pn} {sz[0]}x{sz[1]}, {len(pf)}字段</span></div>'
                h += '<div class="blk-bd" style="padding:4px 8px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px 12px">'
                for f in pf:
                    lbl = find_label(f, locs, ctors, texts)
                    ro = f['readonly']; tag = '[自动]' if ro else '[输入]'; tc = '#888' if ro else '#2563eb'
                    bg = 'background:#F5F5F5' if ro else ''; ra = 'readonly' if ro else ''
                    h += f'<div style="display:flex;align-items:center;gap:4px"><label style="font:9pt \'微软雅黑\';width:80px">{lbl}：<span style="font-size:7pt;color:{tc}">{tag}</span></label><input data-k="{f["name"]}" {ra} style="flex:1;height:28px;font:9pt \'微软雅黑\';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px;{bg}"></div>'
                h += '</div></div>'
            elif pb:
                h += f'<div class="blk"><div class="blk-hd">{pn} <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">{sz[0]}x{sz[1]}</span></div>'
                h += '<div class="blk-bd" style="padding:4px 8px;display:flex;gap:6px">'
                for b in pb:
                    pr = b['text'] in ['查询','启动','产出','称重','确认','开始作业','下一步','净重称重','皮重称重','去皮重','刷新']
                    cl = 'btn primary' if pr else 'btn'
                    h += f'<button class="{cl}" data-k="{b["name"]}" style="width:{b["size"][0]}px;height:{b["size"][1]}px;font:12pt \'微软雅黑\'">{b["text"]}</button>'
                h += '</div></div>'
    else:
        # Simple flat form
        if data['buttons']:
            h += f'<div class="blk"><div class="blk-hd">操作 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">Form {data["size"]}</span></div>'
            h += '<div class="blk-bd" style="padding:4px 8px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">'
            for b in data['buttons']:
                pr = b['text'] in ['查询','启动','产出','称重','确认','开始作业','下一步','净重称重','皮重称重','去皮重','刷新']
                cl = 'btn primary' if pr else 'btn'
                h += f'<button class="{cl}" data-k="{b["name"]}" style="width:{b["size"][0]}px;height:{b["size"][1]}px;font:12pt \'微软雅黑\'">{b["text"]}</button>'
            h += '</div></div>'
        if data['fields']:
            rows = {}
            for f in data['fields']:
                rk = f['loc'][1] // 10
                if rk not in rows: rows[rk] = []
                rows[rk].append(f)
            for rk in sorted(rows.keys()):
                rf = sorted(rows[rk], key=lambda f: f['loc'][0])
                h += '<div class="blk"><div class="blk-hd">字段</div>'
                h += '<div class="blk-bd" style="padding:4px 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">'
                for f in rf: h += input_html(f, locs, ctors, texts)
                h += '</div></div>'
        for gn, cols in data['grids'].items():
            h += f'<div class="blk"><div class="blk-hd">列表 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">{gn} {len(cols)}列</span></div>'
            h += '<div class="grid-wrap" style="min-height:60px;max-height:250px"><table class="grid"><thead><tr>'
            for col in cols: h += f'<th>{col["header"]}</th>'
            h += '</tr></thead><tbody><tr>'
            for col in cols: h += f'<td data-k="g_{col["name"]}">\u2014</td>'
            h += '</tr></tbody></table></div></div>'
    return h

def build_stats(pinfo):
    tables = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-tbl">{t[1]}</span></div>' for t in pinfo.get('tables',[]))
    sps = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-sp">{t[1]}</span></div>' for t in pinfo.get('sps',[]))
    if not pinfo.get('sps'): sps = '<div style="font-size:8pt;color:#888">DAL/WebAPI 直接操作</div>'
    dals = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-bll">{t[1]}</span></div>' for t in pinfo.get('dals',[]))
    forms = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-form">{t[1]}</span></div>' for t in pinfo.get('forms',[]))
    return f'''      <div class="sh">\U0001f4ca 调用统计<span class="tag tag-form" style="margin-left:4px">{pinfo['tag']}</span></div>
      <div class="ss"><h4>数据库表</h4><div style="font-size:8pt;line-height:1.7">{tables}</div></div>
      <div class="ss"><h4>存储过程</h4><div style="font-size:8pt;line-height:1.7">{sps}</div></div>
      <div class="ss"><h4>数据访问层</h4><div style="font-size:8pt;line-height:1.7">{dals}</div></div>
      <div class="ss"><h4>窗体</h4><div style="font-size:8pt;line-height:1.7">{forms}</div></div>
      <div class="src-note"><b>\u2705 源码验证：</b> {pinfo['cs_file']}.cs / .Designer.cs<br>Form {pinfo['size']}</div>'''

pages = {
    'demo-cs-pz-output.html': {'title':'配制产出 \u00b7 CS客户端','nav':'配制产出','tab':'配制产出','tag':'CS\u00b7配制产出','cs_file':'frmME_PZOutput','tables':[('Lot','批次'),('CurrentStatus','设备状态'),('MfgInWHOrder','入库单'),('MfgOrder','工单')],'sps':[('Pro_PZOutput_Packing_New','产出包装入库')],'dals':[('MESZZZX_PZOutputDAL','产出DAL')],'forms':[('frmME_PZOutput','配制产出主页')]},
    'demo-cs-equipment-start.html': {'title':'设备启动 \u00b7 CS客户端','nav':'配制罐清洗启动','tab':'设备启动','tag':'CS\u00b7设备启动','cs_file':'frmME_EquipmentStart','tables':[('BPREquipmentHistory','设备历史'),('CurrentStatus','设备状态'),('MfgOrder','工单')],'sps':[],'dals':[('MESZZZX_EquipmentStartDAL','设备启动DAL')],'forms':[('frmME_EquipmentStart','设备启动主页')]},
    'demo-cs-weighing-test.html': {'title':'称重调试 \u00b7 CS客户端','nav':'称重调试','tab':'称重调试','tag':'CS\u00b7称重调试','cs_file':'frmME_WeightingTest','tables':[('WeighingHistory','称重历史'),('Lot','批次')],'sps':[],'dals':[('MESZZZX_WeighingDAL','称重DAL')],'forms':[('frmME_WeightingTest','称重调试主页')]},
    'demo-cs-surplus-material.html': {'title':'余料称重 \u00b7 CS客户端','nav':'余料称重','tab':'余料称重','tag':'CS\u00b7余料称重','cs_file':'frmME_SurplusMaterial','tables':[('DispatchHistory','发料历史'),('SurplusMaterialList','余料列表'),('Lot','批次')],'sps':[],'dals':[('MESZZZX_SurplusMaterialDAL','余料DAL')],'forms':[('frmME_SurplusMaterial','余料称重主页')]},
    'demo-cs-bpr-record.html': {'title':'BPR作业 \u00b7 CS客户端','nav':'BPR作业','tab':'BPR作业','tag':'CS\u00b7BPR作业','cs_file':'frmME_BPRRecord','tables':[('BPRStartHistory','BPR启动'),('BPREquipmentHistory','设备历史'),('MfgOrder','工单')],'sps':[],'dals':[('CKZY_BPRStartQueryBLL','BPR查询BLL')],'forms':[('frmME_BPRRecord','BPR作业主页')]},
    'demo-cs-template.html': {'title':'原料称重 \u00b7 CS客户端','nav':'原料称重','tab':'原料称重','tag':'CS\u00b7原料称重','cs_file':'frmME_IssueMaterial_Weighting','tables':[('DispatchHistory','发料历史'),('Lot','批次')],'sps':[],'dals':[('MESZZZX_WeighingDAL','称重DAL')],'forms':[('frmME_IssueMaterial_Weighting','原料称重主页')]},
}

designer_map = {
    'frmME_PZOutput':'frmME_PZOutput.Designer.cs',
    'frmME_EquipmentStart':'frmME_EquipmentStart.Designer.cs',
    'frmME_WeightingTest':'frmME_WeightingTest.Designer.cs',
    'frmME_SurplusMaterial':'frmME_SurplusMaterial.Designer.cs',
    'frmME_BPRRecord':'frmME_BPRRecord.Designer.cs',
    'frmME_IssueMaterial_Weighting':'frmME_IssueMaterial_Weighting.Designer.cs',
}

for fname, pinfo in pages.items():
    cs_file = pinfo['cs_file']; designer_file = designer_map.get(cs_file)
    if not designer_file: continue
    dpath = os.path.join(base_cs, designer_file)
    if not os.path.exists(dpath): print(f'SKIP {fname}'); continue
    print(f'{fname} ({cs_file})...')
    data, locs, ctors, texts, readonly = parse_designer(dpath)
    pinfo['size'] = data['size']
    panels_html = build_page(data, locs, ctors, texts, readonly, pinfo)
    nav = sidebar.replace('<div class="tree-item sel">报废单</div>', f'<div class="tree-item sel">{pinfo["nav"]}</div>')
    html = f'<!DOCTYPE html>\n<html lang="zh-CN">\n<head><meta charset="utf-8"><title>{pinfo["title"]}</title>\n{css}\n</head>\n<body>\n  <div style="display:flex;gap:8px">\n    <div class="win">\n      <div class="topbar">\n        <div class="logo">MES 制造执行系统</div>\n        <div class="info"><span>\U0001f4c5 2026-07-29</span><span class="time">14:30:00</span><span>星期三</span><span>| 系统连接：正常</span></div>\n        <span class="ver">当前版本：3.0.5.74</span><span class="user">\U0001f464 超级管理员</span>\n      </div>\n      <div class="body">\n        {nav}\n        <div class="right">\n          <div class="tabs"><div class="tab">首页</div><div class="tab sel">{pinfo["tab"]}</div></div>\n          <div class="content">\n{panels_html}\n          </div>\n        </div>\n      </div>\n    </div>\n    <div class="stats">\n{build_stats(pinfo)}\n    </div>\n  </div>\n{card_script}\n</body>\n</html>'
    with open(os.path.join(base_out, fname), 'w', encoding='utf-8') as f: f.write(html)
    print(f'  OK')

print('Done!')
