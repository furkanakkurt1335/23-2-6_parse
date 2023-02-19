import json, os
import pandas as pd
from fuzzywuzzy import fuzz

# icisleri_df = pd.read_csv('icisleri.csv', encoding='utf-8')
df = pd.read_csv('maras.csv', encoding='utf-8')
auth_l = list()
for i in range(len(df)):
    city = df['Il'][i]
    # city_to_check = 'Kahramanmaraş'
    # ratio_t = fuzz.token_set_ratio(city, city_to_check)
    # if ratio_t < 90:
    #     continue
    district = df['Ilce'][i]
    village = df['Muhtarlik'][i]
    loc = f'{city} {district} {village}'
    auth_l.append(loc)

access_path = 'phone_access_sheets'
file_path = os.path.join(access_path, 'maras.xlsx')
sheet_d = pd.read_excel(file_path, sheet_name=None)

village_d = dict()
city = 'Kahramanmaraş'
for key in sheet_d.keys():
    df = sheet_d[key]
    cols = df.columns
    for i in range(len(df)):
        district = key
        village = df[cols[0]][i]
        if city not in village_d.keys():
            village_d[city] = dict()
        if district not in village_d[city].keys():
            village_d[city][district] = set()
        village_d[city][district].add(village)

# matched_l = list()
# unmatched_l = list()
# for auth in auth_l:
#     max_ratio, match = 0, ''
#     for city in village_d.keys():
#         for district in village_d[city].keys():
#             for village in village_d[city][district]:
#                 loc = f'{city} {district} {village}'
#                 ratio_t = fuzz.token_set_ratio(loc, auth)
#                 if ratio_t > max_ratio:
#                     max_ratio = ratio_t
#                     match = loc
#     if max_ratio > 90:
#         # print(auth, match, max_ratio)
#         matched_l.append((auth, match, max_ratio))
#     else:
#         unmatched_l.append((auth, match, max_ratio))

matched_l = list()
our_villages = 0
for city in village_d.keys():
    for district in village_d[city].keys():
        for village in village_d[city][district]:
            our_villages += 1
            loc = f'{city} {district} {village}'
            max_ratio, match = 0, ''
            for auth in auth_l:
                ratio_t = fuzz.token_set_ratio(loc, auth)
                if ratio_t > max_ratio:
                    max_ratio = ratio_t
                    match = auth
            if max_ratio > 90:
                print(loc, match, max_ratio)
                matched_l.append((loc, auth, ratio_t))
                del auth_l[auth_l.index(match)]


print('All Maras villages:', len(auth_l))
print('Matched Maras villages:', len(matched_l))
print('Unmatched Maras villages:', len(auth_l) - len(matched_l))
print('Our Maras villages:', our_villages)

with open('unmatched_l.json', 'w') as f:
    json.dump(auth_l, f, ensure_ascii=False, indent=4)