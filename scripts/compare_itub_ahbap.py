import pandas as pd
from fuzzywuzzy import fuzz
import json

df = pd.read_csv('Teyitli Enkaz Altı ve Erzak Verileri - İhtiyaç Verileri.csv', encoding='utf-8')
ahbap_loc_l = list()
for i in range(len(df)):
    loc_l = list()
    city = df['İl'][i]
    if city == city:
        loc_l.append(city)
    district = df['İlçe'][i]
    if district == district:
        loc_l.append(district)
    village = df['İhtiyaç - Açık Adresi'][i]
    if village == village:
        loc_l.append(village)
        location = ' '.join(loc_l)
        ahbap_loc_l.append(location)

with open('ahbap_loc_l.json', 'w', encoding='utf-8') as f:
    json.dump(ahbap_loc_l, f, ensure_ascii=False, indent=4)

df = pd.read_csv('results.csv', encoding='utf-8')
itub_loc_l = list()
for i in range(len(df)):
    loc_l = list()
    city = df['İl'][i]
    if city == city:
        loc_l.append(city)
    district = df['İlçe'][i]
    if district == district:
        loc_l.append(district)
    village = df['Köy'][i]
    if village == village:
        loc_l.append(village)
        location = ' '.join(loc_l)
        itub_loc_l.append(location)

with open('itub_loc_l.json', 'w', encoding='utf-8') as f:
    json.dump(itub_loc_l, f, ensure_ascii=False, indent=4)

for ahbap_loc in ahbap_loc_l:
    max_ratio, max_location = 0, ''
    for itub_loc in itub_loc_l:
        ratio = fuzz.token_set_ratio(ahbap_loc, itub_loc)
        if ratio > max_ratio:
            max_ratio = ratio
            max_location = itub_loc
    if max_ratio > 90:
        print('ahbap:', ahbap_loc)
        print('itub:', max_location)
        print('ratio:', max_ratio)
        print()
        input()