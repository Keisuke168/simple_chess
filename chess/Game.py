from ChessBoard import ChessBoard
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

class Game():
    def __init__(self):
        self.board = ChessBoard()
        self.player = 1
    
    def can_move(self,pos):
        return self.board.can_move(pos,self.player)
    
    def progress_game(self,pos,destination):
        self.board.move(pos,destination,self.player)
        self.player *= -1

        for l in self.board.board:
            if self.player*6 in l:
                return 
        if self.player == 1:
            self.label.text ="[color=#3399FF][b]BLACK WIN[/b][/color]"
        else:
            self.label.text = "[color=#3399FF][b]WHITE WIN[/b][/color]"

    
    def get_board(self):
        return self.board.board
    
    def set_widget(self,widget):
        self.label = widget
        self.label.markup = True
        self.label.font_size = 100
        self.label.size = (800, 800)

