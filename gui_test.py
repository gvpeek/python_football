'''
Created on Aug 19, 2012

@author: George Peek
'''

import sys
import pprint
import pygame
from pygame.locals import *

from game import Game
from play import Team

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

run_inside = PlayButton(reset_coords,'run inside','run')
run_outside = PlayButton(reset_coords,'run outside','run')
pass_short = PlayButton(reset_coords,'pass short','pass')
pass_medium = PlayButton(reset_coords,'pass medium','pass')
pass_long = PlayButton(reset_coords,'pass long','pass')
kickoff = PlayButton(reset_coords,'kickoff','special')
onside_kickoff = PlayButton(reset_coords,'onside kickoff','special')
extra_point = PlayButton(reset_coords,'extra point','special')
punt = PlayButton(reset_coords,'punt','special')
field_goal = PlayButton(reset_coords,'field goal','special') 
run_clock = PlayButton(reset_coords,'run clock','special')


play_buttons = [run_inside, run_outside, pass_short, pass_medium, pass_long, kickoff, onside_kickoff, extra_point, punt, field_goal, run_clock]


while True:
    
    fps.tick(5)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouse_pos = myfont.render(str(mousex) + ',' + str(mousey), True, white)
            
            if run_inside.rect.collidepoint((mousex, mousey)):
                game.plays[-1].run_inside()
                game.current_state.check_state(game)
            if run_outside.rect.collidepoint((mousex, mousey)):
                game.plays[-1].run_outside()
                game.current_state.check_state(game)
            if pass_short.rect.collidepoint((mousex, mousey)):
                game.plays[-1].pass_short()
                game.current_state.check_state(game)
            if pass_medium.rect.collidepoint((mousex, mousey)):
                game.plays[-1].pass_medium()
                game.current_state.check_state(game)
            if pass_long.rect.collidepoint((mousex, mousey)):
                game.plays[-1].pass_long()
                game.current_state.check_state(game)
            if kickoff.rect.collidepoint((mousex, mousey)):
                game.plays[-1].kickoff()
                game.current_state.check_state(game)
            if onside_kickoff.rect.collidepoint((mousex, mousey)):
                game.plays[-1].onside_kickoff()
                game.current_state.check_state(game)
            if extra_point.rect.collidepoint((mousex, mousey)):
                game.plays[-1].extra_point()
                game.current_state.check_state(game)
            if punt.rect.collidepoint((mousex, mousey)):
                game.plays[-1].punt()
                game.current_state.check_state(game)
            if field_goal.rect.collidepoint((mousex, mousey)):
                game.plays[-1].field_goal()
                game.current_state.check_state(game)
            if run_clock.rect.collidepoint((mousex, mousey)):
                game.plays[-1].run_clock()
                game.current_state.check_state(game)
    
    screen.fill(blue)
    try:
        screen.blit(mouse_pos,(1100,10))
    except:
        pass

    home_name = myfont.render(game.home.city + game.home.nickname + ' -- ' + str(game.scoreboard.home_score), True, white)
    away_name = myfont.render(game.away.city + game.away.nickname + ' -- ' + str(game.scoreboard.away_score), True, white)
    current_state = myfont.render(str(game.current_state), True, white)
    abs_yardline = myfont.render("Yardline: " + game.scoreboard.absolute_yardline, True, white)
    direction = myfont.render("Direction: " + str(game.field.direction), True, white)
    play_name = myfont.render("Play: " + str(game.scoreboard.play_name), True, white)
    play_rating = myfont.render("Rating: " + str(game.scoreboard.play_rating), True, white)
    playsh = myfont.render("H: " + str(game.home.plays_run) + str(game.home.total_plays_run), True, white)
    playsa = myfont.render("A: " + str(game.away.plays_run) + str(game.away.total_plays_run), True, white)
    yards_gained = myfont.render("Off Yards: " + str(game.scoreboard.offense_yardage), True, white)
    return_yards = myfont.render("Ret Yards: " + str(game.scoreboard.return_yardage), True, white)
    turnover = myfont.render("Turnover: " + str(game.scoreboard.turnover), True, white)
    quarter = myfont.render("Qtr: " + str(game.scoreboard.period), True, white)
    clock = myfont.render("Time: " + str(game.scoreboard.clock), True, white)
    down = myfont.render("Down: " + str(game.scoreboard.down), True, white)
    yards_to_go = myfont.render("Yards To Go: " + str(game.scoreboard.yards_to_go), True, white)

## stats display
    display = [current_state, play_name, yards_gained, return_yards, turnover, quarter, clock, down, yards_to_go, abs_yardline, direction, play_rating, playsh, playsa]
    display_offset = 0
    horizontal_offset = 0
    
    screen.blit(home_name, (25,5))
    screen.blit(away_name, (180,5))
    if game.field.direction == 1:
        pygame.draw.circle(screen,white,(10,12),5)
    elif game.field.direction == -1:
        pygame.draw.circle(screen,white,(165,12),5)
            
    for item in display:
        screen.blit(item, (5,35 + display_offset))
        display_offset += 20
        
## play button display
    for button in play_buttons:
        button.update_coords(reset_coords)
        
    for button in game.current_state.play_choice:
        vars()[button].update_coords(((5 + horizontal_offset),(50 + display_offset)))
        vars()[button].display_button()
        horizontal_offset += 130
  
## field display
    pygame.draw.rect(screen,(0,255,0),(5,(100 + display_offset),1200,500))
    pygame.draw.rect(screen,game.home.primary_color,(5,(100 + display_offset),100,500))
    pygame.draw.rect(screen,game.away.primary_color,(1105,(100 + display_offset),100,500))
    for line in range(12):
        pygame.draw.line(screen,(255,255,255),((5 + (line * 100)),(100 + display_offset)),((5 + (line * 100)),(100 + display_offset + 500)))
    pygame.draw.ellipse(screen,(0,0,0),(((10 * game.field.absolute_yardline) + 90), (display_offset + 300),30,15))


    pygame.display.update()
