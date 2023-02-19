import json
import pandas as pd

with open('msgsu_matched-phone.json') as f:
    matched_phone_l = json.load(f)

cols = ['msgsu_city', 'msgsu_district', 'msgsu_village', 'msgsu_phone', 'phone', 'our-source']
df = pd.DataFrame(matched_phone_l, columns=cols)
df.to_csv('msgsu_matched-phone.csv', index=False)