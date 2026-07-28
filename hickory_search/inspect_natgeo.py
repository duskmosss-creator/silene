import sys
sys.stdout.reconfigure(encoding='utf-8')
from libzim.reader import Archive
import re

a = Archive('zim_downloads/National_Geographic_Appalachian_Collection.zim')

pdfs_to_check = [
    'pdfs/nationalgeograph11889nati.pdf',
    'pdfs/nationalgeograph37natiuoft.pdf',
    'pdfs/194701to12.pdf',
    'pdfs/194905.pdf',
    'pdfs/195011.pdf',
    'pdfs/195105.pdf',
    'pdfs/195204.pdf',
    'pdfs/195304.pdf',
    'pdfs/jishankhan_hotmail_1954.pdf',
    'pdfs/sim_national-geographic_1969-12_136_6.pdf',
    'pdfs/national-geographic-1972-10.pdf',
    'pdfs/sim_national-geographic_1985-06_167_6.pdf',
    'pdfs/sim_national-geographic_1985-12_168_6.pdf',
    'pdfs/national-geographic-1988-07.pdf',
    'pdfs/national-geographic-1996-09.pdf',
    'pdfs/sim_national-geographic_1999-12_196_6.pdf',
    'pdfs/national-geographic-2006-08.pdf',
    'pdfs/sim_national-geographic_2016-05_229_5.pdf',
    'pdfs/sim_national-geographic_2020-04_237_4.pdf',
    'pdfs/sim_national-geographic_2023-01_243_1.pdf',
    'pdfs/national-geographic-2024-01.pdf',
]

missing = []
present = []
for p in pdfs_to_check:
    if a.has_entry_by_path(p):
        item = a.get_entry_by_path(p).get_item()
        size_kb = item.size // 1024
        present.append((p, size_kb))
        print(f'  [OK]     {p}  ({size_kb} KB)')
    else:
        missing.append(p)
        print(f'  [MISSING] {p}')

print(f'\nTotal: {len(present)} present, {len(missing)} missing')
