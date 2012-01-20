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
       
        def calculate_play_type_rating(self):
            self.rating_ri_off = ceil(((self.rating_qb + self.rating_rb*4 + self.rating_ol*5) / 10))
            self.rating_ri_def = ceil((((self.rating_dl*6 + self.rating_lb*3 + self.rating_s) / 10) - 60) / 4)
            self.rating_ro_off = ceil(((self.rating_qb + self.rating_rb*5 + self.rating_wr + self.rating_ol*3) / 10))
            self.rating_ro_def = ceil((((self.rating_dl*3 + self.rating_lb*5 + self.rating_cb + self.rating_s) / 10) - 60) / 4)
            self.rating_ps_off = ceil(((self.rating_qb*4 + self.rating_rb*2 + self.rating_wr*3 + self.rating_ol) / 10))
            self.rating_ps_def = ceil((((self.rating_dl + self.rating_lb*5 + self.rating_cb*3 + self.rating_s) / 10) - 60) / 4)
            self.rating_pm_off = ceil(((self.rating_qb*4 + self.rating_wr*4 + self.rating_ol*2) / 10))
            self.rating_pm_def = ceil((((self.rating_dl*2 + self.rating_lb*2 + self.rating_cb*4 + self.rating_s*2) / 10) - 60) / 4)
            self.rating_pl_off = ceil(((self.rating_qb*4 + self.rating_wr*3 + self.rating_ol*3) / 10))
            self.rating_pl_def = ceil((((self.rating_dl*3 + self.rating_lb + self.rating_cb*3 + self.rating_s*3) / 10) - 60) / 4)
            self.rating_sp_off = self.rating_sp
            self.rating_sp_def = ceil((self.rating_sp - 60) / 4)

            ##Testing
            print self.city, self.nickname, self.rating_ri_off,self.rating_ri_def,self.rating_ro_off,self.rating_ro_def,self.rating_ps_off,self.rating_ps_def,self.rating_pm_off,self.rating_pm_def,self.rating_pl_off,self.rating_pl_def,self.rating_sp_off,self.rating_sp_def
            ##Testing
            return True

        calculate_play_type_rating(self)
        
            ## @QUESTION - is this the best way to populate the initial stats and best place for dict?
        self.stats = {
                        'points' : 0,
                        'points_q1' : 0,
                        'points_q2' : 0,
                        'points_q3' : 0,
                        'points_q4' : 0,
                        'points_ot' : 0,
                        'total_offense' : 0,
                        'home_pass_att' : 0, 
                        'pass_comp' : 0,
                        'pass_int' : 0,
                        'pass_yards' : 0,
                        'pass_td' : 0,
                        'passer_rating' : 0,
                        'sacked' : 0,
                        'sack_yards' : 0,
                        'rush_att' : 0,
                        'rush_yards' : 0,
                        'rush_td' : 0,
                        'rush_fumbles' : 0,
                        'first_downs' : 0,
                        'field_goals_att' : 0,
                        'field_goals' : 0,
                        'punts' : 0,
                        'punt_yards' : 0,
                        'punt_returns' : 0,
                        'punt_return_yards' : 0,
                        'kick_returns' : 0,
                        'kick_return_yards' : 0,
                        'return_yards' : 0,
                        'extra_points_att' : 0,
                        'extra_points' : 0,
                        'two_point_att' : 0,
                        'two_point_conv' : 0,
                        'third_down_att' : 0,
                        'third_down_conv' : 0,
                        'fourth_down_att' : 0,
                        'fourth_down_conv': 0
                        }
        

def get_next_team_id():
    global next_team_id
    team_id = next_team_id
    next_team_id += 1
    return team_id

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")

#print team1.id,team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
#print team2.id,team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp