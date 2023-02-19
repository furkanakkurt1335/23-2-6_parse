import os, json, csv
import pandas as pd
from fuzzywuzzy import fuzz
import datetime, numpy as np
from geopy.geocoders import Nominatim
import csv

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
city_l = ['adiyaman']
city_d = {'adiyaman': 'Adıyaman'}
df = pd.DataFrame()
merged_d = dict()
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        for i in range(len(df_t[sheet_t])):
            d_t = {'il': city_d[city], 'ilce': sheet_t}
            for col in df_t[sheet_t].columns:
                el_t = df_t[sheet_t][col][i]
                if isinstance(el_t, (int, np.integer)):
                    el_t = str(el_t)
                if el_t == el_t:
                    d_t[col] = el_t
                else:
                    d_t[col] = ''
            village = df_t[sheet_t]['mahalle'][i]
            address = f'{city_d[city]} {sheet_t} {village}'
            merged_d[address] = d_t

boun_attr_d = {
    "city": "il",
    "district": "ilce",
    "village": "mahalle",
    "authority": "muhtar",
    "phone": "tel no",
    "date_called": "teyit/ görüşme tarihi & saati",
    "pop": "GÜNCEL nüfus/\nberaber yaşayan\nkişi sayısı",
    "cadir_need": "Çadır ihtiyacı \nolan aile sayısı (sayı girelim, yoksa 0 girelim)",
    "cadir_person": "Köyde çadır kurmayı bilen biri var mı?",
    "food_need": "Gıda ihtiyacı var mı? \nNeler?\nYaklaşık kaç adet?",
    "cloth_need": "Giyecek ihtiyacı var mı?\nNeler?\nYaklaşık kaç adet?",
    "chronic_illness": "Kronik hasta var mı?",
    "handicapped_exists": "Engelli birey var mı? (fiziksel / zihinsel engelli - mümkünse ayrı cevap alalım)",
    "illness": "İlaç, hasta veya bebek\n durumu ve benzeri \ngibi şeyler var mı? ",
    "collapsed_building": "Yıkılan bina sayısı",
    "animal_casualty": "Telef olan hayvan sayısı",
    "animal_food": "Hayvnalar için güncel yem ihtiyacı",
    "extra_need": "Diğer ihtiyaçlar",
    "electric": "Elektrik var mı?",
    "water": "Su var mı?",
    "road_access": "Yol açık mı?",
    "comments": "NOTLAR"
}

village_auth_loc_data_path = os.path.join(THIS_FOLDER, '../data/village_auth_loc_list.json')
with open(village_auth_loc_data_path, 'r') as f:
    village_d = json.load(f)

itub_folder = os.path.join(THIS_FOLDER, '../itub-data')
with open(os.path.join(itub_folder, 'itub-all-api-data.json'), 'r') as f:
    itub_d = json.load(f)
