'''
Created on Jan 13, 2012

@author: George
'''

from random import choice

import playTests
from teamTests import team1,team2

## @QUESTION - is this the best way to handle this. If not, how should I increment and utilize
## id generator outside of scope of game function?
next_game_id = 0
scope = vars()

class Game():
    "Basic Game"
    def __init__(self,home_team,away_team,division_game,conference_game,playoff_game):
        self.game_id = get_next_game_id()
        self.home = home_team
        self.away = away_team
        self.division_game = division_game
        self.conference_game = conference_game 
        self.playoff_game = playoff_game  
        
        self.time = {'clicks' : 0,
                     'minutes' : 15,
                     'seconds' : 00,
                     'quarter' : 1,
                     'end_of_half' : False,
                     'end_of_game' : False,
                     'overtime' : False,
                     'end_of_overtime' : False
                     }
        
        self.position = {
                         'absolute_yardline' : 70,
                         'converted_yardline' : 30,
                         'down' : 1,
                         'yards_to_gain' : 10,
                         'target_yardline' : 30,
                         'in_endzone' : False
                     }
        
        self.situation = {'kickoff' : True,
                          'touchdown' : True
                          }
        
        self.stats ={
                     }

    def coin_flip(self,*side_choice):
        won_toss = False
        side_options = ['Heads','Tails']
        if not side_choice:
            flip_result = choice(side_options)
        if flip_result == side_choice:
            won_toss = True
            self.possession = {'offense':self.home,'defense':self.away}
        else:
            self.possession = {'offense':self.away,'defense':self.home}
        return won_toss

def get_next_game_id():
    team_id = scope['next_game_id']
    scope['next_game_id'] += 1
    return team_id

def change_game_possession(game):
    if game.away.id == game.possession['offense'].id:
        game.possession = {'offense':game.home,'defense':game.away}
    else:
        game.possession = {'offense':game.away,'defense':game.home}

print team1.id,team1.city,team1.nickname,'QB', team1.rating_qb,'RB',team1.rating_rb,'WR',team1.rating_wr,'OL',team1.rating_ol,'DL',team1.rating_dl,'LB',team1.rating_lb,'CB',team1.rating_cb,'S',team1.rating_s,'SP',team1.rating_sp
print team2.id,team2.city,team2.nickname,'QB', team2.rating_qb,'RB',team2.rating_rb,'WR',team2.rating_wr,'OL',team2.rating_ol,'DL',team2.rating_dl,'LB',team2.rating_lb,'CB',team2.rating_cb,'S',team2.rating_s,'SP',team2.rating_sp

home_team = team1
away_team = team2

game = Game(team1,team2,False,False,False)
game.coin_flip()

for i in range(1000):
    play = choice(playTests.plays)
    print ' '
    print play
    current_play = playTests.determinePlayResult(play,game.possession['offense'],game.possession['defense'])
    if current_play['field_goal_attempt']:
        if current_play['field_goal_success']:
            print 'Kick Is Good'
        else:
            print 'Kick No Good'
    if current_play['punt_blocked']:
        print 'Punt Blocked!'
    print 'Yards On Play', current_play['net_yards_on_play']
    if current_play['change_of_possession']:
        change_game_possession(game)