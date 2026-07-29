import os, glob, re

pdfs = [
'194701to12.pdf', '194905.pdf', '195011.pdf', '195105.pdf', '195204.pdf', '195304.pdf',
'201603_201905.pdf', '201608_201905.pdf', '201610_201905.pdf', '201612_201905.pdf',
'2017011.pdf', '201703_201905.pdf', '201704_201905.pdf', '201709_201905.pdf',
'bub_gb_LNQKAAAAYAAJ.pdf', 'bub_gb_rgcVAAAAYAAJ.pdf', 'bub_gb_TAUVAAAAYAAJ.pdf',
'jstor-1764816.pdf', 'nationalgeograp131902nati.pdf', 'nationalgeograp161905nati.pdf',
'nationalgeograp171906nati.pdf', 'nationalgeograp211910nati.pdf', 'nationalgeograp241913nati.pdf',
'nationalgeograp301916nati.pdf', 'nationalgeograp311917nati.pdf', 'nationalgeograp321917nati.pdf',
'nationalgeograp331918nati.pdf', 'nationalgeograp371920nati.pdf', 'nationalgeograp401921nati.pdf',
'nationalgeograp421922nati.pdf', 'nationalgeograph11889nati.pdf', 'nationalgeograph12natiuoft.pdf',
'nationalgeograph19natiuoft.pdf', 'nationalgeograph2009unse.pdf', 'nationalgeograph21natiuoft.pdf',
'nationalgeograph271915nati.pdf', 'nationalgeograph281915nat.pdf', 'nationalgeograph31891nati.pdf',
'nationalgeograph31natiuoft.pdf', 'nationalgeograph351919nat.pdf', 'nationalgeograph36natiuoft.pdf',
'nationalgeograph37natiuoft.pdf', 'nationalgeograph38natiuoft.pdf', 'nationalgeograph39natiuoft.pdf',
'nationalgeograph41892nati.pdf', 'nationalgeograph71896nati.pdf', 'nationalgeograph81897nati.pdf',
'nationalgeographicusa-august2019.pdf', 'nationalgeographicusa-june2019.pdf',
'NationalGeographicUSASeptember2018.pdf', 'NG201706.pdf', 'sim_national-geographic_1888_1_1.pdf',
'sim_national-geographic_the-national-geographic-magazine_1888_1_1.pdf'
]

def parse_date(filename):
    if filename == '194701to12.pdf': return (1947, 1)
    if filename == '194905.pdf': return (1949, 5)
    if filename == '195011.pdf': return (1950, 11)
    if filename == '195105.pdf': return (1951, 5)
    if filename == '195204.pdf': return (1952, 4)
    if filename == '195304.pdf': return (1953, 4)
    
    if filename.startswith('20'):
        m = re.search(r'^(20\d\d)(\d\d)', filename)
        if m: 
            month = int(m.group(2))
            if month > 12: month = 1
            return (int(m.group(1)), month)
            
    m = re.search(r'NG(20\d\d)(\d\d)', filename)
    if m: return (int(m.group(1)), int(m.group(2)))
    
    m = re.search(r'(20\d\d)', filename)
    if m:
        year = int(m.group(1))
        month = 1
        name = filename.lower()
        if 'january' in name or 'jan' in name: month = 1
        elif 'february' in name or 'feb' in name: month = 2
        elif 'march' in name or 'mar' in name: month = 3
        elif 'april' in name or 'apr' in name: month = 4
        elif 'may' in name: month = 5
        elif 'june' in name or 'jun' in name: month = 6
        elif 'july' in name or 'jul' in name: month = 7
        elif 'august' in name or 'aug' in name: month = 8
        elif 'september' in name or 'sep' in name: month = 9
        elif 'october' in name or 'oct' in name: month = 10
        elif 'november' in name or 'nov' in name: month = 11
        elif 'december' in name or 'dec' in name: month = 12
        return (year, month)
        
    m = re.search(r'1888_1_1', filename)
    if m: return (1888, 1)
    
    m = re.search(r'(18\d\d|19\d\d)', filename)
    if m: return (int(m.group(1)), 1)
    
    return (9999, 1)

parsed = []
for p in pdfs:
    parsed.append((p, parse_date(p)))

parsed.sort(key=lambda x: x[1])

for p, (y, m) in parsed:
    print(f"{y}-{m:02d} : {p}")
