import pandas as pd
import json
from fuzzywuzzy import fuzz

with open('village_auth_loc_list.json', 'r', encoding='utf-8') as f:
    village_d = json.load(f)

df = pd.read_excel('Ulasılamıyor_adıyaman2.xlsx', sheet_name=None, header=None)
new_df = pd.DataFrame(columns=['İlçe', 'Mahalle', 'Muhtar', 'Telefon', 'Telefon 2'])
sheet_l = list(df.keys())
no_tel_cnt = 0
filled_cnt = 0
non_filled_cnt = 0
l_t = list()
for sheet_t in sheet_l:
    for i in range(len(df[sheet_t])):
        d_t = {'İlçe': sheet_t, 'Mahalle': df[sheet_t][0][i], 'Muhtar': df[sheet_t][1][i], 'Telefon': df[sheet_t][2][i]}
        if 3 in df[sheet_t].columns:
            d_t['Telefon 2'] = df[sheet_t][3][i]
        tel = str(df[sheet_t][2][i])
        if tel == 'nan':
            no_tel_cnt += 1
            city = 'Adıyaman'
            district = sheet_t
            village = df[sheet_t][0][i]
            loc = f'{city} {district} {village}'
            max_ratio, max_tel = 0, 0
            for city in village_d.keys():
                for district in village_d[city].keys():
                    for village in village_d[city][district].keys():
                        village_loc = f'{city} {district} {village}'
                        ratio_t = fuzz.token_set_ratio(loc, village_loc)
                        if ratio_t > max_ratio:
                            max_ratio = ratio_t
                            max_tel = village_d[city][district][village]['phone']
            if max_ratio > 80:
                d_t['Telefon'] = max_tel
                print(f'Found in village auth data: {loc}')
                filled_cnt += 1
            else:
                print(f'Not found: {loc}')
                non_filled_cnt += 1
        l_t.append(d_t)

for d_t in l_t:
    l_t_t = [d_t['İlçe'], d_t['Mahalle'], d_t['Muhtar'], d_t['Telefon']]
    if 'Telefon 2' in d_t.keys():
        l_t_t.append(d_t['Telefon 2'])
    else:
        l_t_t.append('')
    new_df = new_df.append(pd.Series(l_t_t, index=new_df.columns), ignore_index=True)
new_df.to_csv('Ulasılamıyor_adıyaman2_filled.csv', index=False)
print('No tel: ', no_tel_cnt)
print('Filled: ', filled_cnt)
print('Not filled: ', non_filled_cnt)