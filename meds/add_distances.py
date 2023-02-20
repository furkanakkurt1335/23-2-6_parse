import os, json
import pandas as pd
from fuzzywuzzy import fuzz

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

df = pd.read_excel(os.path.join(THIS_FOLDER, 'köyler_tıbbi_yardım.xls'))

with open(os.path.join(THIS_FOLDER, '../data/village_auth_loc_list.json'), 'r') as f:
    village_d = json.load(f)

dist_d = dict()
for city in village_d.keys():
    for district in village_d[city].keys():
        for neighborhood in village_d[city][district].keys():
            if 'distance' in village_d[city][district][neighborhood].keys():
                dist = village_d[city][district][neighborhood]['distance']
            else:
                dist = '?'
            loc = f'{city} {district} {neighborhood}'
            dist_d[loc] = dist

for i in range(len(df)):
    city = df.iloc[i]['İl']
    district = df.iloc[i]['İlçe']
    neighborhood = df.iloc[i]['Mahalle']
    loc = f'{city} {district} {neighborhood}'
    max_ratio, sel_dist = 0, 0
    for loc2 in dist_d.keys():
        ratio = fuzz.token_set_ratio(loc, loc2)
        if ratio > max_ratio:
            max_ratio = ratio
            sel_dist = dist_d[loc2]
    if max_ratio > 80:
        df.loc[i, 'Mesafe'] = sel_dist
    else:
        df.loc[i, 'Mesafe'] = '?'

df.to_excel(os.path.join(THIS_FOLDER, 'köyler_tıbbi_yardım_mesafe.xls'), index=False)
