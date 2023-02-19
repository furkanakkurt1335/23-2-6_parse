import pandas as pd
import json

with open('msgsu-data/maras.xlsx', 'rb') as f:
    sheet_d = pd.read_excel(f, sheet_name=None, header=None)

village_d = dict()
city = 'Kahramanmaraş'
for key in sheet_d.keys():
    df = sheet_d[key]
    cols = df.columns
    for i in range(len(df)):
        district = key
        village = df[cols[0]][i]
        authority = df[cols[1]][i]
        phone = df[cols[2]][i]
        if city not in village_d.keys():
            village_d[city] = dict()
        if district not in village_d[city].keys():
            village_d[city][district] = dict()
        if village not in village_d[city][district].keys():
            village_d[city][district][village] = {'authority': authority, 'phone': phone}

with open('msgsu-data/maras.json', 'w') as f:
    json.dump(village_d, f, indent=4, ensure_ascii=False)
