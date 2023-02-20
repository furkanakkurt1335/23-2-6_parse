import os, json
import pandas as pd
from fuzzywuzzy import fuzz
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

df = pd.read_excel(os.path.join(THIS_FOLDER, 'köyler_tıbbi_yardım.xls'))

with open(os.path.join(THIS_FOLDER, '../data/village_auth_loc_list.json'), 'r') as f:
    village_d = json.load(f)

icisleri_df = pd.read_csv(os.path.join(THIS_FOLDER, '../data/improved-icisleri.csv'))

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
        if sel_dist == '?':
            geolocator = Nominatim(user_agent="icisleri")
            max_ratio = 0
            for j in range(len(icisleri_df)):
                city2 = icisleri_df.iloc[j]['Il']
                district2 = icisleri_df.iloc[j]['Ilce']
                neighborhood2 = icisleri_df.iloc[j]['Muhtarlik']
                loc2 = f'{city2} {district2} {neighborhood2}'
                ratio = fuzz.token_set_ratio(loc, loc2)
                if ratio > max_ratio:
                    max_ratio = ratio
                    x = icisleri_df.iloc[j]['Boylam']
                    y = icisleri_df.iloc[j]['Enlem']
                    sel_x, sel_y = x, y
            if max_ratio > 80:
                location = geolocator.geocode(city)
                if sel_x == sel_x and sel_y == sel_y:
                    sel_dist = geodesic((sel_y, sel_x), (location.latitude, location.longitude)).km
                    df.loc[i, 'Mesafe'] = sel_dist
    else:
        df.loc[i, 'Mesafe'] = '?'
    print(len(df) - i)

df.to_excel(os.path.join(THIS_FOLDER, 'köyler_tıbbi_yardım_mesafe.xls'), index=False)
