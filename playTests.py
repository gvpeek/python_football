'''
Created on Jan 7, 2012

@author: George Peek
'''

from math import ceil, floor, pow
from random import randint, choice

netYardsOnPlay = 0
#play = raw_input('Select Play:')
plays = ['RI','RO','PS','2PRI','2PRO','2PPS','PM','PL','RC','K','OK','PUNT','FG','XP']



def determinePlayResult(play,offense,defense):
    turnover = False
    change_of_possession = False
    netYardsOnPlay = 0 
    fieldGoalSuccess = False
    fieldGoalAttempt = False
    puntBlocked = False
    playRnd = randint(1,100)
    playRating = determinePlayRating(play,offense,defense)
    if play == 'RC':
        netYardsOnPlay = -2
    elif play in ['K','OK']:
        onside_recover = False
        kickoffYardage = determineKickoffYardage(play,playRating)
        ##TODO: determine position
        ##TODO: if not touchback or out of bounds
        if play == 'OK' and kickoffYardage >= 10:
            onside_recover_random = randint(1,100)
            onside_recover_rating = ceil(offense.rating_sp / 4)
            if onside_recover_random <= onside_recover_rating:
                print 'Offense Recovers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                onside_recover = True
        if onside_recover:
            returnYardage = -(determineReturnYardage(play,offense))
        else:
            returnYardage = determineReturnYardage(play,defense)
            change_of_possession = True            
        print 'kick', kickoffYardage, 'return', returnYardage
        netYardsOnPlay = kickoffYardage - returnYardage
    elif play == 'PUNT':
        puntYardage, puntBlocked = determinePuntYardage(playRating)
        ##TODO: determine position
        ##TODO: if not touchback or out of bounds or fair catch
        returnYardage = determineReturnYardage(play,defense)
        print 'punt', puntYardage, 'return', returnYardage
        netYardsOnPlay = puntYardage - returnYardage
        change_of_possession = True
    elif play in ['FG','XP']:
        fieldGoalAttempt = True
        fieldGoalSuccess = False
        ## Testing
        if play == 'FG':
            convertedYardline = randint(1,70)
        elif play == 'XP':
            convertedYardline = 2
        print convertedYardline, 'yardline'
        ## Testing
        fieldGoalSuccess = determineFieldGoalResult(play,playRating,convertedYardline)
        if not fieldGoalSuccess:
            change_of_possession = True
    else: 
        if playRnd <= playRating:
            playSuccess=True
        else:
            playSuccess=False
            turnover = determineTurnover(play,playRating)
            
        if not turnover:
            netYardsOnPlay=determinePlayYardage(play,playRating,playSuccess)
        else:
            netYardsOnPlay = (determinePlayYardage(play,playRating,playSuccess) - determineReturnYardage(play,defense))
            change_of_possession = True
    return netYardsOnPlay, change_of_possession, fieldGoalAttempt, fieldGoalSuccess, puntBlocked

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
    change_of_possession = False
    turnoverRnd = randint(1,100)
    if play in ['RI','2PRI','RO','2PRO']:
        if turnoverRnd <= ((100 - playRating) / 3.5):
            change_of_possession = True
    elif play in ['PS','2PPS']:
        if turnoverRnd <= ((100 - playRating) / 10):
            change_of_possession = True
    elif play == 'PM':
        if turnoverRnd <= (((100 - playRating) / 10) * 2):
            change_of_possession = True
    elif play == 'PL':
        if turnoverRnd <= (((100 - playRating) / 10) * 2):
            change_of_possession = True
    return change_of_possession

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

