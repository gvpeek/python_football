'''
Created on Mar 1, 2012

@author: peekgv
'''

from random import randint
from math import ceil, floor

#===============================================================================
# 
# To be removed to team.py
class Team():
    "Team"
    def __init__(self, city, nickname):
#        self.id = get_next_team_id()
        self.city = city
        self.nickname = nickname
        self.rating_qb = float(randint(60,90))
        self.rating_rb = float(randint(60,90))
        self.rating_wr = float(randint(60,90))
        self.rating_ol = float(randint(60,90))
        self.rating_dl = float(randint(60,90))
        self.rating_lb = float(randint(60,90))
        self.rating_cb = float(randint(60,90))
        self.rating_s = float(randint(60,90))
        self.rating_sp = float(randint(60,90))
        
        self.away_penalty = float(randint(1,3))


#===============================================================================

class Play(object):
    def __init__(self,offense,defense):
        self.offense = offense
        self.defense = defense
        self.play_rating = 0
        self.play_success = None
        self.offense_yardage = 0
        self.returnable = False
        self.returner_rating = None
        self.return_yardage = 0
        self.turnover = False
        self.change_of_posession = False
        self.onside_recover = False

    def determine_off_rating(self,qb_factor,rb_factor,wr_factor,ol_factor):
        if qb_factor + rb_factor + wr_factor + ol_factor == 10:
            return ceil(((self.offense.rating_qb*qb_factor + self.offense.rating_rb*rb_factor + self.offense.rating_wr*wr_factor + self.offense.rating_ol*ol_factor) / 10))                
        else:
            print 'Offense rating factors do not equal 10'
            raise Exception
        
    def determine_def_rating(self,dl_factor,lb_factor,cb_factor,s_factor):
        if dl_factor + lb_factor + cb_factor + s_factor == 10:
            return ceil((((self.defense.rating_dl*dl_factor + self.defense.rating_lb*lb_factor + self.defense.rating_cb*cb_factor + self.defense.rating_s*s_factor) / 10) - 60) / 4)
        else:
            print 'Defense rating factors do not equal 10'
            raise Exception

    def determine_turnover(self,adjustment):
        turnover_rnd = randint(1,100)
        if turnover_rnd <= ((100 - self.play_rating) / adjustment):
            self.turnover = True
            self.change_of_possession = True
            print 'turn:', self.turnover        
#    def determine_return_yardage(self):
    
    def determine_play_yardage(self,gain_adjustment,loss_adjustment):
        yardage_rnd = randint(1,100)
        loss_rating = ((90 - self.play_rating) + 60)
        if self.play_success or self.turnover:
            self.offense_yardage = floor(((self.play_rating*100)*pow(yardage_rnd,gain_adjustment)) / 100)
        else:
            self.offense_yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,loss_adjustment)) / 100))
            if self.offense_yardage < -5:
                self.offense_yardage= -5

    def run_clock(self):
        self.offense_yardage = -2

    def kickoff(self):
        self.play_rating = (self.offense.rating_sp - ceil((self.defense.rating_sp - 60) / 4)) - self.offense.away_penalty
        if self.play_rating < 60:
            self.play_rating = 60
        kick_rnd = randint(1,20) + 55
        kick_adjustment = (80 - self.play_rating) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)
        
#        return_yards = floor(((return_team.rating_sp*125)*pow(return_rnd,-.4)) / 100)

    def onside_kickoff(self, offense, defense, rating_adjustment=0):
        self.play_rating = offense.rating_special_teams_off - rating_adjustment
        if self.play_rating < 60:
            self.play_rating = 60
        kick_rnd = randint(1,10) + 10
        kick_adjustment = (80 - self.play_rating ) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)
        
        if self.offense_yardage >= 10:
            onside_recover_random = randint(1,100)
            onside_recover_rating = ceil(offense.rating_special_teams_off / 4)
            if onside_recover_random <= onside_recover_rating:
                print 'Offense Recovers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                self.onside_recover = True
                
#        return_yards = floor(((return_team.rating_sp*100)*pow(return_rnd,-1)) / 100)

    def run_inside(self):
        self.play_rating = self.determine_off_rating(1,4,0,5) - self.determine_def_rating(6,3,0,1) - self.offense.away_penalty
        play_rnd = randint(1,100)
        if play_rnd <= self.play_rating:
            self.play_success=True
        else:
            self.play_success=False
            self.determine_turnover(3.5)
        
        self.determine_play_yardage(-.7,-1)
        print self.play_success

#===============================================================================
#
## test execution 
team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
print team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
print team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp
for a in range(9):
    print ' '
    p1 = Play(team1,team2)
    p1.run_clock()
    print p1.offense_yardage
    p2 = Play(team1,team2)
    p2.kickoff()
    print p2.offense_yardage
    p3 = Play(team1,team2)
    p3.run_inside()
    print p3.offense_yardage    
#===============================================================================




