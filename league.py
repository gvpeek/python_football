'''
Created on Apr 29, 2013

@author: George
'''

import csv
from random import choice
from collections import namedtuple

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

teams = {team.id: team for team in [Team(choice(city_list),choice(nickname_list)) for t in range(8)]}

print teams

standings = [{teams[t].city: teams[t].league_stats} for t in teams]
print standings

def update_standings(home,away):
    if game.get_home_team().statbook.stats['score'] == game.get_away_team().statbook.stats['score']:
        home.team.league_stats['ties'] += 1
        away.team.league_stats['ties'] += 1
    if game.get_home_team().statbook.stats['score'] > game.get_away_team().statbook.stats['score']:
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
        
games = [Game(t1,t2) for t1 in teams.values() for t2 in teams.values() if t1.id != t2.id]
for game in games:
    game.start_game()
    update_standings(game.get_home_team(),game.get_away_team())
    print game.get_home_team().team.city, game.get_home_team().statbook.stats['score']
    print game.get_away_team().team.city, game.get_away_team().statbook.stats['score']
    print
    
standings.sort(reverse=True, key=lambda t: t.values()[0]['pct'])
for s in standings:
    print s
