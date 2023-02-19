import requests, json, os

with open('cities.json') as f:
    cities_l = json.load(f)

url = 'https://sonuc.ysk.gov.tr/api/getIlceList?secimId=19668&secimTuru=7&ilId={city_id}&secimCevresiId={env_id}&sandikTuru=-1&yurtIciDisi=1'

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
city_folder = os.path.join(THIS_DIR, 'city_districts')
if not os.path.exists(city_folder):
    os.mkdir(city_folder)

session = requests.Session()

for city in cities_l:
    city_id = city['il_ID']
    city_name = city['il_ADI']
    env_id = city['secim_CEVRESI_ID']
    city_url = url.format(city_id=city_id, env_id=env_id)
    response = session.get(city_url, verify=False)
    data = response.json()
    city_file = os.path.join(city_folder, str(city_id) + '.json')
    with open(city_file, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
