from kivy.uix.screenmanager import Screen, NoTransition, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from tools.card import *
from tools.toolbar import *

import random
from collections import deque
from textwrap import TextWrapper

Window.clearcolor = (1, 1, 1, 1)

CARD_COLORS = [
	(130/255, 90/255, 107/255, 1),
	(132/255, 109/255, 93/255, 1),
	(74/255, 130/255, 76/255, 1),
	(79/255, 128/255, 132/255, 1),
]
# CARD_COLORS = [
#     (110/255, 70/255, 87/255, 1),
#     (112/255, 89/255, 73/255, 1),
#     (54/255, 110/255, 56/255, 1),
#     (59/255, 108/255, 112/255, 1),
# ]

BUTTON_COLOR = [0.2, 0.2, 0.2, 1]
PRESSED_COLOR = [0.1, 0.1, 0.1, 1]
INPUT_COLOR = (0.3, 0.3, 0.3, 1)

TRANSITION_TIME = 0.2

class Table(Screen):
	def __init__(self, **kwargs):
		super(Table, self).__init__(**kwargs)

		self.num_drawn = 0
		self.drawn_cards = []

		self.title_layout = FloatLayout()
		self.title_txt = Label(
			text='Table',
			font_size='25sp',
			pos_hint={'center_x': 0.5, 'center_y': 0.8},
		)
		self.title_layout.add_widget(self.title_txt)
		self.add_widget(self.title_layout)

		self.layout = GridLayout(cols=3, rows=4)

		# Adding 9 cards to gridlayout
		for _ in range(9):
			card_layout = FloatLayout()
			card_layout.add_widget(Card(opacity=0, disabled=True))
			self.layout.add_widget(card_layout)

		# Redraw card button
		self.redraw_layout = FloatLayout()
		self.redraw_btn = Button(
			text='Redraw',
			bold=True,
			on_release=self.reset,
			background_normal='',
			background_color=BUTTON_COLOR,
			size_hint=(None, None),
			size=(Window.size[0] * 0.28, Window.size[1] * 0.15),
			pos_hint={'center_x': 0.58, 'center_y': 0.6},
		)
		
		self.redraw_layout.add_widget(self.redraw_btn)
		self.layout.add_widget(self.redraw_layout)

		# Draw card button
		self.draw_layout = FloatLayout()
		self.draw_btn = Button(
			text='Draw Card',
			bold=True,
			on_release=self.draw_card,
			background_normal='',
			background_color=BUTTON_COLOR,
			size_hint=(None, None),
			size=(Window.size[0] * 0.28, Window.size[1] * 0.15),
			pos_hint={'center_x': 0.5, 'center_y': 0.6},
		)
		
		self.draw_layout.add_widget(self.draw_btn)
		self.layout.add_widget(self.draw_layout)

		# Back button
		self.back_layout = FloatLayout()
		self.back_btn = Button(
			text='Ask another \nquestion',
			bold=True,
			on_release=lambda instance:self.go_without_transition('question'),
			background_normal='',
			background_color=BUTTON_COLOR,
			size_hint=(None, None),
			size=(Window.size[0] * 0.28, Window.size[1] * 0.15),
			pos_hint={'center_x': 0.42, 'center_y': 0.6},
			halign='center'
		)
		
		self.back_layout.add_widget(self.back_btn)
		self.layout.add_widget(self.back_layout)

		self.expanded_layout = FloatLayout()
		self.expanded_card = Button(
			# disabled=True,
			# opacity=0,
			size_hint=(0.98, 0.98),
			pos_hint = {'center_x': 0.5, 'center_y': 0.5},
			background_normal='',
			on_release=self.shrink_card,
			halign='center',
			bold=True,
		)
		self.expanded_layout.add_widget(self.expanded_card)
		# self.add_widget(self.expanded_layout)

		self.currently_expanded = None

		# Layout Styling

		margin_size = 0.05
		self.layout.padding = self.layout.height * margin_size
		self.layout.spacing = self.layout.height * margin_size

		self.add_widget(self.layout) 
		self.add_widget(Toolbar('right', 'right', 'right'))

		self.buttons = self.children[1].children[3:]
		self.buttons.reverse()

	def draw_card(self, *args):
		if self.num_drawn >= 9:
			return

		card_iter = [button.children[0] for button in self.buttons if button.children[0].disabled]
		queue = deque(card_iter)

		card_to_draw = queue[0]

		card_to_draw.opacity = 1
		card_to_draw.disabled = False

		self.num_drawn += 1
		self.drawn_cards = card_to_draw.drawn_cards

		queue.rotate(-1)

	def expand_card(self, card, *args):
		self.currently_expanded = card
		card.expand()
		
		wrap = TextWrapper(width=30)

		self.expanded_card.background_color = card.background_color
		self.expanded_card.text = wrap.fill(text=f'{card.card_val[0]}: {card.card_val[1]}')

		self.add_widget(self.expanded_layout)

		self.redraw_btn.disabled = True
		self.draw_btn.disabled = True
		self.back_btn.disabled = True

	def shrink_card(self, card, *args):
		self.currently_expanded.shrink()

		self.remove_widget(self.expanded_layout)

		self.redraw_btn.disabled = False
		self.draw_btn.disabled = False
		self.back_btn.disabled = False

	def reset(self, *args):
		for button in self.buttons:
			button.children[0].text = ''
			button.children[0].disabled = True
			button.children[0].drawn_cards = []
			button.children[0].opacity = 0
			button.children[0].background_normal = './assets/images/background.jpg'
			button.children[0].background_color = random.choice(CARD_COLORS)
			button.children[0].card_val = 0

		self.num_drawn = 0

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page

	def go_without_transition(self, page, *args):
		self.parent.transition = NoTransition()
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page
		self.parent.transition = SlideTransition()


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
			on_release=self.go_to_table,
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

	def go_to_table(self, *args):
		self.go_without_transition('table')
		self.manager.get_screen('table').reset()

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page

	def go_without_transition(self, page, *args):
		self.parent.transition = NoTransition()
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page
		self.parent.transition = SlideTransition()