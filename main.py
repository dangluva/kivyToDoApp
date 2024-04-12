from kivy.app import App  # Importing the App class from the Kivy framework
from kivy.clock import Clock  # Importing the Clock class from Kivy for scheduling events
from kivy.metrics import dp  # Importing dp (density-independent pixels) from Kivy for consistent sizing
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore  # Importing JsonStore from Kivy for storing data in JSON format
from kivy.uix.popup import Popup  # Importing Popup class from Kivy for creating pop-up windows
from kivy.uix.screenmanager import ScreenManager  # Importing ScreenManager and Screen classes for managing screens
from kivy.uix.boxlayout import BoxLayout  # Importing BoxLayout class from Kivy for arranging widgets in a box layout
from kivy.uix.button import Button  # Importing Button class from Kivy for creating buttons
from kivy.uix.textinput import TextInput  # Importing TextInput class from Kivy for accepting text input

# Constants
BUTTON_HEIGHT = dp(80)  # Defining a constant for button height using density-independent pixels
POPUP_HEIGHT = dp(180)  # Defining a constant for popup height using density-independent pixels

store = JsonStore("data.json")  # Creating a JsonStore object with a filename "data.json" for storing data


class Custombtn(Button):
    key_name = StringProperty()


class Interface(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initializing the ScreenManager
        Clock.schedule_once(self.fetching_data)  # Scheduling the fetching_data method to be called once

    def truncate_string(self, string_input, max_length):
        str_end = '...'
        length = len(string_input)
        if length > max_length:
            return string_input[:max_length - len(str_end)] + str_end
        else:
            return string_input

    def deleting(self, obj_btn):
        id = obj_btn.key_name
        self.ids.gridLayout.remove_widget(self.ids[id])
        store.delete(id)

    def fetching_data(self, dt):
        try:
            keys = store.keys()  # Getting the keys from the JsonStore
            for key in keys:
                layout = BoxLayout(spacing=dp(10), size_hint_y=None,
                                   height=BUTTON_HEIGHT)  # Creating a box layout for each item
                self.ids[key] = layout
                title = Custombtn(background_normal="orange.png", key_name=key, font_name="robotolight.ttf",
                                  text=self.truncate_string(key, 10))  # Creating a button with the key as text
                delete = Custombtn(key_name=key, on_press=self.deleting, background_normal="delete_icon.png",
                                   size_hint=(None, None),
                                   size=(BUTTON_HEIGHT, BUTTON_HEIGHT))  # Creating a delete button
                title.bind(
                    on_press=self.detail_screen)  # Binding the detail_screen method to the title button's press event
                layout.add_widget(title)  # Adding the title button to the layout
                layout.add_widget(delete)  # Adding the delete button to the layout
                self.ids.gridLayout.add_widget(layout)  # Adding the layout to the grid layout
        except Exception as e:  # Handling Error if the JsonStore is empty
            print(e)

    def back_btn(self):
        self.current = "Main Screen"  # Changing the current screen to "Main Screen"
        store.put(self.ids.taskTitle.text, data=self.ids.inputData.text)  # Storing data in the JsonStore

    def detail_screen(self, btn_obj):
        self.ids.taskTitle.text = btn_obj.key_name  # Setting the task title text to the button text
        self.ids.inputData.text = store.get(btn_obj.key_name)[
            "data"]  # Getting data from the JsonStore and setting it as input data
        self.current = "Details Screen"  # Changing the current screen to "Details Screen"

    def add_item(self, obj):
        self.popup.dismiss()  # Dismissing the popup window
        layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=BUTTON_HEIGHT)  # Creating a box layout for the new item
        title = Custombtn(font_name="robotolight.ttf", key_name=self.text_input.text,
                          text=self.truncate_string(self.text_input.text,
                                                    10))  # Creating a button with the text input as text
        delete = Custombtn(on_press=self.deleting, key_name=self.text_input.text, text="Delete", size_hint=(None, None),
                           size=(BUTTON_HEIGHT, BUTTON_HEIGHT), font_size="20sp")  # Creating a delete button
        self.ids[self.text_input.text] = layout
        title.bind(on_press=self.detail_screen)  # Binding the detail_screen method to the title button's press event
        layout.add_widget(title)  # Adding the title button to the layout
        layout.add_widget(delete)  # Adding the delete button to the layout
        store.put(self.text_input.text, data="")  # Storing data in the JsonStore
        self.ids.gridLayout.add_widget(layout)  # Adding the layout to the grid layout

    def show_popup(self):
        layout = BoxLayout(orientation="vertical", padding=dp(16),
                           spacing=dp(10))  # Creating a box layout for the popup content
        btn = Button(background_normal="red.png", text="Submit",
                     font_name="robotolight.ttf")  # Creating a submit button
        btn.bind(on_press=self.add_item)  # Binding the add_item method to the submit button's press event
        self.text_input = TextInput(multiline=False)  # Creating a text input field
        layout.add_widget(self.text_input)  # Adding the text input field to the layout
        layout.add_widget(btn)  # Adding the submit button to the layout
        self.popup = Popup(title_font="robotoblack.ttf", padding=dp(10), title="Task Name", size_hint=(0.8, None),
                           height=POPUP_HEIGHT,
                           content=layout)  # Creating a popup window
        self.popup.open()  # Opening the popup window


class TodoApp(App):
    pass  # Placeholder for the main application class


TodoApp().run()  # Running the Kivy application
