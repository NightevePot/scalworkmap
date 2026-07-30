import re

with open(r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution\frmME_MfgOrder.Designer.cs', 'r', encoding='utf-8') as f:
    c = f.read()

# Extract all Dock assignments
docks = {}
for m in re.finditer(r'this\.(\w+)\.Dock\s*=\s*System\.Windows\.Forms\.DockStyle\.(\w+)', c):
    docks[m.group(1)] = m.group(2)

# Extract sizes
sizes = {}
for m in re.finditer(r'this\.(\w+)\.Size\s*=\s*new\s+System\.Drawing\.Size\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', c):
    sizes[m.group(1)] = (int(m.group(2)), int(m.group(3)))

# Extract locations
locs = {}
for m in re.finditer(r'this\.(\w+)\.Location\s*=\s*new\s+System\.Drawing\.Point\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', c):
    locs[m.group(1)] = (int(m.group(2)), int(m.group(3)))

# TabControl
tabs_add = re.findall(r'this\.(\w+)\.TabPages\.Add\(this\.(\w+)\)', c)
for tab, page in tabs_add:
    # Find tab page text
    tm = re.search(r'this\.(\w+)\.Text\s*=\s*"([^"]*)"', c)
    
# All text values
texts = {}
for m in re.finditer(r'this\.(\w+)\.Text\s*=\s*"([^"]*)"', c):
    texts[m.group(1)] = m.group(2)

# Find Controls.Add to understand hierarchy
print("=== Controls.Add (hierarchy) ===")
for m in re.finditer(r'this\.(\w+)\.Controls\.Add\(this\.(\w+)\)', c):
    parent, child = m.groups()
    dock = docks.get(child, '-')
    sz = sizes.get(child, (0,0))
    txt = texts.get(child, '')
    print(f'  {parent} -> {child}  Dock={dock}  Size={sz}  Text="{txt[:30]}"')

print("\n=== Top-level panel structure ===")
# Find the main container structure
for m in re.finditer(r'this\.(\w+)\.Dock\s*=\s*System\.Windows\.Forms\.DockStyle\.(\w+)', c):
    name, dock = m.groups()
    # Find which panel contains this
    parent = '?'
    for pm in re.finditer(r'this\.(\w+)\.Controls\.Add\(this\.' + re.escape(name) + r'\)', c):
        parent = pm.group(1)
    sz = sizes.get(name, (0,0))
    print(f'  {name}: Dock={dock} Size={sz}  Parent={parent}')

print("\n=== TabControl Pages ===")
for tc, tp in re.findall(r'this\.(\w+)\.TabPages\.Add\(this\.(\w+)\)', c):
    txt = texts.get(tp, '?')
    print(f'  {tc} contains {tp}: "{txt}"')
