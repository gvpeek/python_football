'''
Created on Jan 7, 2012

@author: George Peek
'''

from math import ceil, floor, pow
from random import randint, choice

off = 90

ratingQB = off
ratingRB = off
ratingWR = off
ratingOL = off
ratingSP1 = off

dfc = 75

ratingDL = dfc
ratingLB = dfc
ratingCB = dfc
ratingS = dfc
ratingSP2 = dfc

success = 0
fail = 0
#play = raw_input('Select Play:')
plays = ['RI','RO','PS','2PRI','2PRO','2PPS','PM','PL','K','OK','PUNT','FG','XP']

print ratingQB, ratingRB, ratingWR, ratingOL
print ratingDL, ratingLB, ratingCB, ratingS

def determineYardageGain(play,playRating):
    rnd = randint(1,100)
    if play in ['RI','RO','PS','2PRI','2PRO','2PPS']:
        gain = floor(((playRating*100)*pow(rnd,-.7)) / 100)
    elif play == 'PM':
        gain = floor(((playRating*100)*pow(rnd,-.5)) / 100)
    elif play == 'PL':
        gain = floor(((playRating*100)*pow(rnd,-.4)) / 100)
    else:
        gain =  'Invalid play type!'
    return gain

def determineYardageLoss(play,playRating):
    rnd = randint(1,100)
    lossRating = ((90 - playRating) + 60)
    if play in ['RI','RO','PS','2PRI','2PRO','2PPS']:
        loss = floor(((lossRating*100)*pow(rnd,-1)) / 100)
        if loss > 5:
            loss= 5
    elif play == 'PM':
        loss = floor(((lossRating*100)*pow(rnd,-.8309)) / 100)
        if loss > 8:
            loss= 8
    elif play == 'PL':
        loss = floor(((lossRating*100)*pow(rnd,-.5)) / 100)
        if loss > 12:
            loss= 12
    else:
        loss =  'Invalid play type!'
    return loss 

def determineTurnover(play,playRating):
    changeOfPossession = False
    rnd = randint(1,100)
    if rnd <= ((100 - playRating) / 3.5):
        changeOfPossession = True
    return changeOfPossession

for i in range(100):
    play = choice(plays)
    print play
    rnd = randint(1,101)
    if play in ['RI','2PRI']:
        offRating = ceil(((ratingQB + ratingRB*4 + ratingOL*5) / 10))
        defRating = ceil((((ratingDL*6 + ratingLB*3 + ratingS) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['RO','2PRO']:
        offRating = ceil(((ratingQB + ratingRB*5 + ratingWR + ratingOL*3) / 10))
        defRating = ceil((((ratingDL*3 + ratingLB*5 + ratingCB + ratingS) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['PS','2PPS']:
        offRating = ceil(((ratingQB*4 + ratingRB*2 + ratingWR*3 + ratingOL) / 10))
        defRating = ceil((((ratingDL + ratingLB*5 + ratingCB*3 + ratingS) / 10) - 60) / 4)
        playPenalty = 0
    elif play == 'PM':
        offRating = ceil(((ratingQB*4 + ratingWR*4 + ratingOL*2) / 10))
        defRating = ceil((((ratingDL*2 + ratingLB*2 + ratingCB*4 + ratingS*2) / 10) - 60) / 4)
        playPenalty = 0
    elif play == 'PL':
        offRating = ceil(((ratingQB*4 + ratingWR*3 + ratingOL*3) / 10))
        defRating = ceil((((ratingDL*3 + ratingLB + ratingCB*3 + ratingS*3) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['K','OK','PUNT','FG','XP']:
        print 'specTeamPlay'
        offRating = ratingSP1
        defRating = ceil((ratingSP2 - 60) / 4)
        playPenalty = 0
    
    playRating = ((offRating - defRating) - playPenalty)
    if rnd <= playRating:
        success += 1
        playSuccess=True
        netYardsOnPlay=determineYardageGain(play,playRating)
        print 'Yards Gained', netYardsOnPlay
    else:
        fail += 1
        playSuccess=False
        changeOfPossession = determineTurnover(play,playRating)
        if changeOfPossession:
            print 'Turnover!'
        else:
            netYardsOnPlay=determineYardageLoss(play,playRating)
            print 'Yards Lost', netYardsOnPlay
    
#    if playRating < 60:
#        playRating = 60
print 'Success', success
print 'Fail', fail
print offRating
print defRating    
print playRating