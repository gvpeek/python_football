'''
Created on Jan 15, 2012

@author: George Peek
'''

from random import randint

next_team_id = 0
scope = vars()

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
        

def get_next_team_id():
    team_id = scope['next_team_id']
    scope['next_team_id'] += 1
    return team_id

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")

#print team1.id,team1.city,team1.nickname,team1.rating_qb,team1.rating_rb,team1.rating_wr,team1.rating_ol,team1.rating_dl,team1.rating_lb,team1.rating_cb,team1.rating_s,team1.rating_sp
#print team2.id,team2.city,team2.nickname,team2.rating_qb,team2.rating_rb,team2.rating_wr,team2.rating_ol,team2.rating_dl,team2.rating_lb,team2.rating_cb,team2.rating_s,team2.rating_sp