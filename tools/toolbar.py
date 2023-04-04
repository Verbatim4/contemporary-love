from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color

TRANSITION_TIME = 0.2
TOOLBAR_COLOR = (0.1, 0.1, 0.1, 1)

class Toolbar(FloatLayout):
    def __init__(self, home_dir, daily_dir, reading_dir, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        with self.canvas:
            Color(*TOOLBAR_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.size_hint = (1, 0.07)
        self.pos = (0, 0)

        self.homepage_btn = Button(
            text='H', 
            bold=True,
            on_release=lambda instance:self.go_to_page('home', home_dir),
            size_hint = (0.15, 0.7),
            pos_hint = {'center_x': 0.2, 'center_y': 0.5},
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
        )
        self.add_widget(self.homepage_btn)

        self.daily_btn = Button(
            text='D', 
            bold=True,
            on_release=lambda instance:self.go_to_page('daily', daily_dir),
            size_hint = (0.15, 0.7),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
        )
        self.add_widget(self.daily_btn)

        self.reading_btn = Button(
            text='R', 
            bold=True,
            on_release=lambda instance:self.go_to_page('question', reading_dir),
            size_hint = (0.15, 0.7),
            pos_hint = {'center_x': 0.8, 'center_y': 0.5},
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
        )
        self.add_widget(self.reading_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_page(self, page, direction, *args):
        self.parent.parent.transition.direction = direction
        self.parent.parent.transition.duration = TRANSITION_TIME
        self.parent.parent.current = page
