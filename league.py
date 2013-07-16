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

from display import Display

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
        

class League():
    def __init__(self,
                 number_of_teams,
                 division_names=['PFL'],
                 nbr_playoff_teams=None):
        self.nbr_playoff_teams = nbr_playoff_teams
        self.playoff_field = []

        if number_of_teams < len(division_names):
            'Print number of teams cannot be less than number of divisions.'
            raise Exception
        
        self.teams =  [Team(choice(city_list),choice(nickname_list)) for t in range(number_of_teams)]
        self.team_dict = {team.id: team for team in self.teams}
##### human test
#        self.teams[0].human_control = True
        
        self.divisions=self.create_divisions(self.teams,len(division_names))
        
        self.schedule = Simple_Schedule().generate(self.divisions,True,1)
#        self.schedule = Home_Away_Random_Schedule().generate(self.teams)
        
        self.standings = dict(zip(division_names,self.divisions))

    def create_divisions(self,teams,nbr_div):
        divisions=[]
        t=len(teams)
        n=t/nbr_div
        r=t%nbr_div
        split_start=0
        split_end=0
        for x in xrange(nbr_div):
            split_end += n
            if r:
                split_end += 1
                r -= 1
            divisions.append(teams[split_start:split_end])
            split_start=split_end
        return divisions
        
    def _determine_pct(self,wins,losses,ties):
        return (wins + (ties / 2.0)) / (float(wins + losses + ties))
    
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
        elif home_game_stats['score'] > away_game_stats['score']:
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
        for week in self.schedule:
                for game in week:
                    game.start_game()
                    self.update_standings(game.get_home_team().statbook.stats,
                                          game.get_away_team().statbook.stats,
                                          game.get_home_team().team.id,
                                          game.get_away_team().team.id,
                                          game.get_home_team().team.league_stats,
                                          game.get_away_team().team.league_stats)
                    print game.get_away_team().team.city, game.get_away_team().statbook.stats['score']
                    print game.get_home_team().team.city, game.get_home_team().statbook.stats['score']
                    if game.in_overtime:
                        print (game.period-game.number_of_periods), 'OT'
                    print
            
                self.print_standings()
        
        if self.nbr_playoff_teams:   
            self.play_playoffs()

    def play_playoffs(self):
        self.determine_playoff_field()
        round = 0
        
        current_field = self.playoff_field
        
        while len(current_field) > 1:
            round += 1
            print '\nRound', round
            current_field = self.generate_playoff_schedule(current_field)
        
        print 'Champion\n', current_field[0].city, current_field[0].nickname
        
                
    def determine_playoff_field(self):
        division_winners=[]
        wild_card=[]
        for div in self.standings.values():
            division_winners.append(div[0])
            wild_card.extend(div[1:])
            
        division_winners.sort(reverse=True, key=lambda t: t.league_stats['overall']['pct'])
        wild_card.sort(reverse=True, key=lambda t: t.league_stats['overall']['pct'])

        self.playoff_field = division_winners + wild_card
        self.playoff_field = self.playoff_field[:self.nbr_playoff_teams]

    def generate_playoff_schedule(self,current_field):
        current_round_teams=[]
        next_round_teams=[]
        s=2
        c=1
        while s > 1:
            c *= 2
            s=len(current_field) / c
        r = len(current_field) % c
        
        if r:
            cf_deque=deque(current_field)
            cf_deque.rotate(r*2)
            for x in xrange(r*2):
                current_round_teams.append(cf_deque.popleft())
            next_round_teams.extend(cf_deque)
        else:
            current_round_teams=current_field

        round_games=[]
        for x in xrange(len(current_round_teams)/2):
            round_games.append(Game(current_round_teams[x],current_round_teams[-x-1],use_overtime=True,number_of_overtime_periods=0))
        
        for game in round_games:
            if game.home.human_control or game.away.human_control:
                game.display=Display
            game.start_game()
            print game.get_away_team().team.city, game.get_away_team().statbook.stats['score']
            print game.get_home_team().team.city, game.get_home_team().statbook.stats['score']
            if game.in_overtime:
                print (game.period-game.number_of_periods), 'OT'
            print
            
            next_round_teams.append(game.get_winner())
            
        next_round_teams.sort(reverse=True, key=lambda t: t.league_stats['overall']['pct'])
        return next_round_teams


    def sort_standings(self):
        for div in self.standings.values():
            div.sort(reverse=True, key=lambda t: t.league_stats['overall']['pct'])

    def get_max_width(self, table, index):
        """
        Get the maximum width of the given column index
        from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
        """
        return max([len(row[index]) for row in table])

    def print_standings(self):
        for div in self.standings:
            table=[[div,
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
                   str(s.league_stats['away']['pct'])] for s in self.standings[div]])
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
        games = [Game(t1,t2) for t1 in teams for t2 in teams if t1.id != t2.id]

        for game in games:
            if game.home.human_control or game.away.human_control:
                game.display=Display

        schedule =[]        
        nbr_weeks = len(games) / len(teams)
        r = len(games) % len(teams)
        split_start=0
        split_end=0
        for x in xrange(nbr_weeks):
            split_end += nbr_weeks
            if r:
                split_end += 1
                r -= 1
            schedule.append(games[split_start:split_end])
            split_start=split_end
        shuffle(schedule)
        
        return schedule
        
class Simple_Schedule(Schedule):
    def generate(self,
                 league,
                 overtime,
                 overtime_length):
        # @TODO add variables to easily set overtime
        schedule = []
        for division in league:
            anchor_team = None
            # 'balanced' will contain 1 if even number of teams,, 0 if odd
            # used later to calculate number of weeks needed, since odd
            # numbered divisions require an extra week due to each team having a bye
            balanced = 1 - (len(division) % 2)
            nbr_weeks = len(division) - balanced
            max_weeks = 2 * nbr_weeks
            try:
                schedule[max_weeks]
            except:
                for x in xrange(max_weeks - len(schedule)):
                    schedule.append([])
            ## gpw is games per week
            gpw = len(division) / 2
            rotation1 = deque(division[:gpw])
            rotation2 = deque(division[gpw:])
            if balanced:
                anchor_team = rotation1.popleft()
            for week in range(nbr_weeks):
                if anchor_team:
                    schedule[week].append(Game(anchor_team, rotation2[-1],
                                          use_overtime=overtime,
                                          number_of_overtime_periods=overtime_length)) 
                    schedule[week+nbr_weeks].append(Game(rotation2[-1], anchor_team,
                                                    use_overtime=overtime,
                                                    number_of_overtime_periods=overtime_length))
                for t1, t2 in zip(rotation1,rotation2):
                    schedule[week].append(Game(t1,t2,
                                          use_overtime=overtime,
                                          number_of_overtime_periods=overtime_length))
                    schedule[week+nbr_weeks].append(Game(t2,t1,
                                                    use_overtime=overtime,
                                                    number_of_overtime_periods=overtime_length))

                rotation1.append(rotation2.pop())
                rotation2.appendleft(rotation1.popleft())
        
        for week in schedule:
            for game in week:
                if game.home.human_control or game.away.human_control:
                    game.display=Display        
        
        shuffle(schedule)
        return schedule
    
##### testing

l=League(64,['Group ' + x for x in 'ABCDEFGH'],12)
l.play_season()
