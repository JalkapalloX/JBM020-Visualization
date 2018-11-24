from kivy.app import App
from kivy.uix.label import Label # Button is Element of Label
from kivy.uix.widget import Widget

class Widgets(Widget):
    pass

# Inheritance from classs App
class SimpleKivy2(App):
    def build(self):
        return Widgets()

if __name__ == "__main__":
    SimpleKivy2().run() # Only run if called; Done for imports
                       # into other files
