from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import datetime
from textwrap import TextWrapper
from tools.toolbar import Toolbar
import pandas as pd

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

		self.daily_reading = Button(
			text='Daily Reading', 
			bold=True,
			on_release=lambda instance:self.go_to_page('daily', 'left'),
			size_hint = (0.5, 0.17),
			pos_hint = {'center_x': 0.5, 'center_y': 0.6},
			background_normal='',
			background_color=BUTTON_COLOR,
		)

		self.normal_reading = Button(
			text='Normal Reading', 
			bold=True,
			on_release=lambda instance:self.go_to_page('question', 'left'),
			size_hint = (0.5, 0.17),
			pos_hint = {'center_x': 0.5, 'center_y': 0.4},
			background_normal='',
			background_color=BUTTON_COLOR,
		)

		self.daily_quote = Button(
			text='Daily Quote', 
			bold=True,
			on_release=lambda instance:self.go_to_page('pickquote', 'left'),
			size_hint = (0.5, 0.17),
			pos_hint = {'center_x': 0.5, 'center_y': 0.2},
			background_normal='',
			background_color=BUTTON_COLOR,
		)

		self.toolbar = Toolbar('left', 'left', 'left')

		self.layout.add_widget(self.normal_reading)
		self.layout.add_widget(self.daily_reading)
		self.layout.add_widget(self.daily_quote)

		self.add_widget(self.layout)
		self.add_widget(self.toolbar)

	def on_enter(self, *args):
		daily_quote = self.manager.get_screen('dailyquote')
		daily_quote.quotes = pd.read_csv('./assets/quotes4.csv', sep=',')
		today = str(datetime.date.today())

		with open('./assets/today.txt', 'r+') as f:
			content = f.readlines()
			old_date = content[0]
			old_quote = content[4].strip().split(';')[0]
			old_author = content[4].strip().split(';')[1]
			did_quote = int(content[5].strip().split(':')[1])

			if today != old_date.strip():
				content[0] = today + '\n'
				content[3] = 'daily_card:0\n'
				content[5] = 'daily_quote:0\n'
				f.seek(0)
				f.writelines(content)

			if (today == old_date.strip()) and (did_quote == 1):
				# print(did_quote)
				wrap = TextWrapper(width=40)
				daily_quote.set_quote(wrap.fill(text=old_quote), wrap.fill(text=old_author))

				homepage = self.manager.get_screen('home')
				homepage.daily_quote.on_release = lambda:homepage.go_to_page('dailyquote', 'left')

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page
