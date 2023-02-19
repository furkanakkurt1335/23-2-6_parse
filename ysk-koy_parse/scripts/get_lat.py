from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='Me')

address = f'Gaziantep, Turkey'
location = geolocator.geocode(address)
print(address, location.latitude, location.longitude)