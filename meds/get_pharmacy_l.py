import xml.etree.ElementTree as ET
import json

tree = ET.parse('aeogk.kml')
root = tree.getroot()
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
pharmacy_l = list()
cnt = 0
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
    address = placemark.find('kml:ExtendedData/kml:address', namespaces)
    if address is not None:
        address = address.text
        if address is not None:
            address = address.strip()
        else:
            address = ''
    else:
        address = ''
    if address:
        pharmacy_l[i]['address'] = address

with open('pharmacy_l.json', 'w', encoding='utf-8') as f:
    json.dump(pharmacy_l, f, ensure_ascii=False, indent=4)
    