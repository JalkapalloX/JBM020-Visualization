from __future__ import print_function

# OTHER
import os
import time
import copy
import utilities
import plots
import gc

# KIVY BASE CAPABILITIES
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config

# WIDGETS
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ReferenceListProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.codeinput import CodeInput
from kivy.uix.slider import Slider
from kivydnd.dragndropwidget import DragNDropWidget # https://github.com/GreyGnome/KivyDnD
from kivydnd.dropdestination import DropDestination
import slider

# LAYOUTS
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# DATA ANALYTICS LIBRARY
import pandas as pd
import numpy as np
import dfgui

# PLOTTINGcanvas:
import matplotlib.pyplot as plt

# GLOBAL VARIABLES
G_DATA = []

class DraggableButton(Button, DragNDropWidget):
    def __init__(self, column, origin, **kw):
        self.column = column
        self.origin = origin
        super(DraggableButton, self).__init__(**kw)

class DropDestinationButton(Button, DropDestination):
    def __init__(self, **kw):
        super(DropDestinationButton, self).__init__(**kw)

class ImageButton(ButtonBehavior, Image):
    pass

class CodeScreen(Screen):
    def execute_code(self, text):
        exec(text)

    def show_data(self):
        dfgui.show(G_DATA)

class MainScreen(Screen):
    # DYNAMIC VARIABLES
    # GENERAL
    plot_img = StringProperty('templates/lilac_brested_roller.png') # Image to be shown

    # DATA
    data_name = StringProperty("[b]None[/b]")             # Name of the data set
    data_path = StringProperty("[b]None[/b]")             # Full path to data set

    # PLOT GENERAL
    plot_type = StringProperty("Node-Link Diagram")                 # Type of plot
    color_scheme = StringProperty("viridis")   # Color scheme of plot

    color_column = StringProperty("")
    filter_column = StringProperty("")

    # HEATMAP PROPERTIES
    heatmap_function = StringProperty("Sum")
    heatmap_ordering = StringProperty("Default")

    x_column = StringProperty("")
    y_column = StringProperty("")

    # NODE LINK properties
    node_link_layout = StringProperty("Fruchterman-Reingold")
    node_link_highlight = StringProperty("None")
    node_link_color_nodes = BooleanProperty(True)
    node_link_color_edges = BooleanProperty(True)
    start_node_column = StringProperty("")
    end_node_column = StringProperty("")
    edge_column = StringProperty("")
    size_column = StringProperty("")

    # SLIDER PROPERTIES
    color_slider_max = NumericProperty(0)
    color_slider_min = NumericProperty(0)
    filter_slider_max = NumericProperty(0)
    filter_slider_min = NumericProperty(0)
    x_range_slider_max = NumericProperty(0)
    x_range_slider_min = NumericProperty(0)
    y_range_slider_max = NumericProperty(0)
    y_range_slider_min = NumericProperty(0)
    node_slider_max = NumericProperty(0)
    node_slider_min = NumericProperty(0)
    edge_slider_max = NumericProperty(0)
    edge_slider_min = NumericProperty(0)

    # WHEN 'PLOT' IS PRESSED
    def _draw_plot(self):
        #try:
        utilities.wipe("graphs/")                     # Cleans directory
        if self.plot_type == "Heatmap":
            # subset = utilities.data_filter(G_DATA, self.plot_type,
            #                                (self.color_column, self.x_column, self.y_column, self.filter_column),
            #                                (self.color_slider_min, self.color_slider_max,
            #                                 self.x_range_slider_min, self.x_range_slider_max,
            #                                 self.y_range_slider_min, self.y_range_slider_max,
            #                                 self.filter_slider_min, self.filter_slider_max))

            plots.create_static_plot(self.plot_type,
                                     df = G_DATA,
                                     X = self.x_column,
                                     Y = self.y_column,
                                     values = self.color_column,
                                     aggfunc = self.heatmap_function,
                                     ordering=self.heatmap_ordering,
                                     cmap=self.color_scheme)
        elif self.plot_type == "Node-Link Diagram":
            if self.node_link_highlight == "Dijkstra":
                dist, highlight = utilities.dijkstra(G_DATA, self.start_node_column, self.end_node_column, self.edge_column, int(self.ids.from_node.text), int(self.ids.to_node.text))
            else:
                highlight=[]

            plots.create_static_plot(self.plot_type,
                                     df = G_DATA,
                                     start_node = self.start_node_column,
                                     end_node = self.end_node_column,
                                     layout=self.node_link_layout,
                                     directed=False,
                                     edge_weight=self.edge_column,
                                     node_size=self.size_column,
                                     color=self.color_column,
                                     color_nodes=self.node_link_color_nodes,
                                     color_edges=self.node_link_color_edges,
                                     cmap=self.color_scheme,
                                     highlight=highlight)
        self.plot_img = "graphs/" + os.listdir("graphs/")[0]
        # except:
        #     print("Error")

    # def oops(self, hey):
    #     print("App says: Ooops! Can't drop there!" + hey)

    def _load_data(self):
        global G_DATA

        file_path = utilities.get_file()
        #try:
        G_DATA = utilities.read_data(file_path)
        self.data_name = "[b]" + file_path.split("/")[-1].split(".")[-2] + "[/b]"
        self.data_path = utilities.newline_insert("/".join(file_path.split("/")[:-1]), "/", 28)

        for i in range(len(G_DATA.columns)):
            if(i%2==0):
                background = (0.99,0.99,0.99,1)
            else:
                background = (0.95,0.95,0.98,1)

            drag_button = DraggableButton(text="   [b]o[/b]   " + G_DATA.columns[i] + " <" + str(G_DATA.dtypes[i]) + ">",
                                          markup=True,
                                          pos=(325,Window.height-(280+20*i)),
                                          background_color=background,
                                          drop_func=self.refurbish,
                                          droppable_zone_objects=[self.ids.which_color, self.ids.which_filter,
                                                                  self.ids.which_X, self.ids.which_Y,
                                                                  self.ids.which_start_node, self.ids.which_end_node,
                                                                  self.ids.which_edges, self.ids.which_size,
                                                                  self.ids.whole_screen],
                                          column=G_DATA.columns[i],
                                          origin=(325,Window.height-(280+20*i)))
            self.add_widget(drag_button)
        #except:
        #    print("Data couldn't be transferred!")

    def refurbish(self, DroppedObject):
        drag_button = DraggableButton(text=DroppedObject.text,
                                      markup=True,
                                      pos=DroppedObject.origin,
                                      background_color=DroppedObject.background_color,
                                      drop_func=DroppedObject.drop_func,
                                      droppable_zone_objects=[self.ids.which_color, self.ids.which_filter,
                                                              self.ids.which_X, self.ids.which_Y,
                                                              self.ids.which_start_node, self.ids.which_end_node,
                                                              self.ids.which_edges, self.ids.which_size,
                                                              self.ids.whole_screen],
                                      column=DroppedObject.column,
                                      origin=DroppedObject.origin)
        self.add_widget(drag_button)

    def which_color_update(self, DroppedObject):
        self.color_column=DroppedObject.column
        self.color_slider_max=max(G_DATA[DroppedObject.column])
        self.color_slider_min=min(G_DATA[DroppedObject.column])

    def which_filter_update(self, DroppedObject):
        self.filter_column=DroppedObject.column
        self.filter_slider_max=max(G_DATA[DroppedObject.column])
        self.filter_slider_min=min(G_DATA[DroppedObject.column])

    def which_x_update(self, DroppedObject):
        self.x_column=DroppedObject.column
        self.x_range_slider_max=max(G_DATA[DroppedObject.column])
        self.x_range_slider_min=min(G_DATA[DroppedObject.column])

    def which_y_update(self, DroppedObject):
        self.y_column=DroppedObject.column
        self.y_range_slider_max=max(G_DATA[DroppedObject.column])
        self.y_range_slider_min=min(G_DATA[DroppedObject.column])

    def which_start_node_update(self, DroppedObject):
        self.start_node_column=DroppedObject.column

    def which_end_node_update(self, DroppedObject):
        self.end_node_column=DroppedObject.column

    def which_edge_update(self, DroppedObject):
        self.edge_column=DroppedObject.column
        self.edge_slider_max=max(G_DATA[DroppedObject.column])
        self.edge_slider_min=min(G_DATA[DroppedObject.column])

    def which_size_update(self, DroppedObject):
        self.size_column=DroppedObject.column
        self.node_slider_max=max(G_DATA[DroppedObject.column])
        self.node_slider_min=min(G_DATA[DroppedObject.column])

    def show_data(self):
        dfgui.show(G_DATA)

class ScreenManagement(ScreenManager):
    pass

# INTEGRATE .KV FILE
file_kv = Builder.load_file("GUI.kv")

class GUI(App):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.icon = 'templates/lilac_brested_roller.png'

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
    gc.collect()
