import pandas as pd
import os, json

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
phone_folder = 'phones/'
csv_file = 'urfa.csv'
source_pth = os.path.join(THIS_DIR, phone_folder, 'sources.json')
with open(source_pth, 'r', encoding='utf-8') as f:
    sources = json.load(f)
source = sources[csv_file]
pth = os.path.join(THIS_DIR, phone_folder, csv_file)

df = pd.read_csv(pth)
df.insert(len(df.columns), 'Kaynak', source)

# for i in range(len(df)):
#     phone = str(df['Tel'][i])
#     phone2 = str(df['Tel-2'][i])
#     phone_l = list()
#     if phone != 'nan':
#         phone_l.append(phone)
#     if phone2 != 'nan':
#         phone_l.append(phone2)
#     new_phone = ';'.join(phone_l)
#     df['Tel'][i] = new_phone

# df.drop('Tel-2', axis=1, inplace=True)
df.to_csv(pth, index=False)