from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from tools.card import *
from tools.toolbar import *

from textwrap import TextWrapper
import datetime

TRANSITION_TIME = 0.2
BUTTON_COLOR = [0.2, 0.2, 0.2, 1]
PRESSED_COLOR = [0.1, 0.1, 0.1, 1]

class DailyReading(Screen):
	def __init__(self, **kwargs):
		super(DailyReading, self).__init__(**kwargs)

		self.layout = FloatLayout()

		self.title_layout = FloatLayout()
		self.title_txt = Label(
			text='Daily Reading',
			font_size='25sp',
			pos_hint={'center_x': 0.5, 'center_y': 0.8},
		)
		self.title_layout.add_widget(self.title_txt)
		self.layout.add_widget(self.title_layout)

		self.card_layout = BoxLayout(
			orientation='vertical',
			pos_hint={'center_x': 0.5, 'center_y': 0.85},
		)

		self.daily_card = Card()

		self.daily_card.width *= 1.5
		self.daily_card.height *= 1.5

		today = str(datetime.date.today())

		with open('./assets/today.txt', 'r+') as f:
			content = f.readlines()
			old_date = content[0]
			old_card = content[1].split(':')
			old_color = eval(content[2])
			did_card = int(content[3].strip().split(':')[1])

			if (today == old_date.strip()) and (did_card):
				self.daily_card.card_val = tuple(old_card)
				self.daily_card.set_text(old_card[0])
				self.daily_card.background_color = tuple(old_color)

		self.card_layout.add_widget(self.daily_card)
		self.layout.add_widget(self.card_layout)

		self.expanded_layout = FloatLayout()
		self.expanded_card = Button(
			size_hint=(0.98, 0.98),
			pos_hint = {'center_x': 0.5, 'center_y': 0.5},
			background_normal='',
			on_release=self.shrink_card,
			halign='center',
			bold=True,
		)
		self.expanded_layout.add_widget(self.expanded_card)

		self.back_layout = FloatLayout()
		self.back_btn = Button(
			text='Back to\nHomepage',
			bold=True,
			on_release=lambda instance:self.go_to_page('home', 'right'),
			background_normal='',
			background_color=BUTTON_COLOR,
			size_hint=(None, None),
			size=(Window.size[0] * 0.28, Window.size[1] * 0.15),
			pos_hint={'center_x': 0.5, 'center_y': 0.2},
			halign='center'
		)
		self.back_layout.add_widget(self.back_btn)
		self.layout.add_widget(self.back_layout)

		self.add_widget(self.layout)
		self.add_widget(Toolbar('right', 'left', 'left'))

	def expand_card(self, *args):
		self.daily_card.expand()

		wrap = TextWrapper(width=30)

		self.expanded_card.background_color = self.daily_card.background_color
		self.expanded_card.text = wrap.fill(text=f'{self.daily_card.card_val[0]}: {self.daily_card.card_val[1]}')

		self.add_widget(self.expanded_layout)
		self.daily_card.disabled = True

	def shrink_card(self, *args):
		self.daily_card.shrink()
		self.remove_widget(self.expanded_layout)
		self.daily_card.disabled = False

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page