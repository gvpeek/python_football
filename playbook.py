'''
Created on Mar 24, 2013

@author: George
'''

from random import randint, choice
from math import ceil, floor

class Playbook(list):
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.append(Rush(0,
                         0,
                         -2,
                         1,
                         0,
                         'Run Clock',
                         (1,2,3,4,'C'),
                         0,
                         (0.0,0.0),
                         {},
                         {}))
        self.append(Rush(-.7,
                         -1,
                         -5.0,
                         3.5,
                         1,
                         'Run Inside',
                         (1,2,3,4,'C'),
                         0,
                         (35.0,90.0),
                         {'qb':1,'rb':4,'wr':0,'ol':5},
                         {'dl':6,'lb':3,'cb':0,'s':1}))
        self.append(Rush(-.7,
                         -1,
                         -5.0,
                         3.5,
                         1,
                         'Run Outside',
                         (1,2,3,4,'C'),
                         0,
                         (35.0,90.0),
                         {'qb':1,'rb':5,'wr':1,'ol':3},
                         {'dl':3,'lb':5,'cb':1,'s':1}))
        self.append(Pass(-.7,
                         -1,
                         -5.0,
                         3.5,
                         1,
                         'Pass Short',
                         (1,2,3,4,'C'),
                         0,
                         (35.0,90.0),
                         {'qb':4,'rb':3,'wr':2,'ol':1},
                         {'dl':1,'lb':5,'cb':3,'s':1}))
        self.append(Pass(-.5,
                         -.8309,
                         -8.0,
                         10,
                         1,
                         'Pass Medium',
                         (1,2,3,4,'C'),
                         5,
                         (35.0,90.0),
                         {'qb':4,'rb':0,'wr':4,'ol':2},
                         {'dl':2,'lb':2,'cb':4,'s':2}))
        self.append(Pass(-.4,
                         -.5,
                         -12.0,
                         10,
                         2,
                         'Pass Long',
                         (1,2,3,4,'C'),
                         10,
                         (35.0,90.0),
                         {'qb':4,'rb':0,'wr':3,'ol':3},
                         {'dl':3,'lb':1,'cb':3,'s':3}))
        self.append(Kickoff(20,
                            55,
                            False,
                            'Kickoff',
                            ('K','F'),
                            0,
                            (60.0,100.0),
                            {'sp':1},
                            {}))
        self.append(Kickoff(10,
                            10,
                            True,
                            'Onside Kickoff',
                            ('K','F'),
                            0,
                            (60.0,100.0),
                            {'sp':1},
                            {}))
        self.append(Punt('Punt',
                         (1,2,3,4,'F'),
                         0,
                         (60.0,100.0),
                         {'sp':1},
                         {}))
        self.append(FieldGoal('Field Goal',
                         (1,2,3,4),
                         0,
                         (60.0,90.0),
                         {'sp':1},
                         {}))
        self.append(FieldGoal('Extra Point',
                         ('C'),
                         0,
                         (60.0,90.0),
                         {'sp':1},
                         {}))
        
play_id = 0
global play_id

