import os

# Read scrap-order template for CSS + JS patterns
base = r'E:\code\scal-pda-f\workspace\deepseek'
with open(os.path.join(base, 'demo-cs-scrap-order.html'), 'r', encoding='utf-8') as f:
    tpl = f.read()

css = tpl[tpl.find('<style>'):tpl.find('</style>')+len('</style>')]
# Extract after first <body> to get the card + toast + modal + script sections
body_start = tpl.find('<body>')
card_start = tpl.find('<aside class="card"')
script_start = tpl.find('  <script>')
script_end = tpl.find('</html>')
card_to_end = tpl[card_start:script_end]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>工单 · CS客户端</title>
{css}
</head>
<body>
  <div style="display:flex;gap:8px">
    <div class="win">
      <div class="topbar">
        <div class="logo">MES 制造执行系统</div>
        <div class="info"><span>📅 2026-07-29</span><span class="time">14:30:00</span><span>星期三</span><span>| 系统连接：正常</span></div>
        <span class="ver">当前版本：3.0.5.74</span><span class="user">👤 超级管理员</span>
      </div>
      <div class="body">
        <div class="left">
          <div class="grp-title">主导航</div><div class="tree-item">无</div>
          <div class="grp-title">生产执行</div>
          <div class="tree-item">工单启动</div>
          <div class="tree-item sel">工单</div>
          <div class="tree-item">原料称重</div><div class="tree-item">原料称重复核</div><div class="tree-item">余料称重</div>
          <div class="tree-item">称重调试</div><div class="tree-item">BPR作业</div><div class="tree-item">配制产出</div>
          <div class="tree-item">报废单</div>
        </div>
        <div class="right">
          <div class="tabs"><div class="tab">首页</div><div class="tab sel">工单</div></div>
          <div class="content">

            <!-- ① searchPanel: 查询行 45px -->
            <div class="blk">
              <div class="blk-hd">工单查询 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">searchPanel 1689×45 Dock=Top</span></div>
              <div class="blk-bd" style="padding:4px 8px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">
                <label style="font:9pt '微软雅黑'">工单号：</label>
                <input data-k="SearchArea_MfgOrderNM" value="MO-202607-001" style="width:315px;height:27px;font:9pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px">
                <button class="btn primary" data-k="QueryButton" style="width:124px;height:33px;font:12pt '微软雅黑'">查询</button>
                <button class="btn primary" data-k="SearchArea_CloseButton" style="width:124px;height:33px;font:12pt '微软雅黑'">结案</button>
                <button class="btn" data-k="SearchArea_UnCloseButton" style="width:124px;height:33px;font:12pt '微软雅黑'">结案还原</button>
                <button class="btn" data-k="SearchArea_UpdateButton" style="width:124px;height:33px;font:12pt '微软雅黑'">修改</button>
              </div>
            </div>

            <!-- ② MfgOrderList: 工单列表 239px -->
            <div class="blk">
              <div class="blk-hd">工单列表 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">dgvMfgOrderList 1689×239, 15列</span></div>
              <div class="grid-wrap" style="min-height:100px;max-height:239px">
                <table class="grid" id="mfgGrid">
                  <thead><tr>''' + ''.join(['<th>'+h+'</th>' for h in ['工单号','物料编号','数量','完成数','取样量','计划开工','计划完工','工单状态','修改人','修改时间','MO状态','工单ID','产品类型','采购类型','备注']]) + '''</tr></thead>
                  <tbody>
                    <tr>''' + ''.join(['<td data-k="g_'+k+'">'+v+'</td>' for k,v in zip(['MfgOrderNM','ProductNM','Qty','CompliteQty','SampleQty','ReleaseDate','PlanFinishDate','State','ModifyBy','ModifyTime','MoStatus','MfgOrderId','ProductType','PurchaseType','Reason'],['MO-202607-001','MAT-001','5000','3200','10','2026-07-25','2026-07-30','生产中','超级管理员','2026-07-29','1','1001','成品','正常','—'])]) + '''</tr>
                    <tr>''' + ''.join(['<td data-k="g_'+k+'">'+v+'</td>' for k,v in zip(['MfgOrderNM','ProductNM','Qty','CompliteQty','SampleQty','ReleaseDate','PlanFinishDate','State','ModifyBy','ModifyTime','MoStatus','MfgOrderId','ProductType','PurchaseType','Reason'],['MO-202607-002','MAT-002','3000','1500','5','2026-07-26','2026-07-31','生产中','超级管理员','2026-07-29','1','1002','成品','正常','—'])]) + '''</tr>
                    <tr>''' + ''.join(['<td data-k="g_'+k+'">'+v+'</td>' for k,v in zip(['MfgOrderNM','ProductNM','Qty','CompliteQty','SampleQty','ReleaseDate','PlanFinishDate','State','ModifyBy','ModifyTime','MoStatus','MfgOrderId','ProductType','PurchaseType','Reason'],['MO-202607-003','MAT-003','2000','2000','8','2026-07-20','2026-07-28','已结案','李四','2026-07-29','2','1003','成品','正常','—'])]) + '''</tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- ③ TextAreaPanel: 工单详情 225px, 3列 -->
            <div class="blk">
              <div class="blk-hd">工单详细信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">TextAreaPanel 1689×225 Dock=Top, 17字段</span></div>
              <div class="blk-bd" style="padding:4px 8px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px 12px">'''
for label, kid, val in [
    ('工单编号','TextArea_MfgOrderNM','MO-202607-001'),('物料编号','TextArea_ProductNM','MAT-001'),('完成数','TextArea_CompliteQty','3200'),
    ('规格描述','TextArea_Description',''),('销售单','TextArea_SalesOrder',''),('客户','TextArea_CustomerNM',''),
    ('客户订单号','TextArea_CustomerOrderNM',''),('计划开工日期','TextArea_ReleaseDate','2026-07-25'),('计划完工日期','TextArea_PlanFinishDate','2026-07-30'),
    ('生产批号','TextArea_MfgBatch','B20260725-001'),('数量','TextArea_Qty','5000'),('单位','TextArea_UOMNM','kg'),
    ('工单状态','TextArea_WorkStatus','生产中'),('修改人','TextArea_ModifyBy','超级管理员'),('修改时间','TextArea_LastModifyTime','2026-07-29'),
]:
    readonly = 'readonly' if label in ('工单状态','修改人','修改时间','数量','生产批号','完成数') else ''
    bg = 'background:#F5F5F5' if readonly else ''
    html += f'<div style="display:flex;align-items:center;gap:4px"><label style="font:9pt \'微软雅黑\';width:80px">{label}：</label><input data-k="{kid}" value="{val}" {readonly} style="flex:1;height:28px;font:9pt \'微软雅黑\';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px;{bg}"></div>\n'

html += '''</div>
            </div>

            <!-- ④ DispatchListPanel: 发料信息 267px -->
            <div class="blk">
              <div class="blk-hd">发料信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">DispatchListPanel 1689×267, Left=已发料明细(12列) | Right=发料批次(3列)</span></div>
              <div class="blk-bd" style="padding:4px;display:flex;gap:4px">
                <div style="flex:1;min-width:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">已发料明细 <span style="font-weight:400;color:#888;font-size:7pt">DispatchedMaterialList 999×240, 13列</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid"><thead><tr>''' + ''.join(['<th>'+h+'</th>' for h in ['项次','物料名称','备注','需求数量','线边量','差异量','实发数量','发料量','退回量','退料申请量','备料量','单位','类型']]) + '''</tr></thead>
                      <tbody>
                        <tr>''' + ''.join(['<td data-k="d_'+k+'">'+v+'</td>' for k,v in zip(['Item','ProductNM','Note','RequireQty','LineQty','DifferenceQty','ActDispatchedQty','DispatchQty','ReturnQty','ReturnApplyQty','DispatchPrepareQty','UOMNM','Type'],['1','ZW_NE OP SER','主料','50','0','3.5','46.5','50','3.5','0','50','kg','1'])]) + '''</tr>
                        <tr>''' + ''.join(['<td data-k="d_'+k+'">'+v+'</td>' for k,v in zip(['Item','ProductNM','Note','RequireQty','LineQty','DifferenceQty','ActDispatchedQty','DispatchQty','ReturnQty','ReturnApplyQty','DispatchPrepareQty','UOMNM','Type'],['2','ZW_PH ADJUST','辅料','12.5','0','0','12.5','12.5','0','0','12.5','kg','1'])]) + '''</tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div style="width:400px;flex-shrink:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">发料批次列表 <span style="font-weight:400;color:#888;font-size:7pt">DispatchedLotList 690×240</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid"><thead><tr><th>生产批号</th><th>流水号</th><th>数量</th></tr></thead>
                      <tbody>
                        <tr><td data-k="dl_MFGBatch">B20260725-001</td><td data-k="dl_LotNM">20260729-001</td><td data-k="dl_Qty">50</td></tr>
                        <tr><td data-k="dl_MFGBatch">B20260725-001</td><td data-k="dl_LotNM">20260729-002</td><td data-k="dl_Qty">12.5</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- ⑤ ListPanel2: 批次信息 284px -->
            <div class="blk">
              <div class="blk-hd">批次信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">ListPanel2 1689×284, Left=产出批次(8列) | Right=生产批次汇总(4列)</span></div>
              <div class="blk-bd" style="padding:4px;display:flex;gap:4px">
                <div style="flex:1;min-width:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">产出批次明细列表 <span style="font-weight:400;color:#888;font-size:7pt">LotList 1004×254, 8列</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid"><thead><tr>''' + ''.join(['<th>'+h+'</th>' for h in ['生产批号','流水号','原始开始时间','原始数量','数量','产线','设备','在库状态']]) + '''</tr></thead>
                      <tbody>
                        <tr>''' + ''.join(['<td data-k="l_'+k+'">'+v+'</td>' for k,v in zip(['MfgBatch','LotNM','StartDate','OrigQty','Qty','ProductLine','Equipment','IsStock'],['B20260725-001','LOT-001','2026-07-25 08:00','5000','3200','产线A','EQ-01','在库'])]) + '''</tr>
                        <tr>''' + ''.join(['<td data-k="l_'+k+'">'+v+'</td>' for k,v in zip(['MfgBatch','LotNM','StartDate','OrigQty','Qty','ProductLine','Equipment','IsStock'],['B20260726-001','LOT-002','2026-07-26 08:00','3000','1500','产线B','EQ-02','在库'])]) + '''</tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div style="width:380px;flex-shrink:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">生产批次汇总 <span style="font-weight:400;color:#888;font-size:7pt">LotSummaryList 685×254</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid"><thead><tr><th>生产批号</th><th>在库状态</th><th>原始数量</th><th>数量</th></tr></thead>
                      <tbody>
                        <tr><td data-k="ls_MFGBatch">B20260725-001</td><td data-k="ls_LotEstate">在库</td><td data-k="ls_OrigQty">5000</td><td data-k="ls_Qty">3200</td></tr>
                        <tr><td data-k="ls_MFGBatch">B20260726-001</td><td data-k="ls_LotEstate">在库</td><td data-k="ls_OrigQty">3000</td><td data-k="ls_Qty">1500</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- ⑥ ReductionPanel: 操作记录 161px -->
            <div class="blk">
              <div class="blk-hd">操作记录 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">ReductionPanel 1689×161 Dock=Top</span></div>
              <div class="blk-bd" style="padding:4px">
                <div style="display:flex;gap:8px;align-items:center;margin-bottom:4px">
                  <label style="font:9pt '微软雅黑'">结案还原列表：</label>
                  <label style="font:9pt '微软雅黑'">计划开始日期：</label>
                  <input type="date" value="2026-07-01" style="width:219px;height:29px;font:9pt '微软雅黑';border:1px solid #C0C0C0">
                </div>
                <div class="grid-wrap" style="min-height:60px;max-height:100px">
                  <table class="grid"><thead><tr><th>操作</th><th>操作时间</th><th>操作人</th><th>操作设备</th></tr></thead>
                    <tbody><tr><td data-k="r_TxnId">结案还原</td><td data-k="r_TxnTime">2026-07-29 16:00</td><td data-k="r_TxnUserNM">超级管理员</td><td data-k="r_TxnStationNM">BS-Web</td></tr></tbody>
                  </table>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">
      <div class="sh">📊 调用统计<span class="tag tag-form" style="margin-left:4px">CS·工单</span></div>
      <div style="display:flex;gap:8px;margin-bottom:6px">
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div><div style="font-size:7pt;color:DimGray">数据库表</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">2</div><div style="font-size:7pt;color:DimGray">存储过程</div></div>
        <div style="flex:1;text-align:center;background:#fff;border:1px solid var(--bdr);border-radius:3px;padding:4px"><div style="font-weight:700;font-size:12pt;color:#1a3a5c">2</div><div style="font-size:7pt;color:DimGray">DAL</div></div>
      </div>
      <div class="ss"><h4>数据库表</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">MfgOrder</span> <span class="tag tag-tbl">工单主表</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">MfgOrderBOM</span> <span class="tag tag-tbl">工单BOM</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">Lot</span> <span class="tag tag-tbl">批次</span></div>
      </div></div>
      <div class="ss"><h4>存储过程</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">Pro_MfgOrder_Close_Check</span> <span class="tag tag-sp">结案前校验 (code=200/998/999)</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">Pro_MfgOrder_Close</span> <span class="tag tag-sp">执行结案</span></div>
      </div></div>
      <div class="ss"><h4>数据访问层</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">MESZZZX_MfgOrderDAL</span> <span class="tag tag-bll">工单DAL</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">CKZY_WorkOrder</span> <span class="tag tag-bll">Web工单BLL</span></div>
      </div></div>
      <div class="ss"><h4>窗体</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">frmME_MfgOrder</span> <span class="tag tag-form">工单主页 1710×875</span></div>
      </div></div>
      <div class="src-note"><b>✅ 源码验证：</b> frmME_MfgOrder.cs / .Designer.cs<br>ButtomPanel(Fill) · 6 Panel(Top) · 4 Button · 5 DataGridView · 17 Field</div>
    </div>
  </div>
  ''' + card_to_end + '''

</body>
</html>'''

with open(os.path.join(base, 'demo-cs-mfg-order.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print('OK: demo-cs-mfg-order.html (with interactions)')
