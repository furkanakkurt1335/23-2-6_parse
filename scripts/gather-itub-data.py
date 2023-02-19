from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import requests, re, json, os
from datetime import datetime

import pandas as pd

def getAddress(x, y):
    geolocator = Nominatim(user_agent='Me')
    location = geolocator.reverse(f'{y}, {x}')
    fields = location.address.split(', ')
    new_fields = list()
    for i in range(len(fields)):
        if not fields[i].isnumeric():
            new_fields.append(fields[i])
    fields = new_fields
    district, city = fields[-4], fields[-3]
    centre = geolocator.geocode(city)
    distance = geodesic((location.latitude, location.longitude), (centre.latitude, centre.longitude)).km
    return city, district, distance

def get_res(res_d, f_add):
    i = 1
    url = 'https://services1.arcgis.com/cUk609GYnOSB8Ppx/ArcGIS/rest/services/survey123_1b06d3b50ce541559b5275095d763f1c/FeatureServer/0/query?where=1%3D1&fullText=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=CreationDate%2CCreator%2CEditDate%2CEditor%2C_htiya_duydu_unuz_di_er_temel_m%2C_kinci_ncelikli_ihtiya_duydu_un%2C_nc_ncelikli_ihtiya_duydu_unuz%2Cac_l_yet_durumu%2Cafad_taraf_ndan_arama_kurtarma%2Caltyap_eksikli_i_elektrik_su_do%2Cara_s_k_nt_s_var_m%2Cb_lg_ed_n_len_saat%2Cbirinci_ncelikli_ihtiya_duydu_u%2Cengel_durumlar_nedir%2Cengelli_birey_var_m%2Cenkaz_alt_nda_oldu_unu_bildi_in%2Cenkaz_alt_nda_oldu_unu_tahmin_e%2Chane_say_s_nedir%2Chastaneye_eri_im_sa_lanabiliyor%2Chayvanlar_i_in_gerekli_besin_g%2Ck_y_adi%2Ck_y_n_zde_hasarl_ka_bina_var%2Ck_y_n_zde_y_k_lan_ka_bina_var%2Ck_ydeki_kad_n_n_fusu_nedir%2Ck_ydeki_ocuk_0_18_n_fusu_nedir%2Ck_ydeki_ya_l_n_fusu_65_nedir%2Ck_ydeki_yeti_kin_18_65_n_fusu_n%2Cka_engelli_birey_var%2Ckapal_ya_da_etkilenen_yol_var_m%2Ckay_p_ki_i_say_s_nedir%2Ckronik_hastal_olan_var_m_eker_t%2Cliste_d_nda_belirtmek_istedi_in%2Ctelef_olan_b_y_kba_hayvan_say_s%2Ctelef_olan_k_kba_hayvan_say_s_n%2Cvarsa_eklemek_istedikleriniz%2Cya_am_n_yitiren_ki_i_say_s_nedi%2Cobjectid%2Cglobalid&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=0&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token='
    r = requests.get(url)
    with open('itub-all-api-data.json', 'w') as f:
        json.dump(r.json(), f, indent=4, ensure_ascii=False)
    feats = r.json()['features']
    ph_pattern = '\+90\d{10}'
    ph_url = 'https://www.google.com/search?q=yandex+{city}+{district}+{village}+mahalle+muhtarl%C4%B1%C4%9F%C4%B1+telefon'
    g_id_l = list(res_d.keys())
    for feat in feats[0:]:
        print(i)
        i += 1
        attr = feat['attributes']
        g_id = attr['globalid']
        edit_date = int(str(attr['EditDate'])[:10])
        prev_edit_date = res_d[g_id]['edit_date'] if g_id in g_id_l else 0
        if g_id not in g_id_l:
            res_d[g_id] = { 'edit_date': 0 }
        if 'ts' in f_add:
            res_d[g_id]['ts'] = attr['b_lg_ed_n_len_saat']
            if edit_date == prev_edit_date and 'ts' in res_d[g_id].keys():
                continue
            if res_d[g_id]['ts']:
                try:
                    ts_t = int(str(res_d[g_id]['ts'])[:10])
                    res_d[g_id]['ts'] = datetime.fromtimestamp(ts_t).strftime('%d/%m/%y %H:%M')
                except:
                    res_d[g_id]['ts'] = None
            else:
                res_d[g_id]['ts'] = None
        if 'location' in f_add:
            if edit_date == prev_edit_date and 'location' in res_d[g_id].keys():
                continue
            res_d[g_id]['location'] = feat['geometry']
        if 'address' in f_add:
            if edit_date == prev_edit_date and 'city' in res_d[g_id].keys():
                continue
            x, y = feat['geometry']['x'], feat['geometry']['y']
            city, district, distance = getAddress(x, y)
            res_d[g_id]['distance'] = distance
            if 'k_y_adi' in attr.keys() and attr['k_y_adi']:
                village = attr['k_y_adi'].replace('/', ',')  # some of the names have '/' instead of ','
                if village.count(',') > 1:
                    vl_l = village.split(',')
                    city, district, village = vl_l[0].strip(), vl_l[1].strip(), vl_l[2].strip()
                else:
                    village = village.strip()
            else:
                village = ''
            res_d[g_id]['city'] = city
            res_d[g_id]['district'] = district
            res_d[g_id]['village'] = village.replace('KÖYÜ', '').strip()
        if 'need' in f_add:
            if edit_date == prev_edit_date and 'first_pr' in res_d[g_id].keys():
                continue
            res_d[g_id]['first_pr'] = attr['birinci_ncelikli_ihtiya_duydu_u']
            res_d[g_id]['second_pr'] = attr['_kinci_ncelikli_ihtiya_duydu_un']
            res_d[g_id]['third_pr'] = attr['_nc_ncelikli_ihtiya_duydu_unuz']
        if 'pop' in f_add:
            if edit_date == prev_edit_date and 'child_pop' in res_d[g_id].keys():
                continue
            res_d[g_id]['child_pop'] = attr['k_ydeki_ocuk_0_18_n_fusu_nedir']
            res_d[g_id]['female_pop'] = attr['k_ydeki_kad_n_n_fusu_nedir']
            res_d[g_id]['adult_pop'] = attr['k_ydeki_yeti_kin_18_65_n_fusu_n']
            res_d[g_id]['elder_pop'] = attr['k_ydeki_ya_l_n_fusu_65_nedir']
        if 'house' in f_add:
            if edit_date == prev_edit_date and 'house_count' in res_d[g_id].keys():
                continue
            res_d[g_id]['house_count'] = attr['hane_say_s_nedir']
            res_d[g_id]['collapsed'] = attr['k_y_n_zde_y_k_lan_ka_bina_var']
        if 'comments' in f_add:
            if edit_date == prev_edit_date and 'comments' in res_d[g_id].keys():
                continue
            res_d[g_id]['comments'] = attr['varsa_eklemek_istedikleriniz']
        if 'phone' in f_add:
            if 'city' not in res_d[g_id].keys():
                continue
            req = requests.get(ph_url.format(city=res_d[g_id]['city'], district=res_d[g_id]['district'], village=res_d[g_id]['village']))
            s = req.text.replace(' ', '')
            phs = re.findall(ph_pattern, s)
            if len(phs) > 0:
                res_d[g_id]['phone'] = phs[0].replace('+90', '0')
            else:
                res_d[g_id]['phone'] = None
        if edit_date > prev_edit_date:
            res_d[g_id]['edit_date'] = edit_date

    with open('results.json', 'w') as f:
        json.dump(res_d, f, ensure_ascii=False, indent=4)

