import json, os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open('cities.json') as f:
    cities_l = json.load(f)
city_folder = os.path.join(THIS_DIR, 'city_districts')

district_folder = os.path.join(THIS_DIR, 'district_villages')

village_folder = os.path.join(THIS_DIR, 'village_list')
if not os.path.exists(village_folder):
    os.mkdir(village_folder)

village_d = dict()

for city in cities_l:
    city_id = city['il_ID']
    city_name = city['il_ADI']
    city_district_path = os.path.join(city_folder, str(city_id) + '.json')
    with open(city_district_path) as f:
        city_districts = json.load(f)
    if city_name not in village_d.keys():
        village_d[city_name] = dict()
    for district in city_districts:
        district_id = district['ilce_ID']
        district_name = district['ilce_ADI']
        if district_name not in village_d[city_name].keys():
            village_d[city_name][district_name] = list()
        district_file = os.path.join(district_folder, str(district_id) + '.json')
        with open(district_file) as f:
            district_villages = json.load(f)
        for village in district_villages:
            village_id = village['muhtarlik_ID']
            village_name = village['muhtarlik_ADI']
            if 'KÖYÜ' in village_name and village_name not in village_d[city_name][district_name]:
                village_d[city_name][district_name].append(village_name)

with open('village_list.json', 'w') as f:
    json.dump(village_d, f, indent=4, ensure_ascii=False)