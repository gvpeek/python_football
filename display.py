'''
Created on Aug 19, 2012

@author: George Peek
'''

import sys
import os

from pprint import pprint

import pygame
from pygame.locals import *

class PlayButton():
    def __init__(self, coords, play,base_font,colors):
        self.play = play
        self.width = 80
        self.height = 30
        self.rect = pygame.Rect(coords,(self.width,self.height))
                
        if play.is_rush():
            if play.name == 'Run Clock':
                self.group = 0
                self.color = colors['special_button']
                text_color=colors['black']
            else:
                self.group = 1
                self.color = colors['rush_button']
                text_color=colors['white']
        elif play.is_pass():
            text_color=colors['white']
            self.group = 2
            self.color = colors['pass_button']
        else:
            text_color=colors['black']
            self.group = 0
            self.color = colors['special_button']
        
        self.text = base_font.render(play.short_name.upper(), True, text_color)
        self.text_pos = self.text.get_rect()
            
    def display_button(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.text_pos)
        
    def update_coords(self, new_coords):
        self.rect = pygame.Rect(new_coords,(self.width,self.height))
        self.text_pos.centerx, self.text_pos.centery = self.rect.centerx, self.rect.centery


class Display():
    def __init__(self,field,scoreboard):
        pygame.init()
        
        self.screen = pygame.display.set_mode((700,600))
        self.base_font = pygame.font.SysFont('franklingothicbook',12)
        self.sb_sm_font = pygame.font.SysFont('franklingothicbold',18)
        self.sb_lg_font = pygame.font.SysFont('franklingothicbold',24)
        self.sb_xl_font = pygame.font.SysFont('franklingothicbold',48)
        self.ez_font = pygame.font.SysFont('franklingothicbold',36)
        self.fps = pygame.time.Clock()
        self.reset_coords = (-1000,-1000)
        self.play_buttons=[]
        self.colors = {'white' : (255,255,255),
                  'black' : (0,0,0),
                  'background' : (51,153,204),
                  'scoreboard' : (88,89,91),
                  'scoreboard_text' : (255,255,255),
                  'field' : (153,204,51),
                  'football' : (139,69,19),
                  'rush_button' : (255,102,51),
                  'pass_button' : (51,102,153),
                  'special_button' : (255,204,0)}

        self.build_static_elements(field,scoreboard)
        
    def build_static_elements(self,field,scoreboard):
        self.scoreboard_rect = pygame.Rect(5,5,300,200)
        self.home_text = self.sb_lg_font.render("HOME",
                                            True,
                                            self.colors['scoreboard_text'])
        self.away_text = self.sb_lg_font.render("AWAY",
                                            True,
                                            self.colors['scoreboard_text'])
        self.home_poss = [self.screen,self.colors['scoreboard_text'],(15,35),5,1]
        self.away_poss = [self.screen,self.colors['scoreboard_text'],(165,35),5,1]
        
        self.home_city = self.sb_lg_font.render(scoreboard.scoreboard['home_city'],
                                            True,
                                            self.colors['scoreboard_text'])
        self.home_nick = self.sb_lg_font.render(scoreboard.scoreboard['home_nickname'],
                                            True,
                                            self.colors['scoreboard_text'])
        self.away_city = self.sb_lg_font.render(scoreboard.scoreboard['away_city'],
                                            True,
                                            self.colors['scoreboard_text'])
        self.away_nick = self.sb_lg_font.render(scoreboard.scoreboard['away_nickname'],
                                            True,
                                            self.colors['scoreboard_text'])
        
        
        self.qtr_text = self.sb_sm_font.render("QTR",
                                               True,
                                               self.colors['scoreboard_text'])
        self.qtr_indic = [[self.screen,self.colors['scoreboard_text'],((50+(x*15)),115),5,1] for x in xrange(4)]
        self.down_text = self.sb_sm_font.render("DOWN",
                                               True,
                                               self.colors['scoreboard_text'])
        self.down_indic = [[self.screen,self.colors['scoreboard_text'],((220+(x*15)),115),5,1] for x in xrange(4)]
        self.ydln_text = self.sb_sm_font.render("YARDLINE",
                                               True,
                                               self.colors['scoreboard_text'])
        self.ytg_text = self.sb_sm_font.render("YDS TO GO",
                                               True,
                                               self.colors['scoreboard_text'])
        self.time = self.sb_xl_font.render(scoreboard.scoreboard['clock'], 
                                           True, 
                                           self.colors['scoreboard_text'])
        self.time_pos = self.time.get_rect()
        self.time_pos.centerx, self.time_pos.centery = self.scoreboard_rect.centerx, 180
                
        self.logo = pygame.image.load(os.path.join('images','fieldlogo.png'))
        logo_width, logo_height = self.logo.get_size()
        scaler=.14
        self.logo = pygame.transform.scale(self.logo,(int(logo_width * scaler),int(logo_height * scaler)))

        self.football = pygame.image.load(os.path.join('images','football.png'))
        football_width, football_height = self.football.get_size()
        scaler=.33
        self.football = pygame.transform.scale(self.football,(int(football_width * scaler),int(football_height * scaler)))
        
        # build field elements
        self.field_seg = (.5 * field.length)
        field_top=300
        self.field_rect=pygame.Rect(5,
                               field_top,
                               (12*self.field_seg),
                               ((12*self.field_seg)/2.4))
        self.home_ez_rect=pygame.Rect(5,
                                 field_top,
                                  (self.field_seg),
                                  ((12*self.field_seg)/2.4))
        self.away_ez_rect=pygame.Rect(((11*self.field_seg)+5),
                                 field_top,
                                 (self.field_seg),
                                 ((12*self.field_seg)/2.4))

        self.field_lines=[]
        for x in range(1, int((field.length / 10.0)) + 2): # field lines
            self.field_lines.append([((5 + (x * (field.length / 2.0))),(field_top)),
                                    ((5 + (x * (field.length / 2.0))),(field_top + (6*field.length)/2.4))])
        
        self.home_ez_text=self.ez_font.render(scoreboard.scoreboard['home_city'].upper(),
                                                         True,
                                                         field.endzone_color['home_secondary'])
        self.home_ez_text=pygame.transform.rotate(self.home_ez_text,90)
        self.home_ez_textpos=self.home_ez_text.get_rect()
        self.home_ez_textpos.centerx, self.home_ez_textpos.centery=self.home_ez_rect.centerx, self.home_ez_rect.centery

        self.away_ez_text=self.ez_font.render(scoreboard.scoreboard['away_city'].upper(),
                                                         True,
                                                         field.endzone_color['away_secondary'])
        self.away_ez_text=pygame.transform.rotate(self.away_ez_text,-90)
        self.away_ez_textpos=self.away_ez_text.get_rect()
        self.away_ez_textpos.centerx, self.away_ez_textpos.centery=self.away_ez_rect.centerx, self.away_ez_rect.centery        

        self.logo_pos = self.logo.get_rect()
        self.logo_pos.centerx, self.logo_pos.centery = self.field_rect.centerx, self.field_rect.centery        
        
    def check_user_input(self,run_play):
