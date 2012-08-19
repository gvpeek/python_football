Created on Jan 7, 2012

'''
@author: George Peek
'''

from math import ceil, floor, pow
from random import randint

#play = raw_input('Select Play:')
plays = ['RI','RO','PS','2PRI','2PRO','2PPS','PM','PL','RC','K','OK','PUNT','FG','XP']
plays_off = ['RI','RO','PS','PM','PL','RC']
plays_sp = ['2PRI','2PRO','2PPS','K','OK','PUNT','FG','XP']



def determine_play_result(play,away_possession,position,offense,defense):
    play_result = {
    
        }
#    play_rating = determine_play_rating(play, offense, defense, away_possession)
    
#    if play == 'RC':
#        play_result['offense_yardage'] = -2
#        determine_position(position,play_result['offense_yardage'])
#        play_result['net_yards_on_play'] = play_result['offense_yardage']

#    elif play in ['K','OK']:
#        if play_rating < 60:
#            play_rating = 60
#        onside_recover = False
#        play_result['kickoff_yardage'] = determine_kickoff_yardage(play,play_rating)
#        determine_position(position,play_result['kickoff_yardage'])
 
        #==========================================
        # Determine if offense recovers onside kick
        #==========================================
#        if play == 'OK' and play_result['kickoff_yardage'] >= 10:
#            onside_recover_random = randint(1,100)
#            onside_recover_rating = ceil(offense.rating_sp / 4)
#            if onside_recover_random <= onside_recover_rating:
#                print 'Offense Recovers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
#                onside_recover = True
        
#        if onside_recover:
#            play_result['return_yardage'] = determine_return_yardage(play,offense)
#            determine_position(position,play_result['return_yardage'])
#            play_result['net_yards_on_play'] = play_result['kickoff_yardage'] + play_result['return_yardage']
#        else:
#            play_result['change_of_possession'] = True 
#            if not position['in_home_endzone'] or not position['in_away_endzone']: 
#                play_result['return_yardage'] = determine_return_yardage(play,defense)
#                determine_position(position,play_result['return_yardage'],play_result['change_of_possession'])
#            else:
#                play_result['touchback']
#            play_result['net_yards_on_play'] = play_result['kickoff_yardage'] - play_result['return_yardage']
        
#        print 'kick', play_result['kickoff_yardage'], 'return', play_result['return_yardage']
        
    
#    elif play == 'PUNT':
#        play_result['punt_yardage'], play_result['punt_blocked'] = determine_punt_yardage(play_rating)
#        determine_position(position,play_result['punt_yardage'])
#        play_result['change_of_possession'] = True
#                
#        if not position['in_home_endzone'] or not position['in_away_endzone']: 
#            play_result['return_yardage'] = determine_return_yardage(play,defense)
#            determine_position(position,play_result['return_yardage'],play_result['change_of_possession'])
#        else:
#            play_result['touchback']
#        
#        print 'punt', play_result['punt_yardage'], 'return', play_result['return_yardage']
#        play_result['net_yards_on_play'] = play_result['punt_yardage'] - play_result['return_yardage']
    
    elif play in ['FG','XP']:
#        play_result['field_goal_attempt'] = True
#        play_result['field_goal_success'] = determine_field_goal_result(play, play_rating, position['absolute_yardline'], away_possession)
#        
#        if not play_result['field_goal_success']:
#            play_result['change_of_possession'] = True
#            determine_position(position,-7)
    
    else:
        play_rnd = randint(1,100)
        if play_rnd <= play_rating:
            play_success=True
        else:
            play_success=False
            play_result['turnover'] = determine_turnover(play,play_rating)
        
        play_result['offense_yardage'] = determine_play_yardage(play,play_rating,play_success,play_result['turnover'])
        determine_position(position,play_result['offense_yardage'])

        if play_result['turnover']:
            print 'Turnover!!!!!!!'
            play_result['change_of_possession'] = True
            play_result['return_yardage'] = determine_return_yardage(play,defense)
            determine_position(position,play_result['return_yardage'],play_result['change_of_possession'])

        play_result['net_yards_on_play'] = play_result['offense_yardage'] - play_result['return_yardage']

    return play_result

