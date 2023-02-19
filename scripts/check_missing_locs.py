import os, csv

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(THIS_FOLDER, '../data')
improved_data_path = os.path.join(data_folder, 'improved-icisleri.csv')
headers = ['Il', 'Ilce', 'Muhtarlik', 'Muhtar', 'Boylam', 'Enlem', 'Kaynak']
with open(improved_data_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    data = list(reader)

missing_count = 0
found_count = 0
for i, row in enumerate(data):
    if not (row[4] and row[5]):
        missing_count += 1
print('Finished')
print('Missing count:', missing_count)