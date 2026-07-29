import os, glob, shutil

orig = glob.glob('natgeo_collection/pdfs_original/*.pdf')
existing = {os.path.basename(p) for p in glob.glob('natgeo_collection/pdfs/*.pdf')}
count = 0
for p in orig:
    fname = os.path.basename(p)
    if fname not in existing:
        shutil.copy2(p, f'natgeo_collection/pdfs/{fname}')
        count += 1
        print(f'Copied: {fname}')

total = len(glob.glob('natgeo_collection/pdfs/*.pdf'))
print(f'Done. Copied {count} original PDFs. Total: {total}')
