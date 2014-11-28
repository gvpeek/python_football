'''
Created on May 31, 2012

@author: George Peek
'''

import state_machine

events = [{'touchback' : False},
          {'punt' : False},
          {'kick_attempt' : False},
          {'kick_successful' : False},
          {'safety' : False},
          {'offense_touchdown' : False},
          {'defense_touchdown' : False}]

for event in events:
    print event
    
current_state = state_machine.initialize_state()
    