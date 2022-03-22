#!/usr/bin/env python3
# encoding: utf-8

# TODO [ZK Proximity Search ](thearchive://match/ZK Proximity Search 202203192030)

# import time
# startTime = time.time()

import re
import os

zettelkasten = '/Users/will/Dropbox/zettelkasten'

def zsearch(s, *args):
    for x in args: 
        p = re.search(x, s, re.IGNORECASE)
        if p is None:
            return None
    return s

for filename in os.listdir(zettelkasten):
    if filename.endswith('.md'):
        with open(os.path.join(zettelkasten, filename),"r") as fp:
            for line in fp:
                result_line = zsearch(line, os.environ["KMVAR_firstTerm"], os.environ["KMVAR_secondTerm"], os.environ["KMVAR_thirdTerm"])
                if result_line != None:
                    UUID = filename[-15:-3]
                    print(f'›[[{UUID}]] OR ', end="")

# executionTime = (time.time() - startTime)
# print('\n Execution time in seconds: ' + str(executionTime))
         

