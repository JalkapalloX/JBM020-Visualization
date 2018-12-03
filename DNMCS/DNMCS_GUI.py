# KIVY BASE CAPABILITIES
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# WIDGETS
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget

# LAYOUTS
from kivy.uix.floatlayout import FloatLayout

# DATA ANALYTICS LIBRARY
import pandas as pd

# PLOTTING
import matplotlib.pyplot as plt

# SPECIFY GLOBAL VARIABLES
file_dropped = False
n_tabs = 1

# INTEGRATE .KV FILE
file_kv = Builder.load_file("DNMCS_GUI.kv")

class ImageButton(ButtonBehavior, Image):
    pass

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        # Inherit Grid Layout Code
        super(MainScreen, self).__init__(**kwargs)

        # Light grey background
        Window.clearcolor = (1, 1, 1, 1)

class GUI(App):
    # BUILDING THE GUI (ADDING FUNCTIONALITIES HERE)
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        return MainScreen()

    def reset_drop(self):
        global file_dropped
        file_dropped = False

    # INTEGRATE FILE DROPPING
    def _on_file_drop(self, window, file_path):
        # Refer to global file_dropped
        global file_dropped

        if not file_dropped:
            data_path = file_path
            data = pd.read_csv(file_path.decode("utf-8"))

            file_dropped = True
            drop_information.dismiss()
            return
        else:
            return

if __name__ == "__main__":
    GUI().run()
