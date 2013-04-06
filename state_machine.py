'''
Created on Aug 19, 2012

@author: George Peek
'''

import pprint


#from game import Play
from timekeeping import Clock

class State():
    "Basic State"
    def __init__(self,field,change_possession,get_offense,downs_to_convert = 4, yards_to_convert = 10.0):
        self.active = True
        self.field = field
        self.change_possession = change_possession
        self.get_offense = get_offense
        self.downs_to_convert = downs_to_convert
        self.yards_to_convert = yards_to_convert
    
    def check_state(self):
        print 'check_state'
        return Kickoff(self.field,
                       self.change_possession,
                       self.get_offense)

#        if game.field.in_away_endzone:
#            if game.field.direction == 1:
#                if isinstance(self, Conversion):
#                    self.active = False
#                    game.scoreboard.home_conversion_play()
#                    game.current_state = Kickoff(game)
#                else:
#                    if game.plays[-1].touchback:
#                        print 'Away touchback'
#                        game.field.touchback_set()
#                        game.current_state = DownSet(game)
#                    else:
#                        print 'Home touchdown'
#                        game.scoreboard.home_touchdown()
#                        game.current_state = Conversion(game)
#            elif game.field.direction == -1:
#                print 'Home safety'
#                game.scoreboard.home_safety()
#                game.current_state = Kickoff(game, True)
#        elif game.field.in_home_endzone:
#            if game.field.direction == -1: 
#                if isinstance(self, Conversion):
#                    self.active = False
#                    game.scoreboard.away_conversion_play()
#                    game.current_state = Kickoff(game)
#                else:
#                    if game.plays[-1].touchback:
#                        print 'Home touchback'
#                        game.field.touchback_set()
#                        game.current_state = DownSet(game)
#                    else:
#                        print 'Away touchdown'
#                        game.scoreboard.away_touchdown()
#                        game.current_state = Conversion(game)
#            elif game.field.direction == 1:
#                print 'Away safety'
#                game.scoreboard.away_safety()
#                game.current_state = Kickoff(game, True)               
#        elif isinstance(self, Conversion):
#            self.active = False
#            if game.plays[-1].kick_successful:
#                if game.field.direction == 1:
#                    game.scoreboard.home_conversion_kick()
#                elif game.field.direction == -1:
#                    game.scoreboard.away_conversion_kick()
#            game.current_state = Kickoff(game)
#        elif isinstance(self, Kickoff):
#            self.active = False
#            game.current_state = DownSet(game)
#        elif isinstance(self, DownSet):
#            if game.plays[-1].punt_attempt:
#                self.active = False
#                game.current_state = DownSet(game)
#            elif game.plays[-1].field_goal_attempt:
#                if game.plays[-1].kick_successful == True:
#                    self.active = False
#                    if game.field.direction == 1:
#                        game.scoreboard.home_field_goal()
#                    elif game.field.direction == -1:
#                        game.scoreboard.away_field_goal()
#                    game.current_state = Kickoff(game)
#                else:
#                    game.current_state = DownSet(game)
#            elif game.plays[-1].turnover:
#                self.active = False
#                game.current_state = DownSet(game)               
#            else:
#                self.convert_check()
#                if self.converted:
#                    game.current_state = DownSet(game)
#                elif not self.active:
#                    game.plays[-1].change_of_possession = True
#                    game.field.direction *= -1
#                    game.current_state = DownSet(game)
#        
#        if game.plays[-1].change_of_possession:
#            game.possession[0], game.possession[1] = game.possession[1], game.possession[0]
#
#        if not isinstance(game.current_state, Conversion):
#            game.scoreboard.clock = str(game.current_clock.run_clock())[2:7]
#            if not game.current_clock.time_remaining:
#                if game.timekeeping:
#                    if game.number_of_periods / game.period == 2:
#                        game.end_of_half = True
#                    game.period += 1
#                    game.scoreboard.period = game.period
#                    game.current_clock = game.timekeeping.pop()
#                    game.scoreboard.clock = str(game.current_clock.time_remaining)[2:7]
#                else:
#                    game.end_of_regulation = True
#                    print 'outof timekeeping'
#                    if game.scoreboard.home_score == game.scoreboard.away_score: 
#                        if not game.overtime:
#                            game.overtime = True
#                            game.coin_flip()
#                            game.current_state = Kickoff(game)
#                    if game.overtime:
#                        print 'in overtime'
#                        game.period += 1
#                        game.scoreboard.period = game.period
#                        game.current_clock = Clock()
#                        game.scoreboard.clock = str(game.current_clock.time_remaining)[2:7]
#
#        if game.end_of_half and not isinstance(game.current_state, Conversion):
#            game.set_second_half()
#            game.current_state = Kickoff(game)
#            game.end_of_half = False
#
#        if (game.end_of_regulation and not game.overtime) or (game.overtime and game.scoreboard.home_score != game.scoreboard.away_score):                    
#            game.end_of_game = True
#            game.current_state = EndOfGame(game)
#                    
# 
#        print 'scoreboard'
#        game.scoreboard.absolute_yardline = str(game.field.absolute_yardline)
#        game.scoreboard.converted_yardline = str(game.field.converted_yardline)
#        game.scoreboard.play_name = game.plays[-1].play_call.name
#        game.scoreboard.offense_yardage = game.plays[-1].offense_yardage
#        game.scoreboard.return_yardage = game.plays[-1].return_yardage
#        game.scoreboard.turnover =  game.plays[-1].turnover
##        game.scoreboard.play_rating = game.plays[-1].play_rating
#        if isinstance(game.current_state,DownSet):
#            game.scoreboard.down = game.current_state.down
#            if 0 < game.current_state.target_yardline < 100:
#                game.scoreboard.yards_to_go = game.current_state.yards_to_convert
#            else:
#                game.scoreboard.yards_to_go ='Goal'
#        else:
#            game.scoreboard.down = ''
#            game.scoreboard.yards_to_go = ''
#        
##        pprint.pprint(vars(game.current_state))
##        pprint.pprint(vars(game.field))
#        
#       
#        game.field.play_reset()
#        game.plays.append(Play(game.possession[0],game.possession[1],game.field))
    
#    def check_score(self):


class Kickoff(State):
    "State for kickoffs"
    def __init__(self,*args):
        State.__init__(self,*args)
        self.setup()
        
    def setup(self):
        self.field.kickoff_set()
        
    def check_state(self,events):
        self.change_possession()
        if events.get('away_touchdown') or events.get('away_touchdown'):
            self.field.conversion_set() 
            next_state = Conversion(self.field,
                                    self.change_possession,
                                    self.get_offense)
        
        elif events.get('touchback'):
            self.field.touchback_set()
            next_state = DownSet(self.field,
                                 self.change_possession,
                                 self.get_offense)
        return next_state

class FreeKick(State):
    "State for free kickoffs"
    def __init__(self,*args):
        State.__init__(self,*args)
        self.setup()
        
    def setup(self):
        self.field.free_kick_set()
     
        
class DownSet(State):
    "State for normal offensive possession"
    def __init__(self, *args):
        State.__init__(self,*args)
        self.play_choice = ['run_inside', 'run_outside', 'pass_short', 'pass_medium', 'pass_long', 'field_goal', 'punt', 'run_clock']
        self.down = 1
        self.target_yardline = self.field.absolute_yardline + (self.yards_to_convert * self.get_offense().direction) 
        self.converted = False
        self.active = True
        
    def convert_check(self,direction,current_yardline):
        if not self.active:
            return False
        
        self.yards_to_convert = (self.target_yardline - current_yardline) * direction
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
