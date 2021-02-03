from time import sleep

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from urllib.parse import quote_plus

from plyer import uniqueid

device_id = "Parapluie" #uniqueid.id

def get_gps(device_id, num, street, zipcode, city):

    address = quote_plus(num + ", " + street + ", " + city + ", " + zipcode)
    format = "json"

    params = "search?q=" + address + "&format=" + format
    url = "https://nominatim.openstreetmap.org/" + params

    headers = {"User-Agent": device_id}

    response = UrlRequest(url, req_headers= headers)

    while not response.is_finished:
        sleep(0.1)
        Clock.tick()

    # print(f"Lat: {response.result[0]['lat']}, Long: {response.result[0]['lon']}")
    if response.result:
        return response.result[0]['lat'], response.result[0]['lon']
    else:
        return None, None
    
def get_address(device_id, lat, lon):

    headers = {"User-Agent": device_id}
    format = "json"
    params = "reverse?format=" + format + "&lat=" + str(lat) + "&lon=" + str(lon)
    url = "https://nominatim.openstreetmap.org/" + params

    response = UrlRequest(url, req_headers= headers)

    while not response.is_finished:
        sleep(0.1)
        Clock.tick()

    # print(response.result["address"]["house_number"], response.result["address"]["road"],
    #     response.result["address"]["postcode"], response.result["address"]["city"])
    return (response.result["address"]["house_number"], response.result["address"]["road"],
            response.result["address"]["postcode"], response.result["address"]["city"])

# lat, lon = get_gps(device_id, "126", "rue belleville", "33000", "bordeaux")
# print(lat, " ", lon)