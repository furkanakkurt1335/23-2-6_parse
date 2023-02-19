import os
import pandas as pd
from datetime import datetime

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
filename = 'maras.xlsx'
df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
sheet_l = list(df_t.keys())
sheet_t = sheet_l[5]
for i in range(len(df_t[sheet_t])):
    for col in df_t[sheet_t].columns:
        el_t = df_t[sheet_t][col][i]
        if isinstance(el_t, (datetime)):
            el_t = str(el_t.month) + '-' + str(el_t.day)
            print(el_t)
            input()
