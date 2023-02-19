import json
with open('village_auth_loc_list.json') as f:
    village_auth_loc_d = json.load(f)

distance_count = 0
village_count = 0
for city in village_auth_loc_d.keys():
    for district in village_auth_loc_d[city].keys():
        for village in village_auth_loc_d[city][district].keys():
            village_count += 1
            if 'distance' in village_auth_loc_d[city][district][village].keys():
                distance_count += 1

print('Village count: {}'.format(village_count))
print('Distance count: {}'.format(distance_count))
print('Distance count / village count: {}'.format(distance_count / village_count))