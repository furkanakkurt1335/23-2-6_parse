import json
with open('results.json', 'r') as f:
    res_d = json.load(f)
for key in res_d.keys():
    dist_t = res_d[key]['distance']
    dist_t = '{:.2f}'.format(dist_t)
    res_d[key]['distance'] = float(dist_t)
with open('results.json', 'w') as f:
    json.dump(res_d, f, ensure_ascii=False, indent=4)
