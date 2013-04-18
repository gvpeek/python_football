'''
Created on Mar 1, 2012

@author: George Peek
'''

from math import ceil
from random import choice
from datetime import timedelta
from collections import deque, namedtuple, defaultdict
from pprint import pprint

from playbook import Kickoff, Punt, FieldGoal
from state_machine import initialize_state
from stats import StatBook

class Game():
    "Game"
    def __init__(self, home_team, away_team, league_game=False, division_game=False, conference_game=False, playoff_game=False, number_of_periods=4):
#        self.game_id = get_next_game_id()
        self.home = home_team
        self.away = away_team
#        self.league_game = league_game
#        self.division_game = division_game
#        self.conference_game = conference_game 
        self.playoff_game = playoff_game  
        self.number_of_periods = number_of_periods
        self.period = 1
        self.field = Field(self.get_offense)
        self.scoreboard = Scoreboard()
        self.plays = []
        self.coin_flip_winner = self._coin_flip()
        self._Possession = namedtuple('Possession', ['offense','defense'])
        self.possession = self._possession_setup()
        self.current_state = initialize_state(self.field,
                                   self.change_possession,
                                   self.get_offense)
        self.timekeeping = deque().extend([Clock() for x in range(number_of_periods)])
        self.current_clock = self.timekeeping.pop()
        self.end_of_half = False
        self.end_of_regulation = False
        self.overtime = False
        self.end_of_game = False
        
    def _possession_setup(self):
        PossTeam = namedtuple('PossTeam', ['team','direction','endzone','home_team','plays_run','statbook'])
        
        t1 = PossTeam(self.home,1,0,True,defaultdict(int),StatBook())
        t2 = PossTeam(self.away,-1,100,False,defaultdict(int),StatBook())
        
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

    def get_defense(self):
        return self.possession.defense
    
    def get_home_team(self):
        if self.possession.offense.home_team:
            return self.possession.offense
        else:
            return self.possession.defense

    def get_away_team(self):
        if not self.possession.offense.home_team:
            return self.possession.offense
        else:
            return self.possession.defense
            
    def run_play(self,play_call):
        play = Play(self.possession.offense,
                         self.possession.defense,
                         self.field)
        play.play_call = play_call
        play.run_play()
        self.determine_events(play)
        self.plays.append(play)
        if self.current_state.timed_play():
            self.current_clock.run_clock()
        self.current_state = self.current_state.check_state(play.turnover,
                                                            play.events)
        print ''
        print '*' * 20
        pprint(vars(self.field))
        pprint(vars(play))
        
    def determine_events(self,play):
        if play.play_call.is_field_goal():
            play.events['kick_attempt'] = True
            print 'ayl', (100-abs(self.field.absolute_yardline - self.possession.offense.endzone)), 'k', play.offense_yardage
            if (100 - abs(self.field.absolute_yardline - self.possession.offense.endzone)) <= play.offense_yardage:
                play.events['kick_successful'] = True
                if self.current_state.is_conversion():
                    self.scoreboard.conversion_kick(self.possession.offense.statbook)
                elif self.current_state.is_drive():
                    self.scoreboard.field_goal(self.possession.offense.statbook)
            else:
                play.turnover = True
        else:
            self.field.determine_position(play.offense_yardage * self.possession.offense.direction)
            if not self.field.in_endzone() and play.turnover:
                play.return_yardage = play.play_call.determine_return_yardage(self.possession.defense.team.skills, play.offense_yardage)
                self.field.determine_position(play.return_yardage * self.possession.defense.direction)
            in_endzone = self.field.in_endzone()
            if in_endzone:
                if not in_endzone == self.possession.offense.direction:
                    if self.current_state.is_conversion():
                        self.scoreboard.conversion_play(self.possession.offense.statbook)
                    elif play.turnover:
                        play.events['touchback'] = True
                    else:
                        play.events['offense_touchdown'] = True
                        self.scoreboard.touchdown(self.possession.offense.statbook)
                else:
                    if play.turnover:
                        play.events['defense_touchdown'] = True
                        self.scoreboard.touchdown(self.possession.defense.statbook)
                    else:
                        play.events['safety'] = True
                        self.scoreboard.safety(self.possession.defense.statbook)
                    
