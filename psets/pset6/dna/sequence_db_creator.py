# sequence db creator
import os
import sys
import sqlite3
import csv


# progress bar
def progress_bar(current, total, bar_length=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')


# function to return tupelised lists
def tupelise(lst):
    tmpLst = lst[:]
    # tmp2 = list()
    for i in range(len(tmpLst)):
        tmpLst[i] = (tmpLst[i],)
    return tmpLst


#function to turn list into str separated by commas
def convert_to_str(lst):
    new_str = str()
    for i in  range(len(lst)):
        new_str += str(lst[i]) + ','
    new_str = new_str[:len(new_str)-1]
    return new_str

def main():
    sequences_files = list()
    #concatenating the name of the path (sequences) to each file
    for file in os.listdir('sequences/'):
        sequences_files.append(f'sequences/{file}')
    #todo: work on databases/large
    large_database = "databases/large.csv"
    large_database_dnas = list()
    large_database_sequences = {}
    with open(large_database, newline='') as largeCSVFile:
        reader = csv.DictReader(largeCSVFile)
        #fetching only first row and append to list
        for row in reader:
            for k,v in row.items():
                large_database_dnas.append(k)
            break
        large_database_dnas.pop(0)
    # print(large_database_dnas)

    #todo:get the count for every one in the dnas in every sequence.txt
    for file in sequences_files:
        lines = str()
        with open(file, 'r') as f:
            for line in f.readlines():
                lines += line
            #search for occurences of each substing
            for item in large_database_dnas:
                large_database_sequences[item] = 1
            for key, value in large_database_sequences.items():
                keylen = len(key)
                tmpNum = 0
                tmpNum2 = 0
                tmp_dnaSequence = lines[:]
                for i in range(len(tmp_dnaSequence)):
                    # finding occurences by slicing and matching
                    while tmpNum > 0:
                        tmpNum -= 1
                        continue
                    if tmp_dnaSequence[i:i + keylen] == key:
                        while tmp_dnaSequence[i:i + keylen] == tmp_dnaSequence[i - keylen:i]:
                            tmpNum += 1
                            i += keylen
                        if tmpNum > tmpNum2:
                            tmpNum2 = tmpNum
                # assign it to its respective key in sequences
                large_database_sequences[key] += tmpNum2
            # print(file, large_database_sequences)
            #working on db file
            db_file = 'sequencesdb.db'
            conn = sqlite3.connect(db_file)
            try:
                c = conn.cursor()
                columns = list()
                columns_data = list()
                for k,v in large_database_sequences.items():
                    columns.append(k)
                    columns_data.append(v)
                #adding file name to columns_data list at index 0
                columns_data.insert(0, file)
                #create tables and columns
                # s = "CREATE TABLE IF NOT EXISTS sequences_large (File TEXT," + ', '.join(f"{col}INTEGER" for col in columns) + ")"
                # s = "CREATE TABLE IF NOT EXISTS sequences_large (File Text," + ', '.join(["? INTEGER"] * len(columns)) + ")"
                s = "CREATE TABLE IF NOT EXISTS sequences_large(File TEXT,AGATC,TTTTTTCT ,AATG,TCTAG ,GATA ,TATC ,GAAA,TCTG)"
                c.execute(s)
                conn.commit()

                # t = "INSERT INTO sequences_large VALUES (" + ', '.join(["?"] * len(columns_data)) + ")"
                # c.executemany(t, columns_data)
                columns_as_str =  convert_to_str(columns)
                columns_data_as_str = str(file) + ',' + convert_to_str(columns_data)
                values = tupelise(columns_data)
                print('values', values)
                print('columns data', columns_data)
                print('columns', columns_as_str)
                # t = f"INSERT INTO sequences_large({columns_as_str}) VALUES ("+ ', '.join(["?"] * len(columns)) +")"
                # c.execute(t, values,)
                c.execute(t)
                conn.commit()
                conn.close()
            except sqlite3.OperationalError as e:
                # print('an error occurred!')
                print('sqlite3 operational error',e)
                #todo: work on storing these values!
    #todo: work on the database/small
    small_database = "databases/small.csv"
    small_database_dnas = list()
    small_database_sequences = {}
    with open(small_database, newline='') as smallCSVFile:
        reader = csv.DictReader(smallCSVFile)
        # fetching only first row and append to list
        for row in reader:
            for k, v in row.items():
                small_database_dnas.append(k)
            break
        small_database_dnas.pop(0)
    # print(large_database_dnas)

    # todo:get the count for every one in the dnas in every sequence.txt
    for file in sequences_files:
        lines = str()
        with open(file, 'r') as f:
            for line in f.readlines():
                lines += line
            # search for occurences of each substing
            for item in small_database_dnas:
                small_database_sequences[item] = 1
            for key, value in small_database_sequences.items():
                keylen = len(key)
                tmpNum = 0
                tmpNum2 = 0
                tmp_dnaSequence = lines[:]
                for i in range(len(tmp_dnaSequence)):
                    # finding occurences by slicing and matching
                    while tmpNum > 0:
                        tmpNum -= 1
                        continue
                    if tmp_dnaSequence[i:i + keylen] == key:
                        while tmp_dnaSequence[i:i + keylen] == tmp_dnaSequence[i - keylen:i]:
                            tmpNum += 1
                            i += keylen
                        if tmpNum > tmpNum2:
                            tmpNum2 = tmpNum
                # assign it to its respective key in sequences
                small_database_sequences[key] += tmpNum2
            # print(file, small_database_sequences)
    #retrueve every filename in sequences
main()