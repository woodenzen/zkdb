#!/usr/bin/env python3
# encoding: utf-8

import time
import pathlib
from dateutil.relativedelta import relativedelta

def luhn_checksum(card_number):
    

    
    
startTime = time.time()

# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Functions

def count_words_per_sentence(filename):
    """
    :input type filename: str
    :return type: list[int]
    """
    with open(filename) as f:
        sentences = f.read().split('.')
    return [len(sentence.split()) for sentence in sentences]
  
zettel = open("Extract Knowledge From Reading 202201042008.md", "rt")
data = zettel.read()
words = data.split()
sentences = data.split(".")
outlinks = data.split("[[")

print("Number of words: ",len(words))
print("Number of sentences: ",len(sentences))
print("Number of out outing links: ",len(outlinks)-2)
print(count_words_per_sentence("Extract Knowledge From Reading 202201042008.md"))


executionTime = (time.time() - startTime)
print('\n Execution time in seconds: ' + str(executionTime))