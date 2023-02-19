import json
from fuzzywuzzy import fuzz
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open('village_locs.json', 'r') as f:
    village_locs_d = json.load(f)

with open('village_auth_loc_list.json', 'r') as f:
    village_auth_d = json.load(f)

with open('cities.json') as f:
    cities_l = json.load(f)
city_folder = os.path.join(THIS_DIR, 'city_districts')

district_folder = os.path.join(THIS_DIR, 'district_villages')

with open('resp_city_ids.json') as f:
    resp_city_ids = json.load(f)

i = 0
for city in village_auth_d.keys():
    for district in village_auth_d[city].keys():
        for village in village_auth_d[city][district].keys():
            lat = village_auth_d[city][district][village]['lat']
            if lat == '' or lat == 0 or lat == '0':
                max_ratio, max_ratio_city = 0, ''
                for city_t in village_locs_d.keys():
                    ratio_t = fuzz.token_set_ratio(city, city_t)
                    if ratio_t > max_ratio:
                        max_ratio = ratio_t
                        max_ratio_city = city_t
                if max_ratio > 80:
                    sel_city = max_ratio_city
                else:
                    continue
                max_ratio, max_ratio_district = 0, ''
                for district_t in village_locs_d[city_t].keys():
                    ratio_t = fuzz.token_set_ratio(district, district_t)
                    if ratio_t > max_ratio:
                        max_ratio = ratio_t
                        max_ratio_district = district_t
                if max_ratio > 80:
                    sel_district = max_ratio_district
                else:
                    continue
                max_ratio, max_ratio_village = 0, ''
                for village_t in village_locs_d[city_t][district_t].keys():
                    village_str = village_t.replace('KÖYÜ', '').replace('MAH.', '').strip()
                    ratio_t = fuzz.token_set_ratio(village, village_t)
                    if ratio_t > max_ratio:
                        max_ratio = ratio_t
                        max_ratio_village = village_t
                if max_ratio > 80:
                    sel_village = max_ratio_village
                else:
                    continue
                if village_locs_d[sel_city][sel_district][sel_village]['lat'] == '' or village_locs_d[sel_city][sel_district][sel_village]['lng'] == '':
                    continue
                village_auth_d[city][district][village]['lat'] = village_locs_d[sel_city][sel_district][sel_village]['lat']
                village_auth_d[city][district][village]['lng'] = village_locs_d[sel_city][sel_district][sel_village]['lng']
                print(city, district, village)

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(village_auth_d, f, indent=4, ensure_ascii=False)
