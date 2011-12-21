'''
Created on Dec 6, 2011

@author: George Peek

WARNING: DROPS and reloads existing Nickname table
'''

import sqlite3
import csv

conn = sqlite3.connect('teams.sql')

c = conn.cursor()

## Delete table
c.execute('''drop table nicknames''')
conn.commit()
c.close()

## Create table
## primary key = city/state
c.execute('''create table nicknames
(nickname TEXT PRIMARY KEY, proLevel BOOLEAN, SemiProLevel BOOLEAN, state TEXT)''')

nicknameReader = csv.reader(open('../csv_source_files/nicknames.csv'), delimiter=',', quotechar='|')
for row in nicknameReader:
    print row[0:4]
    c.execute('insert into nicknames values (?,?,?,?)', row[0:4])

conn.commit()
c.close()