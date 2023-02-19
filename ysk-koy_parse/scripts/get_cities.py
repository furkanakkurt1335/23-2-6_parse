import requests, json

url = 'https://sonuc.ysk.gov.tr/api/getIlList?secimId=19668&secimTuru=7&sandikTuru=-1&yurtIciDisi=1'

session = requests.Session()
response = session.get(url, verify=False)
data = response.json()
with open('cities.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)