class Play():
    def __init__(self,
                 name,
                 valid_downs,
                 valid_yardline = 0,
                 rating_bounds = (0.0,100.0),
                 offense_weights={},
                 defense_weights={}):
        '''
        valid_downs = (1,2,3,4,'K','F','E')
        valid for entire field (default) - valid_yardline = 0
        invalid within 10 yards of endzone - valid_yardline = 10
        offense_weights = {'qb':4,'rb':1,'wr':3,'ol':2}
        defense_weights = {'dl':3,'lb':2,'cb':3,'s':2}
        '''
        self.id = self.next_play_id()
        self.name=name
        self.valid_downs = valid_downs
        self.rating_bounds = rating_bounds
        self.valid_yardline = valid_yardline
        self.offense_weights = offense_weights
        self.defense_weights = defense_weights

    def next_play_id(self):
        global play_id
        play_id += 1
        return play_id 

    def determine_play_rating(self,
                              off_skills,
                              def_skills,
                              rating_penalty):
        off_rating = ceil(sum([(self.offense_weights[pos] * off_skills[pos]) for pos in self.offense_weights]) / (.0001 + sum(self.offense_weights.values())))
        off_rating -= rating_penalty
        def_rating = ceil(((sum([(self.defense_weights[pos] * def_skills[pos]) for pos in self.defense_weights]) / (.0001 + sum(self.defense_weights.values()))) - 60) / 4)
        play_rating = off_rating - def_rating
                     
        if play_rating < min(self.rating_bounds):
            play_rating = min(self.rating_bounds)
        elif play_rating > max(self.rating_bounds):
            play_rating = max(self.rating_bounds)
            
        return play_rating
    
    def determine_turnover(self,rating,adjustment,multiplier):
        return randint(1,100) <= (((100 - rating) / adjustment) * multiplier)
       
    def determine_return_yardage(self, def_skills,off_yardage):
        return_rnd = randint(1,100)
        if isinstance(self, Kickoff) or isinstance(self, Punt):
            pos = 'sp'
            if off_yardage <= 15:
                adjustment = -1
            elif off_yardage <= 30:
                adjustment = -.8
            elif off_yardage <= 50:
                adjustment = -.6
            else:
                adjustment = -.4
        elif off_yardage <= 3:
            pos = 'dl'
            adjustment=-1
        elif off_yardage <= 10:
            pos = 'lb'
            adjustment=-.8
        elif off_yardage <= 20:
            pos = 'cb'
            adjustment=-.7
        else:
            pos = 's'
            adjustment=-.6
        print '****', pos, def_skills[pos], adjustment
        return floor(((def_skills[pos]*100)*pow(return_rnd,adjustment)) / 100)
        
    def determine_play_success(self,rating):
        return randint(1,100) <= rating
    
    def determine_play_yardage(self,rating,success,turnover,gain_adjustment,loss_adjustment,max_loss):
        yardage_rnd = randint(1,100)
        loss_rating = ((90 - rating) + 60)
        if success or turnover:
            offense_yardage = floor(((rating*100)*pow(yardage_rnd,gain_adjustment)) / 100)
        else:
            offense_yardage = -(floor(((loss_rating*100)*pow(yardage_rnd,loss_adjustment)) / 100))
        if offense_yardage < max_loss:
            offense_yardage= max_loss
        return offense_yardage

class Rush(Play):
    def __init__(self,
                 gain_adjust,
                 loss_adjust,
                 play_multiplier,
                 turnover_adjust,
                 turnover_multiplier,
                 *args):
        Play.__init__(self,*args)

        self.gain_adjust = gain_adjust
        self.loss_adjust = loss_adjust
        self.turnover_adjust = turnover_adjust
        self.turnover_multiplier = turnover_multiplier
        self.play_multiplier = play_multiplier
        
    def run(self,
            off_skills,
            def_skills,
            rating_penalty):
        turnover = False
        return_yardage = 0

        play_rating = self.determine_play_rating(off_skills, def_skills, rating_penalty)
        play_success = self.determine_play_success(play_rating)
        if not play_success:
            turnover = self.determine_turnover(play_rating,self.turnover_adjust, self.turnover_multiplier)
        off_yardage = self.determine_play_yardage(play_rating, play_success, turnover, self.gain_adjust, self.loss_adjust, self.play_multiplier)
        if turnover:
            return_yardage = self.determine_return_yardage(def_skills, off_yardage)
        
        return off_yardage, turnover, return_yardage

