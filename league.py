'''
Created on Apr 29, 2013

@author: George
'''

import csv
import abc

from math import ceil
from random import choice, shuffle
from collections import namedtuple, deque

from team import Team
from game import Game

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
        
        self.standings = [{self.teams[t].city + ' ' + self.teams[t].nickname : self.teams[t].league_stats} for t in self.teams]
        print self.standings
        
    def update_standings(self,home,away):
        if home.statbook.stats['score'] == away.statbook.stats['score']:
            home.team.league_stats['ties'] += 1
            away.team.league_stats['ties'] += 1
        if home.statbook.stats['score'] > away.statbook.stats['score']:
            home.team.league_stats['wins'] += 1
            home.team.league_stats['win_opp'].append(away.team.id)
            away.team.league_stats['losses'] += 1
            away.team.league_stats['loss_opp'].append(home.team.id)
        else:
            home.team.league_stats['losses'] += 1
            home.team.league_stats['loss_opp'].append(away.team.id)
            away.team.league_stats['wins'] += 1
            away.team.league_stats['win_opp'].append(home.team.id)
        
        home.team.league_stats['points'] += home.statbook.stats['score']
        home.team.league_stats['opp'] += away.statbook.stats['score']
        away.team.league_stats['points'] += away.statbook.stats['score']
        away.team.league_stats['opp'] += home.statbook.stats['score']
        
        home.team.league_stats['pct'] =  (home.team.league_stats['wins'] + home.team.league_stats['ties']) / float(home.team.league_stats['wins'] + home.team.league_stats['losses'] + home.team.league_stats['ties'])
        away.team.league_stats['pct'] =  (away.team.league_stats['wins'] + away.team.league_stats['ties']) / float(away.team.league_stats['wins'] + away.team.league_stats['losses'] + away.team.league_stats['ties'])
        
        self.sort_standings()
            
    def play_season(self):
        for game in self.schedule:
            game.start_game()
            self.update_standings(game.get_home_team(),game.get_away_team())
#            print game.get_away_team().team.city, game.get_away_team().statbook.stats['score']
#            print game.get_home_team().team.city, game.get_home_team().statbook.stats['score']
#            if game.overtime:
#                print 'OT'
#            print
            
            if (self.schedule.index(game) + 1) % len(self.teams) == 0:
                self.print_standings()

    def sort_standings(self):
        self.standings.sort(reverse=True, key=lambda t: t.values()[0]['pct'])

    def print_standings(self):
        for s in self.standings:
            print s
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

l=League(17)
l.play_season()
