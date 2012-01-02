import random
import math
import names
import sqlite3

nextID = 0
year = 1
positionTypes = ['QB']*3+['RB']*5+['WR']*5+['TE']*3+['OG']*4+['OT']*4+['C']*3+['DT']*4+['DE']*4+['LB']*6+['S']*4+['CB']*6+['K']+['P']

class Player():
    "Basic Player"
    def __init__(self, id = 0):
        self.id = nextID
        self.age = 11
        self.firstName = names.firstName()
        self.lastName = names.lastName()
        self.position = random.choice(positionTypes)
        self.speed = random.randint(20,45)
        self.strength = random.randint(20,45)
        self.stamina = random.randint(20,45)
        self.constitution = random.randint(20,45)
        self.agility = random.randint(20,45)
        self.intelligence = random.randint(20,45)
        self.discipline = random.randint(20,45)        
        self.retirementAge = (self.constitution - self.age) + 10
        self.retired = ' '
        self.apexAge = (math.floor(((32 * 100) * math.pow(random.randint(5,100),-.5)) / 100) + 18)
        # self.apexAge = random.randint(20,32)
        self.growthRate = random.randint(1,4)
        self.declinationRate = random.randint(3,5)
        self.rating = (self.speed + self.strength + self.stamina + self.constitution + self.agility + self.intelligence + self.discipline) / 7


        self.passing = tertiaryRating()
        self.rushing = tertiaryRating()
        self.catching = tertiaryRating()
        self.blocking = tertiaryRating()
        self.rundefense = tertiaryRating()
        self.passdefense = tertiaryRating()
        self.kicking = tertiaryRating()
        initialPositionRatings(self)

def primaryRating():
    primerate = random.randint(30,45)
    return primerate

def secondaryRating():
    secondrate = random.randint(20,35)
    return secondrate

def tertiaryRating():
    thirdrate = random.randint(1,20)
    return thirdrate

def initialPositionRatings(player):
    if player.position == 'QB':
        player.passing = primaryRating()
        player.rushing = secondaryRating()
    if player.position == 'RB':
        player.rushing = primaryRating()
        player.catching = secondaryRating()
        player.blocking = secondaryRating()        
    if player.position == 'WR':
        player.catching = primaryRating()
        player.rushing = secondaryRating()
    if player.position == 'TE':
        player.catching = primaryRating()    
        player.blocking = secondaryRating()
    if player.position == 'OG':
        player.blocking = primaryRating()    
    if player.position == 'OT':
        player.blocking = primaryRating()    
    if player.position == 'C':
        player.blocking = primaryRating()    
    if player.position == 'DT':
        player.rundefense = primaryRating()    
        player.passdefense = secondaryRating()
    if player.position == 'DE':
        player.rundefense = primaryRating()    
        player.passdefense = secondaryRating()
    if player.position == 'LB':
        randomPrimary = random.choice(['pass','run'])
        if randomPrimary == 'pass':
            player.passdefense = primaryRating()
            player.rundefense = secondaryRating()
        if randomPrimary == 'run':
            player.rundefense = primaryRating()                
            player.passdefense = secondaryRating()
    if player.position == 'CB':
        player.passdefense = primaryRating()    
        player.rundefense = secondaryRating()
    if player.position == 'S':
        player.passdefense = primaryRating()    
        player.rundefense = secondaryRating()
    if player.position == 'K':
        player.kicking = primaryRating()    
    if player.position == 'P':
        player.kicking = primaryRating()


