#!/usr/bin/python3
# encoding: utf-8

import os
from zkfunctions import TheArchivePath

def check(token, prefix):
    """
    Searches for lines in markdown files that contain all the search terms and start with the given prefix.

    Args:
        token (str): The search terms to look for, separated by spaces.
        prefix (str): The prefix that the matching lines should start with.

    Returns:
        list: A list of tuples containing the matching lines and the filename they were found in.
    """    
    directory = TheArchivePath()
    results = []
    search_terms = token.split()
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r') as file:
                for line_number, line in enumerate(file):
                    if all(term in line for term in search_terms) and line.startswith(prefix):
                        results.append((line, filename))
    return results
   
if __name__ == "__main__":
   lines = check('Lake skilled their', 'Subatomic: ')
if lines:
        for line in lines:
            result = ' '.join(line[0].split()[1:])
            print(f'{result} ({line[1]})\n')