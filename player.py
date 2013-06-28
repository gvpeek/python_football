'''
Created on May 27, 2013

@author: George
'''
from math import pow, floor
from random import randint, choice

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import names

Base = declarative_base()

class DBPLayer(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first_name  = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    position = Column(String)
    constitution = Column(Integer)
    retired = Column(Boolean)
    apex_age = Column(Integer)
    growth_rate = Column(Integer)
    declination_rate = Column(Integer)
    ratings = Column(Integer) # need to convert to dict

    def __init__(self, player):
        self.id = player.id              
        self.first_name = player.first_name      
        self.last_name = player.last_name       
        self.age = player.age             
        self.position = player.position        
        self.constitution = player.constitution    
        self.retired = player.retired         
        self.apex_age = player.apex_age        
        self.growth_rate = player.growth_rate     
        self.declination_rate = player.declination_rate
        self.ratings = player.ratings['rating']         

    def __repr__(self):
        return "<Player('%s','%s','%s','%s', '%s')>" % (self.first_name, self.last_name, self.age, self.position, self.ratings)

class PlayerDatabase():
    def __init__(self,base):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.record = DBPLayer
        
        base.metadata.create_all(self.engine)



#position_types = ['QB']*3+['RB']*5+['WR']*5+['TE']*3+['OG']*4+['OT']*4+['C']*3+['DT']*4+['DE']*4+['LB']*6+['S']*4+['CB']*6+['K']+['P']
position_types = ['QB']+['RB']+['WR']+['OL']+['DL']+['LB']+['S']+['CB']+['K']+['P']+['SP']

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
#        self.retirement_age = (self.constitution - self.age) + 10
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
        self.db = PlayerDatabase(Base)
        self.new_annual_players = new_annual_players
        self.min_max_ratings = [(14,(20,50)), # (age, (min,max))
                                (18,(30,60)),
                                (22,(45,75)),
                                (99,(60,90))] 
        self.players = self._create_players(self.new_annual_players)

    def _create_players(self,number):
        new_players = [Player() for x in xrange(number)]
        
        db_players =[self.db.record(player) for player in new_players]
        session = self.db.Session()
        session.add_all(db_players)
        session.commit()
        
        return new_players
    
    def _age_players(self,years=1):
        for y in xrange(years):
            for player in self.players:
#                if not player.retired and player.age >= player.retirement_age:
#                    player.retired = True
                if not player.retired:
                    player.age += 1
                    if player.age <= player.apex_age:
                        player.ratings['rating'] += randint(1,player.growth_rate)
                    else:
                        player.ratings['rating'] -= randint(3,player.declination_rate)
                    for age,ratings in self.min_max_ratings:
                        if player.age <= age:
                            self._check_rating_range(player, ratings)
                            break
                            
    def _check_rating_range(self,player,range):
        if player.ratings['rating'] < min(range):
            player.retired = True
        elif player.ratings['rating'] > max(range):
            player.ratings['rating'] = max(range)
        
    
    def advance_year(self):
        self._age_players()
        self.players.extend(self._create_players(self.new_annual_players))



        
        
    

##### testing

pm=PlayerManagement(new_annual_players=75)
#for player in pm.players:
#    print player.first_name, \
#          player.last_name, \
#          player.age, \
#          player.position, \
#          player.ratings['rating']
#for zz in xrange(30):
#    pm.advance_year()
#    list=0
#    print
#    pm.players.sort(reverse=True, key=lambda t: t.ratings['rating'])
#    for player in pm.players:
#        if not player.retired and list < 10: # would be more efficient as a generator
#            list += 1
#            print player.first_name, \
#                  player.last_name, \
#                  player.age, \
#                  player.position, \
#                  player.ratings['rating']