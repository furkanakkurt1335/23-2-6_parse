import json, requests, re

with open('village_auth_loc_list.json', 'r', encoding='utf-8') as f:
    village_auth_d = json.load(f)

ph_pattern = '((\+90|90|0)?5\d{9})'
ph_url = 'https://www.google.com/search?q=yandex+{city}+{district}+{village}+{auth}+mahalle+muhtarl%C4%B1%C4%9F%C4%B1+telefon'

i = 0
for city in village_auth_d.keys():
    for district in village_auth_d[city].keys():
        for village in village_auth_d[city][district].keys():
            phone = village_auth_d[city][district][village]['phone']
            # if 'source' in village_auth_d[city][district][village].keys() and village_auth_d[city][district][village]['source'] == 'google search with yandex in query':
            #     pass
            if phone:
                continue
            auth = village_auth_d[city][district][village]['authority']
            req = requests.get(ph_url.format(city=city, district=district, village=village, auth=auth))
            resp = req.text.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
            if 'Theblockwillexpireshortlyafterthoserequestsstop' in resp:
                print('Blocked')
                input()
            ph_l = re.findall(ph_pattern, resp)
            if ph_l:
                for ph in ph_l:
                    phone_t = ph[0]
                    if phone_t[0] == '5' and phone_t[1] in ['1', '2', '6', '7', '8', '9']:
                        continue
                    village_auth_d[city][district][village]['phone'] = phone_t
                    village_auth_d[city][district][village]['source'] = 'google search with yandex in query'
                    print(city, district, village, phone_t)
                    i += 1
                    if i % 10 == 0:
                        with open('village_auth_loc_list.json', 'w', encoding='utf-8') as f:
                            json.dump(village_auth_d, f, ensure_ascii=False, indent=4)
                        print('saved')
                    break
            else:
                print('No phone found for', city, district, village)

with open('village_auth_loc_list.json', 'w', encoding='utf-8') as f:
    json.dump(village_auth_d, f, ensure_ascii=False, indent=4)
