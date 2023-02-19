import os, csv
from time import sleep
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="improve-icisleri-geopy")

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(THIS_FOLDER, '../data')
improved_data_path = os.path.join(data_folder, 'improved-icisleri.csv')
headers = ['Il', 'Ilce', 'Muhtarlik', 'Muhtar', 'Boylam', 'Enlem', 'Kaynak']
with open(improved_data_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    data = list(reader)

missing_count, found_count = 0, 0
for i, row in enumerate(data):
    if not (row[4] and row[5]):
        print(f'Not in data {i}', end=', ')
        city = row[0]
        district = row[1]
        village = row[2]
        loc = geolocator.geocode(f'{city} {district} {village}')
        if loc:
            data[i][4] = loc.longitude
            data[i][5] = loc.latitude
            print('found')
            found_count += 1
        else:
            missing_count += 1
    if i % 100 == 0:
        with open(improved_data_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        print('Saved', i, 'found', found_count, 'missing', missing_count)
with open(improved_data_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)
print('Finished')
print('Found count:', found_count)
print('Missing count:', missing_count)