#!/usr/bin/env python3
# encoding: utf-8
'''
TODO [ZK Proximity Search ](thearchive://match/ZK Proximity Search 202203192030)
To use the or compare arg1 or arg
'''
# * 

# import time
# startTime = time.time()

import re
import os
from zkfunctions import TheArchivePath

directory = TheArchivePath()

def zsearch(s, *args):
    for x in args: 
        p = re.search(x, s, re.IGNORECASE)
        if p is None:
            return None
    return s

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        with open(os.path.join(directory, filename),"r") as fp:
            for line in fp:
                result_line = zsearch(line, os.environ["KMVAR_firstTerm"], os.environ["KMVAR_secondTerm"], os.environ["KMVAR_thirdTerm"])
                if result_line != None:
                    UUID = filename[-15:-3]
                    print(f'›[[{UUID}]] OR ', end="")

# executionTime = (time.time() - startTime)
# print('\n Execution time in seconds: ' + str(executionTime))
         

# Terminal code. egrep -i "\b(?:\S*?"boston"\S*?\W+(?:\w+\W+){0,"10"}?\S*?"love"\S*?|\S*?"love"\S*?\W+(?:\w+\W+){0,"10"}?\S*?"boston"\S*?)\b" *.md