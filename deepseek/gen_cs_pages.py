import os, re

base = r'E:\code\scal-pda-f\workspace\deepseek'

# ====== Page definitions ======
pages = {
    'demo-cs-mfg-order.html': {
        'title': '工单',
        'nav': '工单',
        'tab': '工单',
        'tag': 'CS·工单',
        'form_cs': 'frmME_MfgOrder',
        'desc': '工单查询与管理',
        'blocks': [
            {'title': '工单查询', 'fields': [
                ('工单号', 'sMfgOrderNM', 'MO-202607-001'),
                ('产品名称', 'sProductNM', '示例洗发水'),
                ('状态', 'sStatus', '生产中'),
                ('日期', 'sDate', '2026-07-29'),
            ], 'btns': ['查询', '结案', '反结案']},
            {'title': '工单列表', 'cols': ['工单号','产品名称','工单状态','计划量','完成量','创建时间','结案时间','产线'],
             'rows': [
                ['MO-202607-001','示例洗发水','生产中','5000','3200','2026-07-25','—','产线A'],
                ['MO-202607-002','柔顺护发素','生产中','3000','1500','2026-07-26','—','产线B'],
                ['MO-202607-003','沐浴露','已结案','2000','2000','2026-07-20','2026-07-29','产线A'],
            ]},
        ],
        'stats': {'tables': 3, 'sps': 2, 'dals': 3},
        'tables': [('MfgOrder','工单主表'),('MfgOrderBOM','工单BOM'),('ProductLine','产线')],
        'sps': [('Pro_MfgOrder_Close_Check','结案前校验'),('Pro_MfgOrder_Close','执行结案')],
        'dals': [('MESZZZX_MfgOrderDAL','工单DAL')],
        'forms': [('frmME_MfgOrder','工单主页')],
    },
    'demo-cs-pz-output.html': {
        'title': '配制产出',
        'nav': '配制产出',
        'tab': '配制产出',
        'tag': 'CS·配制产出',
        'form_cs': 'frmME_PZOutput',
        'desc': '配制产出入库登记',
        'blocks': [
            {'title': '产出查询', 'fields': [
                ('工单号', 'sMfgOrderNM', 'MO-202607-001'),
                ('配制罐', 'sTankNO', 'TANK-A'),
                ('产出日期', 'sDate', '2026-07-29'),
            ], 'btns': ['查询', '添加产出', '打印标签']},
            {'title': '产出列表', 'cols': ['产出批号','工单号','配制罐','产出量','产出时间','创建人','状态'],
             'rows': [
                ['LOT-20260729-001','MO-202607-001','TANK-A','1200kg','2026-07-29 14:30','超级管理员','已入库'],
                ['LOT-20260729-002','MO-202607-002','TANK-B','800kg','2026-07-29 10:00','超级管理员','已入库'],
            ]},
        ],
        'stats': {'tables': 4, 'sps': 1, 'dals': 2},
        'tables': [('Lot','批次'),('CurrentStatus','设备状态'),('MfgInWHOrder','入库单'),('MfgOrder','工单')],
        'sps': [('Pro_PZOutput_Packing_New','产出包装')],
        'dals': [('MESZZZX_PZOutputDAL','产出DAL')],
        'forms': [('frmME_PZOutput','配制产出主页')],
    },
    'demo-cs-equipment-start.html': {
        'title': '设备启动',
        'nav': '配制罐清洗启动',
        'tab': '设备启动',
        'tag': 'CS·设备启动',
        'form_cs': 'frmME_EquipmentStart',
        'desc': '配制设备启动记录',
        'blocks': [
            {'title': '设备启动', 'fields': [
                ('工单号', 'sMfgOrderNM', 'MO-202607-001'),
                ('设备编号', 'sEquipmentNM', 'EQ-MIX-01'),
                ('配制罐', 'sTankNO', 'TANK-A'),
                ('启动时间', 'sStartTime', '2026-07-29 08:00'),
            ], 'btns': ['确认启动', '查询']},
            {'title': '启动记录', 'cols': ['设备编号','配制罐','工单号','启动时间','操作人','状态'],
             'rows': [
                ['EQ-MIX-01','TANK-A','MO-202607-001','2026-07-29 08:00','超级管理员','已启动'],
                ['EQ-MIX-02','TANK-B','MO-202607-002','2026-07-29 09:30','超级管理员','已启动'],
            ]},
        ],
        'stats': {'tables': 3, 'sps': 0, 'dals': 2},
        'tables': [('BPREquipmentHistory','设备历史'),('CurrentStatus','设备状态'),('MfgOrder','工单')],
        'sps': [],
        'dals': [('MESZZZX_EquipmentStartDAL','设备启动DAL')],
        'forms': [('frmME_EquipmentStart','设备启动主页')],
    },
    'demo-cs-weighing-test.html': {
        'title': '称重调试',
        'nav': '称重调试',
        'tab': '称重调试',
        'tag': 'CS·称重调试',
        'form_cs': 'frmME_WeightingTest',
        'desc': '称重设备调试与校验',
        'blocks': [
            {'title': '称重调试', 'fields': [
                ('批号', 'sLotNM', 'LOT-20260729-001'),
                ('物料名称', 'sMatNM', 'ZW_NE OP SER'),
                ('理论重量', 'sTheoryWt', '50.00'),
                ('实际重量', 'sActualWt', '50.15'),
            ], 'btns': ['称重', '保存', '取消']},
            {'title': '调试记录', 'cols': ['批号','物料名称','理论重量','实际重量','偏差%','时间','操作人'],
             'rows': [
                ['LOT-20260729-001','ZW_NE OP SER','50.00','50.15','0.3%','2026-07-29 11:00','超级管理员'],
                ['LOT-20260729-002','ZW_PH ADJUST','12.50','12.48','-0.2%','2026-07-29 11:05','超级管理员'],
            ]},
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 2},
        'tables': [('WeighingHistory','称重历史'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_WeighingDAL','称重DAL')],
        'forms': [('frmME_WeightingTest','称重调试主页')],
    },
    'demo-cs-surplus-material.html': {
        'title': '余料称重',
        'nav': '余料称重',
        'tab': '余料称重',
        'tag': 'CS·余料称重',
        'form_cs': 'frmME_SurplusMaterial',
        'desc': '余料退回称重登记',
        'blocks': [
            {'title': '余料称重', 'fields': [
                ('批号', 'sLotNM', 'LOT-20260729-001'),
                ('物料名称', 'sMatNM', 'ZW_NE OP SER'),
                ('余料重量', 'sSurplusWt', '3.50'),
                ('退回原因', 'sReason', '配料剩余'),
            ], 'btns': ['称重', '确认退回', '取消']},
            {'title': '余料记录', 'cols': ['批号','物料名称','余料重量','退回原因','时间','操作人','状态'],
             'rows': [
                ['LOT-20260729-001','ZW_NE OP SER','3.50','配料剩余','2026-07-29 15:00','超级管理员','已退回'],
                ['LOT-20260729-002','ZW_GLYCERIN','2.00','工艺调整','2026-07-29 15:30','李四','已退回'],
            ]},
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 2},
        'tables': [('SurplusMaterial','余料'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_SurplusMaterialDAL','余料DAL')],
        'forms': [('frmME_SurplusMaterial','余料称重主页')],
    },
    'demo-cs-bpr-record.html': {
        'title': 'BPR作业',
        'nav': 'BPR作业',
        'tab': 'BPR作业',
        'tag': 'CS·BPR作业',
        'form_cs': 'BPR操作界面',
        'desc': 'BPR工艺操作记录',
        'blocks': [
            {'title': 'BPR作业', 'fields': [
                ('工单号', 'sMfgOrderNM', 'MO-202607-001'),
                ('工艺步骤', 'sStep', '主配物-加料'),
                ('配制罐', 'sTankNO', 'TANK-A'),
            ], 'btns': ['开始作业', '跳步确认', '完成']},
            {'title': 'BPR记录', 'cols': ['工单号','工艺步骤','配制罐','开始时间','结束时间','操作人','状态'],
             'rows': [
                ['MO-202607-001','预配物-搅拌','TANK-A','2026-07-29 09:00','2026-07-29 09:30','超级管理员','已完成'],
                ['MO-202607-001','主配物-加料','TANK-A','2026-07-29 09:35','—','超级管理员','进行中'],
            ]},
        ],
        'stats': {'tables': 3, 'sps': 0, 'dals': 2},
        'tables': [('BPRStartHistory','BPR启动历史'),('BPREquipmentHistory','BPR设备历史'),('MfgOrder','工单')],
        'sps': [],
        'dals': [('CKZY_BPRStartQueryBLL','BPR查询BLL')],
        'forms': [('BPR作业页面','BS Web端')],
    },
    'demo-cs-template.html': {
        'title': '原料称重',
        'nav': '原料称重',
        'tab': '原料称重',
        'tag': 'CS·原料称重',
        'form_cs': 'frmME_IssueMaterial_Weighting',
        'desc': '投料前称重确认',
        'blocks': [
            {'title': '原料称重', 'fields': [
                ('批号', 'sLotNM', 'LOT-20260729-001'),
                ('物料名称', 'sMatNM', 'ZW_NE OP SER'),
                ('工单号', 'sMfgOrderNM', 'MO-202607-001'),
                ('称重值', 'sWeight', '50.15'),
            ], 'btns': ['称重', '确认', '取消']},
            {'title': '称重记录', 'cols': ['批号','物料名称','工单号','理论量','实际量','允差%','时间','操作人'],
             'rows': [
                ['LOT-20260729-001','ZW_NE OP SER','MO-202607-001','50.00','50.15','0.3%','2026-07-29 10:30','超级管理员'],
                ['LOT-20260729-002','ZW_PH ADJUST','MO-202607-001','12.50','12.48','-0.2%','2026-07-29 10:35','超级管理员'],
            ]},
        ],
        'stats': {'tables': 2, 'sps': 0, 'dals': 2},
        'tables': [('DispatchHistory','发料历史'),('Lot','批次')],
        'sps': [],
        'dals': [('MESZZZX_WeighingDAL','称重DAL')],
        'forms': [('frmME_IssueMaterial_Weighting','原料称重主页')],
    },
}

# ====== Read template ======
with open(os.path.join(base, 'demo-cs-scrap-order.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# ====== Build block HTML ======
def build_blocks(blocks):
    html = ''
    for b in blocks:
        html += '<div class="blk">\n'
        html += f'<div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- {b["title"]}</div>\n'
        html += '<div class="blk-bd" style="padding:0">\n'
        # Fields row
        html += '<div style="padding:4px 8px;background:#F5F5F5;border-bottom:1px solid #C8D0D8;display:flex;gap:4px;align-items:center;flex-wrap:wrap">\n'
        for label, kid, val in b.get('fields', []):
            html += f'<label style="font:9pt \'微软雅黑\'">{label}：</label><input data-k="{kid}" value="{val}" style="width:160px;height:28px;font:9pt \'微软雅黑\';border:1px solid #C0C0C0;border-radius:2px">\n'
        for btn in b.get('btns', []):
            html += f'<button class="btn primary" style="font:12pt \'微软雅黑\';width:90px;height:40px">{btn}</button>\n'
        html += '</div>\n'
        # Grid
        if 'cols' in b:
            html += '<div class="grid-wrap" style="min-height:80px;max-height:300px">\n'
            html += '<table class="grid">\n<thead><tr>\n'
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

# ====== Build stats HTML ======
def build_stats(p):
    s = p['stats']
    tables_html = ''.join(f'<div><span style="font-family:Consolas,monospace;color:#1a3a5c">{t[0]}</span> <span class="tag tag-tbl">{t[1]}</span></div>' for t in p.get('tables',[]))
    sps_html = ''.join(f'<div><span style="font-family:Consolas,monospace;color:#1a3a5c">{t[0]}</span> <span class="tag tag-sp">{t[1]}</span></div>' for t in p.get('sps',[]))
    if not p.get('sps'):
        sps_html = '<div style="font-size:8pt;color:#888;padding:2px 4px">通过 DAL→WebAPI 直接操作，未使用独立存储过程</div>'
    dals_html = ''.join(f'<div><span style="font-family:Consolas,monospace;color:#1a3a5c">{t[0]}</span> <span class="tag tag-bll">{t[1]}</span></div>' for t in p.get('dals',[]))
    forms_html = ''.join(f'<div><span style="font-family:Consolas,monospace;color:#1a3a5c">{t[0]}</span> <span class="tag tag-form">{t[1]}</span></div>' for t in p.get('forms',[]))
    return f'''      <div style="display:flex;gap:8px;margin-bottom:6px">
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['tables']}</div><div style="font-size:7pt;color:DimGray">数据库表</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['sps']}</div><div style="font-size:7pt;color:DimGray">存储过程</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">{s['dals']}</div><div style="font-size:7pt;color:DimGray">DAL类</div></div>
      </div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;margin-right:4px"></span>&#x1F4CA; 数据库表</h4><div style="font-size:8pt;line-height:1.7">{tables_html}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#7c3aed;margin-right:4px"></span>&#x2699; 存储过程</h4><div style="font-size:8pt;line-height:1.7">{sps_html}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#d97706;margin-right:4px"></span>&#x1F9E9; 数据访问层 (DAL)</h4><div style="font-size:8pt;line-height:1.7">{dals_html}</div></div>
      <div class="ss"><h4><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#3b82f6;margin-right:4px"></span>&#x1F5A5; 窗体</h4><div style="font-size:8pt;line-height:1.7">{forms_html}</div></div>'''

# ====== Generate each page ======
for fname, p in pages.items():
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace form content blocks (between <!-- ═══════ Block and next block/modal)
    # Find the blocks section and replace with generated blocks
    blocks_html = build_blocks(p['blocks'])
    # Find the position of first Block marker and last </div> before modal
    blk_start = content.find('<!-- ═══════ Block')
    modal_start = content.find('<!-- ═══════ Toast')
    if blk_start >= 0 and modal_start >= 0:
        content = content[:blk_start] + blocks_html + '\n\n          </div>\n        </div>\n      </div>\n    </div>\n    <div class="stats">\n' + build_stats(p) + '\n' + content[content.find('<div class="src-note">'):]
    
    # 2. Fix source note
    content = content.replace('frmME_AddScrapOrder.cs', f'{p["form_cs"]}.cs')
    
    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')

print('Done!')
