import os, sys, csv
from sys import argv

#function to compare the contents of tupled lists returned by the
#lists declarations on lines 68:71
def compare(lst1, lst2):
    tmplst1 = list()
    tmplst2 = list()
    for i in range(len(lst1)):
        for j in lst1[i]:
            tmplst1.append(str(j))
    for i in range(len(lst2)):
        for j in lst2[i]:
            tmplst2.append(str(j))
    print(tmplst1, tmplst2)
    if tmplst1 == tmplst2:
        return True
    else:
        return False

#checking for len of the sys arguments given
if len(argv) < 3:
    print('Usage: python dna.py data.csv sequence.txt')
    exit()
#assigning the argv contents to file
dnaFile = argv[1]
sequenceFile = argv[2]

#dna sequence as string
dnaSequence = str()
with open(sequenceFile, 'r') as f:
    for line in f.readlines():
        dnaSequence += line
f.close()

#find the dna samples to find count of
sequences = {}
dna_sequences_to_find = list()
with open(dnaFile, newline='') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        for key, value in row.items():
            # put the sequences you're looking for into a list
            dna_sequences_to_find.append(key)
        break
    #get rid of name
    dna_sequences_to_find.pop(0)
#transfering the data in dna_sequences_to_find list to sequences dict
for item in dna_sequences_to_find:
    sequences[item] = 1
#find the number of time each dna in sequences dict appears in the dnaSequence str
for key,value in sequences.items():
    keylen = len(key)
    tmpNum = 0
    tmpNum2 = 0
    tmp_dnaSequence = dnaSequence[:]
    for i in range(len(tmp_dnaSequence)):
        #finding occurences by slicing and matching
        while tmpNum > 0:
            tmpNum -= 1
            continue
        if tmp_dnaSequence[i:i+keylen] == key:
            while tmp_dnaSequence[i:i+keylen] == tmp_dnaSequence[i - keylen:i]:
                tmpNum += 1
                i += keylen
            if tmpNum > tmpNum2:
                tmpNum2 = tmpNum
#assign it to its respective key in sequences
    sequences[key] += tmpNum2
with open(dnaFile, newline='') as csvFile:
    reader = csv.DictReader(csvFile)
    checks_passed = 0
    for row in reader:
        for k, v in sequences.items():
            if sequences[k] == int(row[k]):
                checks_passed += 1
                continue
            else:
                #set checks_passed back to zero
                checks_passed = 0
                break
        if checks_passed == len(sequences):
            print(row['name'])
            sys.exit(0)
    #if none of the people in each row had the passed check
    print('No match')
    sys.exit(1)
