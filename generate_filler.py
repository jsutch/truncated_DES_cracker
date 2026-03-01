# Extension Guess workaround
# some very old password databases using DES crypt(3) hashes will truncate the stored string from 13 chars down to 10 chars, including a 2 byte salt at the beginning
# e.g.
# properly formatted with be:
# crypt.crypt("MyDumbPassword","My")'
# MyKy9iPtz5SPM ==  13bytes. 11 bytes + 2 byte salt
# so, what would be stored in this logic is a truncated 10 byte string -  MyKy9iPtz5, 8 bytes + 2 byte salt (My)
# 
# in this case we're just going to build the output files per-hash for one user. TODO: add logic for larger files.
#userdb = {'alana': 'XLhxUSodwL.V', 'billyb': 'JoGotXZk/v', 'carlc': 'HezNf0NIYm9J', 'darad': 'DhdGPUVK/3'}
from itertools import permutations

# use carlc's hash
name='carlc'
hashcat_file=name + '_hashcat'
john_file=name + '_john_combined'
userhash = 'HezNf0NIYm9J'
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./'
perm = [''.join(i) for i in permutations(chars, 3)]
userarr = [userhash + x for x in perm]

# make an output that hashcat with mode 1500 can attack
f = open(hashcat_file, 'a', encoding="utf-8")
for x in userarr:
    f.write(f"{x}\n")
f.close()


# make an output that john the ripper with mode crypt in "unshadowed" mode can attack
# we could add carl's name to this to take advantage of name munging, but we won't in this example
# also - since we're only attacking one user, differing uid/gid is probably unimportant
f = open(john_file, 'a', encoding="utf-8")
for x in userarr:
    y = f"bob:{x}:500:500:Bob Smith:/home/bob:/bin/bash"
    f.write(f"{y}\n")
f.close()


