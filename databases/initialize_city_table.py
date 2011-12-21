'''
Created on Dec 6, 2011

@author: George Peek

WARNING: DROPS and reloads existing City table
'''

import sqlite3
import csv

conn = sqlite3.connect('teams.sql')

c = conn.cursor()

## Delete table
c.execute('''drop table cities''')
conn.commit()
c.close()

## Create table
## primary key = city/state
c.execute('''create table cities
(city TEXT, state TEXT, proLevel INT, firstTierSemiPro INT, secondTierSemiPro INT, region INT, division INT, PRIMARY KEY (city,state))''')

cityReader = csv.reader(open('..\csv_source_files\metroareas.csv'), delimiter=',', quotechar='|')
for row in cityReader:
    print row
    c.execute('insert into cities values (?,?,?,?,?,?,?)', row)

conn.commit()
c.close()