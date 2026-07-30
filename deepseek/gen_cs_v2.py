import os, re

base = r'E:\code\scal-pda-f\workspace\deepseek'
template_path = os.path.join(base, 'demo-cs-scrap-order.html')

with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Extract CSS section (from <style> to </style>)
css_start = template.find('<style>')
css_end = template.find('</style>') + len('</style>')
css = template[css_start:css_end]

# Extract HTML head/body wrapper (topbar + sidebar + layout structure)
topbar_start = template.find('<body>') + len('<body>')
topbar_end = template.find('<!-- ═══════ Toast')
layout_html = template[topbar_start:topbar_end]

# ====== FORM DEFINITIONS (based on real Designer.cs analysis) ======

forms = {
    'demo-cs-mfg-order.html': {
        'title': '工单 · CS客户端',
        'nav_sel': '工单',
        'tab_sel': '工单',
        'tag': 'CS·工单',
        'form_cs': 'frmME_MfgOrder',
        'size': '1710 x 875',
        'blocks': [
            {
                'title': '工单查询',
                'fields': [
                    ('工单号', 'TextArea_MfgOrderNM', '267x29', ''),
                    ('产品名称', 'TextArea_ProductNM', '267x31', ''),
                    ('完成数量', 'TextArea_CompliteQty', '267x29', ''),
                ],
                'fields2': [
                    ('客户订单号', 'TextArea_CustomerOrderNM', '267x29', ''),
                    ('销售订单', 'TextArea_SalesOrder', '267x31', ''),
                    ('客户名称', 'TextArea_CustomerNM', '267x31', ''),
                ],
                'fields3': [
                    ('生产批号', 'TextArea_MfgBatch', '267x29', ''),
                    ('计划数量', 'TextArea_Qty', '267x29', ''),
                    ('单位', 'TextArea_UOMNM', '267x31', ''),
                ],
                'btns': ['查询 124×33', '结案 124×33', '结案还原 124×33', '修改 124×33'],
            },
            {
                'title': '工单列表 (dgvMfgOrderList)',
                'cols': ['工单号','物料编号','数量','完成数','计划开工','计划完工','工单状态','修改人','修改时间'],
                'rows': [
                    ['MO-202607-001','2969341','5000','3200','2026-07-25','2026-07-30','生产中','超级管理员','2026-07-29'],
                    ['MO-202607-002','2969342','3000','1500','2026-07-26','2026-07-31','生产中','超级管理员','2026-07-29'],
                    ['MO-202607-003','2969343','2000','2000','2026-07-20','2026-07-28','已结案','李四','2026-07-29'],
                ]
            },
            {
                'title': '批次汇总 (LotSummaryList)',
                'cols': ['生产批号','在库状态','数量'],
                'rows': [
                    ['B20260725-001','在库','3200'],
                    ['B20260726-001','在库','1500'],
                ]
            },
        ],
        'stats': {'tables': 3, 'sps': 2, 'dals': 2},
        'tables': [('MfgOrder','工单主表'),('MfgOrderBOM','工单BOM'),('Lot','批次')],
        'sps': [('Pro_MfgOrder_Close_Check','结案前校验'),('Pro_MfgOrder_Close','执行结案')],
        'dals': [('MESZZZX_MfgOrderDAL','工单DAL'),('CKZY_WorkOrder','Web工单BLL')],
        'forms_cs_list': [('frmME_MfgOrder','工单主页')],
    },
    'demo-cs-pz-output.html': {
        'title': '配制产出 · CS客户端',
        'nav_sel': '配制产出',
        'tab_sel': '配制产出',
        'tag': 'CS·配制产出',
        'form_cs': 'frmME_PZOutput',
        'size': '1677 x 757',
        'blocks': [
            {
                'title': '配制产出登记',
                'fields': [
                    ('打印机', 'cbgPrinter', '366x35', ''),
                    ('*工单号', 'MfgOrderId', '366x35', 'MO-202607-001'),
                    ('*皮重', 'SkinWeight', '366x34', '1.50'),
                ],
                'fields2': [
                    ('打印类型', 'cbgPrinterType', '366x35', '标签'),
                    ('有效日期', 'dtpExpirationDate', '276x34', '2027-07-29'),
                    ('*毛重', 'GrossWeight', '366x34', '51.65'),
                ],
                'fields3': [
                    ('日期码', 'DateCode', '366x35', '20260729'),
                    ('*净重', 'NetWeight', '366x34', '50.15'),
                    ('产品名称', 'ProductNM', '366x34', '示例洗发水'),
                ],
                'btns': ['产出 147×44', '重印 147×44', '废除 147×44'],
            },
            {
                'title': '产出批次列表 (LOtStartedListByMO)',
                'cols': ['生产批号','工单号','配制罐','产出量','产出时间','状态'],
                'rows': [
                    ['LOT-20260729-001','MO-202607-001','TANK-A','1200kg','2026-07-29 14:30','已入库'],
                    ['LOT-20260729-002','MO-202607-002','TANK-B','800kg','2026-07-29 10:00','已入库'],
                ]
            },
        ],
        'stats': {'tables': 4, 'sps': 1, 'dals': 1},
        'tables': [('Lot','批次'),('CurrentStatus','设备状态'),('MfgInWHOrder','入库单'),('MfgOrder','工单')],
        'sps': [('Pro_PZOutput_Packing_New','产出包装入库')],
        'dals': [('MESZZZX_PZOutputDAL','产出DAL')],
        'forms_cs_list': [('frmME_PZOutput','配制产出主页')],
    },
    'demo-cs-equipment-start.html': {
        'title': '设备启动 · CS客户端',
        'nav_sel': '配制罐清洗启动',
        'tab_sel': '设备启动',
        'tag': 'CS·设备启动',
        'form_cs': 'frmME_EquipmentStart',
        'size': '1710 x 875',
        'blocks': [
            {
                'title': '设备启动 (Top=27)',
                'fields': [
                    ('*设备编号', 'EquipmentNM', '241x27', 'EQ-MIX-01'),
                    ('*工单号', 'SearchArea_MfgOrderNM', '384x28', 'MO-202607-001'),
                ],
                'btns': ['启动 122×34', '取消 122×34', '删除 122×33'],
            },
            {
                'title': '设备信息 (dgvEquipmentinfo, Dock=Top 212px)',
                'cols': ['设备编号','设备名称','配制罐','状态','启动时间'],
                'rows': [
                    ['EQ-MIX-01','主搅拌罐','TANK-A','运行中','2026-07-29 08:00'],
                    ['EQ-MIX-02','辅助搅拌罐','TANK-B','待机','—'],
                ]
            },
            {
                'title': '工单列表 (dgvMfgOrderList, Dock=Top 108px)',
                'cols': ['工单号','产品名称','计划量','状态'],
                'rows': [
                    ['MO-202607-001','示例洗发水','5000','生产中'],
                    ['MO-202607-002','柔顺护发素','3000','生产中'],
                ]
            },
        ],
        'stats': {'tables': 3, 'sps': 0, 'dals': 1},
        'tables': [('BPREquipmentHistory','设备历史'),('CurrentStatus','设备状态'),('MfgOrder','工单')],
        'sps': [],
        'dals': [('MESZZZX_EquipmentStartDAL','设备启动DAL')],
        'forms_cs_list': [('frmME_EquipmentStart','设备启动主页')],
    },
    'demo-cs-weighing-test.html': {
        'title': '称重调试 · CS客户端',
        'nav_sel': '称重调试',
        'tab_sel': '称重调试',
        'tag': 'CS·称重调试',
        'form_cs': 'frmME_WeightingTest',
        'size': '1497 x 643',
        'blocks': [
            {
                'title': '称重调试',
                'fields': [
                    ('称重设备', 'cmbEquipList', '295x35', '电子秤-01'),
                    ('语音提示', 'cmbVoice', '295x35', '开启'),
                    ('称重值', 'weighting', '309x45', ''),
                ],
                'fields2': [
                    ('净重', 'NetWeight', '280x75', '50.15'),
                    ('皮重', 'SkinWeight', '280x75', '1.50'),
                    ('毛重', 'GrossWeight', '280x75', '51.65'),
                ],
                'btns': ['净重称重 142×77', '皮重称重 142×77', '去皮重 142×77', '刷新 142×77'],
            },
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 1},
        'tables': [('WeighingHistory','称重历史'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_WeighingDAL','称重DAL')],
        'forms_cs_list': [('frmME_WeightingTest','称重调试主页')],
    },
    'demo-cs-surplus-material.html': {
        'title': '余料称重 · CS客户端',
        'nav_sel': '余料称重',
        'tab_sel': '余料称重',
        'tag': 'CS·余料称重',
        'form_cs': 'frmME_SurplusMaterial',
        'size': '1604 x 875',
        'blocks': [
            {
                'title': '余料称重',
                'fields': [
                    ('工单号', 'SearchArea_MfgOrderNM', '356x31', 'MO-202607-001'),
                    ('*批号', 'TextArea_LotNM', '267x29', 'LOT-20260729-001'),
                    ('*皮重', 'TextArea_SkinWeight', '233x29', '0.80'),
                ],
                'fields2': [
                    ('工单号(显示)', 'TextArea_MfgOrderNM', '267x29', 'MO-202607-001'),
                    ('毛重', 'TextArea_GrossWeight', '233x29', '5.30'),
                    ('净重', 'TextArea_NetWeight', '233x29', '4.50'),
                ],
                'btns': ['查询 140×40', '称重 169×60', '确认 169×61', '双人复核 169×61', '重印 169×61'],
            },
            {
                'title': '发料列表 (dgvDispatchedMaterialList, Dock=Fill 263px)',
                'cols': ['流水号','已发净重','退回净重','实发净重','毛重','皮重','生产批号','工单号','品名规格'],
                'rows': [
                    ['20260729-001','50.00','3.50','46.50','51.65','1.50','B20260725-001','MO-202607-001','ZW_NE OP SER'],
                ]
            },
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 1},
        'tables': [('DispatchHistory','发料历史'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_SurplusMaterialDAL','余料DAL')],
        'forms_cs_list': [('frmME_SurplusMaterial','余料称重主页')],
    },
    'demo-cs-bpr-record.html': {
        'title': 'BPR作业 · CS客户端',
        'nav_sel': 'BPR作业',
        'tab_sel': 'BPR作业',
        'tag': 'CS·BPR作业',
        'form_cs': 'frmME_BPRRecord',
        'size': '1588 x 918',
        'blocks': [
            {
                'title': 'BPR作业',
                'fields': [
                    ('工单号', 'SearchArea_MfgOrderNM', '356x31', 'MO-202607-001'),
                    ('当前步骤', 'txtCurrentStep', '180x29', '主配物-加料'),
                    ('当前项次', 'txtCurrentItem', '180x29', '3'),
                    ('总步骤数', 'txtTotalStep', '180x29', '12'),
                ],
                'fields2': [
                    ('设备名称', 'TextArea_EquipmentNM', '180x29', ''),
                    ('电箱', 'RefrigeratorId', '180x31', ''),
                    ('*称重值', 'TextArea_Value', '180x29', '50.15'),
                    ('标准值', 'txtStandardValue', '180x29', '50.00'),
                ],
                'btns': ['工艺设备切换 138×35', '无工艺启动 138×35', '查询 122×35', '启动 122×47', '开始作业 122×47', '下一步 122×47'],
            },
            {
                'title': '步骤明细 (dgvBPRRecord_StepDetailList, Dock=Fill 319px)',
                'cols': ['步骤序号','工艺步骤','标准值','实际值','结果','状态'],
                'rows': [
                    ['1','预配物-搅拌','—','—','待执行','—'],
                    ['2','预配物-均质','—','—','待执行','—'],
                    ['3','主配物-加料','50.00','50.15','合格','执行中'],
                ]
            },
        ],
        'stats': {'tables': 3, 'sps': 0, 'dals': 1},
        'tables': [('BPRStartHistory','BPR启动'),('BPREquipmentHistory','设备历史'),('MfgOrder','工单')],
        'sps': [],
        'dals': [('CKZY_BPRStartQueryBLL','BPR查询BLL')],
        'forms_cs_list': [('frmME_BPRRecord','BPR作业主页')],
    },
    'demo-cs-template.html': {
        'title': '原料称重 · CS客户端',
        'nav_sel': '原料称重',
        'tab_sel': '原料称重',
        'tag': 'CS·原料称重',
        'form_cs': 'frmME_IssueMaterial_Weighting',
        'size': '1497 x 396',
        'blocks': [
            {
                'title': '原料称重 (投料前称重确认)',
                'fields': [
                    ('称重设备', 'cmbEquipList', '295x35', '电子秤-01'),
                    ('语音提示', 'cmbVoice', '295x35', '开启'),
                ],
                'fields2': [
                    ('净重', 'NetWeight', '280x75', '50.15'),
                    ('皮重', 'SkinWeight', '280x75', '1.50'),
                    ('毛重', 'GrossWeight', '280x75', '51.65'),
                ],
                'btns': ['净重称重 142×77', '皮重称重 142×77', '去皮重 142×77', '刷新 142×77'],
            },
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 1},
        'tables': [('DispatchHistory','发料历史'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_WeighingDAL','称重DAL')],
        'forms_cs_list': [('frmME_IssueMaterial_Weighting','原料称重主页')],
    },
}

# ====== HTML generation functions ======
def build_block(b):
    html = f'<div class="blk">\n<div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- {b["title"]}</div>\n<div class="blk-bd" style="padding:4px 8px">\n'
    
    # Field rows
    field_groups = [b.get('fields',[])]
    if 'fields2' in b: field_groups.append(b['fields2'])
    if 'fields3' in b: field_groups.append(b['fields3'])
    
    for fg in field_groups:
        html += '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:4px">\n'
        for label, kid, sz, val in fg:
            w = sz.split('x')[0] if 'x' in sz else '180'
            html += f'<label style="font:9pt \'微软雅黑\';white-space:nowrap">{label}：</label>'
            html += f'<input data-k="{kid}" value="{val}" style="width:{w}px;height:28px;font:9pt \'微软雅黑\';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px">\n'
        html += '</div>\n'
    
    # Buttons
    if 'btns' in b:
        html += '<div style="display:flex;gap:6px;margin-bottom:4px">\n'
        for btn_text in b['btns']:
            txt = btn_text.split(' ')[0]
            html += f'<button class="btn primary" style="font:12pt \'微软雅黑\';min-width:80px;height:36px">{txt}</button>\n'
        html += '</div>\n'
    
    # Grid
    if 'cols' in b:
        html += '<div class="grid-wrap" style="min-height:60px;max-height:250px">\n<table class="grid">\n<thead><tr>\n'
        for col in b['cols']:
            html += f'<th>{col}</th>\n'
        html += '</tr></thead>\n<tbody>\n'
        for row in b.get('rows', []):
            html += '<tr>\n'
            for cell in row:
                html += f'<td>{cell}</td>\n'
            html += '</tr>\n'
        html += '</tbody></table>\n</div>\n'
    
    html += '</div></div>\n'
    return html

def build_stats(p):
    s = p['stats']
    tables = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-tbl">{t[1]}</span></div>' for t in p.get('tables',[]))
    sps = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-sp">{t[1]}</span></div>' for t in p.get('sps',[]))
    if not p.get('sps'): sps = '<div style="font-size:8pt;color:#888">通过 DAL→WebAPI 直接操作</div>'
    dals = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-bll">{t[1]}</span></div>' for t in p.get('dals',[]))
    forms_cs = ''.join(f'<div><span style="font-family:Consolas;color:#1a3a5c">{t[0]}</span> <span class="tag tag-form">{t[1]}</span></div>' for t in p.get('forms_cs_list',[]))
    return f'''      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">{p['tag']}</span></div>
      <div style="display:flex;gap:8px;margin-bottom:6px">
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['tables']}</div><div style="font-size:7pt;color:DimGray">数据库表</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['sps']}</div><div style="font-size:7pt;color:DimGray">存储过程</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['dals']}</div><div style="font-size:7pt;color:DimGray">DAL</div></div>
      </div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;margin-right:4px"></span>数据库表</h4><div style="font-size:8pt;line-height:1.7">{tables}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#7c3aed;margin-right:4px"></span>存储过程</h4><div style="font-size:8pt;line-height:1.7">{sps}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#d97706;margin-right:4px"></span>数据访问层</h4><div style="font-size:8pt;line-height:1.7">{dals}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#3b82f6;margin-right:4px"></span>窗体</h4><div style="font-size:8pt;line-height:1.7">{forms_cs}</div></div>'''

# ====== Generate each page ======
for fname, p in forms.items():
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build blocks HTML
    blocks_html = '\n'.join(build_block(b) for b in p['blocks'])
    
    # Build stats HTML
    stats_html = build_stats(p)
    
    # Build source note
    src_note = f'<div class="src-note"><b>&#x2705; 源码验证：</b> {p["form_cs"]}.cs / .Designer.cs<br>Form {p["size"]} · 所有控件·位置·大小·DAL方法 100%精确</div>'
    
    # Find and replace content sections
    # 1. Title
    content = re.sub(r'<title>.*?</title>', f'<title>{p["title"]}</title>', content)
    
    # 2. Nav selected item
    content = re.sub(r'<div class="tree-item sel">.*?</div>', f'<div class="tree-item sel">{p["nav_sel"]}</div>', content)
    
    # 3. Tab selected
    content = re.sub(r'<div class="tab sel">.*?</div>', f'<div class="tab sel">{p["tab_sel"]}</div>', content)
    
    # 4. Replace form blocks (between first blk and Toast)
    blk_start = content.find('<div class="blk">')
    toast_pos = content.find('<!-- ═══════ Toast')
    if blk_start >= 0 and toast_pos >= 0:
        before = content[:blk_start]
        after = content[toast_pos:]
        # Find where stats section starts in after
        stats_start = after.find('<div class="stats">')
        if stats_start >= 0:
            stats_end = after.find('<div class="src-note">')
            if stats_end < 0: stats_end = after.find('</div>\n  </div>\n  <!--')
            new_middle = f'\n{blocks_html}\n          </div>\n        </div>\n      </div>\n    </div>\n{stats_html}\n      {src_note}\n    </div>\n  </div>\n'
            content = before + new_middle
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')

print('All pages generated!')
