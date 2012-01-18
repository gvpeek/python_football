'''
Created on Jan 13, 2012

@author: George
'''

from random import choice
from copy import deepcopy

import playTests
from teamTests import team1,team2

# @TODO: add logging
#log = open('logfile.txt', 'w')

## @QUESTION - is this the best way to handle this. If not, how should I increment and utilize
## id generator outside of scope of game function?
next_game_id = 0
scope = vars()

class Game():
    "Basic Game"
    def __init__(self, home_team, away_team, league_game=False, division_game=False, conference_game=False, playoff_game=False):
        self.game_id = get_next_game_id()
        self.home = home_team
        self.away = away_team
        self.league_game = league_game
        self.division_game = division_game
        self.conference_game = conference_game 
        self.playoff_game = playoff_game  
        
        self.possession = {
                           'offense':self.home,
                           'defense':self.away
                           }
        
        self.time = {
                     'clicks' : 0.0,
                     'minutes' : 15,
                     'seconds' : 0,
                     'quarter' : 1,
                     'end_of_half' : False,
                     'end_of_game' : False,
                     'overtime' : False,
                     'end_of_overtime' : False,
                     'definitive_overtime' : False
                     }
        
        if self.playoff_game:
            self.time['definitive_overtime'] = True
        
        self.position = {
                         'direction' : 1, ## 1=home, -1=away
                         'absolute_yardline' : 30,
                         'converted_yardline' : 30,
                         'down' : 1,
                         'yards_to_gain' : 10,
                         'target_yardline' : 30,
                         'in_home_endzone' : False,
                         'in_away_endzone' : False
                     }
        
        self.situation = {
                          'kickoff' : True,
                          'touchdown' : False,
                          'home_scored_on_play' : False,
                          'away_scored_on_play' : False
                          }
        
        ## @QUESTION - is this the best way to populate the initial stats and best place for dict?
        initial_stats = {
                        'score' : 0,
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
                        'fourth_down_conv': 0,
                        'score_q1' : 0,
                        'score_q2' : 0,
                        'score_q3' : 0,
                        'score_q4' : 0,
                        'score_ot' : 0
                        }
        
        initial_play_call_counts = {
                                    'RI' : 0.0,
                                    'RO' : 0.0,
                                    'PS' : 0.0,
                                    'PM' : 0.0,
                                    'PL' : 0.0,
                                    'total_plays' : 0.0
                                    }
        
        self.home.stats = deepcopy(initial_stats)
        self.away.stats = deepcopy(initial_stats)
        self.home.play_calls = deepcopy(initial_play_call_counts)
        self.away.play_calls = deepcopy(initial_play_call_counts)

    def coin_flip(self,*side_choice):
        #=======================================================================
        # Away team calls the coin flip. 
        # Since kickoff is first play, team that loses coin toss is offense
        # and receiving team is defense.
        # Since the home team is the default offense, we change possession 
        # if the away team loses toss.
        # Will need to refactor if option to defer the choice is added.
        #=======================================================================
        won_toss = False
        side_options = ['Heads','Tails']
        if not side_choice:
            side_choice = choice(side_options)
        flip_result = choice(side_options)
        if flip_result == side_choice:
            won_toss = True
        else:
            change_game_possession(self)
            self.position['absolute_yardline'] = 70
            self.position['side_of_field'] = 'H'
        print won_toss
        return won_toss
    

def get_next_game_id():
    team_id = scope['next_game_id']
    scope['next_game_id'] += 1
    return team_id

def change_game_possession(game):
    if game.away.id == game.possession['offense'].id:
        game.possession = {'offense':game.home,'defense':game.away}
        game.position['direction'] = 1
    else:
        game.possession = {'offense':game.away,'defense':game.home}
        game.position['direction'] = -1

def determine_time_remaining(current_time):
    ## @QUESTION - better to have this as a "WHILE" of the main logic 
    if (current_time['end_of_game'] and not current_time['overtime']) or current_time['end_of_overtime']:
        return False
    
    current_time['clicks'] += 1
    
    if (current_time['clicks'] % 2) > 0:
        current_time['minutes'] -= 1
        current_time['seconds'] = 30
    else:
        current_time['seconds'] = 0
        
    if current_time['minutes'] == 0 and current_time['seconds'] == 0:
        if current_time['quarter'] == 4:
            current_time['end_of_game'] = True
        else:
            if current_time['quarter'] == 2:
                current_time['end_of_half'] = True
            elif current_time['quarter'] == 5 and not current_time['definitive_overtime']:
                current_time['end_of_overtime'] = True

        current_time['quarter'] += 1
        current_time['minutes'] = 15
        current_time['seconds'] = 00


    print current_time['clicks']
    print current_time['minutes']
    print current_time['seconds']
    print current_time['quarter']
    print current_time['end_of_half']
    print current_time['end_of_game']
    print current_time['overtime']
    print current_time['end_of_overtime']
    print current_time['definitive_overtime']                        
#                     'overtime' : False,

def determine_score(play_result,game):
    if game.position['in_home_endzone']:
        if (game.possession['offense'] == game.away and not play_result['change_of_possession']) or (game.possession['offense'] == game.home and play_result['change_of_possession']):
            game.away.stats['score'] += 6
        elif game.possession['offense'] == game.home and not play_result['change_of_possession']:
            game.away.stats['score'] += 2
    
    if game.position['in_away_endzone']:
        if (game.possession['offense'] == game.home and not play_result['change_of_possession']) or (game.possession['offense'] == game.away and play_result['change_of_possession']):
            game.home.stats['score'] += 6
        elif game.possession['offense'] == game.away and not play_result['change_of_possession']:
            game.home.stats['score'] += 2

    print game.away.city, game.away.nickname, game.away.stats['score']    
    print game.home.city, game.home.nickname, game.home.stats['score']
#        
#        
#        
#         
#            'play_type' : play,
#            'turnover' : False,
#            'change_of_possession' : False,
#            'field_goal_success' : False,
#            'safety' : False,
#            'touchdown' : False     


#------------------------------------------------------------------------------ 

print team1.id,team1.city,team1.nickname,'QB', team1.rating_qb,'RB',team1.rating_rb,'WR',team1.rating_wr,'OL',team1.rating_ol,'DL',team1.rating_dl,'LB',team1.rating_lb,'CB',team1.rating_cb,'S',team1.rating_s,'SP',team1.rating_sp
print team2.id,team2.city,team2.nickname,'QB', team2.rating_qb,'RB',team2.rating_rb,'WR',team2.rating_wr,'OL',team2.rating_ol,'DL',team2.rating_dl,'LB',team2.rating_lb,'CB',team2.rating_cb,'S',team2.rating_s,'SP',team2.rating_sp

home_team = deepcopy(team1)
away_team = deepcopy(team2)

game = Game(team1,team2)
game.coin_flip()

for i in range(130):
    if i == 0:
        play = 'K'
    else:
        play = choice(playTests.plays)
    print ' '
    print play
    current_play = playTests.determine_play_result(play,
                                                   (game.away == game.possession['offense']),
                                                   game.position,
                                                   game.possession['offense'],
                                                   game.possession['defense'])
    
    if current_play['field_goal_attempt']:
        if current_play['field_goal_success']:
            print 'Kick Is Good'
        else:
            print 'Kick No Good'
    if current_play['punt_blocked']:
        print 'Punt Blocked!'
    print 'Yards On Play', current_play['net_yards_on_play']
    determine_score(current_play,game)
    if current_play['change_of_possession']:
        change_game_possession(game)
    determine_time_remaining(game.time)
