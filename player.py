'''
Created on May 27, 2013

@author: George
'''
from math import pow, floor

from random import randint, choice

import names

position_types = ['QB']*3+['RB']*5+['WR']*5+['TE']*3+['OG']*4+['OT']*4+['C']*3+['DT']*4+['DE']*4+['LB']*6+['S']*4+['CB']*6+['K']+['P']

player_id = 0
global player_id

class Player():
    def __init__(self,id=None):
        if id:
            self.id = id
        else:
            self.id = self.get_next_player_id() 
        self.first_name = names.first_name()
        self.last_name = names.last_name()
        self.age = 11
        self.position = choice(position_types)
        
        self.constitution = randint(20,45)
        self.retirement_age = (self.constitution - self.age) + 10
        self.retired = False
        self.apex_age = (floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18)
        self.growth_rate = randint(1,4)
        self.declination_rate = randint(3,5)
        
        self.ratings ={ 'rating': randint(20,45) }
        
    def get_next_player_id(self):
        global player_id
        player_id += 1
        return player_id 
    
class PlayerManagement():
    def __init__(self,new_annual_players=33):
        self.new_annual_players = new_annual_players
        self.min_max_ratings = {18: (20,60),
                                22: (45,75),
                                99: (60,90)} 
        self.players = self._create_players(self.new_annual_players)
        

    def _create_players(self,number):
        return [Player() for x in xrange(number)]
    
    def _age_players(self,years=1):
        for y in xrange(years):
            for player in self.players:
                if not player.retired and player.age >= player.retirement_age:
                    player.retired = True
                if not player.retired:
                    player.age += 1
                    if player.age <= player.apex_age:
                        player.ratings['rating'] += randint(1,player.growth_rate)
                    else:
                        player.ratings['rating'] -= randint(3,player.declination_rate)
    
    def advance_year(self):
        self._age_players()
        self.players.extend(self._create_players(self.new_annual_players))
    
##### testing

pm=PlayerManagement()
for player in pm.players:
    print player.first_name, \
          player.last_name, \
          player.age, \
          player.position, \
          player.ratings['rating']
for zz in xrange(30):
    pm.advance_year()
    print "\n", "New Year..."
    for player in pm.players:
        print player.first_name, \
              player.last_name, \
              player.age, \
              player.position, \
              player.ratings['rating']