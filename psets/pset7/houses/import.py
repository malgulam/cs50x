# TODO
#usage = python import.py characters.csv
import sqlite3
import sys
from sys import argv
import csv
import collections

if len(argv) != 2:
    print('Usage: python import.py characters.csv')
    sys.exit(1)

#characters.csv
students = argv[1]
#students.db
db_file = 'students.db'
conn = sqlite3.connect(db_file)
c = conn.cursor()

#working on students in csv file
students_names_dict = {}
students_id_house_birth = {}
with open(students, newline='') as studentsCSV:
    #counter for ids
    id_counter = 0
    reader = csv.DictReader(studentsCSV)
    for row in reader:
        id_counter += 1
        names = list()
        for name in row['name'].split(" "):
            names.append(name)
        #if the names list length == 2 it is firstname, last name else if it is 3 then it is first,middle, last
        if len(names) == 2:
            firstname = names[0]
            middlename = None
            lastname = names[1]
            totalData = [id_counter, firstname, middlename, lastname, row['house'], row['birth']]
            c.execute('''INSERT INTO students(id, first,middle,last,house,birth) VALUES(?, ?, ?, ?, ?, ?)''', totalData[:])
        if(len(names)) == 3:
            firstname = names[0]
            middlename = names[1]
            lastname = names[2]
            totalData = [id_counter, firstname, middlename, lastname, row['house'], row['birth']]
            c.execute('''INSERT INTO students(id, first,middle,last,house,birth) VALUES(?, ?, ?, ?, ?, ?)''', totalData[:])
conn.commit()
conn.close()


