'''
Created on Jan 15, 2012

@author: George Peek
'''

from random import randint
from math import ceil

from play import Play

next_team_id = 0

class Team():
    "Team"
    def __init__(self, city, nickname):
        self.id = get_next_team_id()
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

       
        def determine_off_rating(qb_factor,rb_factor,wr_factor,ol_factor):
            if qb_factor + rb_factor + wr_factor + ol_factor == 10:
                return ceil(((self.rating_qb*qb_factor + self.rating_rb*rb_factor + self.rating_wr*wr_factor + self.rating_ol*ol_factor) / 10))                
            else:
                print 'Offense rating factors do not equal 10'
                raise Exception
            
        def determine_def_rating(dl_factor,lb_factor,cb_factor,s_factor):
            if dl_factor + lb_factor + cb_factor + s_factor == 10:
                return ceil((((self.rating_dl*dl_factor + self.rating_lb*lb_factor + self.rating_cb*cb_factor + self.rating_s*s_factor) / 10) - 60) / 4)
            else:
                print 'Defense rating factors do not equal 10'
                raise Exception
         

        self.rating_run_inside_off = determine_off_rating(1,4,0,5) 
        self.rating_run_inside_def = determine_def_rating(6,3,0,1) 
        self.rating_run_outside_off = determine_off_rating(1,5,1,3)
        self.rating_run_outside_def = determine_def_rating(3,5,1,1)
        self.rating_pass_short_off = determine_off_rating(4,2,3,1) 
        self.rating_pass_short_def = determine_def_rating(1,5,3,1) 
        self.rating_pass_medium_off = determine_off_rating(4,0,4,2)
        self.rating_pass_medium_def = determine_def_rating(2,2,4,2)
        self.rating_pass_long_off = determine_off_rating(4,0,3,3) 
        self.rating_pass_long_def = determine_def_rating(3,1,3,3) 
        self.rating_special_teams_off = self.rating_sp
        self.rating_special_teams_def = ceil((self.rating_sp - 60) / 4)

        ##Testing
        print self.city, self.nickname, self.rating_run_inside_off,self.rating_run_inside_def,self.rating_run_outside_off,self.rating_run_outside_def,self.rating_pass_short_off,self.rating_pass_short_def,self.rating_pass_medium_off,self.rating_pass_medium_def,self.rating_pass_long_off,self.rating_pass_long_def,self.rating_special_teams_off,self.rating_special_teams_def
        ##Testing
        

def get_next_team_id():
    global next_team_id
    team_id = next_team_id
    next_team_id += 1
    return team_id

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")

for i in range (100):
    p = Play()
    p.onside_kickoff(team1,team2,3)

#print team1.id,team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
#print team2.id,team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp