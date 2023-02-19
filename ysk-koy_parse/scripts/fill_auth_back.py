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

# for city in cities_l:
#     city_id = city['il_ID']
#     if city_id not in resp_city_ids:
#         continue
#     city_name = city['il_ADI']
#     city_district_path = os.path.join(city_folder, str(city_id) + '.json')
#     with open(city_district_path) as f:
#         city_districts = json.load(f)
#     for district in city_districts:
#         district_id = district['ilce_ID']
#         district_name = district['ilce_ADI']
#         district_file = os.path.join(district_folder, str(district_id) + '.json')
#         with open(district_file) as f:
#             district_villages = json.load(f)
#         for village in district_villages:
#             village_id = village['muhtarlik_ID']
#             village_name = village['muhtarlik_ADI']
#             if village_name not in village_auth_d[city_name][district_name].keys():
#                 village_auth_d[city_name][district_name][village_name] = { 'authority': '', 'phone': '', 'lat': 0, 'lng': 0}

for city in village_auth_d.keys():
    for district in village_auth_d[city].keys():
        for village in village_auth_d[city][district].keys():
            if village_auth_d[city][district][village]['authority'] == '':
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
                    ratio_t = fuzz.token_set_ratio(village, village_t)
                    if ratio_t > max_ratio:
                        max_ratio = ratio_t
                        max_ratio_village = village_t
                if max_ratio > 80:
                    sel_village = max_ratio_village
                else:
                    continue
                village_auth_d[city][district][village]['authority'] = village_locs_d[sel_city][sel_district][sel_village]['authority']
                print(city, district, village, village_locs_d[sel_city][sel_district][sel_village]['authority'])

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(village_auth_d, f, indent=4, ensure_ascii=False)
