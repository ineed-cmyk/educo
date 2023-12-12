

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from datetime import datetime
from plyer import notification
import threading
Window.size = (1200, 800)
try:
    # this is to check if theres a file called notes_record
    from schedule_record import *

    # this takes or copies an existing data from notes_record
    #schedule = recorded_schedule
except ModuleNotFoundError:
    # this is to make sure that user has the file by making a new one, w or a doesnt matter for now
    dummy_var = open("schedule_record.py", "w")
    # this basically types the code into notes_record.py, you can use lists or just texts
    dummy_var.write("recorded_schedule = dict()\n")
    dummy_var.close()
    # since there isnt a file called notes_record, theres no data, so you make a fresh data
    schedule = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": []
    }
schedule = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": []
    }

# in this program you will see a lot of 2d lists being targeted
# just remember this:
# for each list in schedule[today]:
#  [0] - when its supposed to alert (in minutes)
#  [1][0] - notification heading
#  [1][1] - notification description


# function to notify or alert
def notify(notify_name, notification_description):
    notification.notify(
        title=notify_name,
        message=notification_description,
        timeout=30
    )


# checks if the input is a day, not some gibberish or number
def check_day_names(user_input):
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if user_input.lower() in week_days:
        return user_input
    else:
        pass


def convert_to_seconds(minutes):
    seconds = minutes * 60
    return seconds


def convert_to_minutes(hours, minutes):
    minutes = (int(hours) * 60) + int(minutes)
    return minutes


def convert_to_hours(minutes):
    hours = minutes / 60
    minutes = minutes % 60
    total_time = [hours, minutes]
    return total_time


# adds a list to schedule
def add_schedule(check_day_name, notify_time, notification_title, notification_description):
    day_name = check_day_names(check_day_name)

    list_of_times = [notify_time, [notification_title, notification_description]]

    schedule[day_name.lower()].append(list_of_times)


# removes a list from schedule
def remove_schedule(day_name, notification_title):
    # selects the key and pair with the day given
    target = schedule[day_name.lower()]

    pop_target = ""

    # goes through each list and checks for the given title
    for sets in target:
        # if title is found it will be recorded in pop_target
        if sets[1][0].lower() == notification_title.lower():
            pop_target = sets
        else:
            pass

    # this code checks if no such title is found
    if pop_target != "":
        target.remove(pop_target)


def get_with_time(day_name, given_time):
    target = schedule[day_name.lower()]

    for sets in target:
        if sets[0] == given_time:
            return sets[1]
        else:
            pass


def check_time(title: None, description: None, target_time: 0):
    """
    We need to make a function that takes a time value and sees if it's the same as current time.
    Put it in a while loop with a sleep function so it checks every minute.
    When the time assigned matches up with the current time, print hello (for now)

    :param target_time: time to wake up at
    :param title: title of notification
    :param description: description of notification
    """
    now = datetime.now()
    hours = now.strftime("%H")
    minutes = now.strftime("%M")
    now = convert_to_minutes(int(hours), int(minutes))
    difference = int(target_time) - int(now)
    target_time = convert_to_seconds(difference)

    # this is a loop through as code below cant take parameters
    def thread_return_function():
        return notify(title, description)

    threading.Timer(target_time, thread_return_function).start()


def alert_in_time():
    now = datetime.now()
    today = now.strftime("%A").lower()
    hours = now.strftime("%H")
    minutes = now.strftime("%M")

    schedule_today = schedule[today]
    # goes through each list
    for sets in schedule_today:
        # checks if time has passed
        print(convert_to_minutes(int(hours), int(minutes)))
        if int(sets[0]) < int(convert_to_minutes(hours, minutes)):
            print("ignored")
            print(sets)
        else:
            check_time(title=sets[1][0], description=sets[1][1], target_time=sets[0])


alert_in_time()

