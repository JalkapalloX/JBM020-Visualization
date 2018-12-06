# OTHER
import os
import utilities
import plots

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
from kivy.properties import StringProperty

# LAYOUTS
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# DATA ANALYTICS LIBRARY
import pandas as pd

# PLOTTING
import matplotlib.pyplot as plt

class ImageButton(ButtonBehavior, Image):
    pass

class MainScreen(Screen):
    plot_img = StringProperty('graphs/Yq6OfCt.png')

    def _draw_plot(self):
        #utilities.wipe("graphs/")
        #utilities.create_plot()
        self.plot_img = "graphs/" + os.listdir("graphs/")[0]

    def _draw_all_plots(self):
        #utilities.wipe("graphs/")
        #utilities.create_all_plots()
        self.plot_img = "graphs/" + os.listdir("graphs/")[0]

class DetailViewScreen(Screen):
    plot_img = StringProperty("")

class ScreenManagement(ScreenManager):
    pass

# INTEGRATE .KV FILE
file_kv = Builder.load_file("DNMCS_GUI.kv")

class GUI(App):
    # BUILDING THE GUI (ADDING FUNCTIONALITIES HERE)
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        return file_kv

    # INTEGRATE FILE DROPPING
    def _on_file_drop(self, window, file_path):
        self.data = utilities.read_data(file_path.decode("utf-8"))
        return

if __name__ == "__main__":
    GUI().run()
