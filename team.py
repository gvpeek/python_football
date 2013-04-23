'''
Created on Mar 30, 2013

@author: George
'''
from random import randint

from playbook import Playbook
from stats import StatBook
from coach import Coach

class Team():
    "Team"
    def __init__(self, city, nickname):
#        self.id = get_next_team_id()
        self.city = city
        self.nickname = nickname
        self.human_control = False
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
        self.stats = StatBook()
        self.coach = Coach()
        self.coach.practice_plays(self.playbook,self.skills)
        
        self.primary_color = (randint(0,255),randint(0,255),randint(0,255))
        self.secondary_color = (randint(0,255),randint(0,255),randint(0,255))