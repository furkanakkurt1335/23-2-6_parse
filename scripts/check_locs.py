import json
from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="me")

with open('results.json', 'r') as f:
    res_d = json.load(f)

adiyaman_count = 0
for key in res_d.keys():
    if 'location' not in res_d[key].keys():
        print('no location', key)
        continue
    x, y = res_d[key]['location']['x'], res_d[key]['location']['y']
    location = geolocator.reverse("{}, {}".format(y, x))
    if 'Adıyaman' in location.address:
        print(location.address)
        adiyaman_count += 1

print(adiyaman_count)