KV = '''

ScreenManager:
    MainScreen:
    Nav_page:
    Credits_page:
    SchedulerPage:

<MainScreen>:
    name:'mainpage'
    Screen:
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'educo_logo.png'

        MDRectangleFlatIconButton:
            icon: "code-braces"
            text: "Credits"
            theme_text_color: "Custom"
            text_color: 120/255, 81/255, 169/255, 1
            line_color: 120/255, 81/255, 169/255, 1
            icon_color: 120/255, 81/255, 169/255, 1
            pos_hint:{"center_x": .5, "center_y": .1} 
            on_press:  root.manager.current = 'credits'
        MDRectangleFlatButton:
            text: "Start!"
            id_bg_color: 0,0,0,0
            text_color: 0, 0, 0, 0
            pos_hint:{"center_x": .5, "center_y": .2} 
            on_press: root.manager.current = 'nav_page'
            size_hint:(0.4,0.1)
            Image:
                source:'Start_button_sq.png'
        
            


<Nav_page>:
    name:'nav_page'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: 'vertical'
                        MDTopAppBar:
                            title: "Navigate"
                            elevation: 10
                            left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                            elevation: 8
                        MDCard:
                            orientation: "vertical"
                            padding: "8dp"
                            size_hint: None, None
                            size: "300dp", "240dp"
                            pos_hint: {"center_x": .5, "center_y": .3}
                            spacing: "10dp"
                                
                            MDLabel:
                                text: "Scheduler"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                            MDSeparator:
                                height: "1dp"
                                
                            MDLabel:
                                text: "This is scheduler.Enter your time and other details to get notified of classes and other things!"
                                elevation: 8
                            MDFlatButton:
                                text: "Go"
                                md_bg_color: 120/255, 81/255, 169/255, 1
                                on_press:  root.manager.current = 'scheduler_page' 
                            
                            
                            
                                
                            

                        Widget:

            MDNavigationDrawer:
                id:nav_drawer
                toggle: True
                BoxLayout:
                    orientation: 'vertical'
                    spacing:'8dp'

                    Image:
                        source:'logo.png'
                    MDLabel:
                        text:"                Your very own toolbox "
                        font_style:'Subtitle1'
                        size_hint_y: None 
                        height: self.texture_size[1]
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Credits'
                                on_press:  root.manager.current = 'credits'
                                IconLeftWidget:
                                    icon: 'code-braces'
                            OneLineIconListItem:
                                text: 'Mainpage'
                                on_press:  root.manager.current = 'mainpage'
                                IconLeftWidget:
                                    icon: 'exit-to-app'
                            OneLineIconListItem:
                                text: 'Scheduler'
                                on_press:  root.manager.current = 'scheduler_page'
                                IconLeftWidget:
                                    icon: 'exit-to-app'

<Credits_page>:

    name: 'credits'
    MDScreen:

    MDCard:
        orientation: "vertical"
        padding: "8dp"
        size_hint: None, None
        size: "300dp", "240dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        spacing: "10dp"

        MDLabel:
            text: "Credits"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]

        MDSeparator:
            height: "1dp"

        MDLabel:
            text: "Murshid- FullStack Developer"

        MDLabel:
            text: "Adeeb- Backend developer,moral support,Video Editor"

        MDLabel:
            text: "Mira- Backend Developer"

        MDLabel:
            text: "Neil- FrontEnd Developer,UI design"

        MDFlatButton:
            text: "Back"

            md_bg_color: 120/255, 81/255, 169/255, 1
            on_press:  root.manager.current = 'mainpage'

<SchedulerPage>:

    name: 'scheduler_page'

    check:check
    title:title
    description:description
    input_hour:input_hour
    input_minute:input_minute

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size


    Screen:

        MDTextField:
            id: check
            hint_text: "Add new or Remove old schedule"
            helper_text: "type add to add new schedule or remove an old schedule"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.8}

        MDTextField:
            id: title
            hint_text: "Enter Notification Title "
            helper_text: "An ID for your notification, will be use full when you want to remove"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.7}

        MDTextField:
            id: description
            hint_text: "Enter Notification "
            helper_text: "Basically what you want to get notified of, you can also put links"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            multiline: True

        MDTextField:
            id: day_name
            hint_text: "Enter Day "
            helper_text: "Please Enter the day you want to get notified"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDTextField:
            id: input_hour
            hint_text: "Enter Notification Time (hours)"
            helper_text: "Please Enter the time you want to get notified"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.4}

        MDTextField:
            id: input_minute
            hint_text: "Enter Notification Time (minutes)"
            helper_text: "Please Enter the time you want to get notified"
            helper_text_mode: "on_focus"
            icon_right: "arrow"
            icon_right_color: app.theme_cls.primary_color
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5, "center_y": 0.3}


        MDRectangleFlatButton:
            text: "Submit"
            pos_hint: {"center_x": 0.5, "center_y": 0.2}
            on_press: root.press()
            
        MDRectangleFlatButton:
            text: "back"
            pos_hint: {"center_x": 0.6, "center_y": 0.2}
            on_press:  root.manager.current = 'nav_page' 



    '''


class MainScreen(Screen):
    pass


class Nav_page(Screen):
    pass


class Credits_page(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class SchedulerPage(BoxLayout, Screen):
    check = ObjectProperty(None)
    title = ObjectProperty(None)
    description = ObjectProperty(None)
    day_name = ObjectProperty(None)
    input_hour = ObjectProperty(None)
    input_minute = ObjectProperty(None)

    def press(self):

        check = self.ids.check.text
        title = self.ids.title.text
        description = self.ids.description.text
        day_name = self.ids.day_name.text
        input_hour = self.ids.input_hour.text
        input_minute = self.ids.input_minute.text

        if check.lower() == "add":
            add_schedule(day_name.lower(), convert_to_minutes(int(input_hour), int(input_minute)), title, description)

            send_data = open("schedule_record.py", "w")
            send_data.write(f"recorded_schedule = {schedule}\n")
            send_data.close()

            alert_in_time()
        elif check.lower() == "remove":
            remove_schedule(day_name, title)

            send_data = open("schedule_record.py", "w")
            send_data.write(f"recorded_schedule = {schedule}\n")
            send_data.close()

            alert_in_time()
        else:
            pass

        self.ids.check.text = ""
        self.ids.title.text = ""
        self.ids.description.text = ""
        self.ids.day_name.text = ""
        self.ids.input_hour.text = ""
        self.ids.input_minute.text = ""


sm = ScreenManager()
sm.add_widget(MainScreen(name='mainpage'))
sm.add_widget(Nav_page(name='nav_page'))
sm.add_widget(Credits_page(name='credits'))
sm.add_widget(SchedulerPage(name='scheduler_page'))


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "700"
        kv = Builder.load_string(KV)
        return kv


if __name__ == '__main__':
    MainApp().run()

