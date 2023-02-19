import os, json, csv
import pandas as pd
from geopy.geocoders import Nominatim
from fuzzywuzzy import fuzz
from time import sleep

geolocator = Nominatim(user_agent="afetharita")

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

icisleri_data = pd.read_csv(os.path.join(THIS_FOLDER, 'data', 'icisleri.csv'))
icisleri_l = list()
for i in range(len(icisleri_data)):
    city = icisleri_data['Il'][i]
    district = icisleri_data['Ilce'][i]
    village = icisleri_data['Muhtarlik'][i]
    lat = icisleri_data['Enlem'][i]
    lng = icisleri_data['Boylam'][i]
    icisleri_l.append({'city': city, 'district': district, 'village': village, 'lat': lat, 'lng': lng})

folder = os.path.join(THIS_FOLDER, 'phone_access_sheets')
city_l = ['maras', 'kilis', 'hatay', 'adiyaman']
city_d = {'maras': 'Kahramanmaraş', 'kilis': 'Kilis', 'hatay': 'Hatay', 'adiyaman': 'Adıyaman'}
df = pd.DataFrame()
col_d = {'mahalle': 'mahalle', 'İlaç': 'ilac_ihtiyac', 'Gıda': 'gida_ihtiyac', 'Çadır': 'cadir_ihtiyac', 'Diğer': 'diger_ihtiyac', 'teyit': 'teyit', 'Giyecek': 'giyecek_ihtiyac'}
merged_l = list()
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        cols = list()
        for col in df_t[sheet_t].columns:
            for key in col_d.keys():
                if key in col:
                    cols.append((key, col))
        for i in range(len(df_t[sheet_t])):
            d_t = {'il': city_d[city], 'ilce': sheet_t, 'lat': '', 'lng': ''}
            for key, col in cols:
                el_t = df_t[sheet_t][col][i]
                if el_t == el_t:
                    d_t[col_d[key]] = df_t[sheet_t][col][i]
                else:
                    d_t[col_d[key]] = ''
            village = df_t[sheet_t]['mahalle'][i]
            address = f'{city_d[city]} {sheet_t} {village}'
            max_ratio, max_lat, max_lng = 0, 0, 0
            for icisleri in icisleri_l:
                icisleri_loc = f'{icisleri["city"]} {icisleri["district"]} {icisleri["village"]}'
                ratio_t = fuzz.token_set_ratio(address, icisleri_loc)
                if ratio_t > max_ratio:
                    max_ratio = ratio_t
                    max_lat = icisleri['lat']
                    max_lng = icisleri['lng']
            if max_ratio > 80 and max_lat == max_lat and max_lng == max_lng:
                d_t['lat'] = max_lat
                d_t['lng'] = max_lng
                # print('Found in icisleri data', address)
            else:
                try:
                    location = geolocator.geocode(address)
                    if location and location.latitude and location.longitude and location.latitude == location.latitude and location.longitude == location.longitude:
                        d_t['lat'] = location.latitude
                        d_t['lng'] = location.longitude
                        # print('Found in geopy', address)
                    else:
                        d_t['lat'] = ''
                        d_t['lng'] = ''
                        # print('Not found', address)
                except:
                    d_t['lat'] = ''
                    d_t['lng'] = ''
                    # print('Not found', address)
            merged_l.append(d_t)
            print(len(merged_l))
            # print(d_t)
            # sleep(1)

for i in range(len(merged_l)):
    for key in merged_l[i].keys():
        if str(merged_l[i][key]).isnumeric():
            merged_l[i][key] = int(merged_l[i][key])

with open('merged.json', 'w') as f:
    json.dump(merged_l, f, indent=4, ensure_ascii=False)

keys_l = ['il', 'ilce', 'mahalle', 'lat', 'lng', 'ilac_ihtiyac', 'gida_ihtiyac', 'cadir_ihtiyac', 'diger_ihtiyac', 'teyit', 'giyecek_ihtiyac']
with open('merged.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, fieldnames=keys_l)
    dict_writer.writeheader()
    dict_writer.writerows(merged_l)
