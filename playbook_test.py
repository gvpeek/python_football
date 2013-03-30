'''
Created on Mar 25, 2013

@author: George
'''

from play import Team


t1=Team('Chicago','Bears')
t2=Team('Arizona','Cardinals')

print t1.skills
print t2.skills


count=0.0
turnover_ctr=0.0

for i in range(1,20):
    for play in t1.playbook:
        count+=1
        off_yd, turnover, ret_yd = play.run(t1.skills,t2.skills,0)
        if turnover:
            turnover_ctr +=1
        print play.id, play.name, '--', off_yd, turnover, ret_yd
print count, turnover_ctr/count
        
print

count=0.0
turnover_ctr=0.0

for i in range(1,20):
    for play in t2.playbook:
        count+=1
        off_yd, turnover, ret_yd = play.run(t2.skills,t1.skills,t1.home_field_advantage)
        if turnover:
            turnover_ctr +=1
        print play.id, play.name, '--',  off_yd, turnover, ret_yd
print count, turnover_ctr/count