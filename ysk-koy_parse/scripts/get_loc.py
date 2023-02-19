import os, json

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(THIS_DIR, 'village_location.csv')) as f:
    village_l = f.read().split('\n')[1:]
village_l = village_l[:-1]

village_loc_d = dict()

for i in range(len(village_l)):
    village_l[i] = village_l[i].split(',')
    city, district, village, authority, lat, lng = village_l[i]
    if city not in village_loc_d.keys():
        village_loc_d[city] = dict()
    if district not in village_loc_d[city].keys():
        village_loc_d[city][district] = dict()
    if village not in village_loc_d[city][district].keys():
        village_loc_d[city][district][village] = { 'authority': authority, 'lat': lat, 'lng': lng }

with open(os.path.join(THIS_DIR, 'village_locs.json'), 'w', encoding='utf-8') as f:
    json.dump(village_loc_d, f, ensure_ascii=False, indent=4)
