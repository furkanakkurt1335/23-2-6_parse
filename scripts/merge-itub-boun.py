import os, json, csv
import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime
import numpy as np
from geopy.geocoders import Nominatim

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

cols_tr_en_path = os.path.join(THIS_FOLDER, 'cols_tr-en.json')
with open(cols_tr_en_path, 'r') as f:
    cols_tr_en_d = json.load(f)
cols_en_tr_path = os.path.join(THIS_FOLDER, 'cols_en-tr.json')
with open(cols_en_tr_path, 'r') as f:
    cols_en_tr_d = json.load(f)

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
city_l = ['maras', 'kilis', 'hatay', 'adiyaman']
city_d = {'maras': 'Kahramanmaraş', 'kilis': 'Kilis', 'hatay': 'Hatay', 'adiyaman': 'Adıyaman'}
df = pd.DataFrame()
merged_l = list()
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        for i in range(len(df_t[sheet_t])):
            d_t = {cols_en_tr_d['city']: city_d[city], cols_en_tr_d['district']: sheet_t}
            for col in df_t[sheet_t].columns:
                el_t = df_t[sheet_t][col][i]
                if isinstance(el_t, (datetime)):
                    el_t = str(el_t.month) + '-' + str(el_t.day)
                if isinstance(el_t, (int, np.integer)):
                    el_t = str(el_t)
                if isinstance(el_t, (bool, np.bool_)):
                    el_t = str(el_t)
                col_to_use = cols_en_tr_d[cols_tr_en_d[col]]
                if el_t == el_t:
                    d_t[col_to_use] = el_t
                else:
                    d_t[col_to_use] = ''
            merged_l.append(d_t)

village_auth_loc_data_path = os.path.join(THIS_FOLDER, '../data/village_auth_loc_list.json')
with open(village_auth_loc_data_path, 'r') as f:
    village_d = json.load(f)

itub_folder = os.path.join(THIS_FOLDER, '../itub-data')
with open(os.path.join(itub_folder, 'itub-all-api-data.json'), 'r') as f:
    itub_d = json.load(f)
feats = itub_d['features']
with open(os.path.join(THIS_FOLDER, 'itub_attr.json'), 'r') as f:
    attr_d = json.load(f)
for feat in feats:
    d_t = dict()
    attr = feat['attributes']
    if not attr[attr_d['village']]:
        x, y = feat['geometry']['x'], feat['geometry']['y']
        geolocator = Nominatim(user_agent="itub")
        location = geolocator.reverse(f'{y}, {x}')
        address = location.raw['address']
        if 'city' in address.keys():
            city = address['city']
        else:
            city = ''
        if 'town' in address.keys():
            district = address['town']
        else:
            district = ''
        if 'suburb' in address.keys():
            village = address['suburb']
        else:
            village = ''
    else:
        city, district, village = '', '', attr[attr_d['village']].replace('/', ',')
    if village.count(',') > 1:
        vl_l = village.split(',')
        city, district, village = vl_l[0].strip(), vl_l[1].strip(), vl_l[2].strip()
    else:
        village = village.strip()
    d_t[cols_en_tr_d['city']] = city
    d_t[cols_en_tr_d['district']] = district
    d_t[cols_en_tr_d['village']] = village
    loc = f'{city} {district} {village}'
    max_score, max_city, max_district, max_village, max_auth, max_phone = 0, '', '', '', '', ''
    for city in village_d.keys():
        for district in village_d[city].keys():
            for village in village_d[city][district].keys():
                score = fuzz.token_set_ratio(loc, f'{city} {district} {village}')
                if score > max_score:
                    max_score = score
                    max_city = city
                    max_district = district
                    max_village = village
                    max_auth = village_d[city][district][village]['authority']
                    max_phone = village_d[city][district][village]['phone']
    if max_score > 80:
        d_t[cols_en_tr_d['authority']] = max_auth
        d_t[cols_en_tr_d['phone']] = max_phone
    else:
        d_t[cols_en_tr_d['authority']] = '?'
        d_t[cols_en_tr_d['phone']] = '?'
    date_called = attr[attr_d['date_called']]
    if date_called:
        d_t[cols_en_tr_d['date_called']] = datetime.fromtimestamp(date_called/1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        d_t[cols_en_tr_d['date_called']] = ''
    pop_l = list()
    if attr[attr_d['child_pop']]:
        pop_l.append(f'Çocuk: {attr[attr_d["child_pop"]]}')
    if attr[attr_d['adult_pop']]:
        pop_l.append(f'Yetişkin: {attr[attr_d["adult_pop"]]}')
    if attr[attr_d['elder_pop']]:
        pop_l.append(f'Yaşlı: {attr[attr_d["elder_pop"]]}')
    if attr[attr_d['female_pop']]:
        pop_l.append(f'Kadın: {attr[attr_d["elder_pop"]]}')
    if attr[attr_d['house_count']]:
        pop_l.append(f'Hane Sayısı: {attr[attr_d["house_count"]]}')
    d_t[cols_en_tr_d['pop']] = ' ; '.join(pop_l)
    need_l = [i for i in [attr[attr_d['first_need']], attr[attr_d['second_need']], attr[attr_d['third_need']], attr[attr_d['extra_need']]] if i]
    d_t[cols_en_tr_d['extra_need']] = ' ; '.join(need_l)
    d_t[cols_en_tr_d['tent_need']] = '?'
    d_t[cols_en_tr_d['tent_knowledge']] = '?'
    d_t[cols_en_tr_d['food_need']] = '?'
    d_t[cols_en_tr_d['cloth_need']] = '?'
    d_t[cols_en_tr_d['chronic_illness']] = attr[attr_d['chronic_illness']]
    handicap_l = [str(i) for i in [attr[attr_d['handicapped_status']], attr[attr_d['handicapped_exists']], attr[attr_d['handicapped_count']]] if i]
    d_t[cols_en_tr_d['handicapped_exists']] = ' ; '.join(handicap_l)
    d_t[cols_en_tr_d['collapsed_building']] = attr[attr_d['collapsed_building']]
    animal_casualty_l = list()
    if attr[attr_d['big_animal_casualty']]:
        animal_casualty_l.append(f'{attr[attr_d["big_animal_casualty"]]} büyük hayvan')
    if attr[attr_d['small_animal_casualty']]:
        animal_casualty_l.append(f'{attr[attr_d["small_animal_casualty"]]} küçük hayvan')
    d_t[cols_en_tr_d['animal_casualty']] = ' ; '.join(animal_casualty_l)
    d_t[cols_en_tr_d['animal_food']] = attr[attr_d['animal_food']]
    d_t[cols_en_tr_d['road_access']] = attr[attr_d['road_access']]
    extra_l = [i for i in [attr[attr_d['extra']], attr[attr_d['comments']]] if i]
    d_t[cols_en_tr_d['comments']] = ' ; '.join(extra_l)
    merged_l.append(d_t)

date_t = datetime.now().strftime('%Y-%m-%d_%H-%M')
filename = f'itub-boun-merged_{date_t}'
with open(os.path.join(itub_folder, f'{filename}.txt'), 'w') as f:
    f.write(str(merged_l))
with open(os.path.join(itub_folder, f'{filename}.json'), 'w') as f:
    json.dump(merged_l, f, indent=4, ensure_ascii=False)

with open(os.path.join(itub_folder, f'{filename}.csv'), 'w') as f:
    w = csv.DictWriter(f, cols_en_tr_d.values())
    w.writeheader()
    w.writerows(merged_l)
