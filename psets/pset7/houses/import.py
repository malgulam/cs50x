# TODO
#usage = python import.py characters.csv
import sqlite3
import sys
from sys import argv
import csv
import collections

if len(argv) < 2:
    print('Usage: python import.py characters.csv')
    sys.exit(1)

#characters.csv
students = argv[1]
#students.db
db_file = 'students.db'
conn = sqlite3.connect(db_file)

#working on students in csv file
students_names_dict = {}
students_id_house_birth = {}
with open(students, newline='') as studentsCSV:
    reader = csv.reader(studentsCSV)
    for row in reader:
        #check if it is the first row
        if row[0] == 'name':
            continue
        else:
            pass
        #determine whether student has only first name and last name
        #or first name, last name, middle name
        name = row[0]
        #if has first name and last
        if name.count(" ") == 2:
            x = name.split(" ")
            #x[0] is first name,y[1] : middle name, y[2]  is student last name
            first_name = x[0]
            middle_name = x[1]
            last_name = x[2]
            students_names_dict[first_name] = middle_name, last_name
            keys = list(students_names_dict.keys())
            students_id_house_birth[first_name] = keys.index(x[0]),row[1], row[2]
        else:
            #name is just first name and last name
            y = name.split(" ")
            #y[0] is student first name, y[1] is student last name
            first_name = y[0]
            last_name = y[1]
            middle_name = None
            students_names_dict[first_name] = middle_name, last_name
            keys = list(students_names_dict.keys())
            students_id_house_birth[first_name] = keys.index(y[0]),row[1], row[2]
