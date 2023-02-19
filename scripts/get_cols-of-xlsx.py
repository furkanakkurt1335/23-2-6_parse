import os
import pandas as pd

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
city_l = ['maras', 'kilis', 'hatay']
city_d = {'maras': 'Kahramanmaraş', 'kilis': 'Kilis', 'hatay': 'Hatay', 'adiyaman': 'Adıyaman'}
col_list = set()
df = pd.DataFrame()
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        for column in df_t[sheet_t].columns:
            col_list.add(column)

print(col_list)
