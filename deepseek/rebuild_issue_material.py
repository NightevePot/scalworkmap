#!/usr/bin/env python3
"""Rebuild demo-cs-template.html from frmME_IssueMaterial source (原料称重主页).
1726×875, 4 DataGridViews, 7 panels. All data from Designer.cs + .cs."""

src = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-scrap-order.html'
dst = r'e:\code\scal-pda-f\workspace\deepseek\demo-cs-template.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════ Identity ═══════
html = html.replace('<title>报废单 · CS客户端</title>', '<title>原料称重 · CS客户端</title>')
html = html.replace('<div class="tree-item sel">报废单</div>', '<div class="tree-item sel">原料称重</div>')
html = html.replace('<div class="tab sel">报废单</div>', '<div class="tab sel">原料称重</div>')

# ═══════ Form content replacement ═══════
old_form_start = '            <!-- ═══════ Block ②: 报废单表头区 (ScrapOrderHeadPanel) ═══════ -->'
form_end_marker = '    <div class="stats">'
pos_start = html.find(old_form_start)
pos_end = html.find(form_end_marker, pos_start)

new_form = '''            <!-- ═══════ frmME_IssueMaterial · 原料称重 1726×875 ═══════ -->

            <!-- panelWorkOrder: 工单选择区 1705×52 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:6px 6px 2px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 基础信息 <span style="font-weight:400;color:#888;font-size:8pt">panelBasicInfoTitle 1705×28</span><span style="float:right;font-size:8pt;color:#888">Text="原料称重"</span></div>
              <div class="blk-bd" style="padding:6px 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                <label style="font:9pt '微软雅黑';color:red">*</label>
                <label style="font:9pt '微软雅黑'">工单：</label>
                <input data-k="MfgOrderNMTextBox" value="MO-SO251206750-02" style="width:200px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0;border-radius:2px" title="ComboGrid控件">
                <label style="font:9pt '微软雅黑';margin-left:8px">工艺版本：</label>
                <span data-k="txt_bprVersion" style="font:9pt '微软雅黑';color:#1a3a5c">V2.1</span>
                <label style="font:9pt '微软雅黑';margin-left:8px">设备名：</label>
                <select data-k="cboDevice" style="width:150px;height:28px;font:9pt '微软雅黑';border:1px solid #C0C0C0">
                  <option>QDZY-10007</option><option>QDZY-10006</option>
                </select>
                <button class="btn primary" data-k="QueryButton" style="font:12pt '微软雅黑';width:80px;height:36px">查询</button>
              </div>
            </div>

            <!-- panelWorkOrderList: 工单列表 1705×113 -->
            <div class="blk" style="border:1px solid #C0C0C0;margin:2px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:#E8F0FE">工单列表 <span style="font-weight:400;color:#888;font-size:8pt">BI_MfgOrderList</span></div>
              <div class="blk-bd" style="padding:0">
                <div class="grid-wrap" style="max-height:100px">
                  <table class="grid">
                    <thead><tr><th>编号</th><th>工单编号</th><th>物料编号</th><th>生产批号</th><th>净重</th><th>单位</th><th>计划开工日</th><th>BPR</th><th>工单状态</th></tr></thead>
                    <tbody><tr><td data-k="MO_SN">1</td><td data-k="MO_MfgOrderNM">MO-SO251206750-02</td><td data-k="MO_ProductNM">2969344</td><td data-k="MO_MFGBatch">B20260729-001</td><td data-k="MO_Qty">50.00</td><td data-k="MO_UOMNM">kg</td><td data-k="MO_ReleaseDate">2026-07-29</td><td data-k="MO_BPRNM">BPR-001</td><td data-k="MO_MOStatus">已发料</td></tr></tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- panelBPRList: BPR配方列表 1705×200 -->
            <div class="blk" style="border:1px solid #C0C0C0;margin:2px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:#E8F0FE">BPR配方列表 <span style="font-weight:400;color:#888;font-size:8pt">IM_BPRList</span></div>
              <div class="blk-bd" style="padding:0">
                <div class="grid-wrap" style="max-height:180px">
                  <table class="grid">
                    <thead><tr><th>标记</th><th>编号</th><th>物料编号</th><th>客户物料编号</th><th>规格描述</th><th>下限</th><th>标准值</th><th>上限</th><th>单位</th><th>称重量</th><th>称重批数</th><th>发料数量</th><th>确认数量</th><th>发料单位</th><th>工单编号</th></tr></thead>
                    <tbody><tr><td data-k="BPR_Flag">●</td><td data-k="BPR_SN">1</td><td data-k="BPR_ProductNM">2969344</td><td data-k="BPR_CsrMatCode">CUST-001</td><td data-k="BPR_Note">25kg/桶</td><td data-k="BPR_MinValue">49.50</td><td data-k="BPR_StandardValue">50.00</td><td data-k="BPR_MaxValue">50.50</td><td data-k="BPR_UOMNM">kg</td><td data-k="BPR_IssueQty">50.15</td><td data-k="BPR_IssueLotCount">3</td><td data-k="BPR_DispatchQty">150.00</td><td data-k="BPR_ConfirmQty">150.00</td><td data-k="BPR_DispatchUOMNM">kg</td><td data-k="BPR_MfgOrderNM">MO-SO251206750-02</td></tr></tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- panelDetail: 明细区 (两栏) 1705×229 -->
            <div style="display:flex;gap:4px;margin:2px 6px">
              <!-- panel5: 已发料明细 1012×229 -->
              <div class="blk" style="flex:1;border:1px solid #C0C0C0;background:#FAFBFC;min-width:0">
                <div class="blk-hd" style="background:#E8F0FE">已发料明细 <span style="font-weight:400;color:#888;font-size:8pt">IM_DispatchList · panel5</span></div>
                <div class="blk-bd" style="padding:0">
                  <div class="grid-wrap" style="max-height:190px">
                    <table class="grid">
                      <thead><tr><th>编号</th><th>生产批号</th><th>有效日期</th><th>流水号</th><th>发料数量</th><th>线边数量</th><th>单位</th><th>发料状态</th><th>物料编号</th><th>工单编号</th><th>其他信息</th><th>毛重</th><th>皮重</th><th>包装层级</th></tr></thead>
                      <tbody><tr><td data-k="DL_SN">1</td><td data-k="DL_MFGBatch">B20260729-001</td><td data-k="DL_ExpirationDate">2027-07-29</td><td data-k="DL_LotNM">LOT-20260729-001</td><td data-k="DL_DispatchQty">50.00</td><td data-k="DL_WipQty">0.00</td><td data-k="DL_UOMNM">kg</td><td data-k="DL_DispatchStatus">已发料</td><td data-k="DL_ProductNM">2969344</td><td data-k="DL_MfgOrderNM">MO-SO251206750-02</td><td data-k="DL_Info">—</td><td data-k="DL_GrossWeight">51.65</td><td data-k="DL_SkinWeight">1.50</td><td data-k="DL_Level">1</td></tr></tbody>
                    </table>
                  </div>
                </div>
              </div>
              <!-- panel6: 原料称重列表 693×229 -->
              <div class="blk" style="flex:0 0 420px;border:1px solid #C0C0C0;background:#FAFBFC">
                <div class="blk-hd" style="background:#E8F0FE">原料称重列表 <span style="font-weight:400;color:#888;font-size:8pt">IM_IssueMaterialList · panel6</span></div>
                <div class="blk-bd" style="padding:0">
                  <div class="grid-wrap" style="max-height:190px">
                    <table class="grid">
                      <thead><tr><th>编号</th><th>流水号</th><th>单位</th><th>净重</th><th>皮重</th><th>毛重</th><th>称重时间</th><th>称重人</th><th>审核人</th><th>有效时间</th></tr></thead>
                      <tbody><tr><td data-k="IM_SN">1</td><td data-k="IM_LotNM">LOT-20260729-001</td><td data-k="IM_UOMNM">kg</td><td data-k="IM_NetWeight">50.15</td><td data-k="IM_SkinWeight">1.50</td><td data-k="IM_GrossWeight">51.65</td><td data-k="IM_WeightTime">2026-07-29 14:30</td><td data-k="IM_WeighingPersonNM">超级管理员</td><td data-k="IM_VerifyPersonNM">—</td><td data-k="IM_ExpirationDate">2027-07-29</td></tr></tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- panel7/panel9: 操作输入区 1705×454 -->
            <div class="blk" style="border:1px solid #C0C0C0;border-radius:4px;margin:4px 6px 6px 6px;background:#FAFBFC">
              <div class="blk-hd" style="background:linear-gradient(180deg,#F0F0F0,#D0D0D0)">- 称重操作 <span style="font-weight:400;color:#888;font-size:8pt">panel9 1705×454</span></div>
              <div class="blk-bd" style="padding:6px 8px">
                <!-- 操作按钮行 -->
                <div style="display:flex;gap:8px;margin-bottom:6px;align-items:center">
                  <button class="btn primary" data-k="IM_Button_Weighting" style="font:12pt '微软雅黑';width:100px;height:48px">称重</button>
                  <button class="btn" data-k="IM_Button_PassWeight" style="font:12pt '微软雅黑';width:100px;height:48px">免称</button>
                  <button class="btn primary" data-k="IM_Button_Confirm" style="font:12pt '微软雅黑';width:100px;height:48px">确认</button>
                  <span style="color:#888;font-size:8pt;margin-left:auto">IM_Button_Weighting→打开frmME_IssueMaterial_Weighting弹窗</span>
                </div>
                <!-- 输入区: 三列布局 -->
                <div style="display:flex;gap:12px">
                  <!-- 左列: 基础信息 -->
                  <div style="flex:1;display:grid;grid-template-columns:80px 1fr;gap:4px 6px;align-items:center;font:9pt '微软雅黑'">
                    <label>流水号：</label><input data-k="txt_LotNM" value="LOT-20260729-001" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" readonly title="ReadOnly">
                    <label>设备名：</label><input data-k="IM_TextArea_EquipmentNM" value="QDZY-10007" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                    <label>容器编号：</label><input data-k="IM_TextArea_ContainerNM" value="TANK-A01" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                    <label>工单编号：</label><input data-k="txt_mfgOrderNM" value="MO-SO251206750-02" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                    <label>出库单编号：</label><input data-k="txt_stockOrderNM" value="SO-20260729-001" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                    <label>调料工单：</label><select data-k="IM_TextArea_ToMfgOrderNMComboBox" style="height:26px;border:1px solid #C0C0C0;border-radius:2px"><option>MO-SO251206750-02</option></select>
                    <label></label><button class="btn" data-k="IM_Button_ToMfgOrder" style="font:9pt '微软雅黑';width:183px;height:38px">调料</button>
                  </div>
                  <!-- 中列: 称重信息 -->
                  <div style="flex:1;display:grid;grid-template-columns:90px 1fr;gap:4px 6px;align-items:center;font:9pt '微软雅黑'">
                    <label>物料编号：</label><input data-k="txt_productNM" value="2969344" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0;font-weight:bold;font-size:14pt" title="ReadOnly">
                    <label>称重范围：</label><input data-k="txt_standardValue" value="49.50 ~ 50.50" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                    <label>生产批号：</label><input data-k="txt_mfgBatch" value="B20260729-001" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                    <label>净重：</label><input data-k="IM_TextArea_NetWeight" value="50.15" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;color:green;font-weight:bold">
                    <label>单位：</label><input data-k="txt_unit" value="kg" readonly style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0" title="ReadOnly">
                    <label>打印机：</label><select data-k="IM_TextArea_Printer" style="height:26px;border:1px solid #C0C0C0;border-radius:2px"><option>ZDesigner ZT410</option></select>
                    <label>标签定义：</label><input data-k="txt_label" value="LABEL-001" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                    <label>打印份数：</label><input data-k="txt_printQty" value="2" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                  </div>
                  <!-- 右列: 重量读数 -->
                  <div style="flex:0 0 280px;display:grid;grid-template-columns:70px 1fr;gap:4px 6px;align-items:center;font:9pt '微软雅黑'">
                    <label>皮重：</label><input data-k="IM_TextArea_SkinWeight" value="1.50" style="height:30px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;font-weight:bold;font-size:12pt" title="从称重弹窗返回">
                    <label>毛重：</label><input data-k="IM_TextArea_GrossWeight" value="51.65" readonly style="height:30px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;background:#FFFFE0;font-weight:bold;font-size:12pt;color:#B8860B" title="ReadOnly">
                    <label>净重：</label><input data-k="IM_TextArea_NetWeight2" value="50.15" style="height:30px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px;font-weight:bold;font-size:12pt;color:green">
                    <label>授权用户：</label><input data-k="txt_superUserNM" placeholder="复核人" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                    <label>授权密码：</label><input data-k="txt_superUserPS" type="password" placeholder="****" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                    <label>超量原因：</label><input data-k="txt_overReason" placeholder="超差原因" style="height:26px;border:1px solid #C0C0C0;border-radius:2px;padding:0 4px">
                  </div>
                </div>
                <!-- 底部按钮行 -->
                <div style="display:flex;gap:8px;margin-top:8px;padding-top:6px;border-top:1px solid #E0E0E0">
                  <button class="btn" data-k="IM_Button_DispatchListRePrint" style="font:9pt '微软雅黑';width:183px;height:40px">已发料明细重印</button>
                  <button class="btn" data-k="IM_Button_IssueMaterialReprint" style="font:9pt '微软雅黑';width:183px;height:40px">原料称重明细重印</button>
                  <span style="flex:1"></span>
                  <button class="btn" data-k="IM_Button_Cancel" style="font:12pt '微软雅黑';width:245px;height:48px;color:#c00">取消称重</button>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="stats">'''

