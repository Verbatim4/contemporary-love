from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

import random
from textwrap import TextWrapper
import pymongo
import datetime

CARD_COLORS = [
	(130/255, 90/255, 107/255, 1),
	(132/255, 109/255, 93/255, 1),
	(74/255, 130/255, 76/255, 1),
	(79/255, 128/255, 132/255, 1),
]


class Card(Button):
	def __init__(self, **kwargs):

		super(Card, self).__init__(**kwargs)

		self.on_release = self.reveal_card

		self.revealed = False

		self._store = JsonStore('./assets/cards.json').get('cards')
		self.cards = [tuple(i.items())[0] for i in self._store]

		# client = pymongo.MongoClient("mongodb+srv://shreksodyne414:Pottermore2@tarotapp.l0jd7et.mongodb.net/?retryWrites=true&w=majority")
		# collection = client.contemporarylove.cards
		# cards_raw = collection.find()[0]['cards']
		# self.cards = [tuple(i.items())[0] for i in cards_raw]

		self.drawn_cards = []

		self.expanded = False

		self.card_val = ()

		# Card Styling

		c = 0.23
		width = Window.size[0] * c
		height = 19/11 * width

		self.size_hint = (None, None)
		self.size = (width, height)

		self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

		self.bold = True
		self.halign = 'center'

		self.background_normal = './assets/images/background.jpg'
		self.background_color = random.choice(CARD_COLORS)

	def set_text(self, text, *args):
		wrap = TextWrapper(width=10)
		self.text = wrap.fill(text=f'{text}')
		self.background_normal = './assets/images/front.jpg'

	def reveal_card(self, *args):
		if not self.expanded:
			if not self.text:
				
				available_cards = [card for card in self.cards if card not in self.drawn_cards]

				card = random.choice(available_cards)
				self.drawn_cards.append(card)
				self.card_val = card

				self.set_text(self.card_val[0])

				if self.parent.parent.parent.parent.current == 'daily':
					with open('./assets/today.txt', 'r+') as f:
						f.seek(0)
						data = f.readlines()
					
						f.seek(0)
						today = str(datetime.date.today())
						data[0] = today + '\n'
						data[1] = ":".join(self.card_val) + '\n'
						data[2] = str(self.background_color) + '\n'
						data[3] = 'daily_card:1\n'

						f.writelines(data)
						f.truncate()

				return 

			self.expand()
			self.parent.parent.parent.expand_card(self)
			return

		self.shrink()
		self.parent.parent.parent.shrink_card(self)

	def expand(self, *args):
		self.expanded = True
	
	def shrink(self, *args):
		self.expanded = False
