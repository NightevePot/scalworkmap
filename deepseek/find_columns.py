import re

with open(r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution\frmME_MfgOrder.cs', encoding='utf-8') as f:
    c = f.read()

print("=== HeaderText assignments ===")
for m in re.finditer(r'\.HeaderText\s*=\s*"([^"]*)"', c):
    print(f'  "{m.group(1)}"')

print("\n=== DataPropertyName assignments ===")
for m in re.finditer(r'\.DataPropertyName\s*=\s*"([^"]*)"', c):
    print(f'  "{m.group(1)}"')

print("\n=== Column Name assignments ===")
for m in re.finditer(r'\.Name\s*=\s*"([^"]*)"', c):
    print(f'  "{m.group(1)}"')

print("\n=== Columns[].HeaderText ===")
for m in re.finditer(r'Columns\["(\w+)"\]\.HeaderText\s*=\s*"([^"]*)"', c):
    print(f'  {m.group(1)}: "{m.group(2)}"')

# Also check the Designer.cs for HeaderText
with open(r'E:\code\scal-mes-client\WinClient\MES\ManufacturingExecution\frmME_MfgOrder.Designer.cs', encoding='utf-8') as f:
    dc = f.read()

print("\n=== Designer.cs HeaderText ===")
for m in re.finditer(r'\.HeaderText\s*=\s*"([^"]*)"', dc):
    print(f'  "{m.group(1)}"')

print("\nDone!")
