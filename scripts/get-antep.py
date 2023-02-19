import pandas as pd
import json
from datetime import datetime

df = pd.read_csv('results.csv', encoding='utf-8')
new_df = pd.DataFrame(columns=df.columns)
for i in range(len(df)):
    city = df['İl'][i]
    village = str(df['Köy'][i])
    ts_t = str(df['Bilgi Alınan Vakit'][i])
    if ts_t != 'nan' and ts_t.isdigit():
        ts_t = datetime.fromtimestamp(int(ts_t[:10])).strftime('%d/%m/%y %H:%M')
        df['Bilgi Alınan Vakit'][i] = ts_t
    if 'antep' in city.lower() or (village != 'nan' and 'antep' in village.lower()):
        new_df = pd.concat([new_df, df.iloc[i:i+1]], ignore_index=True)
new_df.to_csv('itub-antep_16-02_11-40.csv', index=False, encoding='utf-8')