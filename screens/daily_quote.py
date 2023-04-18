from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from tools.card import *
from tools.toolbar import *

from textwrap import TextWrapper
import datetime
import pandas as pd
import random

BUTTON_COLOR = [0.2, 0.2, 0.2, 1]
PICKED_GENRE = ''

#TODO: open today.txt and get genre, then make self.genre variable in pickquote to access in dailyquote


class PickQuote(Screen):
	def __init__(self, **kwargs):
		super(PickQuote, self).__init__(**kwargs)

		self.layout = FloatLayout()
		self.quotes = pd.read_csv('./assets/quotes4.csv', sep=',')
		self.genres = list(self.quotes.GENRE.unique()[:-9])
		self.special_genres = list(self.quotes.GENRE.unique()[-9:])

		self.title_layout = FloatLayout()
		self.title_label = Label(
			text='Daily Quote',
			font_size='18sp',
			pos_hint={'center_x': 0.5, 'center_y': 0.8},
		)
		self.title_layout.add_widget(self.title_label)

		self.random_genres = random.sample(self.genres, 3)
		self.button_layout = FloatLayout()

		self.genre_button_1 = Button(
			text=self.random_genres[0].title(), 
			bold=True,
			size_hint = (0.3, 0.08),
			pos_hint = {'center_x': 0.5, 'center_y': 0.4},
			background_normal='',
			background_color=BUTTON_COLOR,
			on_press=lambda instance:self.set_picked(self.random_genres[0]),
			on_release=lambda instance:self.go_to_page('dailyquote', 'left')
		)
		self.button_layout.add_widget(self.genre_button_1)

		self.genre_button_2 = Button(
			text=self.random_genres[1].title(), 
			bold=True,
			size_hint = (0.3, 0.08),
			pos_hint = {'center_x': 0.5, 'center_y': 0.5},
			background_normal='',
			background_color=BUTTON_COLOR,
			on_press=lambda instance:self.set_picked(self.random_genres[1]),
			on_release=lambda instance:self.go_to_page('dailyquote', 'left')
		)
		self.button_layout.add_widget(self.genre_button_2)


		self.genre_button_3 = Button(
			text=self.random_genres[2].title(), 
			bold=True,
			size_hint = (0.3, 0.08),
			pos_hint = {'center_x': 0.5, 'center_y': 0.6},
			background_normal='',
			background_color=BUTTON_COLOR,
			on_press=lambda instance:self.set_picked(self.random_genres[2]),
			on_release=lambda instance:self.go_to_page('dailyquote', 'left')
		)
		self.button_layout.add_widget(self.genre_button_3)


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

		self.layout.add_widget(self.title_layout)
		self.layout.add_widget(self.button_layout)
		self.layout.add_widget(self.back_btn)
		self.add_widget(self.layout)
		self.add_widget(Toolbar('right', 'right', 'right'))

	def on_pre_enter(self, *args):
		pass

	def set_picked(self, genre, *args):
		self.genre = genre

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page


class DailyQuote(Screen):
	def __init__(self, **kwargs):
		super(DailyQuote, self).__init__(**kwargs)

		self.quote_label = Label(
			text='',
			pos_hint={'center_x': 0.5, 'center_y': 0.6}
		)
		self.author_label = Label(
			text='',
			pos_hint={'center_x': 0.5, 'center_y': 0.4}
		)

		self.back_btn = Button(
			text='Back to \nHomepage',
			pos_hint={'center_x': 0.5, 'center_y': 0.2},
			size_hint=(None, None),
			size=(Window.size[0] * 0.28, Window.size[1] * 0.15),
			on_release=lambda instance:self.go_to_page('home', 'right'),
			halign='center'
		)

		self.add_widget(self.quote_label)
		self.add_widget(self.author_label)
		self.add_widget(self.back_btn)
		self.add_widget(Toolbar('right', 'right', 'right'))

	def on_pre_enter(self, *args):
		today = str(datetime.date.today())
		pick_quote = self.manager.get_screen('pickquote')

		with open('./assets/today.txt', 'r+') as f:
			content = f.readlines()
			old_date = content[0]

			if today != old_date.strip():
				self.available_quotes = self.quotes.loc[self.quotes['GENRE'] == pick_quote.genre]
				self.picked_quote = self.available_quotes.sample(1)
				# print(self.picked_quote)

				raw_quote = ''.join(self.picked_quote['QUOTE'].values)
				raw_author = ''.join(self.picked_quote['AUTHOR'].values)

				wrap = TextWrapper(width=40)
				new_quote = wrap.fill(text=f"{raw_quote}")
				new_author = wrap.fill(text=f"{raw_author}")

				self.set_quote(new_quote, new_author)

				content[0] = today + '\n'
				content[3] = raw_quote + ';' + raw_author + '\n'
				f.seek(0)
				f.write(''.join(content))

	def set_quote(self, quote, author, *args):
		self.quote_label.text = quote
		self.author_label.text = author

	def clear_page(self, *args):
		self.quote_label.text = ''
		self.author_label.text = ''

	def go_to_page(self, page, direction, *args):
		self.parent.transition.direction = direction
		self.parent.transition.duration = TRANSITION_TIME
		self.parent.current = page
		self.clear_page()

	def test(self, *args):
		print('cum')

