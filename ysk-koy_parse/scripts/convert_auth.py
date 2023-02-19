import json
with open('village_auth_loc_list.json') as f:
    village_auth_loc_d = json.load(f)

new_d = dict()
for city in village_auth_loc_d.keys():
    if city not in new_d.keys():
        new_d[city] = dict()
    for district in village_auth_loc_d[city].keys():
        if district not in new_d[city].keys():
            new_d[city][district] = dict()
        for village in village_auth_loc_d[city][district]:
            new_d[city][district][village] = { 'authority': '', 'phone': '', 'lat': 0, 'lng': 0 }

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(new_d, f, indent=4, ensure_ascii=False)