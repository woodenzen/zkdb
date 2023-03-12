#!/usr/bin/env python3
# encoding: utf-8

import pathlib
import os, re, random
from collections import defaultdict
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from writing_rand import zkrand


# import pyperclip

# path to zettelkasten

target_dir = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Regex

date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize a lot of counters

tbooks = 0
tblogs = 0
tpodcast = 0
tarticles = 0
tyoutube = 0
tproof = 0
ttwodo = 0
tvideo = 0
twords = 0
tlinks = 0
tzettel = 0
day0 = date(2018, 11, 14)
atom = ""
counter = 0

# Death Watch

birth = date(1956, 9, 26)
today = date.today()
eighty = date(2036, 9, 26)
covid = date(2020, 3, 14)
since = today - birth
until = eighty - today
quarintine = today - covid
percentSince = round(since.days / 29220 * 100, 1)
percentLeft = round(until.days / 29220 * 100, 1)
percentOfTotal = round(quarintine.days / 29220 * 100, 2)

# Get counts for various date parameters.

yesterday_count = 0
yesterday = date.today() - timedelta(1)
tencount = 0
tencountfiles = []
hundredcount = 0
one_week_ago_count = 0
one_week_ago = datetime.now() - relativedelta(weeks=1)
three_weeks_ago_count = 0
three_weeks_ago = datetime.now() - relativedelta(weeks=3)
six_months_ago_count = 0
six_months_ago = datetime.now() - relativedelta(months=6)
one_yr_ago_count = 0
one_yr_ago = datetime.now() - relativedelta(years=1)
two_yrs_ago_count = 0
two_yrs_ago = datetime.now() - relativedelta(years=2)
three_yrs_ago_count = 0
three_yrs_ago = datetime.now() - relativedelta(years=3)
four_yrs_ago_count = 0
four_yrs_ago = datetime.now() - relativedelta(years=4)
tengap = 7
hundredgap = 100

# Functions
def lines_that_equal(line_to_match, fp):
    return [line for line in fp if line == line_to_match]


def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


def lines_that_start_with(string, fp):
    return [line for line in fp if line.startswith(string)]


def lines_that_end_with(string, fp):
    return [line for line in fp if line.endswith(string)]

# Random Super Slogan

ss = random.choice(
    open("/Users/will/Dropbox/zettelkasten/Super Slogans 202012281549.md").readlines()
)
ss = ss.replace("\xa0", " ")


# Iteration for counting tags, links (tlinks), wc (twords), total zettel (tzettel)

for filename in os.listdir(target_dir):
    if filename.endswith(".md"):
        file = open((os.path.join(target_dir, filename)), "r")
        data = file.read()
        books = data.count("#book")
        tbooks += books
        blog = data.count("#blog-post")
        tblogs += blog
        podcast = data.count("#podcast")
        tpodcast += podcast
        article = data.count("#article")
        tarticles += article
        
        youtube = data.count("#youtube")
        tyoutube += youtube
        
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

for uuid in sorted(files, reverse=True):

    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit(".", 1)[0]

        # Yesterday

        if uuid == yesterday.strftime("%Y%m%d"):
            yesterday_count += 1

        # 10 day gap

        # for i in range(tengap):
        #     targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
        #     if targetdate == uuid:
        #         tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
        #             '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ")")
        #         tencount += 1

        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    atom = ""
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = "-" + line.split(":")[1]
                #   Archive format
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
                #   Original format
                #   tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                #         '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ") \n\t\t\t\t -" + atom)
                tencount += 1

        # 100 day gap

        for i in range(hundredgap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                hundredcount += 1

        # 1 week gap

        if uuid == one_week_ago.strftime("%Y%m%d"):
            one_week_ago_count += 1

        # 3 week gap

        if uuid == three_weeks_ago.strftime("%Y%m%d"):
            three_weeks_ago_count += 1

        # 6 month gap

        if uuid == six_months_ago.strftime("%Y%m%d"):
            six_months_ago_count += 1

        # 1 year gap

        if uuid == one_yr_ago.strftime("%Y%m%d"):
            one_yr_ago_count += 1

        # 2 year gap

        if uuid == two_yrs_ago.strftime("%Y%m%d"):
            two_yrs_ago_count += 1

        # 3 year gap

        if uuid == three_yrs_ago.strftime("%Y%m%d"):
            three_yrs_ago_count += 1
            
        # 4 year gap

        if uuid == four_yrs_ago.strftime("%Y%m%d"):
            four_yrs_ago_count += 1


                
# Print and output

output1 = f""" 
## Memento Mori
Days since birth: {since.days} - {percentSince}%
Days until I'm 80: {until.days} - {percentLeft}%
Days of COVID watch: {quarintine.days} - {percentOfTotal}%
Total days in an eighty-year life. 29220

## Super Slogan
{ss}
{'-'*40}
Zettelkasten Statistics
       ★★★★★
\t{twords} Total word count
\t{tlinks - tzettel} Total link count
\t{tzettel} Total zettel count
       ★★★★★

\t{tproof} [Zettel Proofing](thearchive://match/"#proofing").
\t{tbooks} [Books Processed](thearchive://match/"#book").
\t{tblogs} [Blog Posts](thearchive://match/"#blog-post").
\t{tpodcast} [Podcasts Processed](thearchive://match/"#podcast").
\t{tarticles} [Articles Processed](thearchive://match/"#article").
\t{tyoutube} [YouTube Videos Processed](thearchive://match/"#youtube").
\t{tvideo} [Poetry of Zettelkasting Videos Made](thearchive://match/"#video").

{'-'*40}
[{yesterday_count} notes created on {yesterday.strftime('%Y%m%d')}](thearchive://match/›[[{yesterday.strftime('%Y%m%d')}) yesterday.
[{one_week_ago_count} notes created on {one_week_ago.strftime('%Y%m%d')}](thearchive://match/›[[{one_week_ago.strftime('%Y%m%d')}) one week ago.
[{three_weeks_ago_count} notes created on {three_weeks_ago.strftime('%Y%m%d')}](thearchive://match/›[[{three_weeks_ago.strftime('%Y%m%d')}) three weeks ago.
[{six_months_ago_count} notes created on {six_months_ago.strftime('%Y%m%d')}](thearchive://match/›[[{six_months_ago.strftime('%Y%m%d')}) six months ago.
[{one_yr_ago_count} notes created on {one_yr_ago.strftime('%Y%m%d')}](thearchive://match/›[[{one_yr_ago.strftime('%Y%m%d')}) one year ago.

Four Random Notes Older than One Year Old
"""
# print(f'{output1}')
zkrand()

output = f""" 
{'-'*40}
**{tencount} new zettel in the last {tengap} days.**
{hundredcount} new zettel in the last {hundredgap} days.
{tzettel / (today - day0).days:.2f} zettel created on average since day zero.
{'-'*40}

"""

for newnotes in tencountfiles:
    output += newnotes + "\r"

print(f'{output}') 

# pyperclip.copy(output)


# [{two_yrs_ago_count} notes created on {two_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{two_yrs_ago.strftime('%Y%m%d')}) two years ago.
# [{three_yrs_ago_count} notes created on {three_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{three_yrs_ago.strftime('%Y%m%d')}) tzhree years ago.
# [{four_yrs_ago_count} notes created on {four_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{four_yrs_ago.strftime('%Y%m%d')}) four years ago.