import os, json
import pandas as pd
import numpy as np

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

cols_tr_en_path = os.path.join(THIS_FOLDER, 'cols_tr-en.json')
with open(cols_tr_en_path, 'r') as f:
    cols_tr_en_d = json.load(f)
cols_en_tr_path = os.path.join(THIS_FOLDER, 'cols_en-tr.json')
with open(cols_en_tr_path, 'r') as f:
    cols_en_tr_d = json.load(f)

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
df = pd.DataFrame()
filename = 'hatay.xlsx'
df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
sheet_l = list(df_t.keys())
sheet_t = sheet_l[1]
for i in range(len(df_t[sheet_t])):
    for col in df_t[sheet_t].columns:
        el_t = df_t[sheet_t][col][i]
        if isinstance(el_t, (bool, np.bool_)):
            print(True, df_t[sheet_t][col][i])
            input()