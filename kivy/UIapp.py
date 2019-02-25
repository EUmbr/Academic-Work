from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from object_draw_v0 import Drawer
import os


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1213')
Config.set('graphics', 'height', '715')

Builder.load_file('Main.kv')


class MainUI(Screen):
    def __init__(self, rel, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.rel = rel
        self.text = ''

    def draw(self, instance, text):
        self.text = text
        draw = Drawer(text)
        draw.start()
        self.image = Image(source=text+'.jpg')
        self.show()

    def show(self):
        self.rel.clear_widgets()
        b = BoxLayout(orientation='vertical', padding=20)
        b.add_widget(Label(text='Function: '+self.text,
                           size_hint=[1, .1],
                           color=[0, .68, .71, 1]))
        b.add_widget(self.image)
        a = AnchorLayout(anchor_y='bottom', size_hint=[1, .1])
        a.add_widget(Button(text='Back', size_hint=[.1, .8],
                            on_press=self.change, background_normal='',
                            background_color=[.24, .29, .32, 1]))
        b.add_widget(a)
        self.rel.add_widget(b)

    def change(self, instance):
        sm.transition.direction = 'right'
        sm.current = 'menu'
        os.remove(self.text+'.jpg')


class SettingsScreen(Screen):
    pass


s = SettingsScreen(name='settings')
m = MainUI(s, name='menu')

sm = ScreenManager(transition=SwapTransition())
sm.add_widget(m)
sm.add_widget(s)


class MainApp(App):
    def build(self):
        return sm


a = MainApp()
a.run()
