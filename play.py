'''
Created on Mar 1, 2012

@author: peekgv
'''

from random import randint
from math import ceil, floor
import pprint

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
        
        self.home_field_advantage = float(randint(1,3))


#===============================================================================

#===============================================================================
# 
# To be removed to game.py
class Field():
    "Playing Field"
    def __init__(self):
        self.direction = 1 ## 1=home, -1=away
        self.absolute_yardline = 30
        self.converted_yardline = 30
        self.down = 1
        self.yards_to_gain = 10
        self.target_yardline = 30
        self.in_home_endzone = False
        self.in_away_endzone = False
#===============================================================================

class Play(object):
    def __init__(self,offense,defense,field):
        self.offense = offense
        self.defense = defense
        self.play_rating = 0
        self.play_success = None
        self.offense_yardage = 0
        self.returnable = False
        self.return_yardage = 0
        self.turnover = False
        self.change_of_possession = False
        self.touchback = False
        self.onside_recover = False
        self.field = field
        self.field.in_home_endzone = False
        self.field.in_away_endzone = False
        

    def determine_off_rating(self,qb_factor,rb_factor,wr_factor,ol_factor):
        if qb_factor + rb_factor + wr_factor + ol_factor == 10:
            rating = ceil(((self.offense.rating_qb*qb_factor + self.offense.rating_rb*rb_factor + self.offense.rating_wr*wr_factor + self.offense.rating_ol*ol_factor) / 10))
            rating -= self.defense.home_field_advantage
            return rating           
        else:
            print 'Offense rating factors do not equal 10'
            raise Exception
        
    def determine_def_rating(self,dl_factor,lb_factor,cb_factor,s_factor):
        if dl_factor + lb_factor + cb_factor + s_factor == 10:
            return ceil((((self.defense.rating_dl*dl_factor + self.defense.rating_lb*lb_factor + self.defense.rating_cb*cb_factor + self.defense.rating_s*s_factor) / 10) - 60) / 4)
        else:
            print 'Defense rating factors do not equal 10'
            raise Exception

    def determine_play_success(self):
        self.play_success=False 
        play_rnd = randint(1,100)
        if play_rnd <= self.play_rating:
            self.play_success=True

    def determine_turnover(self,adjustment):
        turnover_rnd = randint(1,100)
        if turnover_rnd <= ((100 - self.play_rating) / adjustment):
            self.turnover = True
       
    def determine_return_yardage(self, returner_rating, adjustment):
        return_rnd = randint(1,100)
        self.return_yardage = floor(((returner_rating*100)*pow(return_rnd,adjustment)) / 100)
    
    def determine_play_yardage(self,gain_adjustment,loss_adjustment):
        yardage_rnd = randint(1,100)
        loss_rating = ((90 - self.play_rating) + 60)
        if self.play_success or self.turnover:
            self.offense_yardage = floor(((self.play_rating*100)*pow(yardage_rnd,gain_adjustment)) / 100)
        else:
            self.offense_yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,loss_adjustment)) / 100))

    def determine_position(self, yardage):
        if self.change_of_possession:
            self.field.direction = self.field.direction * -1

        self.field.absolute_yardline += (yardage * self.field.direction)

        if self.field.absolute_yardline > 50:
            self.field.converted_yardline = 100 - self.field.absolute_yardline
            if self.field.absolute_yardline >= 100:
                self.field.in_away_endzone = True
        else:
            self.field.converted_yardline = self.field.absolute_yardline
            if self.field.absolute_yardline <= 0:
                self.field.in_home_endzone = True

    def determine_kickoff_result(self, random_cap, adjustment):
        self.play_rating = self.offense.rating_sp - self.defense.home_field_advantage
        if self.play_rating < 60:
            self.play_rating = 60
        kick_rnd = randint(1,random_cap) + adjustment
        kick_adjustment = (80 - self.play_rating) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)        

#------------------------------------------------------------------------------ 
# ***** plays

    def run_clock(self):
        self.offense_yardage = -2
        self.determine_position(self.offense_yardage)

    def kickoff(self):
        self.determine_kickoff_result(20,55)
        self.determine_position(self.offense_yardage)
        self.change_of_possession = True 
        if not self.field.in_home_endzone and not self.field.in_away_endzone: 
            self.determine_return_yardage((self.defense.rating_sp * 1.25), -.4)
            self.determine_position(self.return_yardage)
        else:
            self.touchback = True     

    def onside_kickoff(self):
        self.determine_kickoff_result(10,10)
        self.determine_position(self.offense_yardage)
        
        if self.offense_yardage >= 10:
            onside_recover_random = randint(1,100)
            onside_recover_rating = ceil(self.offense.rating_sp / 4)
            if onside_recover_random <= onside_recover_rating:
                print 'Offense Recovers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                self.onside_recover = True
            else:
                self.change_of_possession = True 
                if not self.field.in_home_endzone or not self.field.in_away_endzone: 
                    self.determine_return_yardage(self.defense.rating_sp, -1)
                    self.determine_position(self.return_yardage)
        else:
            self.change_of_possession = True 

    def run_inside(self):
        self.play_rating = self.determine_off_rating(1,4,0,5) - self.determine_def_rating(6,3,0,1)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(3.5)
        
        self.determine_play_yardage(-.7,-1)
        if self.offense_yardage < -5:
            self.offense_yardage= -5
        self.determine_position(self.offense_yardage)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_dl,-1)
            self.determine_position(self.return_yardage)

    def run_outside(self):
        self.play_rating = self.determine_off_rating(1,5,1,3) - self.determine_def_rating(3,5,1,1)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(3.5)
        
        self.determine_play_yardage(-.7,-1)
        if self.offense_yardage < -5:
            self.offense_yardage= -5
        self.determine_position(self.offense_yardage)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_lb,-1)
            self.determine_position(self.return_yardage)

#===============================================================================
#
## test execution 
team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
#print team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
#print team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp
pprint.pprint(vars(team1)) 
print ' '
pprint.pprint(vars(team2)) 

for a in range(9):
    print ' '
    f = Field()
    p1 = Play(team1,team2,f)
    p1.run_clock()
    f = Field()
    p2 = Play(team1,team2,f)
    p2.kickoff()
#    pprint.pprint(vars(p2))
#    pprint.pprint(vars(p2.field))
    f = Field()
    p21 = Play(team1,team2,f)
    p21.onside_kickoff()
    pprint.pprint(vars(p21))
    pprint.pprint(vars(p21.field))
    f = Field()    
    p3 = Play(team1,team2,f)
    p3.run_inside()
#    pprint.pprint(vars(p3))
    f = Field()
    p4 = Play(team1,team2,f)
    p4.run_outside()
#    pprint.pprint(vars(p4)) 
#===============================================================================




