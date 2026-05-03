# Truncated DES Cracker

## the problem
Some very old password databases using DES crypt(3) hashes will truncate the stored string from 13 chars down to 10 chars, including a 2 character salt at the beginning. 

This breaks the input scrubbing logic for tools like john the ripper or hashcat which are expecting the correct 13character length which will lead to the infamous "No password hashes loaded (see FAQ)" or "Token length exception" errors. When attempting inference hashcat --identify will guess these as type 16000 and flail for awhile without producing results.

An example:
--
A properly formatted DES/crypt(3) would be:
```
crypt.crypt("MyDumbPassword","My")'
MyKy9iPtz5SPM ==  13character string. 11 characters + 2 character salt
```

so, what would be stored in this logic is a truncated 10 character string:
```
MyKy9iPtz5, 8 characters + 2 character salt (My)
```


## One workaround - comparecrypt
 In this case my sloppy workaround is to take publicly available pre-mangled stringfiles, chop them down to 8 chars max, then encode and test. Some relatively small examples from SecLists and the trimmed version of rockyou are all from 10s of MB to the low hundreds, but there are also much larger databases that run into the GB. In python2 (or perl) DES crypt is available, but it was removed from python3. The legacycrypt package lets you get around this.

 For these I split the multi-GB file into smaller 200MB chunks with the split command, such as to not overload local memory.This was faster than rewriting a good mangler but  is a pain because you lose the power of good string mangling rules.

## Results
ProTip: as modern testers we get used to baseline minumum lengths and complexity requirements - this was not a limitation with much older systems.
When generating precompiled lists you will also want to run the permutations of alphanumerics, etc from 1-7 characters and add them to the top of your inputs.

in the test I ran:
--
- more than 60% of the hashes were a single character
- 15% unmodified dictionary words
- 5% well known passwords/keyboard positionals
- 5% number permutations.
- 3% complex passwords hobbled by 8character limtation and mangling tests
- The rest remain - as of now - uncracked.

## the other workaround - permutate the missing 3 characters
In this example since we have 10characters and just need 3, we'll just add the characters to make input files which are valid for hashcat and john to read we can use python's permutations module with a limit of 3 output to create suffixes, then mash them together to make a 13character string that will pass format scrutiny
These are technically not bytes, but they do have to be ASCII printable so valid chars are 0x00 to 0xFF in the hash. Basically a-z,A-Z,0-9 and ./ will work in my case, so we'll take each hash, then create new entries in an input file. 

e.g.
truncated TodGPUVr.5 for hashcat becomes:
```
TodGPUVr.5abc
TodGPUVr.5abd
TodGPUVr.5abe
TodGPUVr.5abf
TodGPUVr.5abg
TodGPUVr.5abh
```
and for john unshadow
```
bob:TodGPUVr.5abc:101:101:Bob Smith:/home/bob:/bin/bash
bob:TodGPUVr.5abd:101:101:Bob Smith:/home/bob:/bin/bash
bob:TodGPUVr.5abe:101:101:Bob Smith:/home/bob:/bin/bash
bob:TodGPUVr.5abf:101:101:Bob Smith:/home/bob:/bin/bash
```

these will be read in properly and - with enough compute time - can be productive.

### thanks
thanks to Alec Muffett's Crypt, john the ripper, and hashcat
[Also to Daniel Miessler's SecLists for fresh input strings and fuzzing inputs](https://github.com/danielmiessler/SecLists)
