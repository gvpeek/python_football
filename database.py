'''
Created on Jun 29, 2013

@author: George Peek
'''

from sqlalchemy import create_engine, Column, Integer, String, Boolean, PickleType, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Database():
    def __init__(self, table):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        self.record_class = self._get_record_class(table)
        
        Base.metadata.create_all(self.engine)
        
    def _get_record_class(self,table):
        classes = {'players': DBPlayer }
#                   'teams' : DBTeam,
#                   'stats' : DBStatbook,
        return classes[table]

class DBPlayer(Base):
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
#        self.id = player.id              
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
        return "<Player('%s','%s','%s','%s','%s','%s','%s')>" % (self.id, 
                                                                 self.first_name, 
                                                                 self.last_name, 
                                                                 self.age, 
                                                                 self.position, 
                                                                 self.ratings, 
                                                                 self.retired)
class DBTeam(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    city  = Column(String)
    nickname = Column(String)
    human_control = Column(Boolean)
    skills = Column(PickleType)
    home_field_advantage = Column(Float)
#    playbook = Column(Boolean)
#    apex_age = Column(Integer)
#    growth_rate = Column(Integer)
#    declination_rate = Column(Integer)
    
    def __init__(self, team):
        self.city = team.city
        self.nickname = team.nickname
        self.human_control = team.human_control
        self.skills = team.skills
        self.home_field_advantage = team.home_field_advantage
#        self.playbook = Playbook()
#        self.stats = StatBook()
#        self.coach = Coach()
#        self.coach.practice_plays(self.playbook,self.skills)
#        
#        self.primary_color = (randint(0,255),randint(0,255),randint(0,255))
#        self.secondary_color = (randint(0,255),randint(0,255),randint(0,255))
        
class DBCoach():
    __tablename__ = 'coaches'
    
    id = Column(Integer, primary_key=True)
    skill = Column(Integer)
    play_probabilities = Column(PickleType)
    fg_dist_probabilities= Column(PickleType)
    
    def __init__(self, coach):
        self.skill = coach.skill
        self.play_probabilities = coach.play_probabilities 
        self.fg_dist_probabilities = coach.fg_dist_probabilities
                   