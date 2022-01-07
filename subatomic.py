#!/usr/bin/python3
# encoding: utf-8
import os

def check(token):
    with open(os.environ["KMVAR_fName"]) as f:
        datafile = f.readlines()
    for line in datafile:
        if token in line:
            # print(line.partition("Subatomic: ")[2])   
            return line.partition("Subatomic: ")[2]
    return False  # Because you finished the search without finding
     
    # Use    
output = (f'\t\t- {check("Subatomic: ")}')  
print(output)

