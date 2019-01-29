from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
from kivy.graphics import Color, Rectangle
import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '809')
Config.set('graphics', 'height', '500')


class MyApp(App):
    def exit(self, obj):
        App.get_running_app().stop()

    def build(self):
        root = BoxLayout(orientation='vertical', padding=20)

        with root.canvas:
            Color(rgba=(.13,.16,.19,1))
            Rectangle(size=[809, 500], pos=root.pos)


        al1 = AnchorLayout()

        bl1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=[.6, .12])

        t = TextInput(hint_text='Enter here', multiline=False, background_color=[.93,.93,.93,1], cursor_color=[0,0,0,1], foreground_color=[0,0,0,1], selection_color=[0,.68,.71,.5])
        bl1.add_widget(t)

        b = Button(text='Draw', size_hint=[.1, 1], background_normal='', background_color=[.24,.29,.32,1], on_press=self.draw)
        bl1.add_widget(b)

        al1.add_widget(bl1)

        al2 = AnchorLayout(anchor_y='bottom', size_hint=[1, .4])

        exit_b = Button(text='Exit', size_hint=[.1, .3], background_color=[.24,.29,.32,1], background_normal='', on_press=self.exit)
        al2.add_widget(exit_b)

        bl2 = BoxLayout(orientation='vertical', size_hint=[1, .3])

        bl2.add_widget(Label(text='Hi there!', color=[0,.68,.71,1]))
        bl2.add_widget(Label(text='I am the program that help you draw the logical scheme', color=[0,.68,.71,1]))
        bl2.add_widget(Label(text='Please, write the logical expression in form below', color=[0,.68,.71,1]))

        root.add_widget(bl2)
        root.add_widget(al1)
        root.add_widget(al2)

        return root

    def draw(self, button):
        d = schem.Drawing()
        # Two front gates (SR latch)
        G1 = d.add(l.NAND2, anchor='in1')
        d.add(e.LINE, l=d.unit/6)
        Q1 = d.add(e.DOT)
        d.add(e.LINE, l=d.unit/6)
        Q2 = d.add(e.DOT)
        d.add(e.LINE, l=d.unit/3, rgtlabel='$Q$')
        G2 = d.add(l.NAND2, anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5])
        d.add(e.LINE, l=d.unit/6)
        Qb = d.add(e.DOT)
        d.add(e.LINE, l=d.unit/3)
        Qb2 = d.add(e.DOT)
        d.add(e.LINE, l=d.unit/6, rgtlabel='$\overline{Q}$')
        S1 = d.add(e.LINE, xy=G2.in1, d='up', l=d.unit/6)
        d.add(e.LINE, d='down', xy=Q1.start, l=d.unit/6)
        d.add(e.LINE, to=S1.end)
        R1 = d.add(e.LINE, xy=G1.in2, d='down', l=d.unit/6)
        d.add(e.LINE, d='up', xy=Qb.start, l=d.unit/6)
        d.add(e.LINE, to=R1.end)

        # Two back gates
        d.add(e.LINE, xy=G1.in1, d='left', l=d.unit/6)
        J = d.add(l.NAND3, anchor='out', reverse=True)
        d.add(e.LINE, xy=J.in3, d='up', l=d.unit/6)
        d.add(e.LINE, d='right', tox=Qb2.start)
        d.add(e.LINE, d='down', toy=Qb2.start)
        d.add(e.LINE, d='left', xy=J.in2, l=d.unit/4, lftlabel='$J$')
        d.add(e.LINE, xy=G2.in2, d='left', l=d.unit/6)
        K = d.add(l.NAND3, anchor='out', reverse=True)
        d.add(e.LINE, xy=K.in1, d='down', l=d.unit/6)
        d.add(e.LINE, d='right', tox=Q2.start)
        d.add(e.LINE, d='up', toy=Q2.start)
        d.add(e.LINE, d='left', xy=K.in2, l=d.unit/4, lftlabel='$K$')
        C = d.add(e.LINE, d='down', xy=J.in1, toy=K.in3)
        d.add(e.DOT, xy=C.center)
        d.add(e.LINE, d='left', xy=C.center, l=d.unit/4, lftlabel='$CLK$')
        d.draw()



if __name__ == '__main__':
    MyApp().run()