html = html[:pos_start] + new_form + html[pos_end + len(form_end_marker):]

# ═══════ Stats panel ═══════
html = html.replace(
    '      <div class="sh">&#x1F4CA; 调用统计<span class="tag tag-form" style="margin-left:4px">CS&#xB7;报废单</span></div>',
    '      <div class="sh">&#x1F4CA; 代码分析<span class="tag tag-form" style="margin-left:4px">原料称重 frmME_IssueMaterial</span></div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">5</div>\n          <div style="font-size:7pt;color:DimGray">数据库表</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DataGridView</div>')
html = html.replace(
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">4</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>',
    '<div style="font-weight:700;font-size:12pt;color:#1a3a5c">3</div>\n          <div style="font-size:7pt;color:DimGray">DAL类</div>')

# Replace tables section
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
new_t = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">BI_MfgOrderList</span> <span class="tag tag-tbl">工单列表 9列</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">IM_BPRList</span> <span class="tag tag-tbl">BPR配方 15列</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">IM_DispatchList</span> <span class="tag tag-tbl">已发料明细 14列</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">IM_IssueMaterialList</span> <span class="tag tag-tbl">称重列表 10列</span></div>'''
html = html.replace(old_t, new_t)

# DAL section
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
new_d = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_IssueMaterialDAL</span> <span class="tag tag-bll">原料称重</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">issueMaterialDataAccess → 发料/称重数据操作</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_SurplusMaterialDAL</span> <span class="tag tag-bll">余料</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">surplusMaterialDataAccess → 调料工单相关</div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">MESZZZX_BPRRecordDAL</span> <span class="tag tag-bll">BPR记录</span></div>
          <div style="margin-left:10px;color:#888;font-size:7pt">bprRecordDataAccess → BPR配方数据</div>'''
