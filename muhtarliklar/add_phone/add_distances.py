import json
from fuzzywuzzy import fuzz

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

with open('village_auth_loc_list.json') as f: # read entire data
    village_d = json.load(f)

def getAddress(x, y):
    geolocator = Nominatim(user_agent='Me')
    location = geolocator.reverse(f'{y}, {x}') # get location from lat and lng
    fields = location.address.split(', ') # split address into fields by comma
    new_fields = list()
    for i in range(len(fields)):
        if not fields[i].isnumeric(): # if not zip code
            new_fields.append(fields[i])
    fields = new_fields
    if len(fields) < 4: # if not enough fields
        return '', '', -1 # return empty values
    district, city = fields[-4], fields[-3] # get city and district
    centre = geolocator.geocode(city) # get city centre from city name
    distance = geodesic((location.latitude, location.longitude), (centre.latitude, centre.longitude)).km # get distance from city centre
    return city, district, distance # return city, district and distance

i = 1
for city in village_d.keys(): # iterate over all cities
    for district in village_d[city].keys(): # iterate over all districts
        for village in village_d[city][district]: # iterate over all villages
            if 'distance' in village_d[city][district][village].keys(): # if distance already calculated
                continue
            lat = village_d[city][district][village]['lat'] # get lat and lng
            lng = village_d[city][district][village]['lng']
            if lat == 0 or lat == -1 or lng == 0 or lng == -1: # if no lat or lng
                continue
            city_geopy, district_geopy, distance = getAddress(lat, lng) # get city, district and distance from lat and lng
            if city_geopy == '': # if no city, skip
                continue
            village_d[city][district][village]['distance'] = distance # add distance to data
            print(city, district, village, distance)
            i += 1
            if i % 10 == 0:
                with open('village_auth_loc_list.json', 'w') as f: # save data every 10 villages
                    print('saved')
                    json.dump(village_d, f, indent=4, ensure_ascii=False)

with open('village_auth_loc_list.json', 'w') as f: # save entire data
    json.dump(village_d, f, indent=4, ensure_ascii=False)