#        if in_home_endzone:
#            returnable = False
#            if self.offense.home_team:
#                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
#                    self.events['away_score'] = True
#                else:
#                    self.events['safety'] = True
#            else:
#                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
#                    self.events['touchback'] = True
#                elif isinstance(self.play_call,(FieldGoal)):
#                    self.events['kick_successful'] = True
#                else:
#                    self.events['away_score'] = True
#        elif in_away_endzone:
#            returnable = False
#            if not self.offense.home_team:
#                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
#                    self.events['home_score'] = True
#                else:
#                    self.events['safety'] = True
#            else:
#                if self.turnover or isinstance(self.play_call,(Punt,Kickoff)):
#                    self.events['touchback'] = True
#                elif isinstance(self.play_call,(FieldGoal)):
#                    self.events['kick_successful'] = True
#                else:
#                    self.events['home_score'] = True
#                    
#        if isinstance(self.play_call,Punt):
#            self.events['punt_attempt'] = True
#        if isinstance(self.play_call,FieldGoal):
#            self.events['kick_attempt'] = True 
                        
                

class Field():
    "Playing Field"
    def __init__(self, 
                 get_offense,
                 length=100.0,
                 kickoff_yardline=30.0,
                 free_kick_yardline=20.0,
                 conversion_yardline=98.0,
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
            
        return self.absolute_yardline

    def in_endzone(self):
        in_endzone = 0
        if self.absolute_yardline >= self.away_endzone:
            in_endzone = -1
        elif self.absolute_yardline <= self.home_endzone:
            in_endzone = 1
            
        return in_endzone

    def _set_ball_position(self,yardline):
        self.absolute_yardline = abs(self.get_offense().endzone - yardline)
        if self.absolute_yardline > self.length / 2:
            self.converted_yardline = abs(self.length - self.absolute_yardline)
        else:
            self.converted_yardline = self.absolute_yardline
                
    def kickoff_set(self):
        self._set_ball_position(self.kickoff_yardline)

    def free_kick_set(self):
        self._set_ball_position(self.free_kick_yardline)
            
    def touchback_set(self):
        self._set_ball_position(self.touchback_yardline)
        
    def conversion_set(self):
        self._set_ball_position(self.conversion_yardline)
        
    def failed_field_goal_set(self):
        self._set_ball_position(self.absolute_yardline + self.get_offense().direction * 7)
        
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
                       'punt' : False,
                       'kick_attempt' : False,
                       'kick_successful' : False,
                       'safety' : False,
                       'offense_touchdown' : False,
                       'defense_touchdown' : False} 

    def run_play(self):
        self.offense_yardage, self.turnover = self.play_call.run(self.offense.team.skills,
                                                 self.defense.team.skills,
                                                 self.determine_play_rating_penalty())
     
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
        
    def touchdown(self,statbook):
        statbook.offense_stats['score'] += self.touchdown_pts
        
    def field_goal(self,statbook):
        statbook.offense_stats['score'] += self.field_goal_pts

    def safety(self,statbook):
        statbook.offense_stats['score'] += self.safety_pts

    def conversion_play(self,statbook):
        statbook.offense_stats['score'] += self.conversion_play_pts

    def conversion_kick(self,statbook):
        statbook.offense_stats['score'] += self.conversion_kick_pts
        
class Clock(object):
    "Basic Clock"
    def __init__(self, quarter_length=15):
        self.time_remaining = timedelta(seconds=(quarter_length*60))

    def time_remaining(self):
        return self.time_remaining

    def run_clock(self):
        self.time_remaining -= timedelta(seconds=30)
    
        return self.time_remaining
#===============================================================================