def determinePuntYardage(playRating):
    puntBlocked = False
    puntRnd = randint(1,100)
    puntBlockRnd = randint(1,100)
    puntBlockChance = randint(0,1)
    pivot_point = ceil(playRating / 1.7)
    aboveApex = randint(0,1)
    
    if puntBlockRnd == playRating and puntBlockChance:
        puntBlocked = True
        puntYards = 0.0
    else:
        if aboveApex:
            print 'Above'
            puntYards = (pivot_point + floor(((playRating*100) * pow(puntRnd,-.8309)) / 100))
        else:
            print 'Below'
            puntYards = (pivot_point - floor(((playRating*100) * pow(puntRnd,-.8309)) / 100))
        
        if puntYards < (pivot_point - floor(((playRating*100) * pow(5.0,-.8309)) / 100)):
            puntYards = (pivot_point - floor(((playRating*100) * pow(5.0,-.8309)) / 100))
        elif puntYards > (pivot_point + floor(((playRating*100) * pow(7.0,-.8309)) / 100)):
            puntYards = (pivot_point + floor(((playRating*100) * pow(7.0,-.8309)) / 100))      
    return puntYards, puntBlocked

def determineReturnYardage(play,return_team):
    returnRnd = randint(1,100)
    if play in ['RI','2PRI','RC']:
        returnYards = floor(((return_team.rating_dl*100)*pow(returnRnd,-1)) / 100)
    elif play in ['RO','2PRO']:
        returnYards = floor(((return_team.rating_lb*100)*pow(returnRnd,-1)) / 100)
    elif play in ['PS','2PPS']:
        returnYards = floor(((return_team.rating_lb*100)*pow(returnRnd,-.8)) / 100)
    elif play in ['PM']:
        returnYards = floor(((return_team.rating_cb*100)*pow(returnRnd,-.7)) / 100)
    elif play in ['PL']:
        returnYards = floor(((return_team.rating_s*100)*pow(returnRnd,-.6)) / 100)
    elif play == 'K':
        returnYards = floor(((return_team.rating_sp*125)*pow(returnRnd,-.4)) / 100)
    elif play == 'OK':
        returnYards = floor(((return_team.rating_sp*100)*pow(returnRnd,-1)) / 100)
    elif play == 'PUNT':
        returnYards = floor(((return_team.rating_sp*100)*pow(returnRnd,-.6)) / 100)
    return returnYards

def determinePlayRating(play,offense,defense):
    if play in ['RI','2PRI','RC']:
        offRating = ceil(((offense.rating_qb + offense.rating_rb*4 + offense.rating_ol*5) / 10))
        defRating = ceil((((defense.rating_dl*6 + defense.rating_lb*3 + defense.rating_s) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['RO','2PRO']:
        offRating = ceil(((offense.rating_qb + offense.rating_rb*5 + offense.rating_wr + offense.rating_ol*3) / 10))
        defRating = ceil((((defense.rating_dl*3 + defense.rating_lb*5 + defense.rating_cb + defense.rating_s) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['PS','2PPS']:
        offRating = ceil(((offense.rating_qb*4 + offense.rating_rb*2 + offense.rating_wr*3 + offense.rating_ol) / 10))
        defRating = ceil((((defense.rating_dl + defense.rating_lb*5 + defense.rating_cb*3 + defense.rating_s) / 10) - 60) / 4)
        playPenalty = 0
    elif play == 'PM':
        offRating = ceil(((offense.rating_qb*4 + offense.rating_wr*4 + offense.rating_ol*2) / 10))
        defRating = ceil((((defense.rating_dl*2 + defense.rating_lb*2 + defense.rating_cb*4 + defense.rating_s*2) / 10) - 60) / 4)
        playPenalty = 0
    elif play == 'PL':
        offRating = ceil(((offense.rating_qb*4 + offense.rating_wr*3 + offense.rating_ol*3) / 10))
        defRating = ceil((((defense.rating_dl*3 + defense.rating_lb + defense.rating_cb*3 + defense.rating_s*3) / 10) - 60) / 4)
        playPenalty = 0
    elif play in ['FG','XP','K','OK','PUNT']:
        offRating = offense.rating_sp
        defRating = ceil((defense.rating_sp - 60) / 4)
        playPenalty = 0
    playRating = ((offRating - defRating) - playPenalty)
    if playRating < 35:
        playRating = 35
    elif playRating > 90:
        playRating = 90
    ##Testing
    print offense.city, offense.nickname, offRating
    print defense.city, defense.nickname, defRating    
    print playRating
    ##Testing
    return playRating
    

