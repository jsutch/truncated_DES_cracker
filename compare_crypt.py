# neanderthal brute force hash comparison v.0.0.8
#
# some very old password databases using DES crypt(3) hashes will truncate the stored string from 13 chars down to 10 chars, including a 2 byte salt at the beginning
# e.g.
# properly formatted with be:
# crypt.crypt("MyDumbPassword","My")'
# MyKy9iPtz5SPM ==  13bytes. 11 bytes + 2 byte salt
# so, what would be stored in this logic is a truncated 10 byte string -  MyKy9iPtz5, 8 bytes + 2 byte salt (My)
# 
# TODO
# - automate importing userdb/add command line switch
# - add userdb import from a JSON file or a CSV file
# - fix bytes problem

# imports
import legacycrypt
import os
import attotime
from datetime import datetime

# date
now = datetime.now()
datestamp = f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}"

# datastores
#userdb = {'alana': 'XLhxUSodwL.V', 'billyb': 'JoGotXZk/v', 'carlc': 'HezNf0NIYm9J', 'darad': 'DhdGPUVK/3'}
# import from file formatted as a dict. 
userfile = "inputfile1"
userdb =  open(userfile,'r').read().splitlines()
outcomes = {}
# get the chunked password input files
# static
#passfiles = ['john8.av', 'john8.aw', 'john8.ax', 'john8.ay', 'john8.az', 'john8.ba', 'john8.bb', 'john8.bc', 'john8.bd', 'john8.be', 'john8.bf', 'john8.bj', 'john8.bs']
# Password Input File Imports
# use unix split to slice the huge file into smaller, 200mb chunks with a consistent name
# in this case we're using a 9.1GB file from john_the_ripper
# split --verbose -b200M john8  john8.
# Also - rockyou as a basic starter
#FILES='john8.'
#FILES='rockyou.txt'
passfiles = []
# os.listdir('./')
PATH='./'
for (root, dirs, file) in os.walk(PATH):
    for f in file:
        if FILES in f:
            passfiles.append(f)

# housekeeping
completedchunks = []
total = len(passfiles)
remaining =  total - len(completedchunks)
totallines = 0
correct_guesses = 0
# backup for found passwords
passwd = []
founduser = []

# open a logfile
currenttime=datetime.now().strftime("%Y-%m-%d-%H-%M%S")
LOGFILE=f'password_output-{currenttime}.txt'
logfile  = open(LOGFILE, 'a', encoding="utf-8")

#start = attotime.attodatetime.now()
#end = attotime.attodatetime.now()
#duration = end - start
#print('starting at:', datetime.now())

# main
print("Starting loop with passfiles",datetime.now())
start = attotime.attodatetime.now()
for chunkfile in passfiles:
    remaining =  total - len(completedchunks)
    percentage = 100 - (round(remaining / total, 2) * 100)
    print(f"starting file {chunkfile}, Left to go: {remaining}/{total} {percentage} complete")
    chunk = open(chunkfile,'r').read().splitlines()
    lines = len(chunk)
    totallines = totallines + lines
    print(f"{chunk[:3]}, {lines:,} inputs in chunk, {totallines:,} total thus far")

    # clean up already found users before starting run
    if len(founduser) > 0:
        for user in founduser:
            userdb.pop(user)
            founduser.remove(user) 

    for k, v in userdb.items():
        SALT = v[:2]
        print(k, v, SALT)
        outcomes[k] = {}
        for guess in chunk:
            if legacycrypt.crypt(guess, SALT)[:10] == v:
                print('MATCH', k, v, guess)
                correct_guesses += 1
                outcomes[k][v] = guess
                founduser.append(k)
                passwd.append(guess)
                break
    end = attotime.attodatetime.now()
    duration = end - start
    print(f"Completed chunk {chunkfile} {datetime.now()}  total time per chunk: {duration}. Correct guesses {correct_guesses}" )
    print(" ---------------- ")
    for name, foundpass in outcomes.items():
        logfile.write(f"{name},{foundpass},{datetime.now()}\n")
    # clean up
    completedchunks.append(chunkfile)
    del chunk
print(f"Completed run, {datetime.now()}. {remaining}/{total} completed. {totallines:,} total tries.")
print("Outcomes:")
print(outcomes.items())

# write out logfile
# make this iterative so I can watch the file during long runs
logfile.close()
#with open(f"{datestamp}_crypt.log", 'w') as file:
#    file.write(str(outfile))
#file.close()

