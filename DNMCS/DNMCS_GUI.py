from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# WIDGETS
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown

# LAYOUTS
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout

# INTEGRATE .KV FILE
file_kv = Builder.load_file("DNMCS_GUI.kv")

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        # Inherit Grid Layout Code
        super(MainScreen, self).__init__(**kwargs)

        # Light grey background
        Window.clearcolor = (0.95, 0.95, 0.95, 1)

class GUI(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    GUI().run()
