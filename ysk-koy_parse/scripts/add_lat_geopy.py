from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json

with open('village_auth_loc_list.json', 'r', encoding='utf-8') as f:
    village_d = json.load(f)

geolocator = Nominatim(user_agent='Me')

for city in village_d.keys():
    for district in village_d[city].keys():
        for village in village_d[city][district].keys():
            lat = village_d[city][district][village]['lat']
            if lat:
                continue
            address = f'{village}, {district}, {city}, Turkey'
            location = geolocator.geocode(address)
            if location:
                village_d[city][district][village]['lat'] = location.latitude
                village_d[city][district][village]['lng'] = location.longitude
                print(city, district, village, location.latitude, location.longitude)
                with open('village_auth_loc_list.json', 'w', encoding='utf-8') as f:
                    json.dump(village_d, f, ensure_ascii=False, indent=4)
            else:
                print('No location found for', address)