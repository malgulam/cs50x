#sequences db creator
import os, sys, copy, sqlite3
sys.path.append(".")


#progress bar

def progressBar(current, total, barLength=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

def pattern_retrieval(file_path):
    patterns = {}
    lines = list()
    with open(file_path, 'r') as f:
        lines = f.readlines()
    f.close()
    continuous_line_of_text = str()
    for line in lines:
        continuous_line_of_text += line
    #reading 4 letters at a time
    tmp = copy.copy(continuous_line_of_text)
    # appending the patterns
    while len(tmp)  != 0:
        ptt = str(tmp[0:4])
        if ptt in patterns.keys():
            patterns[ptt] += 1
        else:
            patterns[ptt] = 1
        tmp = tmp[4:] 
    return patterns

#function to return tupelised lists
def tupelise(lst):
    tmpLst = lst[:]
    #tmp2 = list()
    for i in range(len(tmpLst)):
        tmpLst[i] = (tmpLst[i],)
    return tmpLst
        

def db_include(path, filename):
    full_file_path = path + filename
    patterns = pattern_retrieval(full_file_path)
    db_file = 'sequencesdb.db'
    conn = sqlite3.connect(db_file)
    try:
        c = conn.cursor()
        columns = list()
        columns_data = list()
        #create table
        for key, value in patterns.items():
            columns.append(key)
            columns_data.append(value)
        #creating tables and columns
        # s = "CREATE TABLE sequences (File," + ', '.join(f"{col} INTEGER" for col in columns) + ")"
        s = "CREATE TABLE IF NOT EXISTS sequences(File TEXT);"
        c.execute(s)
        # conn.commit()
        #checking current columns
        cursor = conn.execute('select * from sequences')
        columns_present = list(map(lambda x: x[0], cursor.description))
        print(columns_present)
        new_columns = list()
        
        #checking whether new columns are already present
        for i in range(len(columns)):
            if columns[i] not in columns_present:
                new_columns.append(columns[i])
                
            else:
                pass
        if new_columns != None:
            # tupelise new_columns items  
            tmpLST = new_columns[:]
            new_columns.clear()
            new_columns = tupelise(tmpLST)

        else:
            pass
        for nc in new_columns:
            c.execute('''ALTER TABLE sequences ADD COLUMN %s INTEGER''' %nc)
        # c.executemany(f'''ALTER TABLE sequences ADD COLUMN ? INTEGER''', new_columns)
        conn.commit()
        conn.close()
        


        
        
        
    except sqlite3.OperationalError as e :
        #FIX!
        #this is due to the  existence of columns and re-creation of them..ignore!
        print('an error ocurred')
        

#retrieve every filename in sequences directory
path = 'sequences/'
filesList = os.listdir(path)

for file in filesList:
    db_include(path, file)
