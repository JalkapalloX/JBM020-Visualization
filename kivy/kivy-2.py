from kivy.app import App
from kivy.uix.label import Label # Button is Element of Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
#kivy.require("1.8.0")

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        # Don't have to reference base class; enables multi-inheritance
        # --> Access to parent class and its inherited methods
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text = "Username:"))
        self.username = TextInput(multiline = False)
        self.add_widget(self.username)

        self.add_widget(Label(text = "Password:"))
        self.password = TextInput(multiline = False,
                                  password = True)
        self.add_widget(self.password)

# Inheritance from classs App
class SimpleKivy(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    SimpleKivy().run() # Only run if called; Done for imports
                       # into other files
