# Fuel-Specific End Use EUI by Building Type — Census Division Analysis
# Source: U.S. EIA 2018 Commercial Buildings Energy Consumption Survey (CBECS)
# Public use microdata file: cbecs2018_final_public.csv
# User selects a census division (1-9) at runtime
# Calculates median electricity and natural gas EUI by end use for each building type
# End uses: lighting, space cooling, space heating, ventilation, refrigeration (electric)
#           space heating, water heating, cooking (natural gas)
# Output: wide summary table ranked by total median EUI, all 20 building types
# Demonstrates: nested dictionaries, user-defined functions, safe value extraction,
#               multi-column analysis, tuple unpacking, generator expressions

import csv
import statistics

pba_codes = {
    '1':  'Vacant',
    '2':  'Office',
    '4':  'Laboratory',
    '5':  'Nonrefrigerated warehouse',
    '6':  'Food sales',
    '7':  'Public order and safety',
    '8':  'Outpatient health care',
    '11': 'Refrigerated warehouse',
    '12': 'Religious worship',
    '13': 'Public assembly',
    '14': 'Education',
    '15': 'Food service',
    '16': 'Inpatient health care',
    '17': 'Nursing',
    '18': 'Lodging',
    '23': 'Strip shopping center',
    '24': 'Enclosed mall',
    '25': 'Retail other than mall',
    '26': 'Service',
    '91': 'Other'
}
cendiv_names = {
    '1': 'New England',
    '2': 'Middle Atlantic',
    '3': 'East North Central',
    '4': 'West North Central',
    '5': 'South Atlantic',
    '6': 'East South Central',
    '7': 'West South Central',
    '8': 'Mountain',
    '9': 'Pacific',
}

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "cbecs2018_final_public.csv"
fh = open(fname)
reader = csv.reader(fh)
headers = next(reader)
cendiv_idx = headers.index('CENDIV')
pba_idx = headers.index('PBA')
sqft_idx = headers.index('SQFT')
mfbtu_idx = headers.index('MFBTU')
elltbtu_idx = headers.index('ELLTBTU')
elclbtu_idx = headers.index('ELCLBTU')
elhtbtu_idx = headers.index('ELHTBTU')
elvnbtu_idx = headers.index('ELVNBTU')
elrfbtu_idx = headers.index('ELRFBTU')
nghtbtu_idx = headers.index('NGHTBTU')
ngwtbtu_idx = headers.index('NGWTBTU')
ngckbtu_idx = headers.index('NGCKBTU')

def safe_eui(idx):
    try:
        return float(row[idx]) / sqft
    except:
        return 0.0

cendiv_code = input("Enter census division code: ")
if cendiv_code not in cendiv_names:
    print("Invalid census division code.  Please enter a number between 1 and 9.")
    exit() 
cendiv_name = cendiv_names[cendiv_code]

data = dict()
for row in reader:
    try:
        if row[cendiv_idx] != cendiv_code:
            continue
        sqft = float(row[sqft_idx])
        if sqft <= 0:
            continue
        mfbtu = float(row[mfbtu_idx])
        pba = row[pba_idx]

        if pba not in data:
            data[pba] = {
                'total': [], 'el_lt': [], 'el_cl': [], 
                'el_ht': [], 'el_vn': [], 'el_rf': [], 
                'ng_ht': [], 'ng_wt': [], 'ng_ck': []
            }

        data[pba]['total'].append(mfbtu / sqft)
        data[pba]['el_lt'].append(safe_eui(elltbtu_idx))
        data[pba]['el_cl'].append(safe_eui(elclbtu_idx))
        data[pba]['el_ht'].append(safe_eui(elhtbtu_idx))
        data[pba]['el_vn'].append(safe_eui(elvnbtu_idx))
        data[pba]['el_rf'].append(safe_eui(elrfbtu_idx))
        data[pba]['ng_ht'].append(safe_eui(nghtbtu_idx))
        data[pba]['ng_wt'].append(safe_eui(ngwtbtu_idx))
        data[pba]['ng_ck'].append(safe_eui(ngckbtu_idx))
    except:
        continue
#print(data)

results = []
for pba, d in data.items():
    name = pba_codes[pba]
    n = len(d['total'])
    results.append((
        name, n,
        round(statistics.median(d['total']), 1),
        round(statistics.median(d['el_lt']), 1),
        round(statistics.median(d['el_cl']), 1),
        round(statistics.median(d['el_ht']), 1),
        round(statistics.median(d['el_vn']), 1),
        round(statistics.median(d['el_rf']), 1),
        round(statistics.median(d['ng_ht']), 1),
        round(statistics.median(d['ng_wt']), 1),
        round(statistics.median(d['ng_ck']), 1),
    ))

results.sort(key=lambda x: x[2], reverse=True)

for row in results:
    name, n, total, el_lt, el_cl, el_ht, el_vn, el_rf, ng_ht, ng_wt, ng_ck = row
    #print(row)

print(f"Fuel-Specific End Use EUI by Building Type - {cendiv_name} Division")
print(f"Metric: Median EUI (kBtu/sq ft) | Source: 2018 CBECS Microdata")
print() 
print(f"{'Building Type':<30} {'n':>4} {'Total':>7} {'EL-Lt':>7} {'EL-Cl':>7} {'EL-Ht':>7} {'EL-Vn':>7} {'EL-Rf':>7} {'NG-Ht':>7} {'NG-Wt':>7} {'NG-Ck':>7}")
print(f"{'':30} {'':4} {'':7} {'(Lite)':>7} {'(Cool)':>7} {'(Heat)':>7} {'(Vent)':>7} {'(Refr)':>7} {'(Heat)':>7} {'(Watr)':>7} {'(Cook)':>7}")
print("-" * 105)

for row in results:
    name, n, total, el_lt, el_cl, el_ht, el_vn, el_rf, ng_ht, ng_wt, ng_ck = row
    print(f"{name:<30} {n:>4} {total:>7.1f} {el_lt:>7.1f} {el_cl:>7.1f} {el_ht:>7.1f} {el_vn:>7.1f} {el_rf:>7.1f} {ng_ht:>7.1f} {ng_wt:>7.1f} {ng_ck:>7.1f}")

print("-" * 105)
print("EL=Electricity, NG=Natural gas | Lt=Lighting, Cl=Cooling, Ht=Heating, Vn=Ventilation, Rf=Refrigeration, Wt=Water heating, Ck=Cooking")
print(f"\nTotal buildings analyzed: {sum(r[1] for r in results)}")