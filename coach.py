'''
Created on Apr 20, 2013

@author: George
'''

from math import ceil
from random import randint, random, choice
from collections import namedtuple

class Coach():
    def __init__(self):
        self.skill = randint(60,90)
        self.play_probabilities = {}
        self.fg_dist_probabilities={}

    def practice_plays(self,playbook,skills):
#        results = namedtuple('PracticeResults',['id','runs','success','total_yardage','success_yardage','turnover'])
        for play in playbook:
            runs=[]
            success=0
            total_yardage=0
            success_yardage=0
            turnover=0
            if play.is_rush() or play.is_pass():
                for x in range(self.skill):
                    yds,trn = play.run(skills,{'dl':50,'lb':50,'cb':50,'s':50},0)
                    if trn:
                        turnover += 1
                        yds=-20
                    elif yds > 0:
                        success += 1
                        success_yardage += yds
                    runs.append(yds)
                total_yardage = sum(runs)
                self.play_probabilities[play.id]={k: (len([i for i in runs if i >= k])/float(len(runs)))*100 for k in range(1,41)}
            elif play.is_field_goal():
                    kicks=[]
                    for x in range((self.skill / 2)):
                        yds,trn = play.run(skills,{'sp':50},0)
                        kicks.append(yds)
                    max_dist = max(kicks)
                    self.fg_dist_probabilities={k: (len([i for i in kicks if i >= k])/float(len(kicks)))*100 for k in range(1,61)}

                        
    def call_play(self,available_plays,down_distance,score_difference,period,time_remaining,distance_to_endzone):
        ## 
        ## to sort list of namedtupes: 
        ## in place - list.sort(key=lambda tup: tup.success,reverse=True)
        ## sorted_list = sorted(list, key=lambda tup: tup.success,reverse=True)
        choices=[]
        success_rates = []
        play_choice=None
        target_yards=None
        down, dist = down_distance()
        if down in [1,2,3]:
            if down in [1,2]:
                target_yards=ceil(dist/2)
            elif down == 3:
                target_yards=dist
            for play in self.play_probabilities:
                if play in available_plays:
                    try:
                        success_rates.append(self.play_probabilities[play].get(target_yards))
                        choices.append(available_plays[play])
                    except:
                        pass
            if len(success_rates):
                avg=sum(success_rates)/len(success_rates)
                prob=[((item / avg) /len(success_rates)) for item in success_rates]
                
                r = random()
                running_total=0
                for step in prob:
#                    print running_total, r
                    if running_total < r < (running_total + step):
                        play_choice = choices[prob.index(step)]
                        break
                    running_total += step
        elif down == 4:
            try:
                if self.fg_dist_probabilities.get(distance_to_endzone()) >= 40:
                    for play in available_plays.values():
                        if play.is_field_goal():
                            play_choice=play
            except:
                pass
            if not play_choice:
                    for play in available_plays.values():
                        if play.is_punt():
                            play_choice=play
                            
#scoreDifference == -2 ||
#          scoreDifference == -5 ||
#          scoreDifference == -10 ||
#          scoreDifference == -16 ||
#          scoreDifference == -17 ||
#          scoreDifference == -18)
            
                    
        if not play_choice:
            play_choice = choice(available_plays.values())
            
        print play_choice.name
        return play_choice
        
        
        
        
                