from kivy.app import App
from kivy.uix.label import Label # Button is Element of Label



# Inheritance from classs App
class SimpleKivy(App):
    def build(self):
        return Label()

if __name__ == "__main__":
    SimpleKivy().run() # Only run if called; Done for imports
                       # into other files
