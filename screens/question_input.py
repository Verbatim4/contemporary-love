from kivy.uix.screenmanager import Screen, WipeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from tools.toolbar import Toolbar

TRANSITION_TIME = 0.2
BUTTON_COLOR = (0.2, 0.2, 0.2, 1)
INPUT_COLOR = (0.3, 0.3, 0.3, 1)

class QuestionInput(Screen):
    def __init__(self, **kwargs):
        super(QuestionInput, self).__init__(**kwargs)

        self.layout = FloatLayout()

        self.title_layout = FloatLayout()
        self.title_txt = Label(
            text='Enter Question:',
            font_size='25sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
        )
        self.title_layout.add_widget(self.title_txt)
        self.layout.add_widget(self.title_layout)
        
        self.input_field = TextInput(
            size_hint=(0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            background_normal='',
            background_color=INPUT_COLOR,
            background_active='',
            cursor_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=False,
        )

        self.continue_btn = Button(
            text='Proceed',
            bold=True,
            on_release=lambda instance:self.go_without_transition('table'),
            size_hint=(0.6, 0.2),
            pos_hint = {'center_x': 0.5, 'center_y': 0.4},
            background_normal='',
            background_color=BUTTON_COLOR,
        )

        self.homepage_btn = Button(
            text='Back to homepage',
            bold=True,
            on_release=lambda instance:self.go_to_page('home', 'right'),
            size_hint=(0.4, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.2},
            background_normal='',
            background_color=BUTTON_COLOR,
        )

        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.continue_btn)
        self.layout.add_widget(self.homepage_btn)

        self.add_widget(self.layout)
        self.add_widget(Toolbar('right', 'right', 'left'))

    def go_to_page(self, page, direction, *args):
        self.parent.transition.direction = direction
        self.parent.transition.duration = 0
        self.parent.current = page

    def go_without_transition(self, page, *args):
        self.parent.transition = WipeTransition()
        self.parent.current = page
