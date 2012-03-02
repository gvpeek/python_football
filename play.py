'''
Created on Mar 1, 2012

@author: peekgv
'''

from random import randint
from math import ceil

class Play(object):
    def __init__(self):
        self.offense_yardage = 0
        self.returnable = False
        self.returner_rating = None
        self.return_yardage = 0
        self.change_of_posession = False
        self.onside_recover = False
        
    def determine_return_yardage(self):
    
    def run_clock(self, offense_rating, defense_rating, rating_adjustment=0):
        self.offense_yardage = -2

    def kickoff(self, offense, defense, rating_adjustment=0):
        play_rating = offense.rating_special_teams_off - rating_adjustment
        if play_rating < 60:
            play_rating = 60
        kick_rnd = randint(1,20) + 55
        kick_adjustment = (80 - play_rating) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)
        
         return_yards = floor(((return_team.rating_sp*125)*pow(return_rnd,-.4)) / 100)
        print self.offense_yardage 

    def onside_kickoff(self, offense, defense, rating_adjustment=0):
        play_rating = offense.rating_special_teams_off - rating_adjustment
        if play_rating < 60:
            play_rating = 60
        kick_rnd = randint(1,10) + 10
        kick_adjustment = (80 - play_rating ) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)
        
        if self.offense_yardage >= 10:
            onside_recover_random = randint(1,100)
            onside_recover_rating = ceil(offense.rating_special_teams_off / 4)
            if onside_recover_random <= onside_recover_rating:
                print 'Offense Recovers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                self.onside_recover = True
                
        return_yards = floor(((return_team.rating_sp*100)*pow(return_rnd,-1)) / 100)
