import json

with open('village_auth_loc_list.json', 'r', encoding='utf-8') as f:
    village_d = json.load(f)

for city in village_d.keys():
    if city != 'ŞANLIURFA':
        continue
    for district in village_d[city].keys():
        if district != 'BİRECİK':
            continue
        for village in village_d[city][district].keys():
            if village_d[city][district][village]['phone'] != '':
                village_d[city][district][village]['source'] = 'http://www.birecik.gov.tr/muhtarlarimiz-ve-iletisim-bilgileri'

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(village_d, f, ensure_ascii=False, indent=4)