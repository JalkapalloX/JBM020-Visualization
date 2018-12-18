# OTHER
import os
import time
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
from kivy.clock import Clock

# LAYOUTS
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# DATA ANALYTICS LIBRARY
import pandas as pd

# PLOTTING
import matplotlib.pyplot as plt

# GLOBAL VARIABLES
G_DATA = []

class ImageButton(ButtonBehavior, Image):
    pass

class HomeScreen(Screen):
    pass

class MainScreen(Screen):
    # VARIABLES CHANGEABLE BY USER
    title = StringProperty("Title")
    plot_img = StringProperty('lilac_brested_roller.png') # Image to be shown
    data_name = StringProperty("[b]None[/b]")
    data_path = StringProperty("[b]None[/b]")
    plot_type = StringProperty("heatmap")

    def _draw_plot(self):
        utilities.wipe("graphs/")
        plots.create_static_plot(self.plot_type, G_DATA)
        self.plot_img = "graphs/" + os.listdir("graphs/")[0]

    def _draw_all_plots(self):
        #utilities.wipe("graphs/")
        #utilities.create_all_plots()
        self.plot_img = "graphs/" + os.listdir("graphs/")[0]

    def _play(self):
        def set_img(n):
            self.plot_img = "graphs/" + os.listdir("graphs/")[n]
        pass # CODE HERE

    def _load_data(self):
        global G_DATA
        file_path = utilities.get_file()
        try:
            G_DATA = utilities.read_data(file_path)
            self.data_name = "[b]" + file_path + "[/b]"
            self.data_path = "[b]" + file_path + "[/b]"
        except:
            print("Data couldn't be transferred!")


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
        global G_DATA

        file_path = file_path.decode("utf-8")
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".png":
            self.background_img = file_path
        else:
            G_DATA = utilities.read_data(file_path)
            print(G_DATA)

if __name__ == "__main__":
    GUI().run()
