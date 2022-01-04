#!/usr/bin/env python3
# encoding: utf-8

import re

# #True or false search conaines all the words


def zsearch(s, *args):
    for x in args:
        r = "(?=.*" + x + ")"
        p = re.search(r, s, re.IGNORECASE)
        if p is None:
            return None
    return [s]

#   with open(filename, "r") as fp:
#         for line in lines_that_contain("Subatomic: ", fp):
#                 atom = line.split(":")[1]   
    
    
    
x = zsearch("This is a more complicated sentence.", "this", "complicated", "more")
print(x)


# p = re.compile('[a-z]+') 
# p.match("")
# print(p.match(""))
# m = p.match("extract")
# print(m)
