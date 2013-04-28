'''
Created on Aug 19, 2012

@author: George Peek
'''

from game import Game
from team import Team
from display import Display

team1 = Team("Austin","Easy",True)
team2 = Team("Chicago","Grown Men")
game = Game(team1,team2,display=Display())

game.start_game(.5)
