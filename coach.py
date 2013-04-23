'''
Created on Apr 20, 2013

@author: George
'''

from random import randint
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
                self.play_probabilities[play.id]={k: (len([i for i in runs if i >= k])/float(len(runs)))*100 for k in range(1,31)}
            elif play.is_field_goal():
                    kicks=[]
                    for x in range((self.skill / 2)):
                        yds,trn = play.run(skills,{'sp':50},0)
                        kicks.append(yds)
                    max_dist = max(kicks)
                    self.fg_dist_probabilities={k: (len([i for i in kicks if i >= k])/float(len(kicks)))*100 for k in range(1,51)}

                        
    def call_play(self,available_plays):
        ## to sort list of namedtupes: 
        ## in place - list.sort(key=lambda tup: tup.success,reverse=True)
        ## sorted_list = sorted(list, key=lambda tup: tup.success,reverse=True)
        pass
                