#        print 'user input...'
        try:
            while True:
                self.fps.tick(5)
                
                for event in pygame.event.get():
                    if event.type == QUIT:
    #                    sys.exit()
                        pygame.quit()
                        break
                    
                    elif event.type == MOUSEBUTTONDOWN:
                        mousex, mousey = event.pos
                        
                        for button in self.play_buttons:
                            if button.rect.collidepoint((mousex, mousey)):
                                run_play(button.play)
                                break
        except:
            pygame.quit()
        

    def update(self,*args):
        human_control, end_of_game, run_play, available_plays, field, scoreboard = args[0]

#        print scoreboard.scoreboard['description']
        ## update dynamic elements
        self.home_score = self.sb_xl_font.render(str(scoreboard.scoreboard['home_score']), 
                                                True, 
                                                self.colors['scoreboard_text'])
        self.away_score = self.sb_xl_font.render(str(scoreboard.scoreboard['away_score']), 
                                                True, 
                                                self.colors['scoreboard_text'])        
        self.ydln = self.sb_sm_font.render(scoreboard.scoreboard['yardline'], 
                                                True, 
                                                self.colors['scoreboard_text'])
        self.ytg = self.sb_sm_font.render(scoreboard.scoreboard['yards_to_go'], 
                                                True, 
                                                self.colors['scoreboard_text'])
        self.time = self.sb_xl_font.render(scoreboard.scoreboard['clock'], 
                                           True, 
                                           self.colors['scoreboard_text'])
        
        self.screen.fill(self.colors['background'])
        
 
        pygame.draw.rect(self.screen,
                         self.colors['scoreboard'],
                         self.scoreboard_rect)
        self.screen.blit(self.home_text,
                         (10,10))
        self.screen.blit(self.away_text,
                         (160,10))

    
    ## scoreboard display

        self.screen.blit(self.home_city,(10,50))
        self.screen.blit(self.home_nick,(10,70))
        self.screen.blit(self.away_city,(160,50))
        self.screen.blit(self.away_nick,(160,70))
        self.screen.blit(self.home_score,(100,10))
        self.screen.blit(self.away_score,(250,10))
        
        if scoreboard.scoreboard['possession'] == 'Home':
            self.home_poss[4] = 0
            self.away_poss[4] = 1
        if scoreboard.scoreboard['possession'] == 'Away':
            self.home_poss[4] = 1
            self.away_poss[4] = 0
                    
        pygame.draw.circle(*self.home_poss)
        pygame.draw.circle(*self.away_poss)        

        qtr = int(scoreboard.scoreboard['period']) % 4
        self.screen.blit(self.qtr_text,(10,110))
        for item in self.qtr_indic:
            if qtr == 0 and self.qtr_indic.index(item) == 3:
                item[4] = 0
            elif (qtr - 1) == self.qtr_indic.index(item):
                item[4] = 0
            else:
                item[4] = 1
            pygame.draw.circle(*item)
 
        if scoreboard.scoreboard['down']:
            down = int(scoreboard.scoreboard['down'])
        else:
            down = 0
        self.screen.blit(self.down_text,(160,110))
        for item in self.down_indic:
            if (down - 1) == self.down_indic.index(item):
                item[4] = 0
            else:
                item[4] = 1
            pygame.draw.circle(*item)
        self.screen.blit(self.ydln_text,(10,140))
        self.screen.blit(self.ydln,(100,140))
        self.screen.blit(self.ytg_text,(160,140))
        self.screen.blit(self.ytg,(250,140))
        self.screen.blit(self.time,self.time_pos)
            
    ## play button display
        button_column = 320
        button_offset = {0 : button_column,
                         1 : button_column,
                         2 : button_column}

        self.play_buttons = [PlayButton(self.reset_coords,
                                        play,
                                        self.base_font,
                                        self.colors) for play in available_plays.values()]
        for button in self.play_buttons:
            button.update_coords(((5 + button_offset[button.group]),(102 + ((button.group *  (1.2 * button.rect.height))))))
            button.display_button(self.screen)
            button_offset[button.group] += 100

    ## field display
        

        # draw field elements
        pygame.draw.rect(self.screen, # full field
                         self.colors['field'],
                         self.field_rect)        
        pygame.draw.rect(self.screen, # home endzone
                         field.endzone_color['home_primary'],
                         self.home_ez_rect)
        pygame.draw.rect(self.screen, #away endzone
                         field.endzone_color['away_primary'],
                         self.away_ez_rect)

        self.screen.blit(self.home_ez_text,self.home_ez_textpos)
        self.screen.blit(self.away_ez_text,self.away_ez_textpos)
        
        for line in self.field_lines: # field lines
            pygame.draw.line(self.screen,
                             self.colors['white'],
                             line[0],
                             line[1])
        self.screen.blit(self.logo,self.logo_pos)
        self.screen.blit(self.football,
                         (((5 * field.absolute_yardline) + (self.field_seg)),(self.field_rect.top + 200)))
    
        pygame.display.update()

        if human_control or end_of_game:
            if end_of_game:
                pprint 
            self.check_user_input(run_play)     
            
            
            
#### testing
#from game import Game
#from team import Team
#
#team1 = Team("Austin","Easy")
#team2 = Team("Chula Vista","Grown Men")
#game = Game(team1,team2,display=Display)
#
#game.start_game(.2)  
