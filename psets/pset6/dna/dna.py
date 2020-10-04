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

#assigning the argv contents to file
sequenceFile = argv[2]
dnaFile = argv[1]

#working on sequence file
lines = str()
with open(sequenceFile, 'r') as sf:
     for line in sf.readlines():
         lines += line

#working on database
database_count_List = list()
#finding out the dnas to count
with open(dnaFile, newline='') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        for key, value in row.items():
            database_count_List.append(key)
        break
    # get rid of the name in the list
    database_count_List.pop(0)

#dict to store the dna samples and their counts in
sequences = {}
#setting database_count_list to a dict of sequences
for item in database_count_List:
    sequences[item] = 1
#count every repeti
#counting the occurences of the dnas in the sequences file
# dna_count_dict = {}
# for i in range(len(database_count_List)):
#     dna_substring = database_count_List[i]
#     #finding how many times this substring has appeared in the
#     #sequences text
#     dna_count_in_sequences = lines.count(dna_substring)
#     #adding the dna to the dna_count_dict as a default with its respective count
#     dna_count_dict.setdefault(database_count_List[i], dna_count_in_sequences)

#checking who the dna belongs to
for key in
# currentUser_dna_count_list = list()
# checks_passed = 0
# with open(dnaFile, newline='') as csvFile:
#     reader = csv.DictReader(csvFile)
#     for row in reader:
#         row_items = row.items()
#         for key, value in row.items():
#             currentUser_dna_count_list.append(value)
#         # get rid of the name in the list
#         currentUser_dna_count_list.pop(0)
#
#         for i in range(len(currentUser_dna_count_list)):
#             #it'll look like row[AGATC]
#             # print(currentUser_dna_count_list[i])
#             if row[database_count_List[i]] == currentUser_dna_count_list[i]:
#                 checks_passed += 1
#             else:
#                 checks_passed = 0
#                 break
#     #how about use items() list concentrated?
#         currentUser_dna_count_list.clear()
#         # if row_items[] ==
#         current_row_as_list = (list(row_items)[1:])[:]
#         dna_list_items = dna_count_dict.items()
#         current_dna_lists_items_as_list = (list(dna_list_items)[:])[:]
#         if compare(current_row_as_list , current_dna_lists_items_as_list) == True:
#             name = ''
#             for key in row.keys():
#                 print('key:', key)
#                 if key == 'name':
#                     name += row[key]
#                     break
#             print(name)
#             break
#
#         else:
#             # print('NO!')
#             current_row_as_list.clear()
#             current_dna_lists_items_as_list.clear()
#             continue