html = html.replace(old_d, new_d)

# Forms section
old_f = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_AddScrapOrder</span> <span
              class="tag tag-form">报废单主页</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_ScrapOrder</span> <span
              class="tag tag-form">添加/编辑表头</span></div>
          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">EditScrapOrder</span> <span
              class="tag tag-form">添加/编辑明细</span></div>
          <div style="margin-top:2px"><span style="font-family:Consolas,monospace;color:#1a3a5c">ESignature</span> <span
              class="tag tag-form">电子签名(送审)</span></div>'''
new_f = '''          <div><span style="font-family:Consolas,monospace;color:#1a3a5c">frmME_IssueMaterial</span> <span class="tag tag-form">原料称重 1726×875</span></div>
          <div style="margin-top:3px;font-size:8pt">├─ IM_Button_Weighting → <b>frmME_IssueMaterial_Weighting</b> (称重弹窗)</div>
          <div style="font-size:8pt">├─ IM_Button_Confirm → 确认发料 + 打印标签(ZPL)</div>
          <div style="font-size:8pt">├─ IM_Button_ToMfgOrder → 调料(打开余料称重)</div>
          <div style="font-size:8pt">└─ 指纹采集: FingerprintCollection (授权验证)</div>'''
html = html.replace(old_f, new_f)

# Source note
old_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_AddScrapOrder.cs /
        .Designer.cs<br>所有控件&#xB7;表&#xB7;DAL方法&#xB7;Location&#xB7;Size 100%精确</div>'''
