import re

path = r'E:\code\scal-pda-f\workspace\deepseek\demo-cs-mfg-order.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# ReadOnly tags to add
readonly_fields = {
    '工单编号：': 'TextArea_MfgOrderNM',
    '规格描述：': 'TextArea_Description',
    '客户订单号：': 'TextArea_CustomerOrderNM',
    '生产批号：': 'TextArea_MfgBatch',
    '数量：': 'TextArea_Qty',
    '工单状态：': 'TextArea_WorkStatus',
    '修改人：': 'TextArea_ModifyBy',
}

# Editable fields (remove readonly if present)
editable_fields = {
    '完成数：': 'TextArea_CompliteQty',
    '物料编号：': 'TextArea_ProductNM',
    '销售单：': 'TextArea_SalesOrder',
    '客户：': 'TextArea_CustomerNM',
    '计划开工日期：': 'TextArea_ReleaseDate',
    '计划完工日期：': 'TextArea_PlanFinishDate',
    '单位：': 'TextArea_UOMNM',
    '修改时间：': 'TextArea_LastModifyTime',
}

# Add [自动] to readonly labels
for label_text, kid in readonly_fields.items():
    old = f'>{label_text}</label>'
    new = f'>{label_text}<span style="font-size:7pt;color:#888">[自动]</span></label>'
    if old in html:
        html = html.replace(old, new)
        print(f'  [自动] {label_text}')
    else:
        print(f'  MISS: {label_text}')

# Add [输入] to editable labels  
for label_text, kid in editable_fields.items():
    old = f'>{label_text}</label>'
    new = f'>{label_text}<span style="font-size:7pt;color:#2563eb">[输入]</span></label>'
    if old in html:
        html = html.replace(old, new)
        print(f'  [输入] {label_text}')
    else:
        print(f'  MISS: {label_text}')

# Ensure readonly fields have the right attributes
# Add readonly + background to Description and CustomerOrderNM if missing
for fix_kid in ['TextArea_Description', 'TextArea_CustomerOrderNM']:
    pattern = f'<input data-k="{fix_kid}"'
    idx = html.find(pattern)
    if idx >= 0 and 'readonly' not in html[idx:idx+300]:
        html = html.replace(pattern, pattern + ' readonly')
        # Also add background color
        style_end = html.find('>', idx) - 1
        # More targeted fix: add background to style
        old_style = f'{pattern} value="" style="flex:1;height:28px;font:9pt'
        if old_style in html:
            html = html.replace(old_style, f'{pattern} value="" readonly style="flex:1;height:28px;font:9pt;background:#F5F5F5')
            print(f'  Fixed readonly: {fix_kid}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done!')
