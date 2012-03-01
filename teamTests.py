'''
Created on Jan 15, 2012

@author: George Peek
'''

from random import randint
from math import ceil

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
       
        ## @TODO create function to create tuple key
        self.rating.run_inside_off = ceil(((self.rating_qb + self.rating_rb*4 + self.rating_ol*5) / 10))
        self.rating.run_inside_def = ceil((((self.rating_dl*6 + self.rating_lb*3 + self.rating_s) / 10) - 60) / 4)
        self.rating.run_outside_off = ceil(((self.rating_qb + self.rating_rb*5 + self.rating_wr + self.rating_ol*3) / 10))
        self.rating.run_outside_def = ceil((((self.rating_dl*3 + self.rating_lb*5 + self.rating_cb + self.rating_s) / 10) - 60) / 4)
        self.rating.pass_short_off = ceil(((self.rating_qb*4 + self.rating_rb*2 + self.rating_wr*3 + self.rating_ol) / 10))
        self.rating.pass_short_def = ceil((((self.rating_dl + self.rating_lb*5 + self.rating_cb*3 + self.rating_s) / 10) - 60) / 4)
        self.rating.pass_medium_off = ceil(((self.rating_qb*4 + self.rating_wr*4 + self.rating_ol*2) / 10))
        self.rating.pass_medium_def = ceil((((self.rating_dl*2 + self.rating_lb*2 + self.rating_cb*4 + self.rating_s*2) / 10) - 60) / 4)
        self.rating.pass_long_off = ceil(((self.rating_qb*4 + self.rating_wr*3 + self.rating_ol*3) / 10))
        self.rating.pass_long_def = ceil((((self.rating_dl*3 + self.rating_lb + self.rating_cb*3 + self.rating_s*3) / 10) - 60) / 4)
        self.rating.special_teams_off = self.rating_sp
        self.rating.special_teams_def = ceil((self.rating_sp - 60) / 4)

        for r in self.rating:
            if r < 60:
                r = 60
        
        ##Testing
        print self.city, self.nickname, self.rating.ri_off,self.rating.ri_def,self.rating.ro_off,self.rating.ro_def,self.rating.ps_off,self.rating.ps_def,self.rating.pm_off,self.rating.pm_def,self.rating.pl_off,self.rating.pl_def,self.rating.sp_off,self.rating.sp_def
        ##Testing
        

def get_next_team_id():
    global next_team_id
    team_id = next_team_id
    next_team_id += 1
    return team_id

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")

#print team1.id,team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
#print team2.id,team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp