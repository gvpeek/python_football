'''
Created on Aug 19, 2012

@author: George Peek
'''

from play import Play

class State():
    "Basic State"
    def __init__(self):
        pass
    
#    def check_score(self):


class Kickoff(State):
    "State for kickoffs"
    def __init__(self):
        self.play_choice = ['kickoff','onside_kickoff']
        self.play = Play()
        self.active = True
        
    def determine_transition(self):
        self.active = False
        self.get_next_state()
        
class Drive(State):
    "State for normal offensive possession"
    def __init__(self):
        self.play_choice = ['run_clock', 'run_inside', 'run_outside', 'pass_short', 'pass_medium', 'pass_long', 'field_goal', 'punt']

class DownSet(State):
    "State for normal offensive possession"
    def __init__(self,downs_to_convert = 4, yards_to_convert = 10, field):
        self.down = 1
        self.downs_to_convert = downs_to_convert
        self.yards_to_convert = yards_to_convert
        self.target_yardline = field.absolute_yardline + (yards_to_convert * field.direction) 
        self.converted = False
        self.active = True
        
    def convert_check(self,playResult):
        if not self.active:
            return False
        
        self.yards_to_convert -= playResult
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
