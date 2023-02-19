import pandas as pd
import json

with open('village_auth_loc_list.json') as f:
    village_auth_loc_d = json.load(f)
cols = ['il', 'ilce', 'koy', 'muhtar', 'telefon', 'mesafe', 'kaynak']
df = pd.DataFrame(columns=cols)

for city in village_auth_loc_d.keys():
    for district in village_auth_loc_d[city].keys():
        for village in village_auth_loc_d[city][district].keys():
            l_t = [city, district, village, village_auth_loc_d[city][district][village]['authority'], village_auth_loc_d[city][district][village]['phone']]
            if 'distance' in village_auth_loc_d[city][district][village].keys():
                distance_t = village_auth_loc_d[city][district][village]['distance']
                distance_t = '{:.2f}'.format(distance_t)
                l_t.append(distance_t)
            else:
                l_t.append('')
            if 'source' in village_auth_loc_d[city][district][village].keys():
                l_t.append(village_auth_loc_d[city][district][village]['source'])
            else:
                l_t.append('')
            if village.endswith('KÖYÜ'):
                df = pd.concat([pd.DataFrame([l_t], columns=cols), df], ignore_index=True)

df.to_csv('village_auth_loc_list_only-vil.csv', index=False, encoding='utf-8-sig')
