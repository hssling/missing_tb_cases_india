import zipfile
import os

os.makedirs('extracted_sources', exist_ok=True)

zips = ['archive (3).zip', 'archive (4).zip']
for zip_name in zips:
    zpath = os.path.join('SOURCES DATA', zip_name)
    if os.path.exists(zpath):
        with zipfile.ZipFile(zpath, 'r') as z:
            z.extractall('extracted_sources')
        print(f"Extracted {zip_name} to extracted_sources/")
    else:
        print(f"{zpath} not found")

print("\nContents of extracted_sources/:")
for root, dirs, files in os.walk('extracted_sources'):
    level = root.replace('extracted_sources', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files[:10]:  # first 10 files
        print(f"{subindent}{file}")
    if len(files) > 10:
        print(f"{subindent}... and {len(files)-10} more files")
