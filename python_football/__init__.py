from game import Game
from team import Team
from coach import Coach
from stats import StatBook
from playbook import Playbook

def new_game(**kwargs):
    return Game(**kwargs)
    
def new_team(**kwargs):
    return Team(**kwargs)
    
def new_statbook():
    return StatBook()
    
def new_playbook():
    return Playbook()

def new_coach(**kwargs):
    return Coach(**kwargs)