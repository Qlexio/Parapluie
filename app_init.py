from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.popup import Popup

from app_bdd import Dates, Addresses, session
from app_get_loc import get_gps
import app_get_loc

from kivy.core.window import Window

get_main_page= ""

class First(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation= "vertical")

        self.info = Label(text= "Veuillez entrer votre adresse de résidence:",
            size_hint= (1, 0.4)
            )
        self.main_layout.add_widget(self.info)

        self.layout = GridLayout(cols=2)

        self.num_text = Label(text="N°: ")
        self.num_input = TextInput(
            text="",
            multiline=False,
            halign="right",
            input_filter="int",
        )
        self.layout.add_widget(self.num_text)
        self.layout.add_widget(self.num_input)

        self.street_text = Label(text="Rue: ")
        self.street_input = TextInput(
            text="", multiline=False, halign="right"
        )
        self.layout.add_widget(self.street_text)
        self.layout.add_widget(self.street_input)

        self.zip_text = Label(text="Code postal: ")
        self.zip_input = TextInput(
            text="",
            multiline=False,
            halign="right",
            input_filter="int",
        )
        self.layout.add_widget(self.zip_text)
        self.layout.add_widget(self.zip_input)

        self.city_text = Label(text="Ville: ")
        self.city_input = TextInput(
            text="", multiline=False, halign="right"
        )
        self.layout.add_widget(self.city_text)
        self.layout.add_widget(self.city_input)

        self.main_layout.add_widget(self.layout)

        self.ok = Button(text="OK", size_hint= (1, 0.2))
        self.ok.bind(on_press=self.press_ok)
        self.main_layout.add_widget(self.ok)

        self.add_widget(self.main_layout)

    def press_ok(self, instance):
        if (
            self.num_input.text
            and self.street_input.text
            and self.zip_input.text
            and self.city_input
        ):
            self.address_exists()
        else:
            string = "Veuillez remplir "
            if not self.num_input.text:
                string += " N° "
            if not self.street_input.text:
                string += " Rue "
            if not self.zip_input.text:
                string += " Code postal "
            if not self.city_input.text:
                string += " Ville "
            popup_layout = BoxLayout(orientation="vertical")
            popup_text = Label(text=string, text_size = (Window.width * 0.9, None))
            popup_button = Button(text="OK", size_hint=(1, 0.2))
            popup_button.bind(on_press=self.subpress_ok)
            popup_layout.add_widget(popup_text)
            popup_layout.add_widget(popup_button)
            self.subpopup = Popup(title="Attention:", content=popup_layout)
            self.subpopup.open()

    def subpress_ok(self, instance):
        self.subpopup.dismiss()

    def address_exists(self):

        latitude, longitude = get_gps(app_get_loc.device_id, self.num_input.text, 
            self.street_input.text, self.zip_input.text, self.city_input.text)
        if latitude == None and longitude == None:
            popup_layout = BoxLayout(orientation= "vertical")
            popup_text = Label(text= "L'adresse entrée n'est pas valide")
            popup_button = Button(text= "OK", size_hint= (1, 0.2))
            popup_button.bind(on_press= self.subpopup_ok)
            popup_layout.add_widget(popup_text)
            popup_layout.add_widget(popup_button)
            self.popup_address = Popup(title= "Erreur:", content= popup_layout)
            self.popup_address.open()
        else:
            address = Addresses(num = int(self.num_input.text), street = self.street_input.text,
                zipcode = int(self.zip_input.text), city = self.city_input.text, 
                lat = float(latitude), lon = float(longitude))
            session.add(address)
            session.commit()
            get_main_page.sm.current = "Main"

    def subpopup_ok(self, *args):
        self.popup_address.dismiss()