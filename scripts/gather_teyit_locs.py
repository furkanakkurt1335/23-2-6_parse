import os
import pandas as pd
import dateparser, datetime

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))

folder = os.path.join(THIS_FOLDER, '../phone_access_sheets')
city_l = ['maras', 'kilis', 'hatay']
city_d = {'maras': 'Kahramanmaraş', 'kilis': 'Kilis', 'hatay': 'Hatay', 'adiyaman': 'Adıyaman'}
cols = ['il', 'ilce', 'koy', 'muhtar', 'tel', 'teyit']
df = pd.DataFrame(columns=cols)
for city in city_l:
    filename = city + '.xlsx'
    df_t = pd.read_excel(os.path.join(folder, filename), sheet_name=None)
    sheet_l = list(df_t.keys())
    for sheet_t in sheet_l:
        for i in range(len(df_t[sheet_t])):
            include = True
            d_t = {'il': city_d[city], 'ilce': sheet_t}
            village = df_t[sheet_t]['mahalle'][i]
            if village != village:
                continue
            for j, col in enumerate(df_t[sheet_t].columns):
                if 'teyit' in col.lower():
                    date_called = df_t[sheet_t][col][i]
                    if type(date_called) != str:
                        continue
                    date_called = dateparser.parse(date_called)
                    if date_called:
                        if date_called >= datetime.datetime(2023, 2, 16):
                            include = False
                            break
                el_t = df_t[sheet_t][col][i]
                if el_t == el_t:
                    d_t[col] = df_t[sheet_t][col][i]
                else:
                    d_t[col] = ''
            if not include:
                continue
            reached = False
            for key in list(d_t.keys())[6:]:
                if d_t[key]:
                    reached = True
            if reached:
                new_d = {'il': d_t['il'], 'ilce': d_t['ilce'], 'koy': d_t['mahalle'], 'muhtar': d_t['muhtar'], 'tel': d_t['tel no']}
                df = pd.concat([df, pd.DataFrame(new_d, index=[0])], ignore_index=True)
                print(df.tail(1))

df.to_csv(os.path.join(THIS_FOLDER, '../phone_access_sheets/teyit_edilecekler.csv'), index=False)
