'''
Created on Mar 1, 2012

@author: George Peek
'''

from random import choice

from play import Play
from state_machine import Kickoff

class Game():
    "Game"
    def __init__(self, home_team, away_team, league_game=False, division_game=False, conference_game=False, playoff_game=False):
#        self.game_id = get_next_game_id()
        self.home = home_team
        self.away = away_team
        self.league_game = league_game
        self.division_game = division_game
        self.conference_game = conference_game 
        self.playoff_game = playoff_game  
        self.field = Field()
        self.scoreboard = Scoreboard()
        self.plays = []
        self.possession = [self.home, self.away]
        self.coin_flip()
        self.current_state = Kickoff(self)

    def coin_flip(self):
        self.field.direction = choice([-1,1])
        if self.field.direction == -1:
            self.plays.append(Play(self.possession[0],self.possession[1],self.field))
        elif self.field.direction == 1:
            self.possession[0], self.possession[1] = self.possession[1], self.possession[0]
            self.plays.append(Play(self.possession[0],self.possession[1],self.field))
        self.field.kickoff_set()

class Field():
    "Playing Field"
    def __init__(self):
        self.direction = 1 ## 1=home, -1=away
        self.absolute_yardline = 30
        self.converted_yardline = 30
        self.in_home_endzone = False
        self.in_away_endzone = False
        
    def play_reset(self):
        self.in_home_endzone = False
        self.in_away_endzone = False    
    
    def determine_position(self, yardage, change_of_possession):
        if change_of_possession:
            print 'chg pos' + str(change_of_possession)
            self.direction *= -1

        self.absolute_yardline += (yardage * self.direction)

        if self.absolute_yardline > 50:
            self.converted_yardline = 100 - self.absolute_yardline
            if self.absolute_yardline >= 100:
                self.in_away_endzone = True
        else:
            self.converted_yardline = self.absolute_yardline
            if self.absolute_yardline <= 0:
                self.in_home_endzone = True
                
    def kickoff_set(self):
        if self.direction == 1:
            self.absolute_yardline = 30
        elif self.direction == -1:
            self.absolute_yardline = 70
        self.converted_yardline = 30
            
    def touchback_set(self):
        self.direction *= -1
        if self.direction == -1:
            self.absolute_yardline = 80
        elif self.direction == 1:
            self.absolute_yardline = 20
        self.converted_yardline = 20
        
    def conversion_set(self):
        if self.direction == 1:
            self.absolute_yardline = 98
        elif self.direction == -1:
            self.absolute_yardline = 2
        self.converted_yardline = 2
        

class Scoreboard():
    def __init__(self):
        self.absolute_yardline = '30'
        self.play_name = 'None'
        self.play_rating = '0'
        self.offense_yardage ='0'
        self.return_yardage = '0'
        self.turnover = 'False'
        self.down = '1'
        self.yards_to_go = '10'

#===============================================================================