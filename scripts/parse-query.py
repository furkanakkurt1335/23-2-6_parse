import json
with open('query.json', 'r') as f:
    query = json.load(f)

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Me")

feats = query['features']
for feat in feats:
    if 'attributes' in feat.keys() and 'birinci_ncelikli_ihtiya_duydu_u' in feat['attributes'].keys():
        need_t = feat['attributes']['birinci_ncelikli_ihtiya_duydu_u']
        if need_t and 'Çadır' in need_t:
            x, y = feat['geometry']['x'], feat['geometry']['y']
            print(x, y)
            location = geolocator.reverse(f"{y}, {x}")
            print(location.address)
            print(feat['attributes']['k_y_adi'])
            