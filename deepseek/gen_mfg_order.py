import os, re

base = r'E:\code\scal-pda-f\workspace\deepseek'
path = os.path.join(base, 'demo-cs-scrap-order.html')
with open(path, 'r', encoding='utf-8') as f:
    tpl = f.read()

# Extract CSS
css = tpl[tpl.find('<style>'):tpl.find('</style>')+len('</style>')]

# ---- ACCURATE frmME_MfgOrder (based on Designer.cs analysis) ----
# ButtomPanel (Fill) contains 6 stacked panels:
#   1. searchPanel (Top=45px): 工单号 + 查询/结案/结案还原/修改
#   2. searchListPanel (Top=239px): MfgOrderList DGV
#   3. TextAreaPanel (Top=225px): 3-column field layout
#   4. DispatchListPanel (Top=267px): Left=已发料明细, Right=发料批次
#   5. ListPanel2 (Top=284px): Left=产出批次明细, Right=生产批次汇总
#   6. ReductionPanel (Top=161px): 结案还原操作记录

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
          <div class="grp-title">主导航</div>
          <div class="tree-item">无</div>
          <div class="grp-title">生产执行</div>
          <div class="tree-item">工单启动</div>
          <div class="tree-item sel">工单</div>
          <div class="tree-item">原料称重</div>
          <div class="tree-item">原料称重复核</div>
          <div class="tree-item">余料称重</div>
          <div class="tree-item">称重调试</div>
          <div class="tree-item">天平调试</div>
          <div class="tree-item">BPR作业</div>
          <div class="tree-item">BPR作业修改</div>
          <div class="tree-item">配制罐清洗启动</div>
          <div class="tree-item">配制产出</div>
          <div class="tree-item">报废单</div>
        </div>
        <div class="right">
          <div class="tabs"><div class="tab">首页</div><div class="tab sel">工单</div></div>
          <div class="content">

            <!-- Block 1: searchPanel (Top=45px) -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">工单查询 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">searchPanel 1689×45 Dock=Top</span></div>
              <div class="blk-bd" style="padding:4px 8px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">
                <label style="font:9pt '微软雅黑'">工单号：</label>
                <input data-k="SearchArea_MfgOrderNM" value="MO-202607-001" style="width:315px;height:27px;font:9pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px;padding:2px 6px">
                <button class="btn primary" data-k="QueryButton" style="width:124px;height:33px;font:12pt '微软雅黑'">查询</button>
                <button class="btn primary" data-k="SearchArea_CloseButton" style="width:124px;height:33px;font:12pt '微软雅黑'">结案</button>
                <button class="btn" data-k="SearchArea_UnCloseButton" style="width:124px;height:33px;font:12pt '微软雅黑'">结案还原</button>
                <button class="btn" data-k="SearchArea_UpdateButton" style="width:124px;height:33px;font:12pt '微软雅黑'">修改</button>
              </div>
            </div>

            <!-- Block 2: MfgOrderList (Top=239px, 15 columns) -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">工单列表 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">dgvMfgOrderList 1689×239 Dock=Fill, 15列</span></div>
              <div class="grid-wrap" style="min-height:100px;max-height:239px">
                <table class="grid">
                  <thead><tr>
                    <th>工单号</th><th>物料编号</th><th>数量</th><th>完成数</th><th>取样量</th>
                    <th>计划开工</th><th>计划完工</th><th>工单状态</th><th>修改人</th><th>修改时间</th>
                    <th>MO状态</th><th>工单ID</th><th>产品类型</th><th>采购类型</th><th>备注</th>
                  </tr></thead>
                  <tbody>
                    <tr>
                      <td>MO-202607-001</td><td>MAT-001</td><td>5000</td><td>3200</td><td>10</td>
                      <td>2026-07-25</td><td>2026-07-30</td><td>生产中</td><td>超级管理员</td><td>2026-07-29</td>
                      <td>1</td><td>1001</td><td>成品</td><td>正常</td><td>—</td>
                    </tr>
                    <tr>
                      <td>MO-202607-002</td><td>MAT-002</td><td>3000</td><td>1500</td><td>5</td>
                      <td>2026-07-26</td><td>2026-07-31</td><td>生产中</td><td>超级管理员</td><td>2026-07-29</td>
                      <td>1</td><td>1002</td><td>成品</td><td>正常</td><td>—</td>
                    </tr>
                    <tr>
                      <td>MO-202607-003</td><td>MAT-003</td><td>2000</td><td>2000</td><td>8</td>
                      <td>2026-07-20</td><td>2026-07-28</td><td>已结案</td><td>李四</td><td>2026-07-29</td>
                      <td>2</td><td>1003</td><td>成品</td><td>正常</td><td>—</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Block 3: TextAreaPanel (Top=225px, 3-column layout) -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">工单详细信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">TextAreaPanel 1689×225 Dock=Top</span></div>
              <div class="blk-bd" style="padding:4px 8px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px 12px">
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">工单编号：</label><input value="MO-202607-001" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">物料编号：</label><input value="MAT-001" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">完成数：</label><input value="3200" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">规格描述：</label><input value="" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">销售单：</label><input value="" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">客户：</label><input value="" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">客户订单号：</label><input value="" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">计划开工日期：</label><input value="2026-07-25" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">计划完工日期：</label><input value="2026-07-30" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">生产批号：</label><input value="B20260725-001" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">数量：</label><input value="5000" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">单位：</label><input value="kg" style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">工单状态：</label><input value="生产中" readonly style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;background:#F5F5F5"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">修改人：</label><input value="超级管理员" readonly style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;background:#F5F5F5"></div>
                <div style="display:flex;align-items:center;gap:4px"><label style="font:9pt '微软雅黑';width:80px">修改时间：</label><input value="2026-07-29" readonly style="flex:1;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;background:#F5F5F5"></div>
              </div>
            </div>

            <!-- Block 4: DispatchListPanel (Top=267px) Left=已发料明细 Right=发料批次 -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">发料信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">DispatchListPanel 1689×267 Left=999px 已发料明细 | Right=690px 发料批次</span></div>
              <div class="blk-bd" style="padding:4px;display:flex;gap:4px">
                <div style="flex:1;min-width:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">已发料明细 <span style="font-weight:400;color:#888;font-size:7pt">Dock=Left 999×240, 12列</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid">
                      <thead><tr>
                        <th>项次</th><th>物料名称</th><th>备注</th><th>需求数量</th><th>线边量</th><th>差异量</th>
                        <th>实发数量</th><th>发料量</th><th>退回量</th><th>退料申请量</th><th>备料量</th><th>单位</th>
                      </tr></thead>
                      <tbody>
                        <tr><td>1</td><td>ZW_NE OP SER</td><td>主料</td><td>50</td><td>0</td><td>3.5</td><td>46.5</td><td>50</td><td>3.5</td><td>0</td><td>50</td><td>kg</td></tr>
                        <tr><td>2</td><td>ZW_PH ADJUST</td><td>辅料</td><td>12.5</td><td>0</td><td>0</td><td>12.5</td><td>12.5</td><td>0</td><td>0</td><td>12.5</td><td>kg</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div style="width:400px;flex-shrink:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">发料批次列表 <span style="font-weight:400;color:#888;font-size:7pt">Dock=Fill 690×240</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid">
                      <thead><tr><th>生产批号</th><th>流水号</th><th>数量</th></tr></thead>
                      <tbody>
                        <tr><td>B20260725-001</td><td>20260729-001</td><td>50</td></tr>
                        <tr><td>B20260725-001</td><td>20260729-002</td><td>12.5</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- Block 5: ListPanel2 (Top=284px) Left=产出批次明细 Right=生产批次汇总 -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">批次信息 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">ListPanel2 1689×284 Left=1004px 产出批次明细 | Right=685px 生产批次汇总</span></div>
              <div class="blk-bd" style="padding:4px;display:flex;gap:4px">
                <div style="flex:1;min-width:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">产出批次明细列表 <span style="font-weight:400;color:#888;font-size:7pt">Dock=Left 1004×254, 8列</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid">
                      <thead><tr>
                        <th>生产批号</th><th>流水号</th><th>原始开始时间</th><th>原始数量</th><th>数量</th><th>产线</th><th>设备</th><th>在库状态</th>
                      </tr></thead>
                      <tbody>
                        <tr><td>B20260725-001</td><td>LOT-001</td><td>2026-07-25 08:00</td><td>5000</td><td>3200</td><td>产线A</td><td>EQ-01</td><td>在库</td></tr>
                        <tr><td>B20260726-001</td><td>LOT-002</td><td>2026-07-26 08:00</td><td>3000</td><td>1500</td><td>产线B</td><td>EQ-02</td><td>在库</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div style="width:380px;flex-shrink:0">
                  <div style="font-weight:700;font-size:9pt;padding:2px 4px;background:#E8F0FE;margin-bottom:2px">生产批次汇总 <span style="font-weight:400;color:#888;font-size:7pt">Dock=Fill 685×254, 4列</span></div>
                  <div class="grid-wrap" style="min-height:80px;max-height:200px">
                    <table class="grid">
                      <thead><tr><th>生产批号</th><th>在库状态</th><th>原始数量</th><th>数量</th></tr></thead>
                      <tbody>
                        <tr><td>B20260725-001</td><td>在库</td><td>5000</td><td>3200</td></tr>
                        <tr><td>B20260726-001</td><td>在库</td><td>3000</td><td>1500</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- Block 6: ReductionPanel (Top=161px) 底部操作记录 -->
            <div class="blk">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">操作记录 <span style="font-weight:400;color:#888;margin-left:8px;font-size:8pt">ReductionPanel 1689×161 Dock=Top</span></div>
              <div class="blk-bd" style="padding:4px">
                <div style="display:flex;gap:8px;align-items:center;margin-bottom:4px">
                  <label style="font:9pt '微软雅黑'">结案还原列表：</label>
                  <label style="font:9pt '微软雅黑'">计划开始日期：</label>
                  <input type="date" value="2026-07-01" style="width:219px;height:29px;font:9pt '微软雅黑';border:1px solid #C0C0C0">
                </div>
                <div class="grid-wrap" style="min-height:60px;max-height:100px">
                  <table class="grid">
                    <thead><tr><th>操作</th><th>操作时间</th><th>操作人</th><th>操作设备</th></tr></thead>
                    <tbody>
                      <tr><td>结案还原</td><td>2026-07-29 16:00</td><td>超级管理员</td><td>BS-Web</td></tr>
                    </tbody>
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
        <div><span style="font-family:Consolas;color:#1a3a5c">Pro_MfgOrder_Close_Check</span> <span class="tag tag-sp">结案前校验</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">Pro_MfgOrder_Close</span> <span class="tag tag-sp">执行结案</span></div>
      </div></div>
      <div class="ss"><h4>数据访问层</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">MESZZZX_MfgOrderDAL</span> <span class="tag tag-bll">工单DAL</span></div>
        <div><span style="font-family:Consolas;color:#1a3a5c">CKZY_WorkOrder</span> <span class="tag tag-bll">Web工单BLL</span></div>
      </div></div>
      <div class="ss"><h4>窗体</h4><div style="font-size:8pt;line-height:1.7">
        <div><span style="font-family:Consolas;color:#1a3a5c">frmME_MfgOrder</span> <span class="tag tag-form">工单主页 1710×875</span></div>
      </div></div>
      <div class="src-note"><b>✅ 源码验证：</b> frmME_MfgOrder.cs / .Designer.cs<br>6 Panel · 4 Button · 5 DataGridView · 17 Field · Dock=Top 垂直堆叠布局 100%精确</div>
    </div>
  </div>
</body>
</html>'''

with open(os.path.join(base, 'demo-cs-mfg-order.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print('OK: demo-cs-mfg-order.html')
