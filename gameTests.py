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

#class Clock(object):
#    "Basic Clock"
#    def __init__(self, quarter_length=15, playoff_game = False):
#        self.quarter_length = quarter_length
#        self.minutes = deepcopy(quarter_length)
#        self.seconds = 00
#        self.clicks = 0
#        self.quarter = 1
#        self.end_of_half = False
#        self.end_of_regulation = False
#        self.definitive_overtime = playoff_game
#
#    def end_of_quarter(self):
#        if self.minutes == 0 and self.seconds == 0:
#            if self.quarter == 2:
#                    self.end_of_half = True
#                    
#            if self.quarter == 4:
#                self.end_of_regulation = True
#                return False
#            
#            self.quarter += 1
#            self.minutes = self.quarter_length
#            self.seconds = 00        
#        
#    def run_clock(self):
#        if self.end_of_regulation:
#            return False
#    
#        self.clicks += 1
#    
#        if (self.clicks % 2) > 0:
#            self.minutes -= 1
#            self.seconds = 30
#        else:
#            self.seconds = 0
#            
#        self.end_of_quarter()
#        
#        return self.quarter, self.minutes, self.seconds
        
#class overtimeClock(Clock):
#    "Overtime Clock"
#    def __init__(self):
#        self.definitive_overtime = Clock.definitive_overtime
#        self.end_of_ovetime= False
#        
#    def end_of_quarter(self):        
#        if self.minutes == 0 and self.seconds == 0:
#            if not self.definitive_overtime:
#                self.end_of_overtime = True
#                return False
#        else:
#            self.quarter += 1
#            self.minutes = self.quarter_length
#            self.seconds = 00
#            
#        self.end_of_quarter()
#            
#        return self.quarter, self.minutes, self.seconds

## @QUESTION - is this the best way to handle this. If not, how should I increment and utilize
## id generator outside of scope of game function?
next_game_id = 0

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

## @TODO - raise exception if div, conf or playoff True and league False
        class Game_State():
            "Initial Game State"
            def __init__(self,game):
                self.offense = game.home
                self.defense = game.away
                self.clicks = 0.0
                self.minutes = 15
                self.seconds = 0
                self.quarter = 1
                self.end_of_half = False
                self.end_of_game = False
                self.overtime = False
                self.end_of_overtime = False
                self.definitive_overtime = playoff_game
        
                self.direction = 1 ## 1=home, -1=away
                self.absolute_yardline = 30
                self.converted_yardline = 30
                self.down = 1
                self.yards_to_gain = 10
                self.target_yardline = 30
                self.in_home_endzone = False
                self.in_away_endzone = False
             
                self.kickoff = True
                self.turnover = False
                self.change_of_possession = False
                self.touchback = False
                self.net_yards_on_play = 0
                self.offense_yardage = 0
                self.kickoff_yardage = 0
                self.punt_yardage = 0
                self.punt_blocked = False
                self.return_yardage = 0
                self.field_goal_attempt = False
                self.field_goal_success = False
                self.safety = False
                self.touchdown = False  
                self.home_scored_on_play = False
                self.away_scored_on_play = False
        
        
        ## @QUESTION - is this the best way to populate the initial stats and best place for dict?
        def initial_stats(team):
            team.points = 0
            team.points_q1 = 0
            team.points_q2 = 0
            team.points_q3 = 0
            team.points_q4 = 0
            team.points_ot = 0
            team.total_offense = 0
            team.home_pass_att = 0 
            team.pass_comp = 0
            team.pass_int = 0
            team.pass_yards = 0
            team.pass_td = 0
            team.passer_rating = 0
            team.sacked = 0
            team.sack_yards = 0
            team.rush_att = 0
            team.rush_yards = 0
            team.rush_td = 0
            team.rush_fumbles = 0
            team.first_downs = 0
            team.field_goals_att = 0
            team.field_goals = 0
            team.punts = 0
            team.punt_yards = 0
            team.punt_returns = 0
            team.punt_return_yards = 0
            team.kick_returns = 0
            team.kick_return_yards = 0
            team.return_yards = 0
            team.extra_points_att = 0
            team.extra_points = 0
            team.two_point_att = 0
            team.two_point_conv = 0
            team.third_down_att = 0
            team.third_down_conv = 0
            team.fourth_down_att = 0
            team.fourth_down_conv = 0
            
            team.count_ri = 0.0
            team.count_ro = 0.0
            team.count_ps = 0.0
            team.count_pm = 0.0
            team.count_pl = 0.0
            team.count_total_plays = 0.0
        
        self.game_state = Game_State(self)
        initial_stats(self.home)
        initial_stats(self.away)

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
        side_options = ('Heads','Tails')
        if not side_choice:
            side_choice = choice(side_options)
        flip_result = choice(side_options)
        if flip_result == side_choice:
            won_toss = True
        else:
            change_game_possession(self)
            self.game_state.absolute_yardline = 70
            self.game_state.side_of_field = 'H'
        print won_toss
        return won_toss
    