#def determine_play_yardage(play,play_rating,play_success,turnover=False):
#    yardage_rnd = randint(1,100)
#    loss_rating = ((90 - play_rating) + 60)
#    if play in ['RI','RO','PS','2PRI','2PRO','2PPS']:
#        if play_success or turnover:
#            yardage = floor(((play_rating*100)*pow(yardage_rnd,-.7)) / 100)
#        else:
#            yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,-1)) / 100))
#            if yardage < -5:
#                yardage= -5
#    elif play == 'PM':
#        if play_success or turnover:
#            yardage = floor(((play_rating*100)*pow(yardage_rnd,-.5)) / 100)
#        else:
#            yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,-.8309)) / 100))
#            if yardage < -8:
#                yardage= -8
#    elif play == 'PL':
#        if play_success or turnover:
#            yardage = floor(((play_rating*100)*pow(yardage_rnd,-.4)) / 100)
#        else:
#            yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,-.5)) / 100))
#            if yardage < -12:
#                yardage= -12
#    else:
#        print 'Delay of game!'
#        yardage = -5
#    return yardage

#def determine_turnover(play,play_rating):
#    change_of_possession = False
#    turnover_rnd = randint(1,100)
#
#    if play in ['RI','2PRI','RO','2PRO']:
#        if turnover_rnd <= ((100 - play_rating) / 3.5):
#            change_of_possession = True
#    elif play in ['PS','2PPS']:
#        if turnover_rnd <= ((100 - play_rating) / 10):
#            change_of_possession = True
#    elif play == 'PM':
#        if turnover_rnd <= (((100 - play_rating) / 10) * 2):
#            change_of_possession = True
#    elif play == 'PL':
#        if turnover_rnd <= (((100 - play_rating) / 10) * 2):
#            change_of_possession = True
#    return change_of_possession

#def determine_field_goal_result(play, play_rating, absolute_yardline, away_kick_attempt):
#    if away_kick_attempt:
#        distance = absolute_yardline
#    else:
#        distance = 100 - absolute_yardline
#    print 'distance', distance
#    
#    if play == 'FG':
#        fg_rnd = randint(1,110)
#    elif play == 'XP':
#        fg_rnd = randint(1,100)
#    
#    fg_rating = ((80 - play_rating) / 2)
#    
#    if fg_rnd < ((100 - distance) - fg_rating):
#        return True
#    else:
#        return False

#def determine_kickoff_yardage(play,play_rating):
#    if play == 'K':
#        kick_rnd = randint(1,20) + 55
#    elif play == 'OK':
#        kick_rnd = randint(1,15) + 10
#    kick_rating = (80 - play_rating) / 2
#    kick_yardage = ceil(kick_rnd - kick_rating)
#    return kick_yardage

def determine_punt_yardage(play_rating):
    punt_blocked = False
    punt_rnd = randint(1,100)
    punt_block_rnd = randint(1,100)
    punt_block_chance = randint(0,1)
    pivot_point = ceil(play_rating / 1.7)
    above_pivot = randint(0,1)
    
    if punt_block_rnd == play_rating and punt_block_chance:
        punt_blocked = True
        punt_yards = 0.0
    else:
        if above_pivot:
            print 'Above'
            punt_yards = (pivot_point + floor(((play_rating*100) * pow(punt_rnd,-.8309)) / 100))
        else:
            print 'Below'
            punt_yards = (pivot_point - floor(((play_rating*100) * pow(punt_rnd,-.8309)) / 100))
        
        if punt_yards < (pivot_point - floor(((play_rating*100) * pow(5.0,-.8309)) / 100)):
            punt_yards = (pivot_point - floor(((play_rating*100) * pow(5.0,-.8309)) / 100))
        elif punt_yards > (pivot_point + floor(((play_rating*100) * pow(7.0,-.8309)) / 100)):
            punt_yards = (pivot_point + floor(((play_rating*100) * pow(7.0,-.8309)) / 100))      
    return punt_yards, punt_blocked

def determine_return_yardage(play,return_team):
    return_rnd = randint(1,100)
#    if play in ['RI','2PRI','RC']:
#        return_yards = floor(((return_team.rating_dl*100)*pow(return_rnd,-1)) / 100)
#    elif play in ['RO','2PRO']:
#        return_yards = floor(((return_team.rating_lb*100)*pow(return_rnd,-1)) / 100)
#    elif play in ['PS','2PPS']:
#        return_yards = floor(((return_team.rating_lb*100)*pow(return_rnd,-.8)) / 100)
#    elif play in ['PM']:
#        return_yards = floor(((return_team.rating_cb*100)*pow(return_rnd,-.7)) / 100)
#    elif play in ['PL']:
#        return_yards = floor(((return_team.rating_s*100)*pow(return_rnd,-.6)) / 100)
#    elif play == 'K':
#        return_yards = floor(((return_team.rating_sp*125)*pow(return_rnd,-.4)) / 100)
#    elif play == 'OK':
#        return_yards = floor(((return_team.rating_sp*100)*pow(return_rnd,-1)) / 100)
#    elif play == 'PUNT':
#        return_yards = floor(((return_team.rating_sp*100)*pow(return_rnd,-.6)) / 100)
#    return return_yards

