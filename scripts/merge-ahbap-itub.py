import json
import pandas as pd
from fuzzywuzzy import fuzz
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="ahbap")

with open('results.json', 'r', encoding='utf-8') as f:
    itub_data = json.load(f)

df = pd.read_csv('Teyitli Enkaz Altı ve Erzak Verileri - İhtiyaç Verileri.csv', encoding='utf-8')

ahbap_data_d = dict()

village_col = df.columns[4]
district_col = df.columns[5]
city_col = df.columns[6]
person_col = df.columns[7]
phone_col = df.columns[8]
summary_col = df.columns[9]
need_col = df.columns[10]
confirm_col = df.columns[11]
date_col = df.columns[12]
time_col = df.columns[13]
sent_col = df.columns[14]
for i in range(len(df)):
    village = df[village_col][i]
    district = df[district_col][i]
    city = df[city_col][i]
    person = df[person_col][i]
    phone = df[phone_col][i]
    summary = df[summary_col][i]
    need = df[need_col][i]
    confirm = df[confirm_col][i]
    date = df[date_col][i]
    time = df[time_col][i]
    sent = df[sent_col][i]
    location = f'{village} {district} {city}'
    loc_geopy = geolocator.geocode(location)
    if loc_geopy:
        loc_geopy = (loc_geopy.latitude, loc_geopy.longitude)
    max_ratio, max_location = 0, {'village': '', 'district': '', 'city': ''}
    for key in itub_data.keys():
        el = itub_data[key]
        if 'location' in el:
            loc = el['location']
            x, y = loc['x'], loc['y']
        itub_loc_t = f'{el["village"]} {el["district"]} {el["city"]}'
        ratio = fuzz.token_set_ratio(location, itub_loc_t)
        if ratio > max_ratio:
            max_ratio = ratio
            max_location = el['city'], el['district'], el['village']
    if max_ratio > 90:
        sel_loc = max_location
        print(location, sel_loc)
        input()
