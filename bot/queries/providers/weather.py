import forecastio
from geopy.geocoders import Nominatim
from utils.mongo import Mongo
import re
from .baseprovider import BaseProvider

local = {
    'ru': re.compile('(?i)погода'),
    'en': re.compile('(?i)weather')
}


class WeatherProvider(BaseProvider):
    @staticmethod
    def get(query, config, params={}, lang='en'):
        if local[lang].match(query) and 'user_id' in params:
            mongo = Mongo('users')
            user_location = mongo.get_user_location(params['user_id'])
            lat, lng = user_location['lat'], user_location['long']
        else:
            geolocator = Nominatim()
            location = geolocator.geocode(query)
            if location is None:
                return {
                    'content': 'nan'
                }
            lat, lng = location.latitude, location.longitude
        forecast = forecastio.manual('https://api.forecast.io/forecast/%s/%s,%s?units=%s&lang=%s' % (
            config['forecastio_api_key'], lat, lng, "auto", lang
        ))
        if forecast is None:
            return {
                'content': 'nan'
            }
        return {
            'type': 'text',
            'content': forecast.daily().summary
        }
