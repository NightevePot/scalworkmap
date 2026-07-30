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
    # Remove BOM if present
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    # Step 1: Decode as UTF-8 → garbled string
    garbled = raw.decode('utf-8')
    # Step 2: Encode garbled string as GBK → get original UTF-8 bytes
    try:
        # Filter out characters that can't be encoded in GBK (like BOM remnants)
        # Try gbk first, fall back to ignoring errors
        original_bytes = garbled.encode('gbk', errors='replace')
        # Step 3: Decode as UTF-8 → correct Chinese
        fixed = original_bytes.decode('utf-8', errors='replace')
        if '微软雅黑' in fixed:
            # Write without BOM
            with open(path, 'w', encoding='utf-8-sig') as f:
                f.write(fixed)
            print(f'OK: {fname}')
            fixed_count += 1
        else:
            # Try gb18030 as fallback
            original_bytes2 = garbled.encode('gb18030')
            fixed2 = original_bytes2.decode('utf-8', errors='replace')
            if '微软雅黑' in fixed2:
                with open(path, 'w', encoding='utf-8-sig') as f:
                    f.write(fixed2)
                print(f'OK(gb18030): {fname}')
                fixed_count += 1
            else:
                print(f'SKIP: {fname} - unrecognized encoding pattern')
    except Exception as e:
        print(f'ERROR: {fname} - {e}')

print(f'\nFixed {fixed_count}/{len(files)} files')
