'''
Created on Jun 29, 2013

@author: George Peek
'''

from sqlalchemy import create_engine, Column, Integer, String, Boolean, PickleType, Float, ForeignKey
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
#    stats = Column(Integer)
    coach_id = Column(Integer, ForeignKey('coaches.id'))
#@TODO    coach = relationship("Coach", uselist=False, backref="parent")
#    declination_rate = Column(Integer)
    
    def __init__(self, team):
        self.city = team.city
        self.nickname = team.nickname
        self.human_control = team.human_control
        self.skills = team.skills
        self.home_field_advantage = team.home_field_advantage
#        self.playbook = Playbook()
#        self.stats = StatBook()
        self.coach = team.coach
#        
#        self.primary_color = (randint(0,255),randint(0,255),randint(0,255))
#        self.secondary_color = (randint(0,255),randint(0,255),randint(0,255))
        
class DBCoach():
    __tablename__ = 'coaches'
    
    id = Column(Integer, primary_key=True)
    skill = Column(Integer)
    play_probabilities = Column(PickleType)
    fg_dist_probabilities= Column(PickleType)
    team = Column(Integer, ForeignKey('teams.id'))
    
    def __init__(self, coach):
        self.skill = coach.skill
        self.play_probabilities = coach.play_probabilities 
        self.fg_dist_probabilities = coach.fg_dist_probabilities
        
class DBStatBook():
    __tablename__ = 'stats'
    
    id = Column(Integer, primary_key=True)
    total_yards = Column(Float)
    pass_att = Column(Float)
    pass_comp = Column(Float)
    completion_pct = Column(Float)
    pass_yards = Column(Float)
    pass_td = Column(Float)
    intercepted = Column(Float)
    sacked = Column(Float)
    rush_att = Column(Float)
    rush_yards = Column(Float)
    rush_td = Column(Float)
    fumbles = Column(Float)
    fg_att = Column(Float)
    fg = Column(Float)
    xp_att = Column(Float)
    xp = Column(Float)
    conv_att = Column(Float)
    conv = Column(Float)
    punts = Column(Float)
    punt_yards = Column(Float)
    punt_returns = Column(Float)
    punt_return_yards = Column(Float)
    kickoffs = Column(Float)
    kickoff_yards = Column(Float)
    kickoff_touchbacks = Column(Float)
    kick_returns = Column(Float)
    kick_return_yards = Column(Float)
    safeties = Column(Float)
    
    def __init__(self, stats):
        pass
#        self.stats = {'score
#                      'total_yards
#                      'pass_att
#                      'pass_comp
#                      'completion_pct
#                      'pass_yards
#                      'pass_td
#                      'intercepted
#                      'sacked
#                      'rush_att
#                      'rush_yards
#                      'rush_td
#                      'fumbles
#                      'fg_att
#                      'fg
#                      'xp_att
#                      'xp
#                      'conv_att
#                      'conv
#                      'punts
#                      'punt_yards
#                      'punt_returns
#                      'punt_return_yards': 0.0,
#                      'kickoffs
#                      'kickoff_yards
#                      'kickoff_touchbacks
#                      'kick_returns
#                      'kick_return_yards': 0.0,
#                      'safeties': 0.0
#                   