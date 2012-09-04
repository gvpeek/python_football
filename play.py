'''
Created on Mar 1, 2012

@author: peekgv
'''

from random import randint, choice
from math import ceil, floor
import inspect

## for testing
import pprint
## for testing

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
        self.total_plays_run = 0
        self.plays_run = {}
        
        self.primary_color = (randint(0,255),randint(0,255),randint(0,255))
        self.secondary_color = (randint(0,255),randint(0,255),randint(0,255))


#===============================================================================

class Play(object):
    def __init__(self,offense,defense,field):
        self.offense = offense
        self.defense = defense
        self.play_name = None
        self.play_rating = 0
        self.play_success = None
        self.offense_yardage = 0
        self.return_yardage = 0
        self.turnover = False
        self.change_of_possession = False
        self.touchback = False
        self.punt_blocked = False
        self.kick_successful = False
        self.field = field

    def determine_play_rating(self,qb_factor,rb_factor,wr_factor,ol_factor,dl_factor,lb_factor,cb_factor,s_factor):
        rating_penalty = self.determine_play_rating_penalty()
        if qb_factor + rb_factor + wr_factor + ol_factor == 10:
            off_rating = ceil(((self.offense.rating_qb*qb_factor + self.offense.rating_rb*rb_factor + self.offense.rating_wr*wr_factor + self.offense.rating_ol*ol_factor) / 10))
            off_rating -= rating_penalty
        else:
            print 'Offense rating factors do not equal 10'
            raise Exception
        if dl_factor + lb_factor + cb_factor + s_factor == 10:
            def_rating = ceil((((self.defense.rating_dl*dl_factor + self.defense.rating_lb*lb_factor + self.defense.rating_cb*cb_factor + self.defense.rating_s*s_factor) / 10) - 60) / 4)
        else:
            print 'Defense rating factors do not equal 10'
            raise Exception
        self.play_rating = off_rating - def_rating
        if self.play_rating < 35.0:
            self.play_rating = 35.0
        elif self.play_rating > 90.0:
            self.play_rating = 90.0

    def determine_play_rating_penalty(self):
        self.offense.total_plays_run += 1
        if self.play_name in self.offense.plays_run:
            self.offense.plays_run[self.play_name] += 1.0
        else:
            self.offense.plays_run[self.play_name] = 1.0
    
        play_freq_pct = (self.offense.plays_run[self.play_name] / self.offense.total_plays_run)
        if self.offense.total_plays_run > 15 and play_freq_pct > .33:
            penalty = ceil((play_freq_pct) * (self.offense.plays_run[self.play_name] * 2.5))
        else:
            penalty = 0
        
