from kivy.app import App
from kivy.uix.label import Label # Button is Element of Label
#kivy.require("1.8.0")

# Inheritance from classs App
class SimpleKivy(App):
    def build(self):
        return Label(text = "Hello HEEEYAAAHHH!")

if __name__ == "__main__":
    SimpleKivy().run() # Only run if called; Done for imports
                       # into other files
