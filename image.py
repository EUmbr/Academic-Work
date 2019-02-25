from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from object_draw_v0 import Drawer


class CalcApp(App):
    def update(self, instance):
        text = self.Textinput.text
        draw = Drawer(text)
        draw.start()
        wimg = Image(source='123.jpg')
        self.bl.add_widget(wimg)

    def build(self):
        self.bl = BoxLayout()
        eq = BoxLayout(orientation='vertical')
        self.bl.add_widget(eq)
        self.Textinput = TextInput(text='a+b', multiline=False)
        btn = Button(text='Push me!', on_press=self.update)
        eq.add_widget(self.Textinput)
        eq.add_widget(btn)

        return self.bl


if __name__ == '__main__':
    CalcApp().run()
