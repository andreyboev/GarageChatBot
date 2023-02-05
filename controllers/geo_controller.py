from geopy import geocoders


def get_city_info(city: str):
    geolocator = geocoders.Nominatim(user_agent='aiogram')
    geo_objects = geolocator.geocode(city, language='RU', exactly_one=False, addressdetails=True, namedetails=True)
    if geo_objects is not None:
        for city_info in geo_objects:
            if city_info is not None and city_info.raw['type'] in ['town', 'city', 'administrative']:
                return city_info
    return city_info


def check_city(city: str):
    geolocator = geocoders.Nominatim(user_agent='aiogram')
    geo_objects = geolocator.geocode(city, language='RU', exactly_one=False, addressdetails=True, namedetails=True)
    if geo_objects is not None:
        for city_info in geo_objects:
            if city_info is not None and city_info.raw['type'] in ['town', 'city', 'administrative']:
                city_names = [c.lower() for c in city_info.raw['namedetails'].values()]
                if city.lower() in city_names:
                    return True
                else:
                    return False
                latitude = city_info.latitude
                longitude = city_info.longitude
                return latitude > 0 and longitude > 0
    return False
