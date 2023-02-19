import json
with open('village_auth_loc_list.json') as f:
    village_auth_loc_d = json.load(f)

lat_count = 0
village_count = 0
for city in village_auth_loc_d.keys():
    for district in village_auth_loc_d[city].keys():
        for village in village_auth_loc_d[city][district].keys():
            village_count += 1
            lat = village_auth_loc_d[city][district][village]['lat']
            if lat != 0 and lat != -1:
                lat_count += 1

print('Village count: {}'.format(village_count))
print('Lat count: {}'.format(lat_count))
print('Lat count / village count: {}'.format(lat_count / village_count))