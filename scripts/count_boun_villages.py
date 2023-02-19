import os, json, csv
import pandas as pd
from fuzzywuzzy import fuzz

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
city_l = ['maras', 'kilis', 'hatay', 'adiyaman']
city_d = {'maras': 'Kahramanmaraş', 'kilis': 'Kilis', 'hatay': 'Hatay', 'adiyaman': 'Adıyaman'}
df = pd.DataFrame()
merged_d = dict()
village_cnt = 0
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        village_cnt += len(df_t[sheet_t])

print('Village count:', village_cnt)