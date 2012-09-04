'''
Created on Aug 19, 2012

@author: George Peek
'''

from play import Play
import pprint

class State():
    "Basic State"
    def __init__(self):
        self.active = True
    
    def check_state(self, game):
        print 'check_state'
        pprint.pprint(vars(game.plays[-1]))
        next_state = None
        if game.field.direction == 1 and game.field.in_away_endzone and not isinstance(self, Conversion): 
            if game.plays[-1].touchback:
                print 'Away touchback'
                game.field.touchback_set()
                game.current_state = DownSet(game)
            else:
                print 'Home touchdown'
                game.current_state = Conversion(game)
        elif game.field.direction == -1 and game.field.in_home_endzone and not isinstance(self, Conversion):
            if game.plays[-1].touchback:
                print 'Home touchback'
                game.field.touchback_set()
                game.current_state = DownSet(game)
            else:
                print 'Away touchdown'
                game.current_state = Conversion(game)
        elif isinstance(self, Conversion):
            self.active = False
            game.current_state = Kickoff(game)
        elif isinstance(self, Kickoff):
            self.active = False
            game.current_state = DownSet(game)
        elif isinstance(self, DownSet):
            if game.plays[-1].play_name == 'punt':
                game.current_state = DownSet(game)
            elif game.plays[-1].play_name == 'field_goal':
                if game.plays[-1].kick_successful == True:
                    self.active = False
                    game.current_state = Kickoff(game)
                else:
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

        print 'scoreboard'
        game.scoreboard.absolute_yardline = str(game.field.absolute_yardline)
        game.scoreboard.play_name = game.plays[-1].play_name
        game.scoreboard.offense_yardage = game.plays[-1].offense_yardage
        game.scoreboard.return_yardage = game.plays[-1].return_yardage
        game.scoreboard.turnover =  game.plays[-1].turnover
        game.scoreboard.play_rating = game.plays[-1].play_rating
        if isinstance(game.current_state,DownSet):
            game.scoreboard.down = game.current_state.down
            game.scoreboard.yards_to_go = game.current_state.yards_to_convert
        else:
            game.scoreboard.down = ''
            game.scoreboard.yards_to_go = ''
        
        pprint.pprint(vars(game.current_state))
        pprint.pprint(vars(game.field))
        
        game.field.play_reset()
        game.plays.append(Play(game.possession[0],game.possession[1],game.field))
        return next_state
    
#    def check_score(self):


class Kickoff(State):
    "State for kickoffs"
    def __init__(self, game):
        self.play_choice = ['kickoff','onside_kickoff']
        game.field.kickoff_set()
     
        
class Drive(State):
    "State for normal offensive possession"
    def __init__(self):
        self.play_choice = ['run_clock', 'run_inside', 'run_outside', 'pass_short', 'pass_medium', 'pass_long', 'field_goal', 'punt']

class DownSet(State):
    "State for normal offensive possession"
    def __init__(self, game, downs_to_convert = 4, yards_to_convert = 10.0):
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
        
#class Drive():
#    "State for drive"
#    def __init__(self, kickoff=False):