feats = itub_d['features']
attr_d = {"creation_date": "CreationDate", "creator": "Creator", "edit_date": "EditDate", "editor": "Editor", "extra_need": "_htiya_duydu_unuz_di_er_temel_m", "second_need": "_kinci_ncelikli_ihtiya_duydu_un", "third_need": "_nc_ncelikli_ihtiya_duydu_unuz", "emergency_status": "ac_l_yet_durumu", "afad": "afad_taraf_ndan_arama_kurtarma", "infrastructure": "altyap_eksikli_i_elektrik_su_do", "vehicle": "ara_s_k_nt_s_var_m", "date_called": "b_lg_ed_n_len_saat", "first_need": "birinci_ncelikli_ihtiya_duydu_u", "handicapped_status": "engel_durumlar_nedir", "handicapped_exists": "engelli_birey_var_m", "0": "enkaz_alt_nda_oldu_unu_bildi_in", "1": "enkaz_alt_nda_oldu_unu_tahmin_e", "house_count": "hane_say_s_nedir", "hospital_access": "hastaneye_eri_im_sa_lanabiliyor", "animal_food": "hayvanlar_i_in_gerekli_besin_g", "village": "k_y_adi", "damaged_building": "k_y_n_zde_hasarl_ka_bina_var", "collapsed_building": "k_y_n_zde_y_k_lan_ka_bina_var", "female_pop": "k_ydeki_kad_n_n_fusu_nedir", "child_pop": "k_ydeki_ocuk_0_18_n_fusu_nedir", "elder_pop": "k_ydeki_ya_l_n_fusu_65_nedir", "adult_pop": "k_ydeki_yeti_kin_18_65_n_fusu_n", "handicapped_count": "ka_engelli_birey_var", "road_access": "kapal_ya_da_etkilenen_yol_var_m", "2": "kay_p_ki_i_say_s_nedir", "chronic_illness": "kronik_hastal_olan_var_m_eker_t", "extra": "liste_d_nda_belirtmek_istedi_in", "big_animal_casualty": "telef_olan_b_y_kba_hayvan_say_s", "small_animal_casualty": "telef_olan_k_kba_hayvan_say_s_n", "comments": "varsa_eklemek_istedikleriniz", "human_casualty": "ya_am_n_yitiren_ki_i_say_s_nedi", "o_id": "objectid", "g_id": "globalid"}
for feat in feats:
    d_t = dict()
    attr = feat['attributes']
    if not attr[attr_d['village']]:
        x, y = feat['geometry']['x'], feat['geometry']['y']
        geolocator = Nominatim(user_agent="itub")
        location = geolocator.reverse(f'{y}, {x}')
        address = location.raw['address']
        if 'city' in address.keys():
            city = address['city']
        else:
            city = ''
        if 'town' in address.keys():
            district = address['town']
        else:
            district = ''
        if 'suburb' in address.keys():
            village = address['suburb']
        else:
            village = ''
    else:
        city, district, village = '', '', attr[attr_d['village']].replace('/', ',')
    if village.count(',') > 1:
        vl_l = village.split(',')
        city, district, village = vl_l[0].strip(), vl_l[1].strip(), vl_l[2].strip()
    else:
        village = village.strip()
    if 'yaman' not in city.lower():
        continue
    d_t[boun_attr_d['city']] = city
    d_t[boun_attr_d['district']] = district
    d_t[boun_attr_d['village']] = village
    loc = f'{city} {district} {village}'
    max_score, max_city, max_district, max_village, max_auth, max_phone = 0, '', '', '', '', ''
    for city in village_d.keys():
        for district in village_d[city].keys():
            for village in village_d[city][district].keys():
                score = fuzz.token_set_ratio(loc, f'{city} {district} {village}')
                if score > max_score:
                    max_score = score
                    max_city = city
                    max_district = district
                    max_village = village
                    max_auth = village_d[city][district][village]['authority']
                    max_phone = village_d[city][district][village]['phone']
    if max_score > 80:
        d_t[boun_attr_d['authority']] = max_auth
        d_t[boun_attr_d['phone']] = max_phone
    else:
        d_t[boun_attr_d['authority']] = '?'
        d_t[boun_attr_d['phone']] = '?'
    d_t[boun_attr_d['date_called']] = datetime.datetime.fromtimestamp(attr[attr_d['date_called']]/1000).strftime('%Y-%m-%d %H:%M:%S')
    pop_l = list()
    if attr[attr_d['child_pop']]:
        pop_l.append(f'Çocuk: {attr[attr_d["child_pop"]]}')
    if attr[attr_d['adult_pop']]:
        pop_l.append(f'Yetişkin: {attr[attr_d["adult_pop"]]}')
    if attr[attr_d['elder_pop']]:
        pop_l.append(f'Yaşlı: {attr[attr_d["elder_pop"]]}')
    if attr[attr_d['female_pop']]:
        pop_l.append(f'Kadın: {attr[attr_d["elder_pop"]]}')
    if attr[attr_d['house_count']]:
        pop_l.append(f'Hane Sayısı: {attr[attr_d["house_count"]]}')
    d_t[boun_attr_d['pop']] = ' ; '.join(pop_l)
    need_l = [i for i in [attr[attr_d['first_need']], attr[attr_d['second_need']], attr[attr_d['third_need']], attr[attr_d['extra_need']]] if i]
    d_t[boun_attr_d['extra_need']] = ' ; '.join(need_l)
    d_t[boun_attr_d['cadir_need']] = '?'
    d_t[boun_attr_d['cadir_person']] = '?'
    d_t[boun_attr_d['food_need']] = '?'
    d_t[boun_attr_d['cloth_need']] = '?'
    d_t[boun_attr_d['chronic_illness']] = attr[attr_d['chronic_illness']]
    handicap_l = [str(i) for i in [attr[attr_d['handicapped_status']], attr[attr_d['handicapped_exists']], attr[attr_d['handicapped_count']]] if i]
    d_t[boun_attr_d['handicapped_exists']] = ' ; '.join(handicap_l)
    d_t[boun_attr_d['collapsed_building']] = attr[attr_d['collapsed_building']]
    animal_casualty_l = list()
    if attr[attr_d['big_animal_casualty']]:
        animal_casualty_l.append(f'{attr[attr_d["big_animal_casualty"]]} büyük hayvan')
    if attr[attr_d['small_animal_casualty']]:
        animal_casualty_l.append(f'{attr[attr_d["small_animal_casualty"]]} küçük hayvan')
    d_t[boun_attr_d['animal_casualty']] = ' ; '.join(animal_casualty_l)
    d_t[boun_attr_d['animal_food']] = attr[attr_d['animal_food']]
    d_t[boun_attr_d['road_access']] = attr[attr_d['road_access']]
    extra_l = [i for i in [attr[attr_d['extra']], attr[attr_d['comments']]] if i]
    d_t[boun_attr_d['comments']] = ' ; '.join(extra_l)
    merged_d[loc] = d_t

date_t = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
with open(f'itub-boun-merged_adiyaman_{date_t}.json', 'w') as f:
    json.dump(merged_d, f, indent=4, ensure_ascii=False)

merged_l = list()
for key in merged_d.keys():
    el = merged_d[key]
    merged_l.append(el)

with open(f'itub-boun-merged_adiyaman_{date_t}.csv', 'w') as f:
    w = csv.DictWriter(f, boun_attr_d.values())
    w.writeheader()
    w.writerows(merged_l)
