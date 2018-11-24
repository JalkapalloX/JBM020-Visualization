from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

# Inheritance from classs App
class SimpleKivy4(App):
    def build(self):
        return FloatLayout()

if __name__ == "__main__":
    SimpleKivy4().run() # Only run if called; Done for imports
                       # into other files
