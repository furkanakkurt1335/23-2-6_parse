import json
from fuzzywuzzy import fuzz
import pandas as pd

with open('results.json', 'r', encoding='utf-8') as f:
    itub_data = json.load(f)

itub_village_list = list()

for g_id in itub_data.keys():
    el = itub_data[g_id]
    village_t = el["city"], el["district"], el["village"]
    itub_village_list.append(village_t)

with open('village_auth_loc_list.json', 'r', encoding='utf-8') as f:
    village_d = json.load(f)

not_reached = list()
village_count = 0
for city in village_d.keys():
    for district in village_d[city].keys():
        for village in village_d[city][district].keys():
            if village.endswith('KÖYÜ'):
                continue
            village_count += 1
            village_str = ' '.join([city, district, village])
            authority = village_d[city][district][village]['authority']
            phone = village_d[city][district][village]['phone']
            max_ratio, max_loc = 0, ''
            for itub_village in itub_village_list:
                itub_str = ' '.join(itub_village)
                ratio_t = fuzz.token_set_ratio(village_str, itub_str)
                if ratio_t > max_ratio:
                    max_ratio = ratio_t
                    max_loc = itub_village
            if max_ratio < 80:
                not_reached.append((city, district, village, authority, phone))

with open('not_reached.json', 'w', encoding='utf-8') as f:
    json.dump(not_reached, f, indent=4, ensure_ascii=False)

cols = ['İl', 'İlçe', 'Köy', 'Muhtar', 'Telefon']
df = pd.DataFrame(columns=cols)

for city, district, village, authority, phone in not_reached:
    l_t = [city, district, village, authority, phone]
    df = pd.concat([pd.DataFrame([l_t], columns=cols), df], ignore_index=True)

df.to_csv('not_reached.csv', index=False, encoding='utf-8-sig')

print(f'Village count: {village_count}')
print(f'Not reached count: {len(not_reached)}')