#    def tick_clock(self):
#    ## @QUESTION - better to have this as a "WHILE" of the main logic 
#        if (self.game_state.end_of_game and not self.game_state.overtime) or self.game_state.end_of_overtime:
#            return False
#        
#        self.game_state.clicks += 1
#        
#        if (self.game_state.clicks % 2) > 0:
#            self.game_state.minutes -= 1
#            self.game_state.seconds = 30
#        else:
#            self.game_state.seconds = 0
#            
#        if self.game_state.minutes == 0 and self.game_state.seconds == 0:
#            if self.game_state.quarter == 4:
#                self.game_state.end_of_game = True
#            else:
#                if self.game_state.quarter == 2:
#                    self.game_state.end_of_half = True
#                elif self.game_state.quarter == 5 and not self.game_state.definitive_overtime:
#                    self.game_state.end_of_overtime = True
#    
#            self.game_state.quarter += 1
#            self.game_state.minutes = 15
#            self.game_state.seconds = 00
    
    
#        print self.game_state.clicks
#        print self.game_state.minutes
#        print self.game_state.seconds
#        print self.game_state.quarter
#        print self.game_state.end_of_half
#        print self.game_state.end_of_game
#        print self.game_state.overtime
#        print self.game_state.end_of_overtime
#        print self.game_state.definitive_overtime                        
#                     'overtime' : False,
    

def get_next_game_id():
    global next_game_id
    team_id = next_game_id
    next_game_id += 1
    print team_id
    return team_id

def change_game_possession(game):
    if game.away.id == game.game_state.offense.id:
        game.possession = {'offense':game.home,'defense':game.away}
        game.game_state.direction = 1
    else:
        game.possession = {'offense':game.away,'defense':game.home}
        game.game_state.direction = -1



def determine_score(play_result,game):
    if game.game_state.in_home_endzone:
        game.game_state.away_scored_on_play = True
        if (game.game_state.offense == game.away and not play_result['change_of_possession']) or (game.game_state.offense == game.home and play_result['change_of_possession']):
            if play_result['play_type'][0] == '2':
                game.away.points += 2
            else:
                game.away.points += 6
                game.game_state.touchdown = True
        elif game.game_state.offense == game.home and not play_result['change_of_possession']:
            game.away.points += 2
            game.game_state.safety = True
    elif game.game_state.in_away_endzone:
        game.game_state.home_scored_on_play = True
        if (game.game_state.offense == game.home and not play_result['change_of_possession']) or (game.game_state.offense == game.away and play_result['change_of_possession']):
            if play_result['play_type'][0] == '2':
                game.home.points += 2
            else:
                game.home.points += 6
                game.game_state.touchdown = True
        elif game.game_state.offense == game.away and not play_result['change_of_possession']:
            game.home.points += 2
            game.game_state.safety = True
    elif play_result['field_goal_success']:
        if play_result['play_type'] == 'FG':
            points = 3
        elif play_result['play_type'] == 'XP':
            points = 1
        if game.game_state.offense == game.away:
            game.game_state.away_scored_on_play = True
            game.away.points += points
        elif game.game_state.offense == game.home:
            game.game_state.home_scored_on_play = True
            game.home.points += points
        
    print game.away.city, game.away.nickname, game.away.points    
    print game.home.city, game.home.nickname, game.home.points

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
                                                   (game.away == game.game_state.offense),
                                                   game.position,
                                                   game.game_state.offense,
                                                   game.game_state.defense)
    
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
    game.tick_clock()
