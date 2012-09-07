'''
Created on Aug 19, 2012

@author: George Peek
'''

import pprint


from play import Play
from timekeeping import Clock

class State():
    "Basic State"
    def __init__(self):
        self.active = True
    
    def check_state(self, game):
        print 'check_state'

#        pprint.pprint(vars(game.plays[-1]))
        next_state = None
        if game.field.in_away_endzone:
            if game.field.direction == 1:
                if isinstance(self, Conversion):
                    self.active = False
                    game.scoreboard.home_conversion_play()
                    game.current_state = Kickoff(game)
                else:
                    if game.plays[-1].touchback:
                        print 'Away touchback'
                        game.field.touchback_set()
                        game.current_state = DownSet(game)
                    else:
                        print 'Home touchdown'
                        game.scoreboard.home_touchdown()
                        game.current_state = Conversion(game)
            elif game.field.direction == -1:
                print 'Home safety'
                game.scoreboard.home_safety()
                game.current_state = Kickoff(game, True)
        elif game.field.in_home_endzone:
            if game.field.direction == -1: 
                if isinstance(self, Conversion):
                    self.active = False
                    game.scoreboard.away_conversion_play()
                    game.current_state = Kickoff(game)
                else:
                    if game.plays[-1].touchback:
                        print 'Home touchback'
                        game.field.touchback_set()
                        game.current_state = DownSet(game)
                    else:
                        print 'Away touchdown'
                        game.scoreboard.away_touchdown()
                        game.current_state = Conversion(game)
            elif game.field.direction == 1:
                print 'Away safety'
                game.scoreboard.away_safety()
                game.current_state = Kickoff(game, True)               
        elif isinstance(self, Conversion):
            self.active = False
            if game.plays[-1].kick_successful:
                if game.field.direction == 1:
                    game.scoreboard.home_conversion_kick()
                elif game.field.direction == -1:
                    game.scoreboard.away_conversion_kick()
            game.current_state = Kickoff(game)
        elif isinstance(self, Kickoff):
            self.active = False
            game.current_state = DownSet(game)
        elif isinstance(self, DownSet):
            if game.plays[-1].punt_attempt:
                self.active = False
                game.current_state = DownSet(game)
            elif game.plays[-1].field_goal_attempt:
                if game.plays[-1].kick_successful == True:
                    self.active = False
                    if game.field.direction == 1:
                        game.scoreboard.home_field_goal()
                    elif game.field.direction == -1:
                        game.scoreboard.away_field_goal()
                    game.current_state = Kickoff(game)
                else:
                    game.current_state = DownSet(game)
            elif game.plays[-1].turnover:
                self.active = False
                game.current_state = DownSet(game)               
            else:
                self.convert_check()
                if self.converted:
                    game.current_state = DownSet(game)
                elif not self.active:
                    game.plays[-1].change_of_possession = True
                    game.field.direction *= -1
                    game.current_state = DownSet(game)
        
        if game.plays[-1].change_of_possession:
            game.possession[0], game.possession[1] = game.possession[1], game.possession[0]

        if game.end_of_half and not isinstance(game.current_state, Conversion):
            game.set_second_half()
            game.current_state = Kickoff(game)
            game.end_of_half = False

        if not isinstance(game.current_state, Conversion):
            game.scoreboard.clock = str(game.current_clock.run_clock())[2:7]
            if not game.current_clock.time_remaining:
                if game.timekeeping:
                    if game.number_of_periods / game.period == 2:
                        game.end_of_half = True
                    game.period += 1
                    game.scoreboard.period = game.period
                    game.current_clock = game.timekeeping.pop()
                    game.scoreboard.clock = str(game.current_clock.time_remaining)[2:7]
                else:
                    game.end_of_regulation = True
                    print 'outof timekeeping'
                    if game.scoreboard.home_score == game.scoreboard.away_score: 
                        if not game.overtime:
                            game.overtime = True
                            game.coin_flip()
                            game.current_state = Kickoff(game)
                    if game.overtime:
                        print 'in overtime'
                        game.period += 1
                        game.scoreboard.period = game.period
                        game.current_clock = Clock()
                        game.scoreboard.clock = str(game.current_clock.time_remaining)[2:7]

        if (game.end_of_regulation and not game.overtime) or (game.overtime and game.scoreboard.home_score != game.scoreboard.away_score):                    
            game.end_of_game = True
            game.current_state = EndOfGame(game)
                    
 
        print 'scoreboard'
        game.scoreboard.absolute_yardline = str(game.field.absolute_yardline)
        game.scoreboard.play_name = game.plays[-1].play_name
        game.scoreboard.offense_yardage = game.plays[-1].offense_yardage
        game.scoreboard.return_yardage = game.plays[-1].return_yardage
        game.scoreboard.turnover =  game.plays[-1].turnover
        game.scoreboard.play_rating = game.plays[-1].play_rating
        if isinstance(game.current_state,DownSet):
            game.scoreboard.down = game.current_state.down
            if 0 < game.current_state.target_yardline < 100:
                game.scoreboard.yards_to_go = game.current_state.yards_to_convert
            else:
                game.scoreboard.yards_to_go ='Goal'
        else:
            game.scoreboard.down = ''
            game.scoreboard.yards_to_go = ''
        
#        pprint.pprint(vars(game.current_state))
#        pprint.pprint(vars(game.field))
        
       
        game.field.play_reset()
        game.plays.append(Play(game.possession[0],game.possession[1],game.field))
        return next_state
    
#    def check_score(self):


class Kickoff(State):
    "State for kickoffs"
    def __init__(self, game, post_safety=False):
        self.play_choice = ['kickoff','onside_kickoff']
        game.field.kickoff_set(post_safety)

     
        
class DownSet(State):
    "State for normal offensive possession"
    def __init__(self, game, downs_to_convert = 4, yards_to_convert = 10.0):
        self.play_choice = ['run_inside', 'run_outside', 'pass_short', 'pass_medium', 'pass_long', 'field_goal', 'punt', 'run_clock']
        self.down = 1
        self.downs_to_convert = downs_to_convert
        self.yards_to_convert = yards_to_convert
        self.field = game.field
        self.target_yardline = game.field.absolute_yardline + (self.yards_to_convert * self.field.direction) 
        self.converted = False
        self.active = True
        
    def convert_check(self):
        if not self.active:
            return False
        
        self.yards_to_convert = (self.target_yardline - self.field.absolute_yardline) * self.field.direction
        print 'YTC' + str(self.yards_to_convert)
        if (self.yards_to_convert <= 0):
            self.converted = True
            self.active = False
            ##return self.converted 
        elif (self.down == 4):
            self.active = False
            ##return self.active
        else:
            self.down += 1
            return self.down, self.yards_to_convert
        
class Conversion(State):
    "State for conversion attempt after touchdown"
    def __init__(self, game):
        self.play_choice = ['extra_point', 'run_inside', 'run_outside', 'pass_short']
        game.field.conversion_set()
        
class EndOfGame():
    def __init__(self, game):
        self.play_choice = []
