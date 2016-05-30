import forecastio
from geopy.geocoders import Nominatim
import os


def get(query, lang='en'):
    geolocator = Nominatim()
    location = geolocator.geocode(query)
    if location is None:
        return {
            'content': 'nan'
        }
    lat, lng = location.latitude, location.longitude
    forecast = forecastio.manual('https://api.forecast.io/forecast/%s/%s,%s?units=%s&lang=%s' % (
        os.environ['forecastio_api_key'], lat, lng, "auto", lang
    ))
    if forecast is None:
        return {
            'content': 'nan'
        }
    return {
        'type': 'text',
        'content': forecast.daily().summary
    }
