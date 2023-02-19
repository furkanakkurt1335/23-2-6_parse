import json
import pandas as pd
from fuzzywuzzy import fuzz

with open('data.json', 'r') as f:
    data = json.load(f)
feats = data['features']

itub_maras_l = list()
for feat in feats:
    attr = feat['attributes']
    g_id = attr['globalid']
    loc = attr['k_y_adi']
    if loc != None and loc not in itub_maras_l and 'mara' in loc.lower():
        itub_maras_l.append(loc)

print(len(itub_maras_l))
with open('itub_maras_l.json', 'w') as f:
    json.dump(itub_maras_l, f, ensure_ascii=False, indent=4)