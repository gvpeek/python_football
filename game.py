'''
Created on Mar 1, 2012

@author: George Peek
'''

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

def determine_position(position, yardage, reverse_direction=False):
    position['in_home_endzone'] = False
    position['in_away_endzone'] = False
    
    if reverse_direction:
        direction = position['direction'] * -1
    else:
        direction = position['direction']
    position['absolute_yardline'] += (yardage * direction)
    
    if position['absolute_yardline'] > 50:
        position['converted_yardline'] = 100 - position['absolute_yardline']
        if position['absolute_yardline'] >= 100:
            position['in_away_endzone'] = True
    else:
        position['converted_yardline'] = position['absolute_yardline']
        if position['absolute_yardline'] <= 0:
            position['in_home_endzone'] = True
    print 'yardline', position['absolute_yardline'], 'direction', position['direction'], 'home_ez', position['in_home_endzone'], 'away_ez', position['in_away_endzone']