def increasePositionRatings(player,primegrowth):
    secondgrowth = math.ceil(primegrowth / 2)
    thirdgrowth = random.randint(0,1)
    if player.position == 'QB':
        player.passing = player.passing + primegrowth
        player.rushing = player.rushing + secondgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'RB':
        player.rushing = player.rushing + primegrowth
        player.catching = player.catching + secondgrowth
        player.blocking = player.blocking + secondgrowth        
        player.passing = player.passing + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'WR':
        player.catching = player.catching + primegrowth
        player.rushing = player.rushing + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'TE':
        player.catching = player.catching + primegrowth    
        player.blocking = player.blocking + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'OG':
        player.blocking = player.blocking + primegrowth    
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'OT':
        player.blocking = player.blocking + primegrowth    
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'C':
        player.blocking = player.blocking + primegrowth    
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'DT':
        player.rundefense = player.rundefense + primegrowth    
        player.passdefense = player.passdefense + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'DE':
        player.rundefense = player.rundefense + primegrowth    
        player.passdefense = player.passdefense + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'LB':
        player.passdefense = player.passdefense + primegrowth
        player.rundefense = player.rundefense + primegrowth                
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'CB':
        player.passdefense = player.passdefense + primegrowth    
        player.rundefense = player.rundefense + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'S':
        player.passdefense = player.passdefense + primegrowth    
        player.rundefense = player.rundefense + secondgrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.kicking = player.kicking + thirdgrowth
    if player.position == 'K':
        player.kicking = player.kicking + primegrowth    
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth
    if player.position == 'P':
        player.kicking = player.kicking + primegrowth
        player.passing = player.passing + thirdgrowth
        player.rushing = player.rushing + thirdgrowth
        player.catching = player.catching + thirdgrowth
        player.blocking = player.blocking + thirdgrowth
        player.rundefense = player.rundefense + thirdgrowth
        player.passdefense = player.passdefense + thirdgrowth


def advanceYear(player):
    "Advance Year"
    highschoolcap = 65
    collegecap = 75
    procap = 90
    if player.age > player.retirementAge:
        player.retired = 'X'
    if player.retired != 'X':
        primegrowth = random.randint(1,player.growthRate)
        decl = random.randint(3,player.declinationRate)
        player.age = player.age + 1

        if player.age <= player.apexAge:
            increasePositionRatings(player,primegrowth)
            player.speed = player.speed + primegrowth
            player.strength = player.strength + primegrowth
            player.stamina = player.stamina + primegrowth
            player.constitution = player.constitution + primegrowth
            player.agility = player.agility + primegrowth
            player.intelligence = player.intelligence + primegrowth
            player.discipline = player.discipline + primegrowth

            if player.age >= 15 and player.age <= 18:
                if player.speed > highschoolcap:
                    player.speed = highschoolcap
                if player.strength > highschoolcap:
                    player.strength = highschoolcap
                if player.stamina > highschoolcap:
                    player.stamina = highschoolcap
                if player.constitution > highschoolcap:
                    player.constitution = highschoolcap
                if player.agility > highschoolcap:
                    player.agility = highschoolcap
                if player.intelligence > highschoolcap:
                    player.intelligence = highschoolcap
                if player.discipline > highschoolcap:
                    player.discipline = highschoolcap                    
                if player.passing > highschoolcap:
                    player.passing = highschoolcap
                if player.rushing > highschoolcap:
                    player.rushing = highschoolcap
                if player.catching > highschoolcap:
                    player.catching = highschoolcap
                if player.blocking > highschoolcap:
                    player.blocking = highschoolcap
                if player.rundefense > highschoolcap:
                    player.rundefense = highschoolcap
                if player.passdefense > highschoolcap:
                    player.passdefense = highschoolcap
                if player.kicking > highschoolcap:
                    player.kicking = highschoolcap
                    
            if player.age >= 19 and player.age <= 22:
                if player.speed > collegecap:
                    player.speed = collegecap
                if player.strength > collegecap:
                    player.strength = collegecap
                if player.stamina > collegecap:
                    player.stamina = collegecap
                if player.constitution > collegecap:
                    player.constitution = collegecap
                if player.agility > collegecap:
                    player.agility = collegecap
                if player.intelligence > collegecap:
                    player.intelligence = collegecap
                if player.discipline > collegecap:
                    player.discipline = collegecap                       
                if player.passing > collegecap:
                    player.passing = collegecap
                if player.rushing > collegecap:
                    player.rushing = collegecap
                if player.catching > collegecap:
                    player.catching = collegecap
                if player.blocking > collegecap:
                    player.blocking = collegecap
                if player.rundefense > collegecap:
                    player.rundefense = collegecap
                if player.passdefense > collegecap:
                    player.passdefense = collegecap
                if player.kicking > collegecap:
                    player.kicking = collegecap             

            if player.age >= 23:
                if player.speed > procap:
                    player.speed = procap
                if player.strength > procap:
                    player.strength = procap
                if player.stamina > procap:
                    player.stamina = procap
                if player.constitution > procap:
                    player.constitution = procap
                if player.agility > procap:
                    player.agility = procap
                if player.intelligence > procap:
                    player.intelligence = procap
                if player.discipline > procap:
                    player.discipline = procap                       
                if player.passing > procap:
                    player.passing = procap
                if player.rushing > procap:
                    player.rushing = procap
                if player.catching > procap:
                    player.catching = procap
                if player.blocking > procap:
                    player.blocking = procap
                if player.rundefense > procap:
                    player.rundefense = procap
                if player.passdefense > procap:
                    player.passdefense = procap
                if player.kicking > procap:
                    player.kicking = procap               
            
        else:
            player.speed = player.speed - decl
            player.strength = player.strength - decl
            player.stamina = player.stamina - decl
            player.constitution = player.constitution - decl
            player.agility = player.agility - decl
            player.intelligence = player.intelligence - decl
            player.discipline = player.discipline - decl            
            player.passing = player.passing - decl
            player.rushing = player.rushing - decl
            player.catching = player.catching - decl
            player.blocking = player.blocking - decl
            player.rundefense = player.rundefense - decl
            player.passdefense = player.passdefense - decl
            player.kicking = player.kicking - decl

            if player.speed < 1:
                player.speed = 1
            if player.strength < 1:
                player.strength = 1
            if player.stamina < 1:
                player.stamina = 1
            if player.constitution < 1:
                player.constitution = 1
            if player.agility < 1:
                player.agility = 1
            if player.intelligence < 1:
                player.intelligence = 1
            if player.discipline < 1:
                player.discipline = 1                       
            if player.passing < 1:
                player.passing = 1
            if player.rushing < 1:
                player.rushing = 1
            if player.catching < 1:
                player.catching = 1
            if player.blocking < 1:
                player.blocking = 1
            if player.rundefense < 1:
                player.rundefense = 1
            if player.passdefense < 1:
                player.passdefense = 1
            if player.kicking < 1:
                player.kicking = 1             

    # player.rating = (player.speed + player.strength + player.stamina + player.constitution + player.agility + player.intelligence) / 6        

