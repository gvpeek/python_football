'''
Created on Jan 7, 2012

@author: George Peek
'''

from math import ceil, floor, pow
from random import randint, choice

#off = 90
off = randint(60,90)

ratingQB = off
ratingRB = off
ratingWR = off
ratingOL = off
ratingSP1 = off

#dfc = 75
dfc = randint(60,90)

ratingDL = dfc
ratingLB = dfc
ratingCB = dfc
ratingS = dfc
ratingSP2 = dfc

success = 0
fail = 0
netYardsOnPlay = 0
#play = raw_input('Select Play:')
plays = ['RI','RO','PS','2PRI','2PRO','2PPS','PM','PL','RC','K','OK','PUNT','FG','XP']

print ratingQB, ratingRB, ratingWR, ratingOL
print ratingDL, ratingLB, ratingCB, ratingS

def determinePlayResult(play):
    turnover = False
    netYardsOnPlay = 0 
    fieldGoalSuccess = False
    fieldGoalAttempt = False
    playRnd = randint(1,100)
    playRating = determinePlayRating(play)
    if play == 'RC':
        netYardsOnPlay = -2
    elif play in ['K','OK']:
        kickoffYardage = determineKickoffYardage(play,playRating)
        ##TODO: determine position
        ##TODO: if not touchback
        returnYardage = determineReturnYardage(play)
        print 'kick', kickoffYardage, 'return', returnYardage
        netYardsOnPlay = kickoffYardage - returnYardage
#    elif play == 'PUNT':
#        punt block & return Yardage if blocked
#        puntYardage = determinePuntYardage(play,playRating)
#        returnYardage = determineReturnYardage(play)
#        netYardsOnPlay = puntYardage - returnYardage
    elif play in ['FG','XP']:
        fieldGoalAttempt = True
        ## Testing
        if play == 'FG':
            convertedYardline = randint(1,70)
        elif play == 'XP':
            convertedYardline = 2
        print convertedYardline, 'yardline'
        ## Testing
        fieldGoalSuccess = determineFieldGoalResult(play,playRating,convertedYardline)
    else: 
        if playRnd <= playRating:
            playSuccess=True
        else:
            playSuccess=False
            turnover = determineTurnover(play,playRating)
            
        if not turnover:
            netYardsOnPlay=determinePlayYardage(play,playRating,playSuccess)
        else:
            netYardsOnPlay = (determinePlayYardage(play,playRating,playSuccess) - determineReturnYardage(play))
    return netYardsOnPlay, fieldGoalAttempt, fieldGoalSuccess

def determinePlayYardage(play,playRating,playSuccess):
    rnd = randint(1,100)
    lossRating = ((90 - playRating) + 60)
    if play in ['RI','RO','PS','2PRI','2PRO','2PPS']:
        if playSuccess:
            yardage = floor(((playRating*100)*pow(rnd,-.7)) / 100)
        else:
            yardage = -(floor(((lossRating*100)*pow(rnd,-1)) / 100))
            if yardage < -5:
                yardage= -5
    elif play == 'PM':
        if playSuccess:
            yardage = floor(((playRating*100)*pow(rnd,-.5)) / 100)
        else:
            yardage = -(floor(((lossRating*100)*pow(rnd,-.8309)) / 100))
            if yardage < -8:
                yardage= -8
    elif play == 'PL':
        if playSuccess:
            yardage = floor(((playRating*100)*pow(rnd,-.4)) / 100)
        else:
            yardage = -(floor(((lossRating*100)*pow(rnd,-.5)) / 100))
            if yardage < -12:
                yardage= -12
    else:
        print 'Delay of game!'
        yardage = -5
    return yardage

def determineTurnover(play,playRating):
    changeOfPossession = False
    turnoverRnd = randint(1,100)
    if play in ['RI','2PRI','RO','2PRO']:
        if turnoverRnd <= ((100 - playRating) / 3.5):
            changeOfPossession = True
    elif play in ['PS','2PPS']:
        if turnoverRnd <= ((100 - playRating) / 10):
            changeOfPossession = True
    elif play == 'PM':
        if turnoverRnd <= (((100 - playRating) / 10) * 2):
            changeOfPossession = True
    elif play == 'PL':
        if turnoverRnd <= (((100 - playRating) / 10) * 2):
            changeOfPossession = True
    return changeOfPossession

def determineFieldGoalResult(play,playRating,distance):
    if play == 'FG':
        fgRnd = randint(1,110)
    elif play == 'XP':
        fgRnd = randint(1,100)
    
    fgRating = ((80 - playRating) / 2)
    
    if fgRnd < ((100 - distance) - fgRating):
        return True
    else:
        return False

def determineKickoffYardage(play,playRating):
    if play == 'K':
        kickRnd = randint(1,20) + 55
    elif play == 'OK':
        kickRnd = randint(1,15) + 10
    kickRating = (80 - playRating) / 2
    kickYardage = ceil(kickRnd - kickRating)
    return kickYardage

def determineReturnYardage(play):
    returnRnd = randint(1,100)
    if play in ['RI','2PRI','RC']:
        returnYards = floor(((ratingDL*100)*pow(returnRnd,-1)) / 100)
    elif play in ['RO','2PRO']:
        returnYards = floor(((ratingLB*100)*pow(returnRnd,-1)) / 100)
    elif play in ['PS','2PPS']:
        returnYards = floor(((ratingLB*100)*pow(returnRnd,-.8)) / 100)
    elif play in ['PM']:
        returnYards = floor(((ratingCB*100)*pow(returnRnd,-.7)) / 100)
    elif play in ['PL']:
        returnYards = floor(((ratingS*100)*pow(returnRnd,-.6)) / 100)
    elif play == 'K':
        returnYards = floor(((ratingSP2*125)*pow(returnRnd,-.4)) / 100)
    elif play == 'OK':
        returnYards = floor(((ratingSP2*100)*pow(returnRnd,-1)) / 100)
    elif play == 'PUNT':
        returnYards = floor(((ratingSP2*100)*pow(returnRnd,-.6)) / 100)
    return returnYards

def determinePlayRating(play):
    if play in ['RI','2PRI','RC']:
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
    elif play in ['FG','XP','K','OK','PUNT']:
        offRating = ratingSP1
        defRating = ceil((ratingSP2 - 60) / 4)
        playPenalty = 0
    playRating = ((offRating - defRating) - playPenalty)
#    if playRating < 60:
#        playRating = 60
    ##Testing
    print offRating
    print defRating    
    print playRating
    ##Testing
    return playRating
    
for i in range(1000):
    play = choice(plays)
    print ' '
    print play
    yards, fgAtt, fgGood = determinePlayResult(play)
    if fgAtt:
        if fgGood:
            print 'Kick Is Good'
        else:
            print 'Kick No Good' 
    print 'Yards On Play', yards
    
print 'Success', success
print 'Fail', fail
