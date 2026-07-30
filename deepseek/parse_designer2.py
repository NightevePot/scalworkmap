import os, re

base = r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution'
files = [
    'frmME_MfgOrder.Designer.cs',
    'frmME_PZOutput.Designer.cs',
    'frmME_EquipmentStart.Designer.cs',
    'frmME_WeightingTest.Designer.cs',
    'frmME_SurplusMaterial.Designer.cs',
    'frmME_IssueMaterial_Weighting.Designer.cs',
    'frmME_BPRRecord.Designer.cs',
]

for fname in files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        print(f'MISSING: {fname}')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'\n{"="*60}')
    print(f'FORM: {os.path.splitext(os.path.basename(fname))[0]}')
    print(f'{"="*60}')
    
    # Form size
    m = re.search(r'this\.ClientSize\s*=\s*new\s+System\.Drawing\.Size\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content)
    if m: print(f'  Form Size: {m.group(1)} x {m.group(2)}')
    
    # All Location entries: name -> (x, y)
    locs = {}
    for m in re.finditer(r'this\.(\w+)\.Location\s*=\s*new\s+System\.Drawing\.Point\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content):
        locs[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    
    # All Size entries: name -> (w, h)
    sizes = {}
    for m in re.finditer(r'this\.(\w+)\.Size\s*=\s*new\s+System\.Drawing\.Size\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', content):
        sizes[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    
    # All Text entries
    texts = {}
    for m in re.finditer(r'this\.(\w+)\.Text\s*=\s*"([^"]*)"', content):
        texts[m.group(1)] = m.group(2)
    
    # Control types from constructors
    ctors = {}
    for m in re.finditer(r'this\.(\w+)\s*=\s*new\s+(\S+)\s*\(\)', content):
        ctors[m.group(1)] = m.group(2).split('.')[-1]
    
    # All Dock settings
    docks = {}
    for m in re.finditer(r'this\.(\w+)\.Dock\s*=\s*System\.Windows\.Forms\.DockStyle\.(\w+)', content):
        docks[m.group(1)] = m.group(2)
    
    # Extract buttons
    buttons = []
    for name, (x, y) in locs.items():
        ctype = ctors.get(name, '')
        if 'Button' in ctype:
            sz = sizes.get(name, (0, 0))
            txt = texts.get(name, '')
            buttons.append((name, txt, x, y, sz[0], sz[1]))
    
    if buttons:
        print(f'\n  Buttons ({len(buttons)}):')
        for name, txt, x, y, w, h in sorted(buttons, key=lambda b: (b[3], b[2])):
            print(f'    "{txt}" at ({x},{y}) {w}x{h}')
    
    # Extract DataGridViews  
    dgvs = []
    for name, (x, y) in locs.items():
        ctype = ctors.get(name, '')
        if 'DataGridView' in ctype:
            sz = sizes.get(name, (0, 0))
            dgvs.append((name, x, y, sz[0], sz[1]))
    
    if dgvs:
        print(f'\n  DataGridViews ({len(dgvs)}):')
        for name, x, y, w, h in dgvs:
            dock = docks.get(name, 'None')
            print(f'    {name} at ({x},{y}) {w}x{h} Dock={dock}')
    
    # Extract labels
    labels = [(name, texts.get(name,''), x, y) for name, (x, y) in locs.items() if 'Label' in ctors.get(name,'')]
    
    # Extract text inputs (TextBox, ComboBox, DateTimePicker, ComboGrid)
    inputs = []
    for name, (x, y) in locs.items():
        ctype = ctors.get(name, '')
        if any(t in ctype for t in ['TextBox','Combo','DateTime','ComboGrid']):
            sz = sizes.get(name, (0, 0))
            # Find nearby label
            lbl = ''
            for ln, lt, lx, ly in labels:
                if abs(ly - y) <= 3 and lx < x:
                    lbl = lt
                    break
            inputs.append((name, lbl, ctype, x, y, sz[0], sz[1]))
    
    if inputs:
        print(f'\n  Input Fields ({len(inputs)}):')
        for name, lbl, ctype, x, y, w, h in sorted(inputs, key=lambda i: (i[4], i[3])):
            print(f'    [{ctype}] {name}: "{lbl}" at ({x},{y}) {w}x{h}')
    
    # Grid columns (for each DGV, find columns)
    for dname, _, _, _, _ in dgvs:
        col_hdrs = re.findall(r'this\.(\w+)\.HeaderText\s*=\s*"([^"]*)"', content)
        col_widths = {m.group(1): int(m.group(2)) for m in re.finditer(r'this\.(\w+)\.Width\s*=\s*(\d+)', content)}
        # Only show columns that are likely part of this DGV (heuristic: same prefix)
        prefix = dname.split('_')[0] if '_' in dname else dname[:5]
        cols = [(h, col_widths.get(n, 0)) for n, h in col_hdrs if n.startswith(dname) or prefix in n.lower()]
        if cols:
            print(f'\n    {dname} columns:')
            for h, w in cols:
                print(f'      {h} (w={w})')

print('\nDone!')
