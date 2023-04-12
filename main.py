from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.homepage import *
from screens.table import *
# from screens.question_input import *
from screens.daily_reading import *
from screens.daily_quote import *

Window.size =  (360, 640)
Window.clearcolor = (0, 0, 0, 1)

# TODO: add pandas to buildozer.spec

class TarotApp(App):

	def build(self):

		sm = ScreenManager()
		sm.add_widget(HomePage(name='home'))
		sm.add_widget(QuestionInput(name='question'))
		sm.add_widget(Table(name='table'))
		sm.add_widget(DailyReading(name='daily'))
		sm.add_widget(PickQuote(name='pickquote'))
		sm.add_widget(DailyQuote(name='dailyquote'))
		return sm


if __name__ == '__main__':
	TarotApp().run()