# testPlayer = Player()


def playerCounts():
    "Rating Metrics"
    low = 0
    med = 0
    high = 0
    allPro = 0
    total = 0
    totalProAge = 0
    totalPro = 0

    lowCollege = 0
    medCollege = 0
    highCollege = 0
    allStar = 0
    totalCollegeAge = 0
    totalCollege = 0    

    for q in players:
        if q.age<= q.retirementAge:
            if q.position == 'QB':
                q.rating = q.passing

            elif q.position == 'RB':
                q.rating = q.rushing

            elif q.position == 'WR':
                q.rating = q.catching

            elif q.position == 'TE':
                q.rating = q.catching    

            elif q.position == 'OG':
                q.rating = q.blocking    

            elif q.position == 'OT':
                q.rating = q.blocking    

            elif q.position == 'C':
                q.rating = q.blocking    

            elif q.position == 'DT':
                q.rating = q.rundefense    

            elif q.position == 'DE':
                q.rating = q.rundefense    

            elif q.position == 'LB':
                if q.passdefense > q.rundefense:
                    q.rating = q.passdefense
                elif q.rundefense > q.passdefense:
                    q.rating = q.rundefense

            elif q.position == 'CB':
                q.rating = q.passdefense    

            elif q.position == 'S':
                q.rating = q.passdefense    

            elif q.position == 'K':
                q.rating = q.kicking    

            elif q.position == 'P':
                q.rating = q.kicking
            
            total = total + 1
            if q.age >= 19 and q.age <= 22:
                totalCollegeAge = totalCollegeAge + 1
                if q.rating >= 45 and q.rating < 55:
                    lowCollege = lowCollege +1
                    totalCollege = totalCollege + 1
                elif q.rating >= 55 and q.rating < 65:
                    medCollege = medCollege + 1
                    totalCollege = totalCollege + 1
                elif q.rating >= 65 and q.rating < 75:
                    highCollege = highCollege + 1
                    totalCollege = totalCollege + 1
                elif q.rating == 75:
                    print 'College!' , q.firstName, q.lastName, '-', q.position
                    allStar = allStar + 1
                    totalCollege = totalCollege + 1
            if q.age >= 23 and q.age <= q.retirementAge:
                totalProAge = totalProAge + 1
                if q.rating >= 60 and q.rating < 70:
                    low = low +1
                    totalPro = totalPro + 1
                elif q.rating >= 70 and q.rating < 80:
                    med = med + 1
                    totalPro = totalPro + 1
                elif q.rating >= 80 and q.rating < 90:
                    high = high + 1
                    totalPro = totalPro + 1
                elif q.rating == 90:
                    print q.firstName, q.lastName, '-', q.position
                    allPro = allPro + 1
                    totalPro = totalPro + 1
                
    print 'Total: ', total
    print 'Coll Age: ', totalCollegeAge
    print 'College: ', totalCollege
    print 'Coll Low: ', lowCollege
    print 'Coll Med: ', medCollege
    print 'Coll High: ', highCollege
    print 'Coll All Star: ', allStar
    
    print 'Pro Age: ', totalProAge
    print 'Pro: ', totalPro
    print 'Low: ', low
    print 'Med: ', med
    print 'High: ', high
    print 'All Pro: ', allPro
    
                

