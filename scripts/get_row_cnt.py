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
row_cnt = 0
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        for i in range(len(df_t[sheet_t])):
            row_cnt += 1

print(row_cnt)
