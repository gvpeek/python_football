'''
Created on Aug 19, 2012

@author: George Peek
'''

import sys
import pprint
import pygame
from pygame.locals import *

from play import Play, Field, Team

pygame.init()

screen = pygame.display.set_mode((1200,800))
myfont = pygame.font.Font(None,20)
blue = (0,0,255)
white = (255,255,255)

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
f = Field()

current_play = Play(team1,team2,f)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        if event.type == KEYUP:
            if f.direction == 1:
                current_play = Play(team1,team2,f)
            else:
                current_play = Play(team2,team1,f)
                
            if event.key == pygame.K_k:
                current_play.kickoff()
            if event.key == pygame.K_i:
                current_play.run_inside()
            if event.key == pygame.K_o:
                current_play.run_outside()
            if event.key == pygame.K_s:
                current_play.pass_short()
            if event.key == pygame.K_m:
                current_play.pass_medium()
            if event.key == pygame.K_l:
                current_play.pass_long()

    screen.fill(blue)
    
#    pprint.pprint(vars(team1)) 
#    print ' '
#    pprint.pprint(vars(team2)) 
#    print ' '
    home_name = myfont.render(team1.city + team1.nickname, True, white)
    away_name = myfont.render(team2.city + team2.nickname, True, white)
    abs_yardline = myfont.render("Yardline: " + str(f.absolute_yardline), True, white)
    play_name = myfont.render("Play: " + str(current_play.play_name), True, white)
    play_rating = myfont.render("Rating: " + str(current_play.play_rating), True, white)
    plays = myfont.render(str(team1.plays_run) + str(team1.total_plays_run), True, white)
    yards_gained = myfont.render("Off Yards: " + str(current_play.offense_yardage), True, white)
    return_yards = myfont.render("Ret Yards: " + str(current_play.return_yardage), True, white)
    turnover = myfont.render("Turnover: " + str(current_play.turnover), True, white)
#    pprint.pprint(vars(current_play.field))

    display = [abs_yardline, play_name, play_rating, plays, yards_gained, turnover, return_yards]
    display_offset = 0
                   
    screen.blit(home_name, (5,5))
    screen.blit(away_name, (105,5))
    for item in display:
        screen.blit(item, (5,35 + display_offset))
        display_offset += 20
    pygame.display.update()
        
#    screen.blit( (5,55))
#    screen.blit())
#    screen.blit(, (5,95))
#    screen.blit(,115))
#    screen.blit(, (5,135))
