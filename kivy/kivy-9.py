from kivy.app import App
from kivy.lang import Builder

presentation = Builder.load_file("main.kv")

# Inheritance from classs App
class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    MainApp().run() # Only run if called; Done for imports
                    # into other files
