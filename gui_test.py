'''
Created on Aug 19, 2012

@author: George Peek
'''

import sys
import pprint
import pygame
from pygame.locals import *

from game import Game
from team import Team
from playbook import Rush, Pass

pygame.init()

class PlayButton():
    def __init__(self, coords, play):
        self.play = play
        self.rect = pygame.Rect(coords,(100,20))
        self.text = myfont.render(play.name, True, white)
        
        if isinstance(play,Rush):
            self.color = (128,0,0)
        elif isinstance(play,Pass):
            self.color = (0,0,128)
        else:
            self.color = (128,0,128)
            
    def display_button(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.rect)
        
    def update_coords(self, new_coords):
        self.rect = pygame.Rect(new_coords,(100,20))

screen = pygame.display.set_mode((1300,900))
myfont = pygame.font.Font(None,20)
fps = pygame.time.Clock()
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
reset_coords = (-1000,-1000)

team1 = Team("Austin","Easy")
team2 = Team("Chicago","Grown Men")
game = Game(team1,team2)

play_buttons=[]

while True:
    
    fps.tick(5)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouse_pos = myfont.render(str(mousex) + ',' + str(mousey), True, white)
            
            for button in play_buttons:
                if button.rect.collidepoint((mousex, mousey)):
                    game.run_play(button.play)

    screen.fill(blue)
    try:
        screen.blit(mouse_pos,(1100,10))
    except:
        pass

    home_name = myfont.render(game.home.city + ' ' + game.home.nickname + ' -- ' + str(game.get_home_team().statbook.stats['score']), True, white)
    away_name = myfont.render(game.away.city + ' ' + game.away.nickname + ' -- ' + str(game.get_away_team().statbook.stats['score']), True, white)
    current_state = myfont.render(str(game.current_state), True, white)
    abs_yardline = myfont.render("Yardline: " + game.scoreboard.absolute_yardline, True, white)
    conv_yardline = myfont.render("Yardline: " + game.scoreboard.converted_yardline, True, white)
    play_name = myfont.render("Play: " + game.scoreboard.play_name, True, white)
    playsh = myfont.render("O: " + str(game.get_home_team().plays_run) + str(sum(game.get_home_team().plays_run.values())), True, white)
    playsa = myfont.render("D: " + str(game.get_away_team().plays_run) + str(sum(game.get_away_team().plays_run.values())), True, white)
    yards_gained = myfont.render("Off Yards: " + game.scoreboard.offense_yardage, True, white)
    return_yards = myfont.render("Ret Yards: " + game.scoreboard.return_yardage, True, white)
    turnover = myfont.render("Turnover: " + game.scoreboard.turnover, True, white)
    quarter = myfont.render("Qtr: " + game.scoreboard.period, True, white)
    clock = myfont.render("Time: " + game.scoreboard.clock, True, white)
    down = myfont.render("Down: " + game.scoreboard.down, True, white)
    yards_to_go = myfont.render("Yards To Go: " + game.scoreboard.yards_to_go, True, white)

## stats display
    display_offset = 0
    display = [current_state, play_name, yards_gained, return_yards, 
               turnover, quarter, clock, down, 
               yards_to_go, conv_yardline, playsh, playsa]
    horizontal_offset = 0
    
    screen.blit(home_name, (25,5))
    screen.blit(away_name, (180,5))
    if game.possession.offense.direction == 1:
        pygame.draw.circle(screen,white,(10,12),5)
    elif game.possession.offense.direction == -1:
        pygame.draw.circle(screen,white,(165,12),5)
            
    for item in display:
        screen.blit(item, (5,35 + display_offset))
        display_offset += 20
        
    play_buttons = [PlayButton(reset_coords,play) for play in game.get_available_plays()]
## play button display
    for button in play_buttons:
        button.update_coords(reset_coords)
        
#    for button in game.current_state.play_choice:
#        if isinstance(game.current_state,(button.play.valid_states)) and (100-abs(game.field.absolute_yardline - game.possession.offense.endzone)) > button.play.valid_yardline:
        button.update_coords(((5 + horizontal_offset),(50 + display_offset)))
        button.display_button()
        horizontal_offset += 130
  
## field display
    pygame.draw.rect(screen,(0,255,0),(5,(100 + display_offset),1200,500))
    pygame.draw.rect(screen,game.home.primary_color,(5,(100 + display_offset),100,500))
    pygame.draw.rect(screen,game.away.primary_color,(1105,(100 + display_offset),100,500))
    for line in range(12):
        pygame.draw.line(screen,(255,255,255),((5 + (line * 100)),(100 + display_offset)),((5 + (line * 100)),(100 + display_offset + 500)))
    pygame.draw.ellipse(screen,(139,69,19),(((10 * game.field.absolute_yardline) + 90), (display_offset + 300),30,15))


    pygame.display.update()