#def determine_play_rating(play,offense,defense,away_rating_penalty):
#    if play in ['RI','2PRI','RC']:
#        off_rating = ceil(((offense.rating_qb + offense.rating_rb*4 + offense.rating_ol*5) / 10))
#        def_rating = ceil((((defense.rating_dl*6 + defense.rating_lb*3 + defense.rating_s) / 10) - 60) / 4)
#    elif play in ['RO','2PRO']:
#        off_rating = ceil(((offense.rating_qb + offense.rating_rb*5 + offense.rating_wr + offense.rating_ol*3) / 10))
#        def_rating = ceil((((defense.rating_dl*3 + defense.rating_lb*5 + defense.rating_cb + defense.rating_s) / 10) - 60) / 4)
#    elif play in ['PS','2PPS']:
#        off_rating = ceil(((offense.rating_qb*4 + offense.rating_rb*2 + offense.rating_wr*3 + offense.rating_ol) / 10))
#        def_rating = ceil((((defense.rating_dl + defense.rating_lb*5 + defense.rating_cb*3 + defense.rating_s) / 10) - 60) / 4)
#    elif play == 'PM':
#        off_rating = ceil(((offense.rating_qb*4 + offense.rating_wr*4 + offense.rating_ol*2) / 10))
#        def_rating = ceil((((defense.rating_dl*2 + defense.rating_lb*2 + defense.rating_cb*4 + defense.rating_s*2) / 10) - 60) / 4)
#    elif play == 'PL':
#        off_rating = ceil(((offense.rating_qb*4 + offense.rating_wr*3 + offense.rating_ol*3) / 10))
#        def_rating = ceil((((defense.rating_dl*3 + defense.rating_lb + defense.rating_cb*3 + defense.rating_s*3) / 10) - 60) / 4)
#    elif play in ['FG','XP','K','OK','PUNT']:
#        off_rating = offense.rating_sp
#        def_rating = ceil((defense.rating_sp - 60) / 4)
    
#    if play in ['RI','RO','PS','PM','PL']:
#        play_penalty = determine_play_penalty(play,offense,away_rating_penalty)    
#    else:
#        play_penalty = 0 
#    play_rating = ((off_rating - def_rating) - play_penalty)
#    if play_rating < 35:
#        play_rating = 35
#    elif play_rating > 90:
#        play_rating = 90
#    ##Testing
#    print offense.city, offense.nickname, off_rating
#    print defense.city, defense.nickname, def_rating    
#    print 'play_rating', play_rating
#    ##Testing
#    return play_rating

#def determine_play_penalty(play,offense,away_rating_penalty):
#    offense.play_calls['total_plays'] += 1
#    offense.play_calls[play] += 1
#
#    if offense.play_calls['total_plays'] > 15 and ((offense.play_calls[play] / offense.play_calls['total_plays']) > .33):
#        penalty = ceil((offense.play_calls[play] / offense.play_calls['total_plays']) * (offense.play_calls[play] * 2.5))
#    else:
#        penalty = 0
#    
#    if away_rating_penalty:
#        penalty += 3
#    
#    print offense.city, 'penalty', penalty, offense.play_calls['total_plays'],offense.play_calls['RI'],offense.play_calls['RO'],offense.play_calls['PS'],offense.play_calls['PM'],offense.play_calls['PL']
#    return penalty

## MOVED
#def determine_position(position, yardage, reverse_direction=False):
#    position['in_home_endzone'] = False
#    position['in_away_endzone'] = False
#    
#    if reverse_direction:
#        direction = position['direction'] * -1
#    else:
#        direction = position['direction']
#    position['absolute_yardline'] += (yardage * direction)
#    
#    if position['absolute_yardline'] > 50:
#        position['converted_yardline'] = 100 - position['absolute_yardline']
#        if position['absolute_yardline'] >= 100:
#            position['in_away_endzone'] = True
#    else:
#        position['converted_yardline'] = position['absolute_yardline']
#        if position['absolute_yardline'] <= 0:
#            position['in_home_endzone'] = True
#    print 'yardline', position['absolute_yardline'], 'direction', position['direction'], 'home_ez', position['in_home_endzone'], 'away_ez', position['in_away_endzone']
