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

with open("Extract Knowledge From Reading 202201042008.md", "r") as fp:
    for line in fp:
        atom = zsearch(line, "zettel","some")
        if atom != None:
            print(atom) 
  

