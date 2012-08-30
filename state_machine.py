'''
Created on Aug 19, 2012

@author: George Peek
'''

from play import Play

class State():
    "Basic State"
    def __init__(self):
        pass
    
    def check_state(self, game):
        print 'check_state'
        next_state = None
        if game.field.direction == 1 and game.field.in_away_endzone:
            print 'Home touchdown'
        elif game.field.direction == -1 and game.field.in_home_endzone:
            print 'Away touchdown'
        elif isinstance(self, Kickoff):
            self.active = False
            game.current_state = DownSet(game)
        elif isinstance(self, DownSet):
            self.convert_check()
            print self.down
        
        if game.plays[-1].change_of_possession:
            game.possession[0], game.possession[1] = game.possession[1], game.possession[0]
        
        game.plays.append(Play(game.possession[0],game.possession[1],game.field))
        return next_state
    
#    def check_score(self):


class Kickoff(State):
    "State for kickoffs"
    def __init__(self):
        self.play_choice = ['kickoff','onside_kickoff']
        self.active = True
        
        
class Drive(State):
    "State for normal offensive possession"
    def __init__(self):
        self.play_choice = ['run_clock', 'run_inside', 'run_outside', 'pass_short', 'pass_medium', 'pass_long', 'field_goal', 'punt']

class DownSet(State):
    "State for normal offensive possession"
    def __init__(self, game, downs_to_convert = 4, yards_to_convert = 10):
        self.down = 1
        self.downs_to_convert = downs_to_convert
        self.yards_to_convert = yards_to_convert
        self.field = game.field
        self.target_yardline =  + (yards_to_convert * self.field.direction) 
        self.converted = False
        self.active = True
        
    def convert_check(self):
        if not self.active:
            return False
        
        self.yards_to_convert = (self.field.absolute_yardline - self.target_yardline) * self.field.direction
        if (self.yards_to_convert <= 0):
            self.converted = True
            self.active = False
            return self.converted 
        elif (self.down == 4):
            self.active = False
            return self.active
        else:
            self.down += 1
            return self.down, self.yards_to_convert
        
#class Drive():
#    "State for drive"
#    def __init__(self, kickoff=False):

