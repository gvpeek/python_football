'''
Created on Mar 30, 2013

@author: George
'''
from random import randint, shuffle

from playbook import Playbook
from stats import StatBook
from coach import Coach

global team_id
team_id = 0

class Team():
    "Team"
    def __init__(self, 
                 city, 
                 nickname, 
                 skills=None, 
                 home_field_advantage=None, 
                 playbook=None,
                 stats=None,
                 coach=None,
                 primary_color=None,
                 secondary_color=None,
                 human=False,
                 id=None):
        if id:
            self.id = id
        else:
            self.id = self.get_next_team_id()
        self.city = city
        self.nickname = nickname
        self.human_control = human
        self.skills = skills if skills else {'qb': float(randint(60,90)),
                                             'rb': float(randint(60,90)),
                                             'wr': float(randint(60,90)),
                                             'ol': float(randint(60,90)),
                                             'dl': float(randint(60,90)),
                                             'lb': float(randint(60,90)),
                                             'cb': float(randint(60,90)),
                                             's': float(randint(60,90)),
                                             'p': float(randint(60,90)),
                                             'k': float(randint(60,90)),
                                             'sp': float(randint(60,90))}
        
        self.home_field_advantage = home_field_advantage if home_field_advantage else float(randint(1,3))
        self.playbook = playbook if playbook else Playbook()
        self.stats = stats if stats else StatBook()
        self.coach = coach if coach else Coach()
        self.coach.practice_plays(self.playbook,self.skills)
        
        self.primary_color = primary_color if primary_color else (randint(0,255),randint(0,255),randint(0,255))
        self.secondary_color = secondary_color if secondary_color else (randint(0,255),randint(0,255),randint(0,255))
        
        self.league_stats = {
                            'overall' : self._new_record_stats(),
                            'home' : self._new_record_stats(),
                            'away' : self._new_record_stats(),
                            'win_opp' : [],
                            'loss_opp' : []
                            }
        
    def _new_record_stats(self):
        return {'wins': 0,
                'losses' : 0,
                'ties' : 0,
                'pct' : 0.0,
                'points' : 0,
                'opp' : 0}
        
    def get_next_team_id(self):
        global team_id
        team_id += 1
        return team_id 