class Pass(Play):
    def __init__(self,
                 gain_adjust,
                 loss_adjust,
                 play_multiplier,
                 turnover_adjust,
                 turnover_multiplier,
                 *args):
        Play.__init__(self,*args)

        self.gain_adjust = gain_adjust
        self.loss_adjust = loss_adjust
        self.turnover_adjust = turnover_adjust
        self.turnover_multiplier = turnover_multiplier
        self.play_multiplier = play_multiplier
        
    def run(self,
            off_skills,
            def_skills,
            rating_penalty):
        turnover = False
        return_yardage = 0

        play_rating = self.determine_play_rating(off_skills, def_skills, rating_penalty)
        play_success = self.determine_play_success(play_rating)
        if not play_success:
            turnover = self.determine_turnover(play_rating,self.turnover_adjust, self.turnover_multiplier)
        off_yardage = self.determine_play_yardage(play_rating, play_success, turnover, self.gain_adjust, self.loss_adjust, self.play_multiplier)
        if turnover:
            return_yardage = self.determine_return_yardage(def_skills, off_yardage)
        
        return off_yardage, turnover, return_yardage
    
class Kickoff(Play):
    def __init__(self,
                 random_cap, 
                 adjustment,
                 recoverable,
                 *args):
        Play.__init__(self, *args)
        
        self.random_cap = random_cap
        self.adjustment = adjustment
        self.recoverable = recoverable
    
    def determine_play_yardage(self, rating, random_cap, adjustment):
        kick_rnd = randint(1,random_cap) + adjustment
        kick_rating = (80 - rating) / 2
        return ceil(kick_rnd - kick_rating)
        
    def run(self,
            off_skills,
            def_skills,
            rating_penalty):
        turnover = False
        return_yardage = 0

        play_rating = self.determine_play_rating(off_skills, def_skills, rating_penalty)
        off_yardage = self.determine_play_yardage(play_rating, self.random_cap, self.adjustment)
        if self.recoverable and off_yardage >= 10:
            turnover = randint(1,100) <= ceil(off_skills['sp'] / 4)
        if not turnover:
            return_yardage = self.determine_return_yardage(def_skills, off_yardage)
        
        return off_yardage, turnover, return_yardage    
    
class Punt(Play):
    def __init__(self,
                 *args):
        Play.__init__(self, *args)
    
    def determine_play_yardage(self,rating):
        punt_rnd = randint(1,100)
        pivot_point = ceil(rating / 1.7)
        pivot_direction = choice([-1,1])
 
        # enforce minimum punt yardage
        if pivot_direction == -1 and punt_rnd < 5.0:
            punt_rnd = 5.0
        # enforce maximum punt yardage
        if pivot_direction == 1 and punt_rnd < 7.0:
            punt_rnd = 7.0

        return (pivot_point + (pivot_direction * floor(((rating*100) * pow(punt_rnd,-.8309)) / 100)))
            
    def determine_punt_block(self,rating):
        return (randint(1,100)*randint(0,1)) == rating
    
    def run(self,
            off_skills,
            def_skills,
            rating_penalty):
        turnover = False
        return_yardage = 0    
    
        play_rating = self.determine_play_rating(off_skills, def_skills, rating_penalty)
        turnover = self.determine_punt_block(play_rating)
        if not turnover:
            off_yardage = self.determine_play_yardage(play_rating)
        else:
            off_yardage = 0.0
        return_yardage = self.determine_return_yardage(def_skills, off_yardage)

        return off_yardage, turnover, return_yardage
    
class FieldGoal(Play):
    def __init__(self,
                 *args):
        Play.__init__(self, *args)
        
        ''' 
        Field Goal returns maximum distance for a successful kick
        in the off_yardage variable. If yardline is less than or 
        equal to that value, the kick is good. 
        '''

    
    def determine_play_yardage(self,rating):
        kick_rnd = randint(1,100)
        if kick_rnd > 30:
            success_range = (rating / 75.0 * 30) + (.2 * (kick_rnd - 30))
        else:
            success_range = rating / 75.0 * kick_rnd
        return success_range
            
    def run(self,
            off_skills,
            def_skills,
            rating_penalty):
        turnover = False
        return_yardage = 0    
    
        play_rating = self.determine_play_rating(off_skills, def_skills, rating_penalty)
        off_yardage = self.determine_play_yardage(play_rating)
        
        return off_yardage, turnover, return_yardage