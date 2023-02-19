import json

with open('village_auth_loc_list.json') as f:
    village_auth_loc_d = json.load(f)

for city in village_auth_loc_d.keys():
    for district in village_auth_loc_d[city].keys():
        for village in village_auth_loc_d[city][district].keys():
            lat = village_auth_loc_d[city][district][village]['lat']
            lng = village_auth_loc_d[city][district][village]['lng']
            if lat == '' or lng == '':
                village_auth_loc_d[city][district][village]['lat'] = -1
                village_auth_loc_d[city][district][village]['lng'] = -1
            else:
                village_auth_loc_d[city][district][village]['lat'] = float(lat)
                village_auth_loc_d[city][district][village]['lng'] = float(lng)

with open('village_auth_loc_list.json', 'w') as f:
    json.dump(village_auth_loc_d, f, indent=4, ensure_ascii=False)
