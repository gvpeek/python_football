'''
Created on May 27, 2013

@author: George
'''
from math import pow, floor
from random import randint, choice

import names
from database import Database

class Player():
    def __init__(self,position_types):
        self.first_name = names.first_name()
        self.last_name = names.last_name()
        self.age = 11
        self.position = choice(position_types)
        
        self.constitution = randint(20,45)
        self.retired = False
        self.apex_age = (floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18)
        self.growth_rate = randint(1,4)
        self.declination_rate = randint(3,5)
        
        self.ratings ={ 'rating': randint(20,45) }
        
class PlayerManagement():
    def __init__(self,new_annual_players=33):
        self.db = Database('players')
        self.position_types = ['QB']+['RB']+['WR']+['OL']+['DL']+['LB']+['S']+['CB']+['K']+['P']+['SP']
        self.new_annual_players = new_annual_players
        self.min_max_ratings = [(14,(20,50)), # (age, (min,max))
                                (18,(30,60)),
                                (22,(45,75)),
                                (99,(60,90))] 
        
        self._create_players(self.new_annual_players)

    def _create_players(self,number):
        new_players = [Player(self.position_types) for x in xrange(number)]
        
        db_players =[self.db.record_class(player) for player in new_players]
        session = self.db.Session()
        session.add_all(db_players)
        session.commit()
        session.close()
        
        return new_players
    
    def _age_players(self,years=1):
        session = self.db.Session()
        
        for y in xrange(years):
            for player in session.query(self.db.record_class).filter_by(retired=False):
                player.age += 1
                if player.age <= player.apex_age:
                    player.ratings += randint(1,player.growth_rate)
                else:
                    player.ratings -= randint(3,player.declination_rate)
                for age,ratings in self.min_max_ratings:
                    if player.age <= age:
                        self._check_rating_range(player, ratings)
                        break
                session.commit()
        session.close()
                            
    def _check_rating_range(self,player,range):
        if player.ratings < min(range):
            player.retired = True
        elif player.ratings > max(range):
            player.ratings = max(range)
        
    
    def advance_year(self):
        self._age_players()
        self._create_players(self.new_annual_players)



        
        
    

##### testing

pm=PlayerManagement(new_annual_players=75)
for zz in xrange(10):
    print 'year',(zz+1)
    pm.advance_year()

session=pm.db.Session()
for player in session.query(pm.db.record_class).filter_by(retired=False).order_by(pm.db.record_class.ratings):
    print player