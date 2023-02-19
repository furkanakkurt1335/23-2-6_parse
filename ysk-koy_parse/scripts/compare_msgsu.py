import json
from fuzzywuzzy import fuzz

with open ('msgsu-data/kilis.json') as f:
    msgsu_maras_d = json.load(f)

with open ('village_auth_loc_list.json') as f:
    village_d = json.load(f)

not_matched_count = 0
matched_phone_l = list()
for city in msgsu_maras_d.keys():
    for district in msgsu_maras_d[city].keys():
        for village in msgsu_maras_d[city][district].keys():
            authority = msgsu_maras_d[city][district][village]['authority']
            phone = msgsu_maras_d[city][district][village]['phone']
            loc = f'{city} {district} {village}'
            loc_without_district = f'{city} {village}'
            max_ratio = 0
            loc_d = dict()
            max_ratio_without_district = 0
            wo_district_d = dict()
            for city_t in village_d.keys():
                for district_t in village_d[city_t].keys():
                    for village_t in village_d[city_t][district_t].keys():
                        loc_t = f'{city_t} {district_t} {village_t}'
                        phone_t = village_d[city_t][district_t][village_t]['phone']
                        if 'source' in village_d[city_t][district_t][village_t].keys():
                            source_t = village_d[city_t][district_t][village_t]['source']
                        else:
                            source_t = ''
                        ratio_t = fuzz.token_set_ratio(loc, loc_t)
                        if ratio_t > max_ratio:
                            max_ratio = ratio_t
                            loc_d['ratio'] = ratio_t
                            loc_d['phone'] = phone_t
                            loc_d['source'] = source_t
                            loc_d['city'] = city_t
                            loc_d['district'] = district_t
                            loc_d['village'] = village_t
                        loc_without_district_t = f'{city_t} {village_t}'
                        ratio_without_district_t = fuzz.token_set_ratio(loc_without_district, loc_without_district_t)
                        if ratio_without_district_t > max_ratio_without_district:
                            max_ratio_without_district = ratio_without_district_t
                            wo_district_d['ratio'] = ratio_without_district_t
                            wo_district_d['phone'] = phone_t
                            wo_district_d['source'] = source_t
                            wo_district_d['city'] = city_t
                            wo_district_d['district'] = district_t
                            wo_district_d['village'] = village_t
            if max_ratio > 80 and fuzz.token_set_ratio(loc_d['district'], village) < 80 and fuzz.token_set_ratio(loc_d['village'], district) < 80:
                sel_loc = f'{loc_d["city"]} {loc_d["district"]} {loc_d["village"]}'
                sel_phone = loc_d['phone']
                sel_source = loc_d['source']
                sel_city = loc_d['city']
                sel_district = loc_d['district']
                sel_village = loc_d['village']
                d_t = {'phone': sel_phone, 'msgsu_phone': phone, 'loc': sel_loc, 'msgsu_loc': loc, 'city': sel_city, 'district': sel_district, 'village': sel_village, 'msgsu_city': city, 'msgsu_district': district, 'msgsu_village': village, 'our-source': sel_source}
                matched_phone_l.append(d_t)
                print(f'Matched {loc} with {sel_loc}', max_ratio)
            elif max_ratio_without_district > 85:
                sel_loc = f'{wo_district_d["city"]} {wo_district_d["district"]} {wo_district_d["village"]}'
                sel_phone = wo_district_d['phone']
                sel_source = wo_district_d['source']
                sel_city = wo_district_d['city']
                sel_district = wo_district_d['district']
                sel_village = wo_district_d['village']
                d_t = {'phone': sel_phone, 'msgsu_phone': phone, 'loc': sel_loc, 'msgsu_loc': loc, 'city': sel_city, 'district': sel_district, 'village': sel_village, 'msgsu_city': city, 'msgsu_district': district, 'msgsu_village': village, 'our-source': sel_source}
                matched_phone_l.append(d_t)
                print(f'Matched {loc} with {sel_loc}', max_ratio_without_district)
            else:
                not_matched_count += 1
                print(f'No match found for {loc}')
                continue

print(not_matched_count, 'records not matched.')

with open('msgsu_matched-phone_kilis.json', 'w') as f:
    json.dump(matched_phone_l, f, indent=4, ensure_ascii=False)