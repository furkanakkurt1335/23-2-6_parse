import json, os, requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas as pd
from fuzzywuzzy import fuzz

geolocator = Nominatim(user_agent="meds")

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
cred_path = os.path.join(THIS_DIR, 'credentials.json')
with open(cred_path, 'r') as f:
    credentials = json.load(f)

api_key = credentials['API_KEY']
geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={api_key}'

pharmacy_l_path = os.path.join(THIS_DIR, 'pharmacy_l.json')
with open(pharmacy_l_path, 'r', encoding='utf-8') as f:
    pharmacy_l = json.load(f)

csv_path = os.path.join(THIS_DIR, 'köyler_tıbbi_yardım.csv')
df = pd.read_csv(csv_path, encoding='utf-8')

village_d_path = os.path.join(THIS_DIR, '../data/village_auth_loc_list.json')
with open(village_d_path, 'r', encoding='utf-8') as f:
    village_d = json.load(f)

for i, row in df.iterrows():
    city, district, village = row['İl'], row['İlçe'], row['Mahalle']
    loc = f'{village}, {district}, {city}'
    max_ratio, max_city, max_district, max_village = 0, None, None, None
    for city in village_d.keys():
        for district in village_d[city].keys():
            for village in village_d[city][district].keys():
                loc_t = f'{village}, {district}, {city}'
                ratio = fuzz.token_set_ratio(loc, loc_t)
                if ratio > max_ratio:
                    max_ratio = ratio
                    max_city = city
                    max_district = district
                    max_village = village
    sel_city, sel_district, sel_village, sel_lat, sel_lng = None, None, None, None, None
    if max_ratio > 80:
        sel_city = max_city
        sel_district = max_district
        sel_village = max_village
        sel_lat = village_d[sel_city][sel_district][sel_village]['lat']
        sel_lng = village_d[sel_city][sel_district][sel_village]['lng']
        if sel_lat == 0 or sel_lng == 0 or sel_lat == -1 or sel_lng == -1:
            sel_lat = None
            sel_lng = None
    if sel_lat is None or sel_lng is None:
        # print(f'Using geopy for geocoding {loc}...')
        location = geolocator.geocode(loc)
        if location:
            sel_lat = location.latitude
            sel_lng = location.longitude
        else:
            # print('Using Google API for geocoding...')
            req = requests.get(geo_url.format(addr=loc, api_key=api_key))
            if req.status_code == 200:
                res = req.json()
                if res['results']:
                    sel_lat = res['results'][0]['geometry']['location']['lat']
                    sel_lng = res['results'][0]['geometry']['location']['lng']
                else:
                    sel_lat = None
                    sel_lng = None
            else:
                sel_lat = None
                sel_lng = None
    nearest_pharmacy, nearest_pharmacy_distance, nearest_pharmacy_direction, nearest_pharmacy_address = None, None, None, None
    for pharmacy in pharmacy_l:
        if 'coordinates' not in pharmacy.keys() or sel_lat is None or sel_lng is None:
            continue
        loc_lat = sel_lat
        loc_lng = sel_lng
        pharm_lat = pharmacy['coordinates']['lat']
        pharm_lng = pharmacy['coordinates']['lng']
        if loc_lat > pharm_lat:
            if loc_lng > pharm_lng:
                direction = 'GB'
            elif loc_lng < pharm_lng:
                direction = 'GD'
        else:
            if loc_lng > pharm_lng:
                direction = 'KB'
            elif loc_lng < pharm_lng:
                direction = 'KD'
        distance = geodesic((sel_lat, sel_lng), (pharmacy['coordinates']['lat'], pharmacy['coordinates']['lng'])).km
        if nearest_pharmacy_distance is None or distance < nearest_pharmacy_distance:
            nearest_pharmacy = pharmacy['name']
            nearest_pharmacy_address = pharmacy['address']
            address = pharmacy['address']
            nearest_pharmacy_distance = distance
            nearest_pharmacy_direction = direction
    if nearest_pharmacy_distance > 100:
        print(f'Pharmacy {pharmacy["name"]} is too far away from {loc} ({nearest_pharmacy_distance} km).')
    df.loc[i, 'En Yakın Eczanenin İsmi'] = nearest_pharmacy
    df.loc[i, 'Adresi'] = nearest_pharmacy_address
    df.loc[i, 'Mesafesi'] = nearest_pharmacy_distance
    df.loc[i, 'Yönü'] = nearest_pharmacy_direction

df.to_csv('köyler_tıbbi-yardım_eczane-adres.csv', index=False)