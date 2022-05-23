from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
import math
import numpy as np
from ChessBoard import ChessBoard
from Game import Game


class RootWidget(Widget):
    pass

class Pieces(Widget):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.grabing = ()
        self.movable = np.zeros((8,8))

    def update_window(self):
        bd=self.game.get_board()
        for i in range(8):
            for j in range(8):
                if(bd[i][j] !=0):
                    with self.canvas:
                        Rectangle(source='./images/{}.png'.format(bd[i][j]), pos=(100*j, 100*i), size=(100, 100))     

    def draw_movable(self):
        for i in range(8):
            for j in range(8):
                if(self.movable[i][j] == 1):
                    with self.canvas:
                        Color(0,0,1,0.5)
                        Rectangle(pos=(100*j, 100*i), size=(100, 100))

    def on_touch_down(self,touch):
        self.canvas.clear()
        position = (math.floor((touch.spos[0]*64)/8),math.floor((touch.spos[1]*64)/8))
        # print(position[1],position[0])
        if len(self.grabing)>0:
            if self.movable[position[1]][position[0]]==1:
                self.game.progress_game(self.grabing,position)
            self.movable = np.zeros((8,8))
            self.grabing = ()
        else:
            self.movable = self.game.can_move(position)
            self.draw_movable()
            self.grabing = position

        self.update_window()    



class Board(Widget):
    def update_window(self):
        temp=False
        for i in range(8):
            temp =not temp
            for j in range(8):
                with self.canvas:
                    if temp:
                        Color(112/255, 128/255, 144/255)
                        Rectangle(pos=(100*i, 100*j), size=(100, 100))
                        temp=not temp
                    else:
                        Color(1,1,1)
                        Rectangle(pos=(100*i, 100*j), size=(100, 100))
                        temp=not temp

class MyApp(App):
    title = 'chess game'

    def build(self):
        label = Label()
        game = Game()
        game.set_widget(label)
        widget = RootWidget()
        widget.add_widget(Board())
        widget.add_widget(Pieces(game))
        

        for child in widget.children:
            child.update_window()

        widget.add_widget(label)
        return widget


if __name__ == '__main__':
    MyApp().run()