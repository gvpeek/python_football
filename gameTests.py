'''
Created on Jan 13, 2012

@author: George
'''

from random import choice

def coin_flip(side_choice):
    won_toss = False
    side_options = ['Heads','Tails']
    flip_result = choice(side_options)
    if flip_result == side_choice:
        won_toss = True
    return won_toss

for i in range(50):
    x=coin_flip('Heads')
    print x