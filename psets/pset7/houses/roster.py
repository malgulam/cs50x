# TODO
import sys
from sys import argv
import sqlite3

if len(argv) != 2:
    print("Usage: python roster.py Gryffindor")
    sys.exit(1)

#setting house choice
house_choice = argv[1].lower()

#working on database
db_file = 'students.db'
conn = sqlite3.connect(db_file)
c = conn.cursor()

#connect to db and retrieve house names
#todo: get rid of DISTINCT
c.execute('''SELECT DISTINCT house from students''')
houses = c.fetchall()
if house_choice not in houses:
    print(f'{house_choice} not house in houses.Houses are: {houses}')

#retrieve name and birth of persons in that house
c.execute(f'''SELECT first, middle, last, birth FROM students WHERE lower(house)="{house_choice}" ORDER BY last, first''')
roster = c.fetchall()
#since the middle name will be None if not present it's easier to append with each row
names_ = list
for row in roster:
    if row[1] != None:
        print(f'{row[0]} {row[1]} {row[2]} born, {row[3]}')
    else:
        print(f'{row[0]}  {row[2]} born, {row[3]}')

