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

def zsearch(s, first_term, second_term, third_term=None):
    """
    Searches for multiple terms in a string.

    Args:
        s (str): The string to search.
        first_term (str): The first search term.
        second_term (str): The second search term.
        third_term (str, optional): The third search term. Defaults to None.

    Returns:
        str: The original string if all search terms are found, otherwise None.
    """
    if third_term is not None:
        search_terms = [first_term, second_term, third_term]
    else:
        search_terms = [first_term, second_term]
    for term in search_terms:
        p = re.search(term, s, re.IGNORECASE)
        if p is None:
            return None
    return s

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        with open(os.path.join(directory, filename),"r") as fp:
            for line in fp:
                if os.environ.get("cook"):
                    result_line = zsearch(line, "love", "taste", "cook")
                else:
                    result_line = zsearch(line, "love", "taste")
                if result_line is not None:
                    UUID = filename[-15:-3]
                    print(f'›[[{UUID}]] OR ', end="")
# executionTime = (time.time() - startTime)
# print('\n Execution time in seconds: ' + str(executionTime))
         

# Terminal code. egrep -i "\b(?:\S*?"boston"\S*?\W+(?:\w+\W+){0,"10"}?\S*?"love"\S*?|\S*?"love"\S*?\W+(?:\w+\W+){0,"10"}?\S*?"boston"\S*?)\b" *.md

if __name__ == "__main__":
    pass