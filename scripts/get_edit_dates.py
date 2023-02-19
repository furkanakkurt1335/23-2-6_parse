import json
from datetime import datetime

date_l = list()
with open('data.json', 'r') as f:
    data = json.load(f)
    feats = data['features']
    for feat in feats:
        attr = feat['attributes']
        g_id = attr['globalid']
        edit_date = str(attr['EditDate'])[:10]
        if edit_date != 'None':
            dt_t = datetime.fromtimestamp(int(edit_date)).strftime('%d/%m/%y %H:%M')
        else:
            dt_t = ''
        phone_date_str = str(attr['b_lg_ed_n_len_saat'])[:10]
        if phone_date_str != 'None':
            phone_dt_t = datetime.fromtimestamp(int(phone_date_str)).strftime('%d/%m/%y %H:%M')
        else:
            phone_dt_t = ''
        village_t = attr['k_y_adi']
        if dt_t.startswith('14/02/23') and phone_dt_t.startswith('14/02/23') and 'kahramanmara' in village_t.lower():
            date_l.append({'g_id': g_id, 'edit_date': dt_t, 'phone_date': phone_dt_t, 'village': village_t})

print(len(date_l))
# print(date_l)
with open('date_l.json', 'w') as f:
    json.dump(date_l, f, indent=4, ensure_ascii=False)