players = []

conn = sqlite3.connect('../python_football_2012.sql')

c = conn.cursor()

## Delete table
c.execute('''drop table players''')
conn.commit()

## Create table
c.execute('''create table players
(id , age , firstName , lastName ,  position , speed , strength , stamina , constitution ,
    agility , intelligence , discipline , retirementAge , retired , apexAge , growthRate ,
    declinationRate , rating , passing , rushing , catching , blocking , rundefense , passdefense , kicking)''')
conn.commit()

for x in range(2500):
    holdPlayer = Player()
    print holdPlayer.id
    c.execute('insert into players values (holdPlayer.id, holdPlayer.age, holdPlayer.firstName , holdPlayer.lastName ,  holdPlayer.position , holdPlayer.speed , holdPlayer.strength , holdPlayer.stamina , holdPlayer.constitution , holdPlayer.agility , holdPlayer.intelligence , holdPlayer.discipline , holdPlayer.retirementAge , holdPlayer.retired , holdPlayer.apexAge , holdPlayer.growthRate , holdPlayer.declinationRate , holdPlayer.rating , holdPlayer.passing , holdPlayer.rushing , holdPlayer.catching , holdPlayer.blocking , holdPlayer.rundefense , holdPlayer.passdefense , holdPlayer.kicking)')
    nextID = nextID + 1

#for years in range(40):
#    print year
#    year = year + 1
#
#    for y in players:
#
#        advanceYear(y)
#    
#    for x in range(2500):
#        holdPlayer = Player()
#        players.append(holdPlayer)
#        nextID = nextID + 1
#
#    playerCounts()
#
#    print ' '
#
#
#pro = []
#
#for player in players:
#    if player.age >= 23 and player.age <= player.retirementAge and player.rating >= 60 :
#        pro.append(player)
#
#import operator
#
#pro.sort(key=operator.attrgetter('position'))
#
#for x in pro:
#    print x.firstName, x.lastName, ',', x.position, ',', x.rating
    
##for y in players:
##    print ' '
##    print 'ID: ', y.id
##    print 'Age: ', y.age
##    print 'Apex: ', y.apexAge
##    print 'Retire: ', y.retirementAge
##    print 'Growth: ', y.growthRate
##    print 'Decline: ', y.declinationRate
##    print 'Speed: ', y.speed
##    print 'Str: ', y.strength
##    print 'Stamina: ', y.stamina
##    print 'Const: ', y.constitution
##    print 'Agility: ', y.agility
##    print 'Intell: ', y.intelligence
##
##    advanceYear(y)
##
##    print 'ID: ', y.id
##    print 'Age: ', y.age
##    print 'Apex: ', y.apexAge
##    print 'Retire: ', y.retirementAge
##    print 'Growth: ', y.growthRate
##    print 'Decline: ', y.declinationRate
##    print 'Speed: ', y.speed
##    print 'Str: ', y.strength
##    print 'Stamina: ', y.stamina
##    print 'Const: ', y.constitution
##    print 'Agility: ', y.agility
##    print 'Intell: ', y.intelligence
    

# player1.rushing = random.randint(28,46)
# print player1.rushing


 
