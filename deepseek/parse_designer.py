import os, re, glob

base = r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution'
files = [
    'frmME_MfgOrder.Designer.cs',
    'frmME_PZOutput.Designer.cs',
    'frmME_EquipmentStart.Designer.cs',
    'frmME_WeightingTest.Designer.cs',
    'frmME_SurplusMaterial.Designer.cs',
    'frmME_IssueMaterial_Weighting.Designer.cs',
    'frmME_BPRRecord.Designer.cs',
    'frmME_ScrapOrder/frmME_ScrapOrder.Designer.cs',
]

for fname in files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        print(f'MISSING: {fname}')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    form_name = os.path.splitext(os.path.basename(fname))[0]
    print(f'\n{"="*60}')
    print(f'FORM: {form_name}')
    print(f'{"="*60}')
    
    # Form size
    m = re.search(r'this\.ClientSize\s*=\s*new\s+System\.Drawing\.Size\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content)
    if m:
        print(f'  Size: {m.group(1)} x {m.group(2)}')
    
    # TabControl tabs
    tabs = re.findall(r'this\.(\w+)\.Text\s*=\s*"([^"]+)"', content)
    tab_names = {}
    for name, text in tabs:
        if 'tabPage' in name.lower() or 'tab' in name.lower():
            tab_names[name] = text
    if tab_names:
        print(f'  Tabs: {len(tab_names)} pages')
        for n, t in tab_names.items():
            print(f'    - {t}')
    
    # All controls with Location and Size
    controls = []
    # Find all control declarations (controlName.Location = ...)
    locs = dict(re.findall(r'this\.(\w+)\.Location\s*=\s*new\s+System\.Drawing\.Point\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content))
    sizes = dict(re.findall(r'this\.(\w+)\.Size\s*=\s*new\s+System\.Drawing\.Size\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content))
    texts = dict(re.findall(r'this\.(\w+)\.Text\s*=\s*"([^"]*)"', content))
    
    # Categorize controls
    panels = []
    buttons = []
    labels = []
    dgvs = []
    textboxes = []
    
    all_ctrl_names = set()
    for name in locs:
        all_ctrl_names.add(name)
    for name in sizes:
        all_ctrl_names.add(name)
    
    # Determine control type from constructor
    ctor_map = {}
    for m in re.finditer(r'this\.(\w+)\s*=\s*new\s+(\S+)\s*\(\)', content):
        ctor_name, ctor_type = m.groups()
        ctor_type = ctor_type.split('.')[-1]
        ctor_map[ctor_name] = ctor_type
    
    for name in sorted(all_ctrl_names):
        ctype = ctor_map.get(name, '?')
        loc = locs.get(name, (0,0))
        sz = sizes.get(name, (0,0))
        txt = texts.get(name, '')
        
        if 'Panel' in ctype or ctype == 'Panel':
            panels.append((name, txt, int(loc[0]), int(loc[1]), int(sz[0]), int(sz[1])))
        elif 'Button' in ctype or ctype == 'Button':
            buttons.append((name, txt, int(loc[0]), int(loc[1]), int(sz[0]), int(sz[1])))
        elif 'Label' in ctype or ctype == 'Label':
            labels.append((name, txt, int(loc[0]), int(loc[1]), int(sz[0]), int(sz[1])))
        elif 'DataGridView' in ctype or ctype == 'DataGridView':
            dgvs.append((name, txt, int(loc[0]), int(loc[1]), int(sz[0]), int(sz[1])))
        elif 'TextBox' in ctype or 'Combo' in ctype or 'DateTime' in ctype:
            textboxes.append((name, txt, int(loc[0]), int(loc[1]), int(sz[0]), int(sz[1])))
    
    # Print buttons
    if buttons:
        print(f'  Buttons ({len(buttons)}):')
        for name, txt, x, y, w, h in sorted(buttons, key=lambda b: (b[3], b[2])):
            print(f'    [{txt}] at ({x},{y}) {w}x{h}')
    
    # Print DataGridViews
    if dgvs:
        print(f'  DataGridViews ({len(dgvs)}):')
        for name, txt, x, y, w, h in dgvs:
            print(f'    [{name}] at ({x},{y}) {w}x{h}')
            # Find columns for this DGV
            col_pattern = re.compile(rf'this\.(\w+)\.HeaderText\s*=\s*"([^"]*)"')
            width_pattern = re.compile(rf'this\.(\w+)\.Width\s*=\s*(\d+)')
            cols = col_pattern.findall(content)
            widths = dict(width_pattern.findall(content))
            # Filter columns likely belonging to this DGV
            print(f'      Columns:')
            for cn, ch in cols:
                cw = widths.get(cn, '?')
                if cn not in texts and cn not in [b[0] for b in buttons]:
                    print(f'        {ch} (w={cw})')
    
    # Print textboxes/combos
    if textboxes:
        print(f'  TextBoxes/Combos ({len(textboxes)}):')
        for name, txt, x, y, w, h in sorted(textboxes, key=lambda t: (t[3], t[2]))[:15]:
            lbl = ''
            for ln, lt, lx, ly, lw, lh in labels:
                if abs(ly - y) < 5 and lx < x:
                    lbl = f' [{lt}]'
                    break
            print(f'    [{name}] {txt} at ({x},{y}) {w}x{h}{lbl}')

print('\nDone!')
