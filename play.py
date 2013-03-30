'''
Created on Mar 1, 2012

@author: peekgv
'''

from random import randint
from math import ceil

#===============================================================================
# 
# To be removed to team.py
from playbook import Playbook

class Team():
    "Team"
    def __init__(self, city, nickname):
#        self.id = get_next_team_id()
        self.city = city
        self.nickname = nickname
        self.skills = {'qb': float(randint(60,90)),
                       'rb': float(randint(60,90)),
                       'wr': float(randint(60,90)),
                       'ol': float(randint(60,90)),
                       'dl': float(randint(60,90)),
                       'lb': float(randint(60,90)),
                       'cb': float(randint(60,90)),
                       's': float(randint(60,90)),
                       'sp': float(randint(60,90))}
        
        self.home_field_advantage = float(randint(1,3))
        self.playbook = Playbook()
        
        self.primary_color = (randint(0,255),randint(0,255),randint(0,255))
        self.secondary_color = (randint(0,255),randint(0,255),randint(0,255))


#===============================================================================

class Play():
    def __init__(self,offense,defense,field):
        self.offense = offense
        self.defense = defense
        self.play_call = None
        self.play_rating_penalty = 0
        self.play_success = None
        self.offense_yardage = 0
        self.return_yardage = 0
        self.turnover = False
        self.change_of_possession = False
        self.touchback = False
        self.punt_attempt = False
        self.punt_blocked = False
        self.field_goal_attempt = False
        self.kick_successful = False
        self.field = field

    def run_play(self,play_call):
        self.play_call.run(self.offense.skills,
                           self.defense.skills,
                           self.determine_play_rating_penalty())
    
    def determine_play_rating_penalty(self):
        self.offense.total_plays_run += 1
        if self.play_name in self.offense.plays_run:
            self.offense.plays_run[self.play_name] += 1.0
        else:
            self.offense.plays_run[self.play_name] = 1.0
    
        play_freq_pct = (self.offense.plays_run[self.play_name] / self.offense.total_plays_run)
        if self.offense.total_plays_run > 15 and play_freq_pct > .33:
            penalty = ceil((play_freq_pct) * (self.offense.plays_run[self.play_name] * 2.5))
        else:
            penalty = 0
        
#        if game.home_team == play.defense:
        penalty += self.defense.home_field_advantage

        return penalty