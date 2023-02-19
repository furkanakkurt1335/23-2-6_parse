import requests, json, os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open('cities.json') as f:
    cities_l = json.load(f)
city_folder = os.path.join(THIS_DIR, 'city_districts')

url = 'https://sonuc.ysk.gov.tr/api/getMuhtarlikList?secimId=19668&secimTuru=7&ilceId={district_id}&beldeId=0&birimId=0&secimCevresiId={env_id}&sandikTuru=-1&yurtIciDisi=1'

district_folder = os.path.join(THIS_DIR, 'district_villages')
if not os.path.exists(district_folder):
    os.mkdir(district_folder)

session = requests.Session()

def turkishize(text):
    text = text.replace('I', 'İ')
    text = text.replace('i', 'ı')
    return text

for city in cities_l:
    city_id = city['il_ID']
    city_district_path = os.path.join(city_folder, str(city_id) + '.json')
    with open(city_district_path) as f:
        city_districts = json.load(f)
    for district in city_districts:
        district_id = district['ilce_ID']
        district_name = district['ilce_ADI']
        env_id = district['secim_CEVRESI_ID']
        district_url = url.format(district_id=district_id, env_id=env_id)
        response = session.get(district_url, verify=False)
        data = response.json()
        district_file = os.path.join(district_folder, str(district_id) + '.json')
        with open(district_file, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