#        if game.home_team == play.defense:
        penalty += self.defense.home_field_advantage

        return penalty

    def determine_play_success(self):
        self.play_success=False 
        play_rnd = randint(1,100)
        if play_rnd <= self.play_rating:
            self.play_success=True

    def determine_turnover(self,adjustment,multiplier):
        turnover_rnd = randint(1,100)
        if turnover_rnd <= (((100 - self.play_rating) / adjustment) * multiplier):
            self.turnover = True
       
    def determine_return_yardage(self, returner_rating, adjustment):
        return_rnd = randint(1,100)
        self.return_yardage = floor(((returner_rating*100)*pow(return_rnd,adjustment)) / 100)
    
    def determine_play_yardage(self,gain_adjustment,loss_adjustment,max_loss):
        yardage_rnd = randint(1,100)
        loss_rating = ((90 - self.play_rating) + 60)
        if self.play_success or self.turnover:
            self.offense_yardage = floor(((self.play_rating*100)*pow(yardage_rnd,gain_adjustment)) / 100)
        else:
            self.offense_yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,loss_adjustment)) / 100))
        if self.offense_yardage < max_loss:
            self.offense_yardage= max_loss

    def determine_kickoff_result(self, random_cap, adjustment):
        self.play_rating = self.offense.rating_sp - self.defense.home_field_advantage
        if self.play_rating < 60:
            self.play_rating = 60
        kick_rnd = randint(1,random_cap) + adjustment
        kick_adjustment = (80 - self.play_rating) / 2
        self.offense_yardage = ceil(kick_rnd - kick_adjustment)

    def determine_punt_yardage(self):
        punt_rnd = randint(1,100)
        punt_block_rnd = randint(1,100)
        punt_block_chance = randint(0,1)
        pivot_point = ceil(self.play_rating / 1.7)
        pivot_direction = choice([-1,1])
 
        # enforce minimum punt yardage
        if pivot_direction == -1 and punt_rnd < 5.0:
            punt_rnd = 5.0
        # enforce maximum punt yardage
        if pivot_direction == 1 and punt_rnd < 7.0:
            punt_rnd = 7.0
     
        if (punt_block_rnd == self.play_rating) and punt_block_chance:
            self.punt_blocked = True
            self.offense_yardage = 0.0
        else:
            self.offense_yardage = (pivot_point + (pivot_direction * floor(((self.play_rating*100) * pow(punt_rnd,-.8309)) / 100)))

    def determine_field_goal_result(self, adjustment):
        self.play_rating = self.offense.rating_sp - (self.defense.home_field_advantage + ceil((self.defense.rating_sp - 60) / 4))
        if self.field.direction == 1:
            distance = 100 - self.field.absolute_yardline
        else:
            distance = self.field.absolute_yardline
        
        fg_rnd = randint(1,adjustment)
        fg_rating = ((80 - self.play_rating) / 2)
        
        if fg_rnd < ((100 - distance) - fg_rating):
            self.kick_successful = True
            
