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
#from playbook import Rush, Pass

class PlayButton():
    def __init__(self, coords, play,myfont,colors):
        self.play = play
        self.rect = pygame.Rect(coords,(100,20))
        self.text = myfont.render(play.name, True, colors['white'])
        
        if play.is_rush():
            self.color = colors['rush_button']
        elif play.is_pass():
            self.color = colors['pass_button']
        else:
            self.color = colors['special_button']
            
    def display_button(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.rect)
        
    def update_coords(self, new_coords):
        self.rect = pygame.Rect(new_coords,(100,20))


class Display():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1300,900))
        self.myfont = pygame.font.Font(None,20)
        self.fps = pygame.time.Clock()
        self.reset_coords = (-1000,-1000)
        self.play_buttons=[]
        self.colors = {'blue' : (0,0,255),
                  'white' : (255,255,255),
                  'black' : (0,0,0),
                  'field' : (0,255,0),
                  'football' : (139,69,19),
                  'rush_button' : (128,0,0),
                  'pass_button' : (0,0,128),
                  'special_button' : (128,0,128)}
        
    def check_user_input(self,run_play):
        while True:
            self.fps.tick(5)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    
                    for button in self.play_buttons:
                        if button.rect.collidepoint((mousex, mousey)):
                            run_play(button.play)
                            break
        

    def update(self,*args):
        human_control, end_of_game, run_play, available_plays, field, scoreboard = args[0]

        self.screen.fill(self.colors['blue'])

        display =[self.myfont.render("Yardline: " + scoreboard.scoreboard['yardline'], True, self.colors['white']),
                  self.myfont.render("Qtr: " + scoreboard.scoreboard['period'], True, self.colors['white']),
                  self.myfont.render("Time: " + scoreboard.scoreboard['clock'], True, self.colors['white']),
                  self.myfont.render("Down: " + scoreboard.scoreboard['down'], True, self.colors['white']),
                  self.myfont.render("Yards To Go: " + scoreboard.scoreboard['yards_to_go'], True, self.colors['white'])
                  ]
    
    ## stats display
        display_offset = 0
        horizontal_offset = 0
        
        self.screen.blit(self.myfont.render(scoreboard.scoreboard['home_city'] + ' ' + scoreboard.scoreboard['home_nickname'] + ' -- ' + str(scoreboard.scoreboard['home_score']), True, self.colors['white']),(25,5))
        self.screen.blit(self.myfont.render(scoreboard.scoreboard['away_city'] + ' ' + scoreboard.scoreboard['away_nickname'] + ' -- ' + str(scoreboard.scoreboard['away_score']), True, self.colors['white']),(180,5))
        if scoreboard.scoreboard['possession'] == 'Home':
            pygame.draw.circle(self.screen,self.colors['white'],(10,12),5)
        elif scoreboard.scoreboard['possession'] == 'Away':
            pygame.draw.circle(self.screen,self.colors['white'],(165,12),5)
                
        for item in display:
            self.screen.blit(item, (5,35 + display_offset))
            display_offset += 20
            
        self.play_buttons = [PlayButton(self.reset_coords,
                                        play,
                                        self.myfont,
                                        self.colors) for play in available_plays.values()]
    ## play button display
        for button in self.play_buttons:
            button.update_coords(((5 + horizontal_offset),(50 + display_offset)))
            button.display_button(self.screen)
            horizontal_offset += 130
      
    ## field display
        pygame.draw.rect(self.screen,self.colors['field'],(5,(100 + display_offset),1200,500))
        pygame.draw.rect(self.screen,field.endzone_prim_color,(5,(100 + display_offset),100,500))
        pygame.draw.rect(self.screen,field.endzone_prim_color,(1105,(100 + display_offset),100,500))
        for line in range(12):
            pygame.draw.line(self.screen,self.colors['white'],((5 + (line * 100)),(100 + display_offset)),((5 + (line * 100)),(100 + display_offset + 500)))
        pygame.draw.ellipse(self.screen,self.colors['football'],(((10 * field.absolute_yardline) + 90), (display_offset + 300),30,15))
    
    
        pygame.display.update()

        print scoreboard.scoreboard['period'],scoreboard.scoreboard['clock']
        print end_of_game, human_control
        
        if human_control and not end_of_game:
            self.check_user_input(run_play)       
