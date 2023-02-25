import xml.etree.ElementTree as ET
import json, os, requests

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

geo_path = os.path.join(THIS_DIR, 'geocoding')
cred_path = os.path.join(geo_path, 'credentials.json')
with open(cred_path, 'r') as f:
    credentials = json.load(f)

api_key = credentials['API_KEY']
geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={api_key}'

kml_path = os.path.join(THIS_DIR, 'aeogk.kml')
tree = ET.parse(kml_path)
root = tree.getroot()
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
pharmacy_l = list()
pharmacy_l_path = os.path.join(THIS_DIR, 'pharmacy_l.json')
for i, placemark in enumerate(root.findall('kml:Document/kml:Folder/kml:Placemark', namespaces)):
    name = placemark.find('kml:name', namespaces)
    pharmacy_l.append(dict({'name': name.text.strip()}))
    if name is not None:
        name = name.text.strip()
    else:
        name = ''
    coordinates = placemark.find('kml:Point/kml:coordinates', namespaces)
    if coordinates is not None:
        coordinates = coordinates.text.strip()
    else:
        coordinates = ''
    if coordinates:
        lat, lng = coordinates.split(',')[:2]
        pharmacy_l[i]['coordinates'] = {'lat': lat, 'lng': lng}
    for data in placemark.findall('kml:ExtendedData/kml:Data', namespaces):
        if not data.find('kml:value', namespaces).text:
            continue
        if 'extended_data' not in pharmacy_l[i].keys():
            pharmacy_l[i]['extended_data'] = dict()
        pharmacy_l[i]['extended_data'][data.get('name')] = data.find('kml:value', namespaces).text
    address = placemark.find('kml:address', namespaces)
    if address is not None and address.text is not None:
        address = address.text.strip()
        pharmacy_l[i]['address'] = address
    elif 'extended_data' in pharmacy_l[i].keys() and 'Adres' in pharmacy_l[i]['extended_data'].keys():
        pharmacy_l[i]['address'] = pharmacy_l[i]['extended_data']['Adres']
    elif 'extended_data' in pharmacy_l[i].keys() and 'ADRES' in pharmacy_l[i]['extended_data'].keys():
        pharmacy_l[i]['address'] = pharmacy_l[i]['extended_data']['ADRES']
    else:
        pharmacy_l[i]['address'] = ''
    if 'coordinates' not in pharmacy_l[i].keys():
        address = pharmacy_l[i]['address']
        response = requests.get(geo_url.format(addr=address, api_key=api_key))
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                pharmacy_l[i]['coordinates'] = {'lat': lat, 'lng': lng}
        else:
            print('Error: {}'.format(response.status_code))
    with open(pharmacy_l_path, 'w', encoding='utf-8') as f:
        json.dump(pharmacy_l, f, ensure_ascii=False, indent=4)

with open(pharmacy_l_path, 'w', encoding='utf-8') as f:
    json.dump(pharmacy_l, f, ensure_ascii=False, indent=4)