#------------------------------------------------------------------------------ 
# ***** plays

    def run_clock(self):
        self.play_name = inspect.stack()[0][3]
        self.offense_yardage = -2
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

    def kickoff(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_kickoff_result(20,55)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)
        self.change_of_possession = True 
        if not self.field.in_home_endzone and not self.field.in_away_endzone: 
            self.determine_return_yardage((self.defense.rating_sp * 1.25), -.4)
            self.field.determine_position(self.return_yardage, self.change_of_possession)
        else:
            self.touchback = True    

    def onside_kickoff(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_kickoff_result(10,10)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)
        
        if self.offense_yardage >= 10:
            onside_recover_random = randint(1,100)
            onside_recover_rating = ceil(self.offense.rating_sp / 4)
            if onside_recover_random <= onside_recover_rating:
                self.onside_recover = True
            else:
                self.change_of_possession = True 
                if not self.field.in_home_endzone and not self.field.in_away_endzone: 
                    self.determine_return_yardage(self.defense.rating_sp, -1)
                    self.field.determine_position(self.return_yardage, self.change_of_possession)
                else:
                    self.touchback = True  
        else:
            self.change_of_possession = True

    def punt(self): 
        self.play_name = inspect.stack()[0][3]
        self.play_rating = self.offense.rating_sp - (self.defense.home_field_advantage + ceil((self.defense.rating_sp - 60) / 4))
        self.determine_punt_yardage()
        self.field.determine_position(self.offense_yardage, self.change_of_possession)
        self.change_of_possession = True
                
        if not self.field.in_home_endzone and not self.field.in_away_endzone: 
            self.determine_return_yardage(self.defense.rating_sp, -.6)
            self.field.determine_position(self.return_yardage, self.change_of_possession)
        else:
            self.touchback = True

    def field_goal(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_field_goal_result(110)
        
        if not self.kick_successful:
            self.change_of_possession = True
            self.field.determine_position(7, self.change_of_possession)
 
    def extra_point(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_field_goal_result(100)
        
    def run_inside(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_play_rating(1,4,0,5,6,3,0,1)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(3.5,1)
        
        self.determine_play_yardage(-.7,-1,-5.0)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_dl,-1)
            self.field.determine_position(self.return_yardage, self.change_of_possession)

    def run_outside(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_play_rating(1,5,1,3,3,5,1,1)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(3.5,1)
        
        self.determine_play_yardage(-.7,-1,-5.0)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_lb,-1)
            self.field.determine_position(self.return_yardage, self.change_of_possession)

    def pass_short(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_play_rating(4,2,3,1,1,5,3,1)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(10,1)
        
        self.determine_play_yardage(-.7,-1,-5.0)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_lb,-.8)
            self.field.determine_position(self.return_yardage, self.change_of_possession)

    def pass_medium(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_play_rating(4,0,4,2,2,2,4,2)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(10,1.5)
        
        self.determine_play_yardage(-.5,-.8309,-8.0)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_cb,-.7)
            self.field.determine_position(self.return_yardage, self.change_of_possession)
            
    def pass_long(self):
        self.play_name = inspect.stack()[0][3]
        self.determine_play_rating(4,0,3,3,3,1,3,3)
        self.determine_play_success()
        if not self.play_success: 
            self.determine_turnover(10,2)
        
        self.determine_play_yardage(-.4,-.5,-12.0)
        self.field.determine_position(self.offense_yardage, self.change_of_possession)

        if self.turnover:
            self.change_of_possession = True
            self.determine_return_yardage(self.defense.rating_s,-.6)
            self.field.determine_position(self.return_yardage, self.change_of_possession)

#===============================================================================
#
## test execution 
#def test_execution():
#    team1 = Team("Austin","Easy")
#    team2 = Team("Chicago","Grown Men")
#    
#    pprint.pprint(vars(team1)) 
#    print ' '
#    pprint.pprint(vars(team2)) 
#    
#    for a in range(20):
#        print ' '
#        f = Field()
#        p1 = Play(team1,team2,f)
#        p1.run_clock()
#        f = Field()
#        p2 = Play(team1,team2,f)
#        p2.kickoff()
#    #    pprint.pprint(vars(p2))
#    #    pprint.pprint(vars(p2.field))
#        f = Field()
#        p21 = Play(team1,team2,f)
#        p21.onside_kickoff()
#    #    pprint.pprint(vars(p21))
#    #    pprint.pprint(vars(p21.field))
#        f = Field()
#        p22 = Play(team1,team2,f)
#        p22.punt()
#    #    pprint.pprint(vars(p22))
#    #    pprint.pprint(vars(p22.field))
#        f = Field()
#        f.absolute_yardline, f.direction = randint(1,99), choice([1,-1])
#    #    print f.absolute_yardline
#        p23 = Play(team1,team2,f)
#        p23.field_goal()
#        pprint.pprint(vars(p23))
#        pprint.pprint(vars(p23.field))
#        f = Field()
#        f.absolute_yardline = 2
#        p24 = Play(team1,team2,f)
#        p24.extra_point()
#        pprint.pprint(vars(p24))
#        pprint.pprint(vars(p24.field))
#        f = Field()    
#        p3 = Play(team1,team2,f)
#        p3.run_inside()
#        pprint.pprint(vars(p3))
#        f = Field()
#        p4 = Play(team1,team2,f)
#        p4.run_outside()
#        pprint.pprint(vars(p4)) 
#        f = Field()
#        p5 = Play(team1,team2,f)
#        p5.pass_short()
#    #    pprint.pprint(vars(p5))
#    #    pprint.pprint(vars(p5.field))
#        pprint.pprint(vars(p5.offense))
#        f = Field()
#        p6 = Play(team1,team2,f)
#        p6.pass_medium()
#    #    pprint.pprint(vars(p6))
#    #    pprint.pprint(vars(p6.field))
#        f = Field()
#        p7 = Play(team1,team2,f)
#        p7.pass_long()
#        pprint.pprint(vars(p7))
#        pprint.pprint(vars(p7.field))
#    #===============================================================================
#    
#    
    