new_src = '''      <div class="src-note"><b>&#x2705; 源码验证：</b> frmME_IssueMaterial.cs / .Designer.cs<br>
        1726×875 · panelMain(Dock=Fill) · panelWorkOrder→panelWorkOrderList→panelBPRList→panelDetail→panel7<br>
        4 DataGridView: BI_MfgOrderList(9列) · IM_BPRList(15列) · IM_DispatchList(14列) · IM_IssueMaterialList(10列)</div>'''
html = html.replace(old_src, new_src)

# ═══════ Remove modals ═══════
modal_start = html.find('<!-- ═══════ Modal: frmME_ScrapOrder')
script_start = html.find('<script>')
if modal_start != -1 and script_start != -1:
    html = html[:modal_start] + '\n  ' + html[script_start:]

# ═══════ Replace JS map ═══════
map_start = html.find('const map = {')
if map_start != -1:
    brace_count = 0
    in_map = False
    map_end = -1
    for i in range(map_start, len(html)):
        if html[i] == '{': brace_count += 1; in_map = True
        elif html[i] == '}':
            brace_count -= 1
            if in_map and brace_count == 0: map_end = i + 1; break
    if map_end != -1:
        new_map = '''    // ═══════ 字段血缘 Map (原料称重 · frmME_IssueMaterial) ═══════
    const map = {
      // === 工单选择区 ===
      MfgOrderNMTextBox: ['工单号', 'MfgOrder.MfgOrderNM', 'ComboGrid', ['BindMfgOrderNM→MfgOrderNMTextBox']],
      cboDevice: ['设备名', 'Config.ini', 'ComboBox', ['frmME_IssueMaterial_Load→Printer()']],
      txt_bprVersion: ['工艺版本', 'BPR.ProcessSpecVersion', 'Label', ['查询工单→BPR版本']],
      QueryButton: ['查询按钮', 'Button.Click', 'Button', ['QueryButton_Click→BindMfgOrderNM']],
      // === BI_MfgOrderList 工单列表 ===
      MO_SN: ['编号', 'MfgOrder.RN', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      MO_MfgOrderNM: ['工单编号', 'MfgOrder.MfgOrderNM', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      MO_ProductNM: ['物料编号', 'Product.ProductNM', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      MO_MFGBatch: ['生产批号', 'MfgOrder.MFGBatch', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      MO_Qty: ['净重', 'MfgOrder.Qty', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      MO_MOStatus: ['工单状态', 'MfgOrder.MOStatus', 'DataGridView col', ['MfgOrderDataTable→BI_MfgOrderList']],
      // === IM_BPRList BPR配方 ===
      BPR_ProductNM: ['物料编号', 'BPR.ProductNM', 'DataGridView col', ['BPRRecordDAL→IM_BPRList']],
      BPR_MinValue: ['下限', 'BPR.MinValue', 'DataGridView col', ['BPRRecordDAL→IM_BPRList']],
      BPR_StandardValue: ['标准值', 'BPR.StandardValue', 'DataGridView col', ['BPRRecordDAL→IM_BPRList']],
      BPR_MaxValue: ['上限', 'BPR.MaxValue', 'DataGridView col', ['BPRRecordDAL→IM_BPRList']],
      BPR_IssueQty: ['称重量', 'BPR.IssueQty', 'DataGridView col', ['BPRRecordDAL→IM_BPRList']],
      // === IM_DispatchList 已发料明细 ===
      DL_LotNM: ['流水号', 'Dispatch.LotNM', 'DataGridView col', ['IssueMaterialDAL→IM_DispatchList']],
      DL_DispatchQty: ['发料数量', 'Dispatch.DispatchQty', 'DataGridView col', ['IssueMaterialDAL→IM_DispatchList']],
      DL_DispatchStatus: ['发料状态', 'Dispatch.Status', 'DataGridView col', ['IssueMaterialDAL→IM_DispatchList']],
      DL_GrossWeight: ['毛重', 'Dispatch.GrossWeight', 'DataGridView col', ['IssueMaterialDAL→IM_DispatchList']],
      DL_SkinWeight: ['皮重', 'Dispatch.SkinWeight', 'DataGridView col', ['IssueMaterialDAL→IM_DispatchList']],
      // === IM_IssueMaterialList 原料称重列表 ===
      IM_NetWeight: ['净重', 'IssueMaterial.NetWeight', 'DataGridView col', ['IssueMaterialDAL→IM_IssueMaterialList']],
      IM_SkinWeight: ['皮重', 'IssueMaterial.SkinWeight', 'DataGridView col', ['IssueMaterialDAL→IM_IssueMaterialList']],
      IM_GrossWeight: ['毛重', 'IssueMaterial.GrossWeight', 'DataGridView col', ['IssueMaterialDAL→IM_IssueMaterialList']],
      IM_WeightTime: ['称重时间', 'IssueMaterial.WeightTime', 'DataGridView col', ['IssueMaterialDAL→IM_IssueMaterialList']],
      IM_WeighingPersonNM: ['称重人', 'IssueMaterial.WeighingPersonNM', 'DataGridView col', ['IssueMaterialDAL→IM_IssueMaterialList']],
      // === 操作区按钮 ===
      IM_Button_Weighting: ['称重按钮', 'Button.Click→打开称重弹窗', 'Button 100×48', ['frmME_IssueMaterial_Weighting(equipNM)']],
      IM_Button_PassWeight: ['免称按钮', 'Button.Click→跳过称重', 'Button 100×48', ['IM_Button_PassWeight_Click']],
      IM_Button_Confirm: ['确认按钮', 'Button.Click→确认发料+打印', 'Button 100×48', ['IM_Button_Confirm_Click→ZPL打印']],
      IM_Button_ToMfgOrder: ['调料按钮', 'Button.Click→打开余料', 'Button 183×46', ['IM_Button_ToMfgOrder_Click']],
      IM_Button_Cancel: ['取消称重', 'Button.Click→取消操作', 'Button 245×48', ['IM_Button_Cancel_Click']],
      // === 重量字段 ===
      IM_TextArea_SkinWeight: ['皮重', '从称重弹窗返回', 'TextBox', ['frmME_IssueMaterial_Weighting.GetSkinWeight']],
      IM_TextArea_GrossWeight: ['毛重', '从称重弹窗返回', 'TextBox(ReadOnly)', ['frmME_IssueMaterial_Weighting.GetGrossWeight']],
      IM_TextArea_NetWeight: ['净重', '从称重弹窗返回', 'TextBox', ['frmME_IssueMaterial_Weighting.GetNetWeight']],
      txt_superUserNM: ['授权用户', '用户输入', 'TextBox', ['指纹/密码验证→superUserNM']],
    };'''
        html = html[:map_start] + new_map + html[map_end:]

