from kivy.app import App
from kivy.lang import Builder
import DragableButton  # import to get auto register

kv = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'cannot drag here'
    BoxLayout:
        id: from_box
        DragableButton:
            text: 'Drag me!!! 1'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            drop_func: app.greet

        DragableButton:
            text: 'Drag me!!! 2'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            remove_on_drag: False
            drop_func: app.greet

            size: 120,25

        DragableButton:
            text: 'Drag me!!! 3'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            drag_opacity: .5
            drop_func: app.greet
    Label:
        id: to_box
        text: 'grad here for some effect'
'''


class MyPaintApp(App):
    def build(self):
        return Builder.load_string(kv)

    def greet(self):
        print("Dragging done!!!")

if __name__ == '__main__':
    MyPaintApp().run()
