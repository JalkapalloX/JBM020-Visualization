from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# WIDGETS
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown

# LAYOUTS
from kivy.uix.floatlayout import FloatLayout

# DATA ANALYTICS LIBRARY
import pandas as pd

# SPECIFY GLOBAL VARIABLES
file_dropped = False

# INTEGRATE .KV FILE
file_kv = Builder.load_file("DNMCS_GUI.kv")

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

    # INTEGRATE FILE DROPPING
    def _on_file_drop(self, window, file_path):
        # Refer to global file_dropped
        global file_dropped

        if not file_dropped:
            data_path = file_path
            data = pd.read_csv(file_path.decode("utf-8"))
            print(data.head())
            file_dropped = True
            return
        else:
            print("Nope!")
            return

if __name__ == "__main__":
    GUI().run()
