import os

base = r'E:\code\scal-pda-f\workspace\deepseek'
files = [
    'demo-cs-mfg-order.html',
    'demo-cs-pz-output.html',
    'demo-cs-equipment-start.html',
    'demo-cs-weighing-test.html',
    'demo-cs-surplus-material.html',
    'demo-cs-bpr-record.html',
    'demo-cs-template.html',
]

fixed_count = 0
for fname in files:
    path = os.path.join(base, fname)
    with open(path, 'rb') as f:
        raw = f.read()
    # Strip BOM
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    if has_bom:
        raw = raw[3:]
    # Decode as UTF-8 → garbled string
    garbled = raw.decode('utf-8')
    # Step 1: Encode garbled as GB18030 → get original bytes
    try:
        original = garbled.encode('gb18030')
    except:
        # Some chars can't be GB18030 encoded, use replace
        original = garbled.encode('gb18030', errors='replace')
    # Step 2: Decode original bytes as UTF-8
    try:
        fixed = original.decode('utf-8')
    except:
        fixed = original.decode('utf-8', errors='replace')
    # Verify
    ok = '微软雅黑' in fixed and 'MES' in fixed
    if ok:
        # Write back as UTF-8 with BOM (matching original)
        out = fixed.encode('utf-8')
        if has_bom:
            out = b'\xef\xbb\xbf' + out
        with open(path, 'wb') as f:
            f.write(out)
        print(f'OK: {fname}')
        fixed_count += 1
    else:
        print(f'SKIP: {fname} - verify failed, msyh={"微软雅黑" in fixed}')

print(f'\nFixed {fixed_count}/{len(files)} files')