# ═══════ Replace button JS ═══════
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

new_btn = '''    // ═══════ 按钮交互 (frmME_IssueMaterial 实际事件) ═══════
    document.querySelectorAll('button[data-k]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var k = this.dataset.k;
        // 称重→打开称重弹窗 frmME_IssueMaterial_Weighting
        if (k === 'IM_Button_Weighting') { toast('📟 打开称重弹窗 frmME_IssueMaterial_Weighting(QDZY-10007)'); return }
        // 免称→跳过称重直接确认
        if (k === 'IM_Button_PassWeight') { toast('⏭ 免称模式：跳过称重步骤'); return }
        // 确认→确认发料 + ZPL标签打印
        if (k === 'IM_Button_Confirm') { if (!confirm('确认发料？\\n将保存称重数据并打印标签。')) return; toast('✅ 发料确认完成，标签已发送至打印机'); return }
        // 调料→打开余料称重
        if (k === 'IM_Button_ToMfgOrder') { toast('📦 调料 → 打开余料称重 (frmME_SurplusMaterial)'); return }
        // 取消称重
        if (k === 'IM_Button_Cancel') { if (!confirm('确认取消当前称重操作？')) return; toast('❌ 已取消称重'); return }
        // 重印按钮
        if (k === 'IM_Button_DispatchListRePrint') { toast('🖨 已发料明细重印 → ZPL打印机'); return }
        if (k === 'IM_Button_IssueMaterialReprint') { toast('🖨 原料称重明细重印 → ZPL打印机'); return }
        // 查询工单
        if (k === 'QueryButton') { toast('🔍 查询工单: BindMfgOrderNM(pageIndex=' + (Math.floor(Math.random()*3)+1) + ')'); return }
        show(k);
      })
    });'''

html = html.replace(old_btn, new_btn)

# Clean up submit functions
html = html.replace("function submitHead() { closeModal('modalHead'); toast('✅ 报废单表头已保存（模拟）') }", "// (原料称重无模态弹窗)")
html = html.replace("function submitList() { closeModal('modalList'); toast('✅ 报废单明细已保存（模拟）') }", "")

# ═══════ Write ═══════
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ demo-cs-template.html rebuilt from frmME_IssueMaterial source!")
print(f"   Size: {len(html)} bytes")
print("   4 DataGridViews: BI_MfgOrderList(9) · IM_BPRList(15) · IM_DispatchList(14) · IM_IssueMaterialList(10)")
