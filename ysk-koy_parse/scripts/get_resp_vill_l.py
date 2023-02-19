import json, os
import pandas as pd
from fuzzywuzzy import fuzz

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def getAddress(x, y):
    geolocator = Nominatim(user_agent='Me')
    location = geolocator.reverse(f'{y}, {x}')
    fields = location.address.split(', ')
    new_fields = list()
    for i in range(len(fields)):
        if not fields[i].isnumeric():
            new_fields.append(fields[i])
    fields = new_fields
    district, city = fields[-4], fields[-3]
    centre = geolocator.geocode(city)
    distance = geodesic((location.latitude, location.longitude), (centre.latitude, centre.longitude)).km
    return city, district, distance

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open('cities.json') as f:
    cities_l = json.load(f)
city_folder = os.path.join(THIS_DIR, 'city_districts')

district_folder = os.path.join(THIS_DIR, 'district_villages')

with open('resp_city_ids.json') as f:
    resp_city_ids = json.load(f)

village_d = dict()
df = pd.DataFrame(columns=['il', 'ilce', 'koy'])

for city in cities_l:
    city_id = city['il_ID']
    if city_id not in resp_city_ids:
        continue
    city_name = city['il_ADI']
    city_district_path = os.path.join(city_folder, str(city_id) + '.json')
    with open(city_district_path) as f:
        city_districts = json.load(f)
    if city_name not in village_d.keys():
        village_d[city_name] = dict()
    for district in city_districts:
        district_id = district['ilce_ID']
        district_name = district['ilce_ADI']
        if district_name not in village_d[city_name].keys():
            village_d[city_name][district_name] = dict()
        district_file = os.path.join(district_folder, str(district_id) + '.json')
        with open(district_file) as f:
            district_villages = json.load(f)
        for village in district_villages:
            village_id = village['muhtarlik_ID']
            village_name = village['muhtarlik_ADI']
            if 'KÖYÜ' in village_name and village_name not in village_d[city_name][district_name]:
                village_d[city_name][district_name][village_name] = { 'authority': '', 'phone': '', 'lat': 0, 'lng': 0}

with open('village_locs.json') as f:
    village_loc_d = json.load(f)

for city in village_d.keys():
    max_ratio, max_city = 0, ''
    for loc_city in village_loc_d.keys():
        ratio_t = fuzz.token_set_ratio(city, loc_city)
        if ratio_t > max_ratio:
            max_ratio, max_city = ratio_t, loc_city
    if max_ratio > 80:
        loc_city = max_city
    else:
        continue
    for district in village_d[city].keys():
        max_ratio, max_district = 0, ''
        for loc_district in village_loc_d[loc_city].keys():
            ratio_t = fuzz.token_set_ratio(district, loc_district)
            if ratio_t > max_ratio:
                max_ratio, max_district = ratio_t, loc_district
        if max_ratio > 80:
            loc_district = max_district
        else:
            continue
        for village in village_d[city][district]:
            village_t = village.replace('KÖYÜ', '').strip()
            max_ratio, max_village = 0, ''
            for loc_village in village_loc_d[loc_city][loc_district]:
                ratio_t = fuzz.token_set_ratio(village_t, loc_village)
                if ratio_t > max_ratio:
                    max_ratio, max_village = ratio_t, loc_village
            if max_ratio > 80:
                loc_village = max_village
            else:
                continue
            auth = village_loc_d[loc_city][loc_district][loc_village]['authority']
            village_d[city][district][village]['authority'] = village_loc_d[loc_city][loc_district][loc_village]['authority']
            lat = village_loc_d[loc_city][loc_district][loc_village]['lat']
            lng = village_loc_d[loc_city][loc_district][loc_village]['lng']
            village_d[city][district][village]['lat'] = village_loc_d[loc_city][loc_district][loc_village]['lat']
            village_d[city][district][village]['lng'] = village_loc_d[loc_city][loc_district][loc_village]['lng']
            if lat == 0 or lng == 0 or lat == '' or lng == '':
                continue
            city_geopy, district_geopy, distance = getAddress(lat, lng)
            village_d[city][district][village]['distance'] = distance

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(village_d, f, indent=4, ensure_ascii=False)
