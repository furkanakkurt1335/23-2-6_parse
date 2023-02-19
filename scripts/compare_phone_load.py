import json
import pandas as pd
from fuzzywuzzy import fuzz

icisleri_df = pd.read_csv('icisleri.csv', encoding='utf-8')
auth_l = list()
for i in range(len(icisleri_df)):
    city = icisleri_df['Il'][i]
    district = icisleri_df['Ilce'][i]
    village = icisleri_df['Muhtarlik'][i]
    loc = f'{city} {district} {village}'
    auth_l.append(loc)

with open('data.json', 'r') as f:
    data = json.load(f)
feats = data['features']

itub_auth_l = list()
for feat in feats:
    attr = feat['attributes']
    g_id = attr['globalid']
    loc = attr['k_y_adi']
    if loc != None and loc not in itub_auth_l and 'kahramanmara' in loc.lower():
        itub_auth_l.append(loc)

matched_l = list()
for loc in auth_l:
    max_ratio, match = 0, ''
    for itub_loc in itub_auth_l:
        ratio_t = fuzz.token_set_ratio(loc, itub_loc)
        if ratio_t > max_ratio:
            max_ratio = ratio_t
            match = itub_loc
    if max_ratio > 90:
        matched_l.append((loc, match, max_ratio))
        print(loc, match, max_ratio)

print(len(matched_l))
