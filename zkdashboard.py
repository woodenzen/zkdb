#!/usr/bin/env python3

import pathlib
import re
from collections import defaultdict
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
import random
from dateutil.relativedelta import relativedelta
import pyperclip

# path to zettelkasten

target_dir = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Regex

date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize a lot of counters

tbooks = 0
tblogs = 0
tarticles = 0
tproof = 0
ttwodo = 0
tvideo = 0
twords = 0
tlinks = 0
tzettel = 0
yesterday_count = 0
tencount = 0
tencountfiles = []
hundredcount = 0
one_yr_ago_count = 0
two_yrs_ago_count = 0
tengap = 10
hundredgap = 100
day0 = date(2018, 11, 14)


# Death Watch

birth = date(1956, 9, 26)
today = date.today()
eighty = date(2036, 9, 26)
covid = date(2020, 3, 14)
since = today - birth
until = eighty - today
quarintine = today - covid

# Random Super Slogan

ss = random.choice(
    open("/Users/will/Dropbox/zettelkasten/Super Slogans 202012281549.md").readlines())
ss = ss.replace(u'\xa0', u' ')


# Iteration for counting tags, links (tlinks), wc (twords), total zettel (tzettel)

for filename in os.listdir(target_dir):
    if filename.endswith(".md"):
        file = open((os.path.join(target_dir, filename)), "r")
        data = file.read()
        books = data.count("#book")
        tbooks += books
        blog = data.count("#blog-post")
        tblogs += blog
        article = data.count("#article")
        tarticles += article
        proof = data.count("#proofing")
        tproof += proof
        video = data.count("#video")
        tvideo += video
        twodo = data.count("#2do")
        ttwodo += twodo
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
for child in target_dir.iterdir():
    # Skip directories
    if child.is_dir():
        continue
    match = date_pattern.search(child.name)
    # Skip files that do not match the date pattern
    if match is None:
        continue
    file_date = match.group()
    files[file_date].append(child)

# Get counts for various date parameters.

for uuid in sorted(files, reverse=True):

    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit('.', 1)[0]

# Yesterday

        yesterday = (date.today() - timedelta(1))
        if uuid == yesterday.strftime('%Y%m%d'):
            yesterday_count += 1

# 10 day gap

        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
            if targetdate == uuid:
                tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                    '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ")")
                tencount += 1

# 100 day gap

        for i in range(hundredgap):
            targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
            if targetdate == uuid:
                hundredcount += 1

# 1 year gap

        one_yr_ago = datetime.now() - relativedelta(years=1)
        if uuid == one_yr_ago.strftime('%Y%m%d'):
            one_yr_ago_count += 1

# 2 year gap

        two_yrs_ago = datetime.now() - relativedelta(years=2)
        if uuid == two_yrs_ago.strftime('%Y%m%d'):
            two_yrs_ago_count += 1

# Print and output

output = f""" 
## Memento Mori
Days since birth: {since.days}
Days until I'm 80: {until.days}
Days of COVID watch: {quarintine.days}

## Super Slogan
{ss}
{'-'*40}

\t{twords} Total word count
\t{tlinks - tzettel} Total link count
\t{tzettel} Total zettel count

\t{tproof} Zettel Proofing
\t{ttwodo} 2do's\n
\t{tbooks} Books Processed
\t{tblogs} Blog Posts
\t{tarticles} Articles Processed
\t{tvideo} Poetry of Zettelkasting videos

{'-'*40}
[{yesterday_count} new zettel yesterday.](thearchive://match/›[[{uuid}).
[{one_yr_ago_count} notes created on {one_yr_ago.strftime('%Y%m%d')}](thearchive://match/›[[{one_yr_ago.strftime('%Y%m%d')})
[{two_yrs_ago_count} notes created on {two_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{two_yrs_ago.strftime('%Y%m%d')})
{tencount} new zettel in {tengap} days.
{hundredcount} new zettel in {hundredgap} days.
{tzettel / (today - day0).days:.1f} zettel created on average since day zero.
{'-'*40}

## {tencount} Notes created in the last 10 days

"""

for newnotes in tencountfiles:
    output += newnotes + '\n'

print(output)
# pyperclip.copy(output)
