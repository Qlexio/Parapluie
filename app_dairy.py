"""
Manage Dairy page.

Show one page for one day
Move to different dates and hours
Add entry for one or multiple hours
"""

# from app_dairy_file import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

import calendar_data as cal_d
from calendar_ui import CalendarWidget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen


from app_bdd import Dates, Addresses, session
from app_get_loc import get_gps
import app_get_loc


# TODO Import calendar module
# TODO get today's date with datetime and show today's dairy
# TODO put actions in while loop:
# add entry
# next day
# previous day
# other day
# delete dairy informations
# quit

first_page = ""
main_app = ""

choosen_date = []
choosen_date.append(CalendarWidget().active_date[0])
choosen_date.append(
    CalendarWidget().month_names[CalendarWidget().active_date[1] - 1]
)
choosen_date.append(CalendarWidget().active_date[2])
choosen_date.append(CalendarWidget().days_abrs[CalendarWidget().week_day_num])
date_info = []
date_info.append(CalendarWidget().quarter_nums)
date_info.append(CalendarWidget().quarter)
date_info.append(CalendarWidget().week_day_num)

class Dairy(Screen):
    """Main Class for displaying window."""

    def __init__(self, **kwargs):
        """Initialize Dairy class."""
        super().__init__(**kwargs)
        self.date_layout = ""

        """Prncipal method."""
        main_layout = BoxLayout(orientation="vertical")

        # top buttons next, previous day and calendar
        top_layout = BoxLayout(size_hint=(1, 0.2))
        prev_day = Button(text="<<")
        prev_day.bind(on_press=Change_Day.prev_d)
        next_day = Button(text=">>")
        next_day.bind(on_press=Change_Day.next_d)
        calendar_button = Button(text="Calendrier")
        calendar_button.bind(on_press=Calendar_Buttons)
        top_layout.add_widget(prev_day)
        top_layout.add_widget(calendar_button)
        top_layout.add_widget(next_day)

        main_layout.add_widget(top_layout)
        # show choosen date, default = current date
        self.date_layout = Date_Layout()

        main_layout.add_widget(self.date_layout)
        # hours button of the day, with label and address.
        # TODO see to get hour, label and address if saved in dairy.txt
        self.hours_layout = Hour_Layout()
        self.hours_layout.bind(minimum_height=self.hours_layout.setter("height"))
        scroll = ScrollView()

        scroll.add_widget(self.hours_layout)
        main_layout.add_widget(scroll)
        # TODO return to main page
        cancel_button = Button(text="Retour", size_hint=(1, 0.2))
        cancel_button.bind(on_press= self.get_main)

        main_layout.add_widget(cancel_button)

        self.add_widget(main_layout)
    
    def get_main(self, *arg):
        first_page.sm.current = "Main"


