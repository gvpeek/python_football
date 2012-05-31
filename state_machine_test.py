'''
Created on May 31, 2012

@author: George Peek
'''

class State():
    "Basic State"
    def __init__(self):
        pass
    
class DownSet(State):
    "State for normal offensive possession"
    def __init__(self):
        self.down = 1
        self.yardsToGo = 10
        self.converted = False
        self.active = True
        
    def convertCheck(self,playResult):
        if not self.active:
            return False
        
        self.yardsToGo -= playResult
        if (self.yardsToGo <= 0):
            self.converted = True
            self.active = False
            return self.converted 
        elif (self.down == 4):
            self.active = False
            return self.active
        else:
            self.down += 1
            return self.down, self.yardsToGo
        