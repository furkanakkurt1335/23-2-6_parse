import json
from fuzzywuzzy import fuzz
import pandas as pd

with open('unmatched_l.json', 'r') as f:
    unmatched_l = json.load(f)

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

match_count = 0
for loc in unmatched_l:
    max_ratio, match = 0, ''
    for itub_loc in itub_maras_l:
        ratio_t = fuzz.token_set_ratio(loc, itub_loc)
        if ratio_t > max_ratio:
            max_ratio = ratio_t
            match = itub_loc
    if max_ratio > 90:
        print(loc, match, max_ratio)
        match_count += 1

print('Matched:', match_count)
print('Unmatched:', len(unmatched_l) - match_count)