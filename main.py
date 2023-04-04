from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.homepage import HomePage
from screens.table import Table
from screens.question_input import QuestionInput
from screens.daily_reading import DailyReading

Window.size =  (360, 640)
Window.clearcolor = (0, 0, 0, 1)


class TarotApp(App):
    def build(self):
        
        table = Table(name='table')

        sm = ScreenManager()
        sm.add_widget(HomePage(name='home'))
        sm.add_widget(QuestionInput(name='question'))
        sm.add_widget(table)
        sm.add_widget(DailyReading(name='daily'))
        return sm


if __name__ == '__main__':
    TarotApp().run()
