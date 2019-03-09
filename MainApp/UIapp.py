from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from scheme import Drawer
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
        try:
            draw = Drawer(text)
            draw.start()
        except Exception:
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='Incorrect input\nTry again!'))
            butt = Button(text='Close', size_hint_y=0.4)
            content.add_widget(butt)

            popup = Popup(title='WARNING', content=content,
                          auto_dismiss=False, size_hint=[.25, .35])
            butt.bind(on_press=popup.dismiss)
            popup.open()
        else:
            self.image = Image(source=text+'.jpg')
            self.show()
            sm.transition.direction = 'left'
            sm.current = 'settings'

    def show(self):
        self.rel.clear_widgets()
        b = BoxLayout(orientation='vertical', padding=20)
        b.add_widget(Label(text='Function: '+self.text,
                           size_hint=[1, .1],
                           color=[0, .68, .71, 1],
                           font_size=25))
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

    def isEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def pars(self, instance, value):
        oper = ('+', '&')
        if len(value) == 1:
            if ((value[-1].isalpha() and self.isEnglish(value[-1])) or
                    value[-1] is '!' or value[-1] is '('):
                pass
            else:
                print('wrong')
                instance.text = ''
        elif len(value) > 1:
            v1 = value[-1]
            v2 = value[-2]

            if ((v1.isalpha() and (v2 in oper or v2 is '!' or v2 is '(') and self.isEnglish(v1)) or
                    (v1.isdigit() and v2.isalpha()) or
                    (v1 in oper and v2 not in oper and v2 is not '(') or
                    (v1 is '(' and (v2 in oper or v2 is '(' or v2 is '!')) or
                    (v1 is ')' and (v2.isalnum() or v2 is ')')) or
                    (v1 is '!' and (v2 in oper or v2 is '('))):
                pass
            else:
                print('wrong')
                instance.text = value[:-1]


class SettingsScreen(Screen):
    pass


s = SettingsScreen(name='settings')
m = MainUI(s, name='menu')

sm = ScreenManager(transition=SwapTransition())
sm.add_widget(m)
sm.add_widget(s)


class MainApp(App):
    def build(self):
        self.title = 'Logical Expression Drawer'
        self.icon = 'network.png'
        return sm


a = MainApp()
a.run()