class Change_Day:
    """Change days one by one."""

    global choosen_date
    global date_info

    def prev_d(self, *args):
        """Get previous day."""
        if choosen_date[0] == 1:
            if date_info[2] == 0:
                choosen_date[0] = date_info[1][0][-1][-1][0]
                choosen_date[1] = CalendarWidget().month_names[
                    date_info[0][0][1] - 1
                ]
                choosen_date[2] = date_info[0][0][0]
                date_info[2] = 6
                date_info[0] = cal_d.calc_quarter(
                    date_info[0][0][0], date_info[0][0][1]
                )
                date_info[1] = cal_d.get_quarter(
                    date_info[0][1][0], date_info[0][1][1]
                )
                choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]
            else:
                choosen_date[0] = date_info[1][1][0][date_info[2] - 1][0]
                choosen_date[1] = CalendarWidget().month_names[
                    date_info[0][0][1] - 1
                ]
                choosen_date[2] = date_info[0][0][0]
                date_info[2] = date_info[1][1][0][date_info[2] - 1][1]
                date_info[0] = cal_d.calc_quarter(
                    date_info[0][0][0], date_info[0][0][1]
                )
                date_info[1] = cal_d.get_quarter(
                    date_info[0][1][0], date_info[0][1][1]
                )
                choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]
        else:
            choosen_date[0] = choosen_date[0] - 1
            if date_info[2] == 0:
                date_info[2] = 6
            else:
                date_info[2] -= 1
            choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]

        main_app.date_layout.text = (
            str(choosen_date[3])
            + " "
            + str(choosen_date[0])
            + " "
            + str(choosen_date[1])
            + " "
            + str(choosen_date[2])
        )

        hour_update()

    def next_d(self, *args):
        """Get next day."""
        last_week = sorted(date_info[1][1][-1])
        if choosen_date[0] == last_week[-1][0]:
            if date_info[2] == 6:
                choosen_date[0] = 1
                choosen_date[1] = CalendarWidget().month_names[
                    date_info[0][2][1] - 1
                ]
                choosen_date[2] = date_info[0][2][0]
                date_info[2] = 0
                date_info[0] = cal_d.calc_quarter(
                    date_info[0][2][0], date_info[0][2][1]
                )
                date_info[1] = cal_d.get_quarter(
                    date_info[0][1][0], date_info[0][1][1]
                )
                choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]
            else:
                choosen_date[0] = 1
                choosen_date[1] = CalendarWidget().month_names[
                    date_info[0][2][1] - 1
                ]
                choosen_date[2] = date_info[0][2][0]
                date_info[2] = date_info[1][1][-1][date_info[2] + 1][1]
                date_info[0] = cal_d.calc_quarter(
                    date_info[0][2][0], date_info[0][2][1]
                )
                date_info[1] = cal_d.get_quarter(
                    date_info[0][1][0], date_info[0][1][1]
                )
                choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]
        else:
            choosen_date[0] = choosen_date[0] + 1
            if date_info[2] == 6:
                date_info[2] = 0
            else:
                date_info[2] += 1
            choosen_date[3] = CalendarWidget().days_abrs[date_info[2]]

        main_app.date_layout.text = (
            str(choosen_date[3])
            + " "
            + str(choosen_date[0])
            + " "
            + str(choosen_date[1])
            + " "
            + str(choosen_date[2])
        )

        hour_update()


class Date_Layout(Label):
    """Show current or choosen date."""

    global choosen_date

    def __init__(self, **kwargs):
        """Initialize Date_layout class."""
        super().__init__(**kwargs)
        self.text = (
            str(choosen_date[3])
            + " "
            + str(choosen_date[0])
            + " "
            + str(choosen_date[1])
            + " "
            + str(choosen_date[2])
        )
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.size_hint = (1, 0.2)


class Calendar_Popup(GridLayout):
    """Add CalendarWidget and buttons to layout."""

    def __init__(self, **kwargs):
        """Set CalendarWidget and buttons."""
        super().__init__(**kwargs)

        self.cols = 1
        self.size_hint = (1, 1)
        self.ok_canc_bool = False

        self.add_widget(CalendarWidget())

        self.bot_layout = BoxLayout(size_hint=(1, 0.2))

        self.ok = Button(text="OK")
        self.ok.bind(on_press=self.press_ok)
        self.cancel = Button(text="Annuler")
        self.cancel.bind(on_press=self.press_cancel)

        self.bot_layout.add_widget(self.ok)
        self.bot_layout.add_widget(self.cancel)
        self.add_widget(self.bot_layout)

    def press_ok(self, *args):
        """Set booleen to True and dismiss popup."""
        self.ok_canc_bool = True
        self.parent.parent.parent.dismiss()

    def press_cancel(self, *args):
        """Set booleen to False and dismiss popup."""
        self.ok_canc_bool = False
        self.parent.parent.parent.dismiss()


