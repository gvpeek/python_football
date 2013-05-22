'''
Created on Apr 29, 2013

@author: George
'''

import csv
import abc

from math import ceil
from random import choice, shuffle
from collections import namedtuple, deque
from sys import stdout

from team import Team
from game import Game

'''
Initialize Cities and Nicknames
'''
cities=[]
city_list=[]
City = namedtuple('City',['name','state','pro','semipro','amateur','region','division'])

nicknames=[]
nickname_list=[]
Nickname = namedtuple('Nickname',['name','pro','semipro']) #,'state','divisions'])

with open('csv_source_files\metroareas.csv', 'r') as cities_file:
    cities_reader = csv.reader(cities_file,delimiter=',')
    for c in cities_reader:
        cities.append(City(*c))
        city_list.append(c[0])
    
    
with open(r'csv_source_files\nicknames.csv', 'r+b') as nicknames_file:
    nickname_reader = csv.reader(nicknames_file,delimiter=',')
    for n in nickname_reader:
        nicknames.append(Nickname(*n[0:3]))
        nickname_list.append(n[0])
        
print city_list
print nickname_list


class League():
    def __init__(self,number_of_teams):
        self.teams = {team.id: team for team in [Team(choice(city_list),choice(nickname_list)) for t in range(number_of_teams)]}
        print self.teams
        
        self.schedule = Home_Away_Random_Schedule().generate(self.teams)
        
        self.standings = [t for t in self.teams.values()]
        print self.standings
        
    def _determine_pct(self,wins,losses,ties):
        return (wins + ties) / (float(wins + losses + ties))
    
    def update_standings(self,
                         home_game_stats,
                         away_game_stats,
                         home_team_id,
                         away_team_id,
                         home_league_stats,
                         away_league_stats):
        if home_game_stats['score'] == away_game_stats['score']:
            home_league_stats['overall']['ties'] += 1
            away_league_stats['overall']['ties'] += 1
            home_league_stats['home']['ties'] += 1
            away_league_stats['away']['ties'] += 1
        if home_game_stats['score'] > away_game_stats['score']:
            home_league_stats['overall']['wins'] += 1
            home_league_stats['home']['wins'] += 1
            home_league_stats['win_opp'].append(away_team_id)
            away_league_stats['overall']['losses'] += 1
            away_league_stats['away']['losses'] += 1
            away_league_stats['loss_opp'].append(home_team_id)
        else:
            home_league_stats['overall']['losses'] += 1
            home_league_stats['home']['losses'] += 1
            home_league_stats['loss_opp'].append(away_team_id)
            away_league_stats['overall']['wins'] += 1
            away_league_stats['away']['wins'] += 1
            away_league_stats['win_opp'].append(home_team_id)
        
        home_league_stats['overall']['points'] += home_game_stats['score']
        home_league_stats['overall']['opp'] += away_game_stats['score']
        home_league_stats['home']['points'] += home_game_stats['score']
        home_league_stats['home']['opp'] += away_game_stats['score']
        away_league_stats['overall']['points'] += away_game_stats['score']
        away_league_stats['overall']['opp'] += home_game_stats['score']
        away_league_stats['away']['points'] += away_game_stats['score']
        away_league_stats['away']['opp'] += home_game_stats['score']
        
        home_league_stats['overall']['pct'] =  self._determine_pct(home_league_stats['overall']['wins'], home_league_stats['overall']['losses'], home_league_stats['overall']['ties'])
        home_league_stats['home']['pct'] =  self._determine_pct(home_league_stats['home']['wins'], home_league_stats['home']['losses'], home_league_stats['home']['ties'])
        away_league_stats['overall']['pct'] =  self._determine_pct(away_league_stats['overall']['wins'], away_league_stats['overall']['losses'], away_league_stats['overall']['ties'])
        away_league_stats['away']['pct'] =  self._determine_pct(away_league_stats['away']['wins'], away_league_stats['away']['losses'], away_league_stats['away']['ties'])
        
        
        self.sort_standings()
            
    def play_season(self):
        for game in self.schedule:
            game.start_game()
            self.update_standings(game.get_home_team().statbook.stats,
                                  game.get_away_team().statbook.stats,
                                  game.get_home_team().team.id,
                                  game.get_away_team().team.id,
                                  game.get_home_team().team.league_stats,
                                  game.get_away_team().team.league_stats)
            print game.get_away_team().team.city, game.get_away_team().statbook.stats['score']
            print game.get_home_team().team.city, game.get_home_team().statbook.stats['score']
            if game.overtime:
                print 'OT'
            print
            
            if (self.schedule.index(game) + 1) % len(self.teams) == 0:
                self.print_standings()

    def sort_standings(self):
        self.standings.sort(reverse=True, key=lambda t: t.league_stats['overall']['pct'])

    def get_max_width(self, table, index):
        """
        Get the maximum width of the given column index
        from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
        """
        return max([len(row[index]) for row in table])

    def print_standings(self):
        table=[[' ',
               'W',
               'L',
               'T',
               'Pct.',
               'HW',
               'HL',
               'HT',
               'HPct.',
               'AW',
               'AL',
               'AT',
               'APct.'
               ]]
        table.extend([[s.city + ' ' + s.nickname,
               str(s.league_stats['overall']['wins']),
               str(s.league_stats['overall']['losses']),
               str(s.league_stats['overall']['ties']),
               str(s.league_stats['overall']['pct']),
               str(s.league_stats['home']['wins']),
               str(s.league_stats['home']['losses']),
               str(s.league_stats['home']['ties']),
               str(s.league_stats['home']['pct']),
               str(s.league_stats['away']['wins']),
               str(s.league_stats['away']['losses']),
               str(s.league_stats['away']['ties']),
               str(s.league_stats['away']['pct'])] for s in self.standings])
#            print '{} {} \t {}-{}-{} {:.3f}'.format(s.city,
#                                       s.nickname,
#                                       s.league_stats['overall']['wins'],
#                                       s.league_stats['overall']['losses'],
#                                       s.league_stats['overall']['ties'],
#                                       s.league_stats['overall']['pct'])
        '''
        below from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
        '''
        col_paddings = []
        
        for i in range(len(table[0])):
            col_paddings.append(self.get_max_width(table, i))

        for row in table:
            # left col
            print >> stdout, row[0].ljust(col_paddings[0] + 1),
            # rest of the cols
            for i in range(1, len(row)):
                col = row[i].rjust(col_paddings[i] + 2)
                print >> stdout, col,
            print >> stdout
        print 


class Schedule():
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generate(self,team):
        return

class Home_Away_Random_Schedule(Schedule):
    def generate(self,teams):
        schedule = [Game(t1,t2) for t1 in teams.values() for t2 in teams.values() if t1.id != t2.id]
        shuffle(schedule)
        
        return schedule
        
class Simple_Schedule(Schedule):
    def generate(self,teams):
        anchor_team = None
        schedule = {}
        week = 0
        ## gpw is games per week
        gpw = int(ceil(len(teams) / 2.0))
        rotation1 = deque(teams[:gpw])
        rotation2 = deque(teams[-gpw:])
        if len(teams) % 2 == 0:
            anchor_team = rotation1.popleft()
        for i in range(len(teams) - 1):
            week += 1
            schedule[week] = [(anchor_team, rotation2[-1])] + zip(rotation1,rotation2)
            rotation1.append(rotation2.pop())
            rotation2.appendleft(rotation1.popleft())
            # print anchor_team, rotation1, rotation2
        return schedule

##### testing

l=League(20)
l.play_season()