def writeCSV(res_d):
    field_order = ['city', 'district', 'village', 'distance', 'first_pr', 'second_pr', 'third_pr', 'phone', 'child_pop', 'female_pop', 'adult_pop', 'elder_pop', 'house_count', 'collapsed', 'ts', 'comments']
    tr_cols = ['İl', 'İlçe', 'Köy', 'Merkeze uzaklık (km)', 'Birincil Öncelik', 'İkincil', 'Üçüncül', 'Telefon', 'Çocuk', 'Kadın', 'Yetişkin', 'Yaşlı', 'Hane', 'Yıkılan', 'Bilgi Alınan Vakit', 'Ek']
    df = pd.DataFrame(columns=tr_cols)
    for key in res_d.keys():
        res_t = res_d[key].copy()
        l_t = list()
        for k in field_order:
            if k == 'distance':
                distance_t = res_t[k]
                distance_t = '{:.2f}'.format(distance_t)
                l_t.append(distance_t)
            else:
                l_t.append(res_t[k])
        df = pd.concat([pd.DataFrame([l_t], columns=tr_cols), df], ignore_index=True)
    df['İl'].replace('Antep', 'Gaziantep', inplace=True)
    df['İl'].replace('Maraş', 'Kahramanmaraş', inplace=True)
    df['İl'].replace('Adiyaman', 'Adıyaman', inplace=True)
    # df.to_csv('results.csv', sep='\t', index=False, encoding='utf-8')
    # df.to_csv('results.csv', index=False, encoding='utf-8')
    date_t = datetime.now().strftime('%m-%d_%H-%M')
    df.to_csv(f'itub_results_{date_t}.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    res_d_path = 'results.json'
    if not os.path.exists(res_d_path):
        with open(res_d_path, 'w') as f:
            json.dump(dict(), f)

    with open(res_d_path, 'r') as f:
        res_d = json.load(f)

    fields_to_add = ['address', 'need', 'pop', 'house', 'ts', 'comments', 'phone', 'location']
    # fields_to_add = ['location']
    get_res(res_d, fields_to_add)
    with open('results.json', 'r') as f:
        res_d = json.load(f)
    writeCSV(res_d)
