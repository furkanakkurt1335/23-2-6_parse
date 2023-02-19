import json
from fuzzywuzzy import fuzz
import pandas as pd
import os

phone_access_path = 'phone_access_sheets'
file_path = os.path.join(phone_access_path, 'hatay.xlsx')
sheet_d = pd.read_excel(file_path, sheet_name=None)
hatay_phone_l = list()

city = 'Hatay'
for key in sheet_d.keys():
    df = sheet_d[key]
    cols = df.columns
    for i in range(len(df)):
        district = key
        village = df[cols[0]][i]
        loc = f'{city} {district} {village}'
        hatay_phone_l.append(loc)

print('Our Hatay villages:', len(hatay_phone_l))

with open('data.json', 'r') as f:
    data = json.load(f)
feats = data['features']

itub_hatay_l = list()
for feat in feats:
    attr = feat['attributes']
    g_id = attr['globalid']
    loc = attr['k_y_adi']
    if loc != None and loc not in itub_hatay_l and 'hatay' in loc.lower():
        itub_hatay_l.append(loc)

print('Itub Hatay villages:', len(itub_hatay_l))

match_count = 0
for loc in hatay_phone_l:
    max_ratio, match = 0, ''
    for itub_loc in itub_hatay_l:
        ratio_t = fuzz.token_set_ratio(loc, itub_loc)
        if ratio_t > max_ratio:
            max_ratio = ratio_t
            match = itub_loc
    if max_ratio > 90:
        print('Matched:', loc, match, max_ratio)
        match_count += 1
    else:
        print('Unmatched:', loc)

print('Matched:', match_count)
print('Unmatched:', len(itub_hatay_l) - match_count)