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
        if self.field.direction == 1:
            self.plays.append(Play(self.possession[0],self.possession[1],self.field))
        elif self.field.direction == -1:
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
    def __init__(self, touchdown_pts=6, field_goal_pts=3, safety_pts=2, conversion_play_pts=2, conversion_kick_pts=1):
        self.absolute_yardline = '30'
        self.play_name = 'None'
        self.play_rating = '0'
        self.offense_yardage ='0'
        self.return_yardage = '0'
        self.turnover = 'False'
        self.down = '1'
        self.yards_to_go = '10'
        
        self.touchdown_pts = touchdown_pts
        self.field_goal_pts = field_goal_pts   
        self.safety_pts = safety_pts       
        self.conversion_play_pts = conversion_play_pts
        self.conversion_kick_pts = conversion_kick_pts
        
        self.home_score = 0
        self.away_score = 0
        
    def home_touchdown(self):
        self.home_score += self.touchdown_pts
        
    def away_touchdown(self):
        self.away_score += self.touchdown_pts
        
    def home_field_goal(self):
        self.home_score += self.field_goal_pts
        
    def away_field_goal(self):
        self.away_score += self.field_goal_pts

    def home_safety(self):
        self.home_score += self.safety_pts
        
    def away_safety(self):
        self.away_score += self.safety_pts

    def home_conversion_play(self):
        self.home_score += self.conversion_play_pts
        
    def away_conversion_play(self):
        self.away_score += self.conversion_play_pts

    def home_conversion_kick(self):
        self.home_score += self.conversion_kick_pts
        
    def away_conversion_kick(self):
        self.away_score += self.conversion_kick_pts
#===============================================================================