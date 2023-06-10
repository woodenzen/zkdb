"""
A program for analyzing notes stored in The Archive.

The program can count the number of links and words in the notes, as well as group the notes by date. The program can also generate a random notes, over a specified size, from The Archive. It includes a random slogan generator, ZK stats, trends, and a list of notes created in the last 10 days.

Variables:
    zettelkasten: A pathlib.Path object representing the path to The Archive.
    date_pattern: A regular expression pattern for matching dates in filenames.
    link_pattern: A regular expression pattern for matching links in note text.
    tzettel: An integer representing the total number of notes in The Archive.
    day0: A date object representing the start date for calculating the average number of notes created per day.
    atom: A string representing the subatomic structure of a note.
    counter: An integer representing a counter for iterating over notes.
    today: A date object representing the current date.
    twords: An integer representing the total number of words in The Archive.
    tlinks: An integer representing the total number of links in The Archive.
    tencountfiles: A list of strings representing the filenames of notes created in the last 10 days.
    tengap: An integer representing the number of days to look back for notes.

"""

import pathlib
import os, re, random
from collections import defaultdict
from datetime import date
from datetime import timedelta
from zkfunctions import trend, large_note_rand, TheArchivePath, lines_that_contain, bookography


#####
# Variables
#####
# path to zettelkasten
zettelkasten = pathlib.Path(TheArchivePath())

# Regex
date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize counters and variables
tzettel = 0
day0 = date(2018, 11, 14)
atom = ""
counter = 0
today = date.today()
twords = 0
tlinks = 0
tzettel = 0
tencountfiles = []
tengap = 10

# Random Super Slogan

ss = random.choice(
    open("/Users/will/Dropbox/zettelkasten/Super Slogans 202012281549.md").readlines()
)
ss = ss.replace("\xa0", " ")

# Iteration for counting tags, links (tlinks), wc (twords), total zettel (tzettel)

for filename in os.listdir(zettelkasten):
    if filename.endswith(".md"):
        file = open((os.path.join(zettelkasten, filename)), "r")
        data = file.read()
        links = data.count("]]")
        tlinks += links
        per_word = data.split()
        twords += len(per_word)
        tzettel += 1

        continue
    else:
        continue


# Files is a dictionary mapping of a date to the list of files with that date
files = defaultdict(list)
for child in zettelkasten.iterdir():
    # Skip directories
    if child.is_dir():
        continue
    match = date_pattern.search(child.name)
    # Skip files that do not match the date pattern
    if match is None:
        continue
    file_date = match.group()
    files[file_date].append(child)

for uuid in sorted(files, reverse=True):
    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit(".", 1)[0]
        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    atom = ""
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = "*" + line.split(":")[1]
                #   Archive formatted links if the placement of the output is destined for The Archive
                        # tencountfiles.append(file_name.rsplit((uuid), 1)[0] + "[[" + full_uuid + "]]\n   -" + atom)
                #   Markdown format
                tencountfiles.append(
                    "- "
                    + file_name.rsplit((uuid), 1)[0]
                    + "["
                    + uuid
                    + "](thearchive://match/"
                    + file_name
                    + ")\n\t\t"
                    + atom
                )

# Random Zettel Function    
large_note_rand(500, 5000, 10)

# Trending Function
direction = '⎯'
if trend(10) > trend(10+1):
    direction = '⬆︎'
elif trend(100) < trend(100+1) :
    direction = '⬇︎'

# Bookography Function
highest_number, current_week, goal = bookography(52)

# Output

output = f""" 
{'-'*40}
## Book Goal Progress 
**I've read {highest_number} books so far this year.** \n**It is week {current_week} of my one-book-per-week challenge.**\n**My goal is to read {goal} books this year.**

{'-'*40}

## Super Slogan
{ss}
{'-'*40}

Zettelkasten Statistics
       ★★★★★
{twords} Total word count
{tlinks - tzettel} Total link count
{tzettel} Total zettel count
       ★★★★★

{trend(10)[1]} day tend: {trend(10)[0]}/{trend(10+1)[0]} {direction}
{trend(100)[1]} day trend: {trend(100)[0]}/{trend(100+1)[0]} {direction}
{tzettel / (today - day0).days:.2f} zettel created on average since day zero.

{'-'*40}

"""

for newnotes in tencountfiles:
    output += newnotes + "\r"

print(f'{output}') 