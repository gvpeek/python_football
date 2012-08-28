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

class PlayButton():
    def __init__(self, coords, text, play_category):
        self.rect = pygame.Rect(coords,(100,20))
        self.text = myfont.render(text, True, white)
        if play_category == 'run':
            self.color = (128,0,0)
        elif play_category == 'pass':
            self.color = (0,0,128)
        elif play_category == 'special':
            self.color = (128,0,128)
        else:
            self.color = (128,128,128)             
            
    def display_button(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.rect)
        
    def update_coords(self, new_coords):
        self.rect = pygame.Rect(new_coords,(100,20))

screen = pygame.display.set_mode((1200,800))
myfont = pygame.font.Font(None,20)
blue = (0,0,255)
white = (255,255,255)

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
f = Field()

run_i = PlayButton((0,0),'run_inside','run')
run_o = PlayButton((0,0),'run_outside','run')
pass_s = PlayButton((0,0),'pass short','pass')
pass_m = PlayButton((0,0),'pass medium','pass')
pass_l = PlayButton((0,0),'pass long','pass')

play_buttons = [run_i, run_o, pass_s, pass_m, pass_l]

def set_play():
    if f.direction == 1:
        current_play = Play(team1,team2,f)
    else:
        current_play = Play(team2,team1,f)
    return current_play
    
current_play = set_play()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        if event.type == KEYUP:
            if event.key == pygame.K_k:
                current_play = set_play()
                current_play.kickoff()
            if event.key == pygame.K_i:
                current_play = set_play()
                current_play.run_inside()
            if event.key == pygame.K_o:
                current_play = set_play()
                current_play.run_outside()
            if event.key == pygame.K_s:
                current_play = set_play()
                current_play.pass_short()
            if event.key == pygame.K_m:
                current_play = set_play()
                current_play.pass_medium()
            if event.key == pygame.K_l:
                current_play = set_play()
                current_play.pass_long()
        
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouse_pos = myfont.render(str(mousex) + ',' + str(mousey), True, white)
            
            if run_i.rect.collidepoint((mousex, mousey)):
                current_play = set_play()
                current_play.run_inside()
            if run_o.rect.collidepoint((mousex, mousey)):
                current_play = set_play()
                current_play.run_outside()
            if pass_s.rect.collidepoint((mousex, mousey)):
                current_play = set_play()
                current_play.pass_short()
            if pass_m.rect.collidepoint((mousex, mousey)):
                current_play = set_play()
                current_play.pass_medium()
            if pass_l.rect.collidepoint((mousex, mousey)):
                current_play = set_play()
                current_play.pass_long()
            
            
            

    screen.fill(blue)
    try:
        screen.blit(mouse_pos,(1100,10))
    except:
        pass
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
        
    for button in play_buttons:
        button.update_coords((5,(35 + display_offset)))
        button.display_button()
        display_offset += 30
        
    pygame.display.update()
        
#    screen.blit( (5,55))
#    screen.blit())
#    screen.blit(, (5,95))
#    screen.blit(,115))
#    screen.blit(, (5,135))
