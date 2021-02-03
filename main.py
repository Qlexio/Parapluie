from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.utils import platform

from datetime import datetime
from plyer import notification
from plyer import vibrator 
from plyer import gps
from plyer import uniqueid

class Error_Sys(Screen):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = BoxLayout()
        self.text = ""
        self.label = Label(text= self.text)
        layout.add_widget(self.label)
        self.add_widget(layout)

import_error = Error_Sys(name= "Import_Error")
try:
    from kivy_garden.mapview import MapView, MapMarker
except Exception as e:
    error_text = "Mapview import: " + str(e)
    import_error.label.text= error_text

from app_dairy import Dairy
import app_dairy
from app_init import First
import app_init
from app_bdd import Dates, Addresses, session
from app_get_loc import get_address, get_gps
import app_get_loc
from weather_forecast import get_current_weather, get_forecast

import certifi
import os

# Here's all the magic !
os.environ['SSL_CERT_FILE'] = certifi.where()


class Forecast(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.current_time = datetime.now()

        #test variable
        self.test = ""
        self.type = ""
        self.status = ""

        #image
        self.image_bool = True

        #gps config and start, get lat and lon values
        self.address = ""
        self.lat = 0
        self.lon = 0

        main_layout = BoxLayout(orientation= "vertical")

        actual_forecast = GridLayout(cols= 2, size_hint= (1, 0.3))#size_hint= (1, 1))
        Clock.schedule_interval(self.update_image, 300)
        self.img = Image(source= "./umbrella.png", size_hint= (0.4, 1), 
            pos_hint= {"center_x": 0.5, "center_y": 0.5}
            )
        info = BoxLayout(orientation= "vertical")
        Clock.schedule_interval(self.update_clock, 1)
        self.time_label = Label(text= self.current_time.strftime("%H:%M:%S"))
        info.add_widget(self.time_label)
        self.pos_label = Label(text= f"{self.address} + {self.test}", 
            text_size= (info.width * 3, None))
        info.add_widget(self.pos_label)

        actual_forecast.add_widget(self.img)
        actual_forecast.add_widget(info)

        main_layout.add_widget(actual_forecast)

        # if platform == "android":
        #     Clock.schedule_interval(self.gps_run, 10)

        self.next_forecast = BoxLayout(orientation= "vertical")
        next = Label(text= "Prévisions à venir", size_hint= (1, 0.2),
            text_size = (Window.width * 0.9, None)
            )
        self.next_forecast.add_widget(next)
        
        self.map = MapView(zoom= 11, lat= float(self.lat), lon= float(self.lon))
        self.current_loc = MapMarker(lat= float(self.lat), lon= float(self.lon), source= "./marker.png")
        self.current_loc.bind(on_press= self.marker_popup)
        self.map.add_marker(self.current_loc)
        self.next_forecast.add_widget(self.map)
        main_layout.add_widget(self.next_forecast)

        button = Button(text="Agenda", size_hint= (1, 0.2))
        button.bind(on_press=self.get_dairy)
        main_layout.add_widget(button)

        self.add_widget(main_layout)

    def marker_popup(self, *args):
        box = BoxLayout(orientation= "vertical")
        text = "Vous êtes au: \n" + self.address
        label = Label(text= text, text_size = (Window.width * 0.9, None))
        ok_button = Button(text="OK", size_hint= (1, 0.2))
        ok_button.bind(on_press= self.marker_popup_dismiss)
        box.add_widget(label)
        box.add_widget(ok_button)
        self.mark_popup = Popup(title= "Informations:", content= box)
        self.mark_popup.open()
    
    def marker_popup_dismiss(self, *args):
        self.mark_popup.dismiss()

    def get_dairy(self, *arg):
        my_app.sm.current = "Agenda"
    
    def update_clock(self, *args):
        self.time_label.text = main_time().strftime("%H:%M:%S")
        
        self.pos_label.text= f"{self.address} + {self.test} \n {self.lat}, {self.lon}" #Une phrase super gavée longue pour tester ce que je veux faire
        self.current_loc.lat = float(self.lat)
        self.current_loc.lon = float(self.lon)

        if self.image_bool and self.lat != 0 and self.lon != 0:
            if get_current_weather(self.lat, self.lon) < 0.1:
                self.img.source = "./sun.png"
            else:
                self.img.source = "./umbrella.png"
            self.image_bool = False
    
    def update_image(self, *args):
        if get_current_weather(self.lat, self.lon) < 0.1:
            self.img.source = "./sun.png"
        else:
            self.img.source = "./umbrella.png"
    
    # def gps_run(self, *args):
    #     gps_initialisation = GPS_Init()
    #     gps_initialisation.gps_loc_gps()


map_bool = True
def get_location(**kwargs):
    global map_bool    

    lat = kwargs.get("lat", "No lat")
    lon = kwargs.get("lon", "No lon")

    num, street, zipcode, city = get_address(app_get_loc.device_id, lat, lon)
    forecasting.address = num + " " + street + " " + zipcode + " " + city
    forecasting.lat = float(lat)
    forecasting.lon = float(lon)

    if map_bool:
        forecasting.map.center_on(float(lat), float(lon))
        map_bool = False

def get_status(stype, status):
    forecasting.type = str(stype)
    forecasting.status = str(status)

def main_time():
    return datetime.now()


def get_init():

    if not session.query(Addresses).filter(Addresses.id == 1).all():
        return False
    else:
        return True


# class Error_Sys(Screen):
#     def __init__(self, **kwargs):

#         super().__init__(**kwargs)

#         layout = BoxLayout()
#         self.text = ""
#         self.label = Label(text= self.text)
#         layout.add_widget(self.label)
#         self.add_widget(layout)

# class Testing(Screen):
#     def __init__(self, **kwargs):

#         super().__init__(**kwargs)
#         layout = BoxLayout()
#         img = Image(source="./sun.png")
#         layout.add_widget(img)
#         self.add_widget(layout)
from jnius import autoclass, java_method, PythonJavaClass

error_test = Error_Sys(name= "GPS_Test")
error_gps = Error_Sys(name = "GPS_Init")
class GPS_Init():

    def __init__(self):
        try:
            self.lat= 0
            self.lon= 0
            # self.speed= ""
            # self.bearing= ""
            # self.altitude= ""
            # self.accuracy= ""
            
            self.Looper = autoclass('android.os.Looper')
            self.context = autoclass('android.content.Context')
            self.activity = autoclass('org.renpy.android.PythonActivity').mActivity
            self.locationManager = self.activity.getSystemService(self.context.LOCATION_SERVICE)
            self.location_listener = _LocationListener(self)
        except Exception as e:
            error_gps.label.text = "GPS_Init: " + str(e)

    
    def gps_loc_gps(self, *args):
        try:
            providers_name = self.locationManager.getProviders(True).toArray()

            # error_test.label.text = (str(providers_name[0]) + "\n" + str(providers_name[1]) 
            #     + "\n" + str(providers_name[2]))
            for provider in providers_name:
                if str(provider) == "gps":
                    # self.running_gps(provider)
                    self.locationManager.requestLocationUpdates(
                        provider,
                        1000,  # minTime, in milliseconds
                        1,  # minDistance, in meters
                        self.location_listener,
                        self.Looper.getMainLooper())
                    # if self.lat != 0 and self.lon != 0:
                    #     break
                # elif str(provider) == "network":
                #     self.running_gps(provider)
                    error_test.label.text = (str(provider) + "\n" + "Lat : " + str(type(self.lat)) + "\n" + 
                        str(self.lat) + "\n Lon: " + str(type(self.lon)) + "\n" + str(self.lon)
                        + "\n" + main_time().strftime("%H:%M:%S"))
                # error_test.label.text += str(provider) + "\n"# str(locationManager.getProvider(provider)) + " - "

        except Exception as e:
            error_text = "Launch GPS: " + str(e)
            error_test.label.text = error_text

    # def running_gps(self, provider):
    #     self.locationManager.requestLocationUpdates(
    #     provider,
    #     5000,  # minTime, in milliseconds
    #     1,  # minDistance, in meters
    #     self.location_listener,
    #     self.Looper.getMainLooper())


class _LocationListener(PythonJavaClass):
    __javainterfaces__ = ['android/location/LocationListener']

    def __init__(self, root):
        self.root = root
        super(_LocationListener, self).__init__()

    @java_method('(Landroid/location/Location;)V')
    def onLocationChanged(self, location):
        self.root.lat=location.getLatitude()
        self.root.lon=location.getLongitude()
        # self.root.speed=location.getSpeed()
        # self.root.bearing=location.getBearing()
        # self.root.altitude=location.getAltitude()
        # self.root.accuracy=location.getAccuracy()

    # @java_method('(Ljava/lang/String;)V')
    # def onProviderEnabled(self, status):
    #     if self.root.on_status:
    #         self.root.on_status('provider-enabled', status)

    # @java_method('(Ljava/lang/String;)V')
    # def onProviderDisabled(self, status):
    #     if self.root.on_status:
    #         self.root.on_status('provider-disabled', status)

    # @java_method('(Ljava/lang/String;ILandroid/os/Bundle;)V')
    # def onStatusChanged(self, provider, status, extras):
    #     if self.root.on_status:
    #         s_status = 'unknown'
    #         if status == 0x00:
    #             s_status = 'out-of-service'
    #         elif status == 0x01:
    #             s_status = 'temporarily-unavailable'
    #         elif status == 0x02:
    #             s_status = 'available'
    #         self.root.on_status('provider-status', '{}: {}'.format(
    #             provider, s_status))


class Application(App):

    def __init__(self, **kwargs):
        """Initialize Dairy class."""
        super().__init__(**kwargs)

        self.sm = ScreenManager()
        self.dairy = Dairy(name="Agenda")
        self.forecast = Forecast(name="Main")
        self.init_page = First(name= "First")
        self.error = Error_Sys(name= "Error")

        # self.testing = Testing(name= "Test")
        # self.sm.add_widget(self.testing)

        self.sm.add_widget(self.dairy)
        self.sm.add_widget(self.forecast)
        self.sm.add_widget(self.init_page)
        self.sm.add_widget(self.error)

        self.sm.add_widget(import_error)
        self.sm.add_widget(error_test)
        self.sm.add_widget(error_gps)

    def build(self):

        if platform == "android":
            try:
                from android.permissions import request_permissions, Permission 
            except Exception as e:
                error_text = "android.Permission: " + str(e)
                self.error.label.text = error_text
                self.sm.current = "Error"
                return self.sm    
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,
                Permission.INTERNET, Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION,
                Permission.VIBRATE, Permission.ACCESS_NETWORK_STATE, Permission.CHANGE_NETWORK_STATE])

        try:
            from jnius import autoclass
        except Exception as e:
            error_text = "jnius: " + str(e)
            self.error.label.text = error_text
            self.sm.current = "Error"
            return self.sm

        if platform == "android":
            try:
                # from android import AndroidService
                service = autoclass('org.parapluie.parapluie.ServiceParapservice')
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                argument = ''
                service.start(mActivity, argument)
                self.service = service
            except Exception as e:
                error_text = "Service: " + str(e)
                self.error.label.text = error_text
                self.sm.current = "Error"
                return self.sm

            try:
                from oscpy.server import OSCThreadServer
            except Exception as e:
                error_text = "oscAPI import: " + str(e)
                self.error.label.text = error_text
                self.sm.current = "Error"
                return self.sm

            try:
                self.osc = OSCThreadServer()
                self.osc.listen(address= b"localhost", port= 8000 ,default= True)
                Clock.schedule_interval(self.listener, 0)
                # @osc.address(u"/listener")
                # def listener(*args):
                #     self.forecast.test = args
            except Exception as e:
                error_text = "osc: " + str(e)
                self.error.label.text = error_text
                self.sm.current = "Error"
                return self.sm

        if import_error.label.text != "":
            self.sm.current = "Import_Error"
            return self.sm

        try:
            if get_init():
                self.sm.current = "Main"
            else:
                self.sm.current = "First"
        except Exception as e:
            error_text = "Screen: " + str(e)
            self.error.label.text = error_text
            self.sm.current = "Error"
            return self.sm

        # if error_test.label.text != "":
        #     self.sm.current = "GPS_Test"
        #     return self.sm

        if platform == "android":
            try:
                self.gps_run = GPS_Init()
                self.gps_run.gps_loc_gps()
                self.forecast.lat = self.gps_run.lat
                self.forecast.lon = self.gps_run.lon
            
                # Clock.schedule_interval(self.gps_run.gps_loc_gps, 10)
                # if error_test.label.text != "":
                #     self.sm.current = "GPS_Test"
                #     return self.sm
            except Exception as e:
                self.error.label.text = "Clock: " + str(e)
                self.sm.current = "Error"
                return self.sm

        if error_gps.label.text != "":
                    self.sm.current = "GPS_Init"
                    return self.sm
        if error_test.label.text != "":
                    self.sm.current = "GPS_Test"
                    return self.sm
        
            # try:
            #     gps.configure(on_location= get_location, on_status= get_status)
            #     gps.start()
            # except Exception as e:
            #     error_text = "GPS: " + str(e)
            #     self.error.label.text = error_text
            #     self.sm.current = "Error"
            #     return self.sm
            

        return self.sm

    def listener(self, *args):
        self.osc.bind(b"/listener", self.test)

    def test(self, message):
        self.forecast.test = message.decode("utf-8")

    # def gps_run(self, *args):
    #     try:
    #         gps_initialisation = GPS_Init()
    #         gps_initialisation.gps_loc_gps()

    #         if error_test.label.text != "":
    #             self.sm.current = "GPS_Test"
    #             return self.sm
    #         # self.forecast.lat = gps_initialisation.lat
    #         # self.forecast.lon = gps_initialisation.lon
    # #         self.error.label.text = "Lat: " + str(gps_initialisation.lat) + "\n" + "Lon: " + str(gps_initialisation.lon)
    # #         self.sm.current = "Error"
    # #         return self.sm
    #     except Exception as e:
    #         self.error.label.text = str(e)
    #         self.sm.current = "Error"
    #         return self.sm


my_app = Application()
forecasting = my_app.forecast
app_dairy.main_app = my_app.dairy
app_dairy.first_page = my_app
app_init.get_main_page = my_app

if __name__ == "__main__":
    app = my_app  
    app.run()