from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from tools.toolbar import Toolbar

TRANSITION_TIME = 0.2
BUTTON_COLOR = (0.2, 0.2, 0.2, 1)


class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        
        self.layout = FloatLayout()

        self.title_layout = FloatLayout()
        self.title_txt = Label(
            text='Contemporary Love',
            font_size='25sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
        )
        self.title_layout.add_widget(self.title_txt)
        self.layout.add_widget(self.title_layout)

        self.normal_reading = Button(
            text='Normal Reading', 
            bold=True,
            on_release=self.go_to_question,
            size_hint = (0.5, 0.17),
            pos_hint = {'center_x': 0.5, 'center_y': 0.4},
            background_normal='',
            background_color=BUTTON_COLOR,
        )
        
        self.daily_reading = Button(
            text='Daily Reading', 
            bold=True,
            on_release=self.go_to_daily,
            size_hint = (0.5, 0.17),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            background_normal='',
            background_color=BUTTON_COLOR,
        )

        self.toolbar = Toolbar('left', 'left', 'left')

        self.layout.add_widget(self.normal_reading)
        self.layout.add_widget(self.daily_reading)

        self.add_widget(self.layout)
        self.add_widget(self.toolbar)
    
    def go_to_question(self, *args):
        self.parent.transition.direction = 'left'
        self.parent.transition.duration = TRANSITION_TIME
        self.parent.current = 'question'
    

    def go_to_daily(self,  *args):
        self.parent.transition.direction = 'left'
        self.parent.transition.duration = TRANSITION_TIME
        self.parent.current = 'daily'