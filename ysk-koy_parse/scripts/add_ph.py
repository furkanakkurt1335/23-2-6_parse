import os, json
from fuzzywuzzy import fuzz
import pandas as pd

with open('village_auth_loc_list.json') as f:
    village_d = json.load(f)

phone_filepath = 'phones/phones.csv'

df = pd.read_csv(phone_filepath)

i = 1
for i in range(len(df)):
    city = df['Il'][i]
    district = df['Ilce'][i]
    village = df['Muhtarlik'][i]
    authority = df['Muhtar'][i]
    phone = df['Tel'][i]
    source = df['Kaynak'][i]
    max_ratio, max_city = 0, ''
    for city_t in village_d.keys():
        ratio_t = fuzz.token_set_ratio(city, city_t)
        if ratio_t > max_ratio:
            max_ratio, max_city = ratio_t, city_t
    if max_ratio > 80:
        sel_city = max_city
    else:
        continue
    max_ratio, max_district = 0, ''
    for district_t in village_d[sel_city].keys():
        ratio_t = fuzz.token_set_ratio(district, district_t)
        if ratio_t > max_ratio:
            max_ratio, max_district = ratio_t, district_t
    sel_village = ''
    if max_ratio > 80:
        sel_district = max_district
        max_ratio, max_village = 0, ''
        for village_t in village_d[sel_city][sel_district].keys():
            village_str = village_t.replace('KÖYÜ', '').replace('MAH.', '').strip()
            ratio_t = fuzz.token_set_ratio(village, village_str)
            if ratio_t > max_ratio:
                max_ratio, max_village = ratio_t, village_t
        if max_ratio > 80:
            sel_village = max_village
        else:
            sel_village = ''
    sel_district = ''
    if sel_village == '':
        max_ratio, max_village = 0, ''
        for district_low_t in village_d[sel_city].keys():
            for village_low_t in village_d[sel_city][district_low_t].keys():
                authority_low_t = village_d[sel_city][district_low_t][village_low_t]['authority']
                ratio_vill_low_t = fuzz.token_set_ratio(village, village_low_t)
                ratio_auth_low_t = fuzz.token_set_ratio(authority, authority_low_t)
                ratio_sum_low_t = ratio_vill_low_t + ratio_auth_low_t
                if ratio_sum_low_t > max_ratio:
                    max_ratio, max_district, max_village = ratio_sum_low_t, district_low_t, village_low_t
        if max_ratio > 160:
            sel_district = max_district
            sel_village = max_village
        else:
            sel_district = ''
            sel_village = ''
            continue
    if authority != '':
        village_d[sel_city][sel_district][sel_village]['authority'] = authority
    if phone == '':
        curr_phone = str(village_d[sel_city][sel_district][sel_village]['phone'])
        phone_l = curr_phone.split(';')
        phone_l.append(str(phone))
        phone_l = [i for i in list(set(phone_l)) if i != '']
        phone = ';'.join(phone_l)
        village_d[sel_city][sel_district][sel_village]['phone'] = phone
        village_d[sel_city][sel_district][sel_village]['source'] = source
        i += 1

print(i, 'records added.')

# with open('village_auth_loc_list.json', 'w') as f:
#     json.dump(village_d, f, indent=4, ensure_ascii=False)
