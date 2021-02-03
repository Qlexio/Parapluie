from app_get_loc import get_gps
#Latitude et longitude
### 126 rue Belleville 33000 Bordeaux
# lat= 44.8327537
# lon= -0.5839025
### 208 avenue de la Marne 33700 Mérignac
# lat= 44.832676
# lon= -0.6404702
# lat, lon = get_gps("Parapluie", "126", "rue belleville", "33000", "bordeaux")

from time import sleep
from datetime import datetime, timedelta

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from urllib.parse import quote_plus

# now = quote_plus((datetime.now() - timedelta(hours=2)).isoformat())
# print(now)

def get_current_weather(lat, lon):

    now = quote_plus((datetime.now() - timedelta(hours=2) + timedelta(minutes=1)).isoformat())

    url = ("https://api.climacell.co/v3/weather/nowcast?lat=" + str(lat) + "&lon=" + 
        str(lon) + "&unit_system=si&timestep=1&start_time=" + now + "&end_time=" + now + 
        "&fields%5B%5D=precipitation&apikey=59A8aKoDs3S4N7n9OZxv4ldEkFsL3he6")

    response = UrlRequest(url)

    while not response.is_finished:
        sleep(0.1)
        Clock.tick()

    return response.result[0]["precipitation"]["value"]

def get_forecast(lat, lon):

    now = quote_plus((datetime.now() - timedelta(hours=2)).isoformat())
    # end = quote_plus((datetime.now() - timedelta(hours=2) + timedelta(hours=48) + timedelta(minutes=1)).isoformat())

    url = ("https://api.climacell.co/v3/weather/forecast/hourly?lat=" + str(lat) + "&lon=" 
        + str(lon) + "&unit_system=si&start_time=" + now + #"&end_time=" + end +
        "&fields%5B%5D=precipitation&fields%5B%5D=precipitation_probability" + 
        "&apikey=59A8aKoDs3S4N7n9OZxv4ldEkFsL3he6")

    response = UrlRequest(url)

    while not response.is_finished:
        sleep(0.1)
        Clock.tick()

    print(str(int(response.result[0]["observation_time"]["value"].split("T")[1].split(":")[0]) + 2))
    #return response.result

# get_forecast(lat, lon)
# print(get_current_weather(lat, lon))

# print(int(datetime.now().strftime("%M")))

# print(lat, " ", lon)

# forecast_results = get_forecast(lat, lon)
# for i in forecast_results:
#     print(i)
# print("-" * 80)
# print(len(forecast_results))
# test= (1, 2)
# x = f"{test[0]}  ***  {test[1]}"
# print(type(test[0]))