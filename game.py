'''
Created on Mar 1, 2012

@author: George Peek
'''

from math import ceil
from random import choice
from collections import deque
from copy import deepcopy
from collections import namedtuple, defaultdict

from playbook import Kickoff, Punt, FieldGoal
from timekeeping import Clock
from state_machine import State

class Game():
    "Game"
    def __init__(self, home_team, away_team, league_game=False, division_game=False, conference_game=False, playoff_game=False, number_of_periods=4):
#        self.game_id = get_next_game_id()
        self.home = deepcopy(home_team)
        self.away = deepcopy(away_team)
        self.league_game = league_game
        self.division_game = division_game
        self.conference_game = conference_game 
        self.playoff_game = playoff_game  
        self.number_of_periods = number_of_periods
        self.period = 1
        self.field = Field(self.get_offense)
        self.scoreboard = Scoreboard()
        self.plays = []
        self.coin_flip_winner = self._coin_flip()
        self._Possession = namedtuple('Possession', ['offense','defense'])
        self.possession = self._possession_setup()
        self.current_state = State(self.field,
                                   self.change_possession,
                                   self.get_offense).check_state()
        self.timekeeping = deque()
        self.timekeeping.extend([Clock() for x in range(number_of_periods)])
        self.current_clock = self.timekeeping.pop()
        self.end_of_half = False
        self.end_of_regulation = False
        self.overtime = False
        self.end_of_game = False
        
    def _possession_setup(self):
        PossTeam = namedtuple('PossTeam', ['team','direction','home_team','plays_run'])
        
        t1 = PossTeam(self.home,1,True,defaultdict(int))
        t2 = PossTeam(self.away,-1,False,defaultdict(int))
        
        # set coin flip loser as initial offense because they will be kicking off
        if self.coin_flip_winner == t1.direction:
            return self._Possession(t2,t1)
        else:
            return self._Possession(t1,t2)

    def _coin_flip(self):
        return choice([-1,1])
        
    def set_second_half(self):
        ## sets up kickoff the opposite of opening kick
        if (self.coin_flip_winner * -1) == self.offense.direction:
            self.change_possession()
        self.field.kickoff_set()
        
    def change_possession(self):
        print 'chg possession'
        self.possession = self._Possession(self.possession[1],self.possession[0])
        
    def get_offense(self):
        return self.possession.offense
        
    def run_play(self,play_call):
        play = Play(self.possession.offense,
                         self.possession.defense,
                         self.field)
        play.play_call = play_call
        play.run_play()
        self.plays.append(play)
        self.current_state = self.current_state.check_state(play.events)
        
class Field():
    "Playing Field"
    def __init__(self, 
                 get_offense,
                 length=100.0,
                 kickoff_yardline=30.0,
                 free_kick_yardline=20.0,
                 conversion_yardline=2.0,
                 touchback_yardline=20.0):
        self.get_offense = get_offense
        self.length = length
        self.kickoff_yardline = kickoff_yardline
        self.free_kick_yardline = free_kick_yardline
        self.conversion_yardline = conversion_yardline
        self.touchback_yardline = touchback_yardline
        self.absolute_yardline = self.kickoff_yardline
        self.converted_yardline = self.kickoff_yardline
        self.home_endzone = 0.0
        self.away_endzone = self.length
        
    def determine_position(self, yardage):
        self.absolute_yardline += yardage

        if self.absolute_yardline > (self.length / 2):
            self.converted_yardline = self.length - self.absolute_yardline
        else:
            self.converted_yardline = self.absolute_yardline

    def _set_ball_position(self,yardline):
        if self.get_offense().direction == 1:
            self.absolute_yardline = yardline
        elif self.get_offense().direction == -1:
            self.absolute_yardline = self.length - yardline
        self.converted_yardline = yardline        
                
    def kickoff_set(self):
        self._set_ball_position(self.kickoff_yardline)

    def free_kick_set(self):
        self._set_ball_position(self.free_kick_yardline)
            
    def touchback_set(self):
        self._set_ball_position(self.touchback_yardline)
        
    def conversion_set(self):
        self._set_ball_position(self.conversion_yardline)
        
class Play():
    def __init__(self,offense,defense,field):
        self.offense = offense
        self.defense = defense
        self.field = field
        self.play_call = None
        self.offense_yardage = 0
        self.return_yardage = 0
        self.turnover = False
        self.events = {'touchback' : False,
                       'punt_attempt' : False,
                       'punt_blocked' : False,
                       'kick_attempt' : False,
                       'kick_successful' : False,
                       'safety' : False,
                       'offense_touchdown' : False,
                       'defense_touchdown' : False}

    def run_play(self):
        self.offense_yardage, self.turnover,self.return_yardage = self.play_call.run(self.offense.team.skills,
                                                 self.defense.team.skills,
                                                 self.determine_play_rating_penalty())
        self.field.determine_position(self.offense_yardage * self.offense.direction)
        returnable = self.check_for_events()
        if returnable:
            self.field.determine_position(self.return_yardage * self.defense.direction)
     
    def check_for_events(self):
        returnable = self.turnover or isinstance(self.play_call,(Punt,Kickoff))
        in_home_endzone = False
        in_away_endzone = False
        if self.field.absolute_yardline >= self.field.away_endzone:
            in_away_endzone = True
        if self.field.absolute_yardline <= self.field.home_endzone:
            in_home_endzone = True
            
        if in_home_endzone:
            returnable = False
            if self.offense.home_team:
                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
                    self.events['away_touchdown'] = True
                else:
                    self.events['safety'] = True
            else:
                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
                    self.events['touchback'] = True
                elif isinstance(self.play_call,(FieldGoal)):
                    self.events['kick_successful'] = True
                else:
                    self.events['away_touchdown'] = True
        elif in_away_endzone:
            returnable = False
            if not self.offense.home_team:
                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
                    self.events['home_touchdown'] = True
                else:
                    self.events['safety'] = True
            else:
                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
                    self.events['touchback'] = True
                elif isinstance(self.play_call,(FieldGoal)):
                    self.events['kick_successful'] = True
                else:
                    self.events['home_touchdown'] = True
                    
        if isinstance(self.play_call,Punt):
            self.events['punt_attempt'] = True
        if isinstance(self.play_call,FieldGoal):
            self.events['kick_attempt'] = True    
            
        return returnable
    
    def determine_play_rating_penalty(self):
        self.offense.plays_run[self.play_call.id] += 1.0
            
        current_play_ctr = self.offense.plays_run[self.play_call.id]
        total_play_ctr = sum(self.offense.plays_run.values())
    
        play_freq_pct = (current_play_ctr / total_play_ctr)
        if total_play_ctr > 15 and play_freq_pct > .33:
            penalty = ceil((play_freq_pct) * (current_play_ctr * 2.5))
        else:
            penalty = 0
        
        if not self.offense.home_team:
            penalty += self.defense.team.home_field_advantage

        return penalty       

class Scoreboard():
    def __init__(self, touchdown_pts=6, field_goal_pts=3, safety_pts=2, conversion_play_pts=2, conversion_kick_pts=1):
        self.absolute_yardline = '30'
        self.converted_yardline = '30'
        self.play_name = 'None'
        self.play_rating = '0'
        self.offense_yardage ='0'
        self.return_yardage = '0'
        self.turnover = 'False'
        self.down = '1'
        self.yards_to_go = '10'
        self.clock = '15:00'
        self.period = '1'
        
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