def popup_close(popup):
    """Set date when calendar popup closes."""
    global choosen_date
    global date_info

    cal_path = popup.content.children[1]

    if popup.content.ok_canc_bool:
        choosen_date[0] = cal_path.active_date[0]
        choosen_date[1] = cal_path.month_names[cal_path.active_date[1] - 1]
        choosen_date[2] = cal_path.active_date[2]
        choosen_date[3] = cal_path.days_abrs[cal_path.week_day_num]
        date_info[0] = cal_path.quarter_nums
        date_info[1] = cal_path.quarter
        date_info[2] = cal_path.week_day_num

    main_app.date_layout.text = (
        str(choosen_date[3])
        + " "
        + str(choosen_date[0])
        + " "
        + str(choosen_date[1])
        + " "
        + str(choosen_date[2])
    )
    
    hour_update()

class Calendar_Buttons:
    """Show popup when pressing "calendar" button."""

    def __init__(self, *args):
        """Popup calendar and dismiss actions."""
        self.calendar = Popup(title="Calendrier", content=Calendar_Popup())
        self.calendar.open()

        self.calendar.bind(on_dismiss=popup_close)


class Hour_Layout(GridLayout):
    """Hour class for setting hours display."""

    def __init__(self, **kwargs):
        """Set hour buttons."""
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (1, None)

        self.label = ""
        self.address = ". . ."
        self.city = ". . ."

        year_day = int(str(choosen_date[2]) + str(date_info[0][1][1]) + str(choosen_date[0]))
        tasks = (session.query(Dates.hour, Dates.label, Addresses.num, Addresses.street,
            Addresses.zipcode, Addresses.city).join(Addresses).filter(Dates.year_to_day== year_day).all())
        # print(tasks[0])

        self.hour_button = []
        for hour in range(24):
            if hour <= 9:
                hour = "0" + str(hour)
            
            for task in tasks:
                if str(hour) + "00" == task[0]:
                    self.label = task[1]
                    self.address = str(task[2]) + " " + task[3]
                    self.city = str(task[4]) + " " + task[5]
                    break
                else:
                    self.label = ""
                    self.address = ". . ."
                    self.city = ". . ."
                
            self.hour_text = (
                str(hour)
                + ":00\n"
                + self.label
                + "\n"
                + self.address
                + "\n"
                + self.city
            )
            self.hour_button_temp = Button(
                text=self.hour_text, size_hint_y=None, halign="center"
            )
            
            self.hour_button.append(self.hour_button_temp)

            self.temp = int(hour) * 2
            self.add_widget(self.hour_button[self.temp])

            self.hour_button[self.temp].bind(on_press=Hour_Button)

            for task in tasks:
                if str(hour) + "30" == task[0]:
                    self.label = task[1]
                    self.address = str(task[2]) + " " + task[3]
                    self.city = str(task[4]) + " " + task[5]
                    break
                else:
                    self.label = ""
                    self.address = ". . ."
                    self.city = ". . ."
               
            self.hour_text = (
                str(hour)
                + ":30\n"
                + self.label
                + "\n"
                + self.address
                + "\n"
                + self.city
            )
            self.hour_button_temp = Button(
                text=self.hour_text, size_hint_y=None, halign="center"
            )
            
            self.hour_button.append(self.hour_button_temp)

            self.temp = int(hour) * 2 + 1
            self.add_widget(self.hour_button[self.temp])

            self.hour_button[self.temp].bind(on_press=Hour_Button)

        self.bind(width=self.update_text_width)

    def update_text_width(self, *_):
        """Automatically resize button text."""
        for i in range(48):
            self.hour_button[i].text_size = (Window.width * 0.9, None)
            self.hour_button[i].size[1] = 200
            self.hour_button[i].texture_update()


class Hour_Button:
    def __init__(self, instance):
        super().__init__()
        self.instance = instance
        self.content = Hour_Popup(self.instance.text)

        self.hour_popup = Popup(title="Agenda", content=self.content)
        self.hour_popup.open()


class Hour_Popup(BoxLayout):
    def __init__(self, instance, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.instance = instance
        self.subpopup_bool = False

        self.original_text = self.instance.split("\n")
        self.num_street = self.original_text[2].split(" ", 1)
        self.zip_city = self.original_text[3].split(" ", 1)

        self.hour = Label(text=self.original_text[0], size_hint=(1, 0.2))
        self.add_widget(self.hour)
        # hour\n
        # label\n
        # n° + rue\n
        # zipcode + ville
        self.layout = GridLayout(cols=2)
        self.label_text = Label(text="Tache: ")
        self.label_input = TextInput(
            text=self.original_text[1], multiline=False, halign="right"
        )
        self.layout.add_widget(self.label_text)
        self.layout.add_widget(self.label_input)

        self.num_text = Label(text="N°: ")
        if self.num_street[0] == ".":
            self.num_street[0]= ""
        self.num_input = TextInput(
            text=self.num_street[0],
            multiline=False,
            halign="right",
            input_filter="int",
        )
        self.layout.add_widget(self.num_text)
        self.layout.add_widget(self.num_input)

        self.street_text = Label(text="Rue: ")
        if self.num_street[1] == ". .":
            self.num_street[1]= ""
        self.street_input = TextInput(
            text=self.num_street[1], multiline=False, halign="right"
        )
        self.layout.add_widget(self.street_text)
        self.layout.add_widget(self.street_input)

        self.zip_text = Label(text="Code postal: ")
        if self.zip_city[0] == ".":
            self.zip_city[0] = ""
        self.zip_input = TextInput(
            text=self.zip_city[0],
            multiline=False,
            halign="right",
            input_filter="int",
        )
        self.layout.add_widget(self.zip_text)
        self.layout.add_widget(self.zip_input)

        self.city_text = Label(text="Ville: ")
        if self.zip_city[1] == ". .":
            self.zip_city[1] = ""
        self.city_input = TextInput(
            text=self.zip_city[1], multiline=False, halign="right"
        )
        self.layout.add_widget(self.city_text)
        self.layout.add_widget(self.city_input)

        self.ok = Button(text="OK")
        self.ok.bind(on_press=self.press_ok)
        self.cancel = Button(text="Annuler")
        self.cancel.bind(on_press=self.press_canc)
        self.layout.add_widget(self.ok)
        self.layout.add_widget(self.cancel)

        self.add_widget(self.layout)

    def press_ok(self, instance):
        if (
            self.num_input.text
            and self.street_input.text
            and self.zip_input.text
            and self.city_input
        ):
            year_day = int(str(choosen_date[2]) + str(date_info[0][1][1]) + str(choosen_date[0]))
            hour_list = self.hour.text.split(":")
            hour = str(hour_list[0]) + str(hour_list[1])

            # line to modify adding get_forecast() but see before the fonction return
            # latitude, longitude = get_gps(app_get_loc.device_id, self.num_input.text,
            #     self.street_input.text, self.zip_input.text, self.city_input.text)

            if self.date_exists():
                #create adress if not exists and update Dates.adress_id with good adress
                id= self.address_exists()

                for date in (session.query(Dates).filter(Dates.year_to_day == year_day).
                    filter(Dates.hour == hour).all()):
                    date.address_id = id
                    date.label= self.label_input.text
                session.commit()
            else:
                #create adress if not exists and create Dates row
                id = self.address_exists()

                date = Dates(year_to_day= year_day, hour= hour, label= self.label_input.text,
                    address_id= id)
                session.add(date)
                session.commit()
            if self.subpopup_bool:
                hour_update()
                self.parent.parent.parent.dismiss()
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
            string += ' ou cliquez sur "Annuler".'
            popup_layout = BoxLayout(orientation="vertical")
            popup_text = Label(text=string)
            popup_button = Button(text="OK", size_hint=(1, 0.2))
            popup_button.bind(on_press=self.subpress_ok)
            popup_layout.add_widget(popup_text)
            popup_layout.add_widget(popup_button)
            self.subpopup = Popup(title="Attention:", content=popup_layout)
            self.subpopup.open()

    def press_canc(self, instance):
        self.parent.parent.parent.dismiss()

    def subpress_ok(self, instance):
        self.subpopup.dismiss()

    def date_exists(self):

        year_day = int(str(choosen_date[2]) + str(date_info[0][1][1]) + str(choosen_date[0]))
        hour_list = self.hour.text.split(":")
        hour = str(hour_list[0]) + str(hour_list[1])

        if (session.query(Dates.year_to_day, Dates.hour).
            filter(Dates.year_to_day == year_day).filter(Dates.hour == hour).all()
            ):
            return True
        else:
            return False
            
    def address_exists(self):

        if not (session.query(Addresses).filter(Addresses.num == int(self.num_input.text)).
            filter(Addresses.street == self.street_input.text).filter(Addresses.zipcode 
            == int(self.zip_input.text)).filter(Addresses.city == self.city_input.text).all()):

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
                address = (session.query(Addresses.id).filter(Addresses.num == int(self.num_input.text)).
                    filter(Addresses.street == self.street_input.text).filter(Addresses.zipcode 
                    == int(self.zip_input.text)).filter(Addresses.city == self.city_input.text).all())
                self.subpopup_bool = True
                return address[0][0]
        else:
            address = (session.query(Addresses.id).filter(Addresses.num == int(self.num_input.text)).
                filter(Addresses.street == self.street_input.text).filter(Addresses.zipcode 
                == int(self.zip_input.text)).filter(Addresses.city == self.city_input.text).all())
            self.subpopup_bool = True
            return address[0][0]
    
    def subpopup_ok(self, *args):
        self.subpopup_bool = False
        self.popup_address.dismiss()

def hour_update():
    year_day = int(str(choosen_date[2]) + str(date_info[0][1][1]) + str(choosen_date[0]))
    tasks = (session.query(Dates.hour, Dates.label, Addresses.num, Addresses.street,
        Addresses.zipcode, Addresses.city).join(Addresses).filter(Dates.year_to_day== year_day).all())

    for hour_place in range(48):
        label = ""
        address = ". . ."
        city = ". . ."
        if hour_place % 2 == 0:
            hour = int(hour_place / 2)
            if hour <= 9:
                hour = "0" + str(hour)
            hour = str(hour)
            main_app.hours_layout.hour_button[hour_place].text = (
                str(hour)
                + ":00\n"
                + label
                + "\n"
                + address
                + "\n"
                + city
            )
        else:
            hour = int((hour_place - 1) / 2)
            if hour <= 9:
                hour = "0" + str(hour)
            hour = str(hour)
            main_app.hours_layout.hour_button[hour_place].text = (
                str(hour)
                + ":30\n"
                + label
                + "\n"
                + address
                + "\n"
                + city
            )

        for task in tasks:
            if hour_place % 2 == 0:
                if hour + "00" == task[0]:
                    label = task[1]
                    address = str(task[2]) + " " + task[3]
                    city = str(task[4]) + " " + task[5] 
                    main_app.hours_layout.hour_button[hour_place].text = (
                        str(hour)
                        + ":00\n"
                        + label
                        + "\n"
                        + address
                        + "\n"
                        + city
                    )
                    break
            else:
                if hour + "30" == task[0]:
                    label = task[1]
                    address = str(task[2]) + " " + task[3]
                    city = str(task[4]) + " " + task[5]
                    main_app.hours_layout.hour_button[hour_place].text = (
                        str(hour)
                        + ":30\n"
                        + label
                        + "\n"
                        + address
                        + "\n"
                        + city
                    )
                    break

# class Application(App):

#     def __init__(self, **kwargs):
#         """Initialize Dairy class."""
#         super().__init__(**kwargs)
#         self.sm = ScreenManager()
#         self.dairy = Dairy(name="Agenda")

#     def build(self):
#         self.sm.add_widget(self.dairy)
#         return self.sm

# my_app = Application()
# main_app = my_app.dairy

# if __name__ == "__main__":
#     app = my_app  # Dairy()
#     app.run()
