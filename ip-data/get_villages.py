import pandas as pd
import os, json
from datetime import datetime
from fuzzywuzzy import fuzz

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
xlsx_path = os.path.join(THIS_DIR, 'Muhtar_Arama_Listeler.xlsx')
df = pd.read_excel(xlsx_path, sheet_name=None, header=1)

def is_village(city, district, village):
    global village_d, false_count, not_village_l
    loc = f'{city} {district} {village}'
    loc_wo_district = f'{city} {village}'
    max_ratio = 0
    max_ratio_wo_district = 0
    for city in village_d.keys():
        for district in village_d[city].keys():
            for village in village_d[city][district]:
                if 'KÖYÜ' not in village:
                    continue
                village = village.replace('KÖYÜ', '')
                loc_t = f'{city} {district} {village}'
                ratio_t = fuzz.token_set_ratio(loc, loc_t)
                if ratio_t > max_ratio:
                    max_ratio = ratio_t
                if max_ratio > 80:
                    return True
                loc_wo_district_t = f'{city} {village}'
                ratio_wo_district = fuzz.token_set_ratio(loc_wo_district, loc_wo_district_t)
                if ratio_wo_district > max_ratio_wo_district:
                    max_ratio_wo_district = ratio_wo_district
                if max_ratio_wo_district > 90:
                    return True
    false_count += 1
    not_village_l.append(loc)
    # print('Not village', loc)
    return False

false_count = 0
not_village_l = []
village_path = os.path.join(THIS_DIR, '../data/village_auth_loc_list.json')
with open(village_path, 'r', encoding='utf-8') as f:
    village_d = json.load(f)

tr_key_d = {'city': 'İl', 'district': 'İlçe', 'village': 'Köy adı', 'authority': 'Muhtar adı', 'auth_phone': 'Telefon numarası', 'date': 'Görüşme tarihi', 'coll_appr': 'Yaklaşık kaç bina enkaz halinde?', 'tent': 'Çadır', 'food_need': 'Yiyecek ihtiyacını karşılayabiliyor musunuz?', 'pill': 'İlaç ihtiyacı, sağlık durumu kritik olan, engelli bilgisi', 'animal': 'Hayvanları varsa hayvanlarla/ yem ile ilgili sıkıntınız var mı?', 'extra': 'Not', 'cloth': 'Giysi', 'hygiene': 'Hijyen'}

row_l = []
sheet_l = list(df.keys())
for sheet_name in sheet_l:
    city = sheet_name
    key_l = list(df[sheet_name].keys())
    key_d = {'district': '', 'village': '', 'authority': '', 'auth_phone': '', 'date': '', 'coll_appr': '', 'tent': '', 'food_need': '', 'pill': [], 'animal': '', 'extra': [], 'cloth': '', 'hygiene': []}
    for i in range(len(key_l)):
        key_t = str(key_l[i])
        if 'İlaç' in key_t:
            key_d['pill'].append(key_t)
        elif 'Diğer' in key_t:
            key_d['extra'].append(key_t)
        elif 'İLÇE' in key_t.strip() and not key_d['district']:
            key_d['district'] = key_t
        elif 'mahalle' in key_t.lower() and not key_d['village']:
            key_d['village'] = key_t
        elif 'hayvan' in key_t.lower():
            key_d['animal'] = key_t
        elif 'Yiyecek' in key_t:
            key_d['food_need'] = key_t
        elif 'Çadır' in key_t:
            key_d['tent'] = key_t
        elif 'enkaz' in key_t.lower():
            key_d['coll_appr'] = key_t
        elif 'Tarih' in key_t:
            key_d['date'] = key_t
        elif 'muhtar' in key_t.lower():
            key_d['authority'] = key_t
        elif 'tel' in key_t.lower():
            key_d['auth_phone'] = key_t
        elif 'Giysi' in key_t:
            key_d['cloth'] = key_t
        elif 'bebek bezi' in key_t.lower() or 'KADIN PEDİ' in key_t or 'HASTA PEDİ' in key_t or 'temizlik' in key_t.lower():
            key_d['hygiene'].append(key_t)
    prev_district = ''
    for i in range(len(df[sheet_name])):
        district = str(df[sheet_name][key_d['district']][i])
        if district.strip() == '"':
            district = prev_district
        else:
            prev_district = district
        village = df[sheet_name][key_d['village']][i]
        if not is_village(city, district, village):
            continue
        if not key_d['authority']:
            authority = ''
        else:
            authority = df[sheet_name][key_d['authority']][i]
        auth_phone = df[sheet_name][key_d['auth_phone']][i]
        date = df[sheet_name][key_d['date']][i]
        if type(date) == datetime:
            date = date.strftime('%d.%m.%Y')
        coll_appr = df[sheet_name][key_d['coll_appr']][i]
        if not key_d['tent']:
            tent = ''
        else:
            tent = df[sheet_name][key_d['tent']][i]
        food_need = df[sheet_name][key_d['food_need']][i]
        pill_l = []
        for pill_key in key_d['pill']:
            content_t = str(df[sheet_name][pill_key][i]).strip()
            if content_t != 'nan':
                pill_l.append(content_t)
        pill = ', '.join(pill_l)
        animal = df[sheet_name][key_d['animal']][i]
        extra_l = []
        for extra_key in key_d['extra']:
            content_t = str(df[sheet_name][extra_key][i]).strip()
            if content_t != 'nan':
                extra_l.append(content_t)
        extra = ', '.join(extra_l)
        if not key_d['cloth']:
            cloth = ''
        else:
            cloth = df[sheet_name][key_d['cloth']][i]
        hygiene_l = []
        for hygiene_key in key_d['hygiene']:
            content_t = str(df[sheet_name][hygiene_key][i]).strip()
            if content_t != 'nan':
                hygiene_l.append(content_t)
        hygiene = ', '.join(hygiene_l)
        row_l.append({tr_key_d['city']: city, tr_key_d['district']: district, tr_key_d['village']: village, tr_key_d['authority']: authority, tr_key_d['auth_phone']: auth_phone, tr_key_d['date']: date, tr_key_d['coll_appr']: coll_appr, tr_key_d['tent']: tent, tr_key_d['food_need']: food_need, tr_key_d['pill']: pill, tr_key_d['animal']: animal, tr_key_d['extra']: extra, tr_key_d['cloth']: cloth, tr_key_d['hygiene']: hygiene})
        print('Remaining', len(df[sheet_name]) - i - 1, 'rows', sheet_name)

key_l = [tr_key_d['city'], tr_key_d['district'], tr_key_d['village'], tr_key_d['authority'], tr_key_d['auth_phone'], tr_key_d['date'], tr_key_d['coll_appr'], tr_key_d['tent'], tr_key_d['food_need'], tr_key_d['cloth'], tr_key_d['hygiene'], tr_key_d['pill'], tr_key_d['animal'], tr_key_d['extra']]
df = pd.DataFrame(row_l, columns=key_l)
df.to_csv(os.path.join(THIS_DIR, 'muhtar-arama-merged.csv'), index=False)
print('False', false_count)
with open(os.path.join(THIS_DIR, 'not_village_l.json'), 'w') as f:
    json.dump(not_village_l, f, indent=4, ensure_ascii=False)