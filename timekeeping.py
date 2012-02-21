'''
Created on Feb 21, 2012

@author: peekgv
'''

#===============================================================================
# >>> number_of_quarters = 4
# >>> from collections import deque
# >>> d = deque()
# >>> for i in range(number_of_quarters):
#    d.append(Clock())
# 
# >>> ct = None    
# >>> if not ct:
#    ct = d.popleft()
# >>> while ct.minutes > 0 or ct.seconds > 0:
#    ct.run_clock()
#===============================================================================


from copy import deepcopy

class Clock(object):
    "Basic Clock"
    def __init__(self, quarter_length=15):
        self.minutes = deepcopy(quarter_length)
        self.seconds = 00
        self.clicks = 0
        self.active = True

    def run_clock(self):

        if self.active:
            self.clicks += 1
    
            if (self.clicks % 2) > 0:
                self.minutes -= 1
                self.seconds = 30
            else:
                self.seconds = 0
        
        if self.minutes == 0 and self.seconds == 0:
            self.active = False

        return self.minutes, self.seconds, self.active