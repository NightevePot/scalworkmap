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
    # Step 1: Decode as UTF-8 → garbled string
    garbled = raw.decode('utf-8')
    # Step 2: Encode garbled string as GBK → get original UTF-8 bytes
    try:
        original_bytes = garbled.encode('gbk')
        # Step 3: Decode those bytes as UTF-8 → correct Chinese
        fixed = original_bytes.decode('utf-8')
        if '微软雅黑' in fixed and '寰' not in fixed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f'OK: {fname}')
            fixed_count += 1
        else:
            print(f'SKIP: {fname} - verify failed')
            # Show snippet for diagnosis
            idx = fixed.find('微软雅黑') if '微软雅黑' in fixed else -1
            gidx = fixed.find('寰') if '寰' in fixed else -1
            print(f'  msyh at {idx}, garbled at {gidx}')
    except Exception as e:
        print(f'ERROR: {fname} - {e}')

print(f'\nFixed {fixed_count}/{len(files)} files')
