from geopy.geocoders import Nominatim
import time
from math import radians, sin, cos, sqrt, atan2

geolocator = Nominatim(user_agent="lab_locator")


def get_coordinates(lab_name, city=None, region=None):
    try:
        print(f"Отримуємо координати для лабораторії: {lab_name}")
        query = lab_name
        if city:
            query += f", {city}"
        if region:
            query += f", {region}"

        # пошук лабораторії за назвою з лімітом
        locations = geolocator.geocode(query, exactly_one=False, limit=70)


        if locations:
            coordinates_list = []
            for idx, location in enumerate(locations):

                time.sleep(1)
                coordinates_list.append((location.latitude, location.longitude))
                print(f"Знайдено координати для {lab_name}: {location.latitude}, {location.longitude}")
                print(f"Оброблено лабораторію {idx + 1} з {len(locations)}")

            return coordinates_list

        print(f"Не знайдено координат для {lab_name}")
        return []

    except Exception as e:
        print(f"Помилка при отриманні координат для {lab_name}: {e}")
        return []




# Формула Гаверсина
def haversine(lat1, lon1, lat2, lon2):

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])


    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371
    distance = R * c

    return distance

def get_city_and_region(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="uk", exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city', None)
            region = address.get('state', None)
            print(f"Місто: {city}, Регіон: {region}")
            return city, region
        return None, None
    except Exception as e:
        print(f"Помилка при визначенні міста та регіону: {e}")
        return None, None