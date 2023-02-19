import pandas as pd
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
phone_folder = 'phones/'
csv_files = [i for i in os.listdir(os.path.join(THIS_DIR, phone_folder)) if i.endswith('.csv')]
cols = ['Il', 'Ilce', 'Muhtarlik', 'Muhtar', 'Tel', 'Kaynak']
df = pd.DataFrame(columns=cols)

for file in csv_files:
    print(file, 'added')
    file_pth = os.path.join(THIS_DIR, phone_folder, file)
    df_t = pd.read_csv(file_pth)
    df = pd.concat([df_t, df], ignore_index=True)

phones_pth = os.path.join(THIS_DIR, phone_folder, 'phones.csv')
df.to_csv(phones_pth, index=False)