# FILENAME: pyowmtest.py
# A test using the PyOWM Python library

import pyowm
from pyowm.caches.lrucache import LRUCache

API_KEY = "5f491cf983a134e99b6acac98697d065"

owm = pyowm.OWM(API_KEY)
cache = LRUCache()

reg = owm.city_id_registry()
obs = owm.weather_at_place("Ellicott City")

weather = obs.get_weather()

print("It is currently", round(weather.get_temperature(unit="fahrenheit").get("temp")), "degrees Fahrenheit and", weather.get_detailed_status(), ".")