'''
Created on Aug 19, 2012

@author: George Peek
'''

import sys
import pprint
import pygame
from pygame.locals import *

from play import Game, Play, Field, Team

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

screen = pygame.display.set_mode((1400,800))
myfont = pygame.font.Font(None,20)
blue = (0,0,255)
white = (255,255,255)

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
game = Game(team1,team2)

run_i = PlayButton((0,0),'run_inside','run')
run_o = PlayButton((0,0),'run_outside','run')
pass_s = PlayButton((0,0),'pass short','pass')
pass_m = PlayButton((0,0),'pass medium','pass')
pass_l = PlayButton((0,0),'pass long','pass')

play_buttons = [run_i, run_o, pass_s, pass_m, pass_l]

#def set_play():
#    if game.field.direction == 1:
#        current_play = Play(game.home,game.away,game.field)
#    else:
#        current_play = Play(game.away,game.home,game.field)
#    return current_play
#    
#current_play = set_play()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        if event.type == KEYUP:
            if event.key == pygame.K_k:
#                current_play = set_play()
                game.plays[-1].kickoff()
                game.current_state.check_state(game.plays[-1])
            if event.key == pygame.K_i:
#                current_play = set_play()
                game.plays[-1].run_inside()
            if event.key == pygame.K_o:
#                current_play = set_play()
                game.plays[-1].run_outside()
            if event.key == pygame.K_s:
#                current_play = set_play()
                game.plays[-1].pass_short()
            if event.key == pygame.K_m:
#                current_play = set_play()
                game.plays[-1].pass_medium()
            if event.key == pygame.K_l:
#                current_play = set_play()
                game.plays[-1].pass_long()
        
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouse_pos = myfont.render(str(mousex) + ',' + str(mousey), True, white)
            
            if run_i.rect.collidepoint((mousex, mousey)):
#                current_play = set_play()
                game.plays[-1].run_inside()
            if run_o.rect.collidepoint((mousex, mousey)):
#                current_play = set_play()
                game.plays[-1].run_outside()
            if pass_s.rect.collidepoint((mousex, mousey)):
#                current_play = set_play()
                game.plays[-1].pass_short()
            if pass_m.rect.collidepoint((mousex, mousey)):
#                current_play = set_play()
                game.plays[-1].pass_medium()
            if pass_l.rect.collidepoint((mousex, mousey)):
#                current_play = set_play()
                game.plays[-1].pass_long()
            
            
            

    screen.fill(blue)
    try:
        screen.blit(mouse_pos,(1100,10))
    except:
        pass
#    pprint.pprint(vars(team1)) 
#    print ' '
#    pprint.pprint(vars(team2)) 
#    print ' '
    home_name = myfont.render(game.home.city + game.home.nickname, True, white)
    away_name = myfont.render(game.away.city + game.away.nickname, True, white)
    abs_yardline = myfont.render("Yardline: " + str(game.field.absolute_yardline), True, white)
    direction = myfont.render("Direction: " + str(game.field.direction), True, white)
    play_name = myfont.render("Play: " + str(game.plays[-1].play_name), True, white)
    play_rating = myfont.render("Rating: " + str(game.plays[-1].play_rating), True, white)
    playsh = myfont.render("H: " + str(game.home.plays_run) + str(game.home.total_plays_run), True, white)
    playsa = myfont.render("A: " + str(game.away.plays_run) + str(game.away.total_plays_run), True, white)
    yards_gained = myfont.render("Off Yards: " + str(game.plays[-1].offense_yardage), True, white)
    return_yards = myfont.render("Ret Yards: " + str(game.plays[-1].return_yardage), True, white)
    turnover = myfont.render("Turnover: " + str(game.plays[-1].turnover), True, white)
#    pprint.pprint(vars(current_play.field))

## stats display
    display = [abs_yardline, direction, play_name, play_rating, playsh, playsa, yards_gained, turnover, return_yards]
    display_offset = 0
    horizontal_offset = 0
    
    screen.blit(home_name, (5,5))
    screen.blit(away_name, (105,5))
    for item in display:
        screen.blit(item, (5,35 + display_offset))
        display_offset += 20
        
## play button display
    for button in play_buttons:
        button.update_coords(((5 + horizontal_offset),(50 + display_offset)))
        button.display_button()
        horizontal_offset += 130

## field display
    pygame.draw.rect(screen,(0,255,0),(5,(100 + display_offset),1200,500))
    pygame.draw.rect(screen,game.home.primary_color,(5,(100 + display_offset),100,500))
    pygame.draw.rect(screen,game.away.primary_color,(1105,(100 + display_offset),100,500))
    for line in range(12):
        pygame.draw.line(screen,(255,255,255),((5 + (line * 100)),(100 + display_offset)),((5 + (line * 100)),(100 + display_offset + 500)))
    pygame.draw.ellipse(screen,(0,0,0),(((10 * game.field.absolute_yardline) + 90), (display_offset + 300),30,15))


    pygame.display.update()
        
#    screen.blit( (5,55))
#    screen.blit())
#    screen.blit(, (5,95))
#    screen.blit(,115))
#    screen.blit(, (5,135))
