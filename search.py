#!/usr/bin/env python3
# encoding: utf-8

import re
import os

zettelkasten = '/Users/will/Dropbox/zettelkasten'

def zsearch(s, *args):
    for x in args:
        r = (r"(?=.* " + x + ")")
        p = re.search(r, s, re.IGNORECASE)
        if p is None:
            return None
    return s

for filename in os.listdir(zettelkasten):
    if filename.endswith('.md'):
        with open(os.path.join(zettelkasten, filename),"r") as fp:
            for line in fp:
                atom = zsearch(line, "knowledgeable")
                if atom != None:
                    print(atom)
                    print(filename) 
        

