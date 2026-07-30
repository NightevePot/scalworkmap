import os, glob

base = r'E:\code\scal-pda-f\workspace\deepseek'

# Files to fix (all CS demos except scrap-order which is correct)
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
    # The file was saved as UTF-8 but Chinese chars were double-encoded.
    # Fix: decode as UTF-8 → encode as Latin-1 → decode as UTF-8
    try:
        broken = raw.decode('utf-8')
        fixed = broken.encode('latin-1').decode('utf-8')
        # Verify the fix worked (check for common correct Chinese chars)
        if '微软雅黑' in fixed and '寰' not in fixed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f'OK: {fname}')
            fixed_count += 1
        else:
            print(f'SKIP: {fname} - already correct or different encoding')
    except Exception as e:
        print(f'ERROR: {fname} - {e}')

print(f'\nFixed {fixed_count}/{len(files)} files')
