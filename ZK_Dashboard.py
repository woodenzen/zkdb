# Import the required modules
import os
import random
import datetime
from avg_per_day import calculate_avg_notes_per_day
from occurances_in_zk import count_target_occurrences
from TheArchivePath import TheArchivePath
import daily_results
from zk_stats import zk_stats
from get_word_count import get_word_count
from bookography import bookography
from momento_mori import momento_mori


# Set the path to the directory to search for files
zettelkasten = TheArchivePath()

#####
# Variables
#####
twords = get_word_count()
tlinks = count_target_occurrences(']]')
tzettel = 0
ss = random.choice(open("/Users/will/Dropbox/zettelkasten/Super Slogans 202012281549.md").readlines())
ss = ss.replace("\xa0", " ")

# Set the length and start of the current and comparison date ranges for trending
short = 10
long = 100

# Functions
## Trending Function Call
current = daily_results.trend(short, short)
past = daily_results.trend(long, long)
## Basic stats Function Call
zk_stats()
# Bookography Function Call
highest_number, current_week, goal = bookography(52)
# Momento Mori Function Call
momento_mori()

## Print the dashboard
output = f"""
{'–'*5}
## Read **{goal}** Books in {datetime.date.today().year} 
- **I've read {highest_number} books so far this year.**
- **It is week {current_week} of my one-book-per-week challenge.**

{'–'*5}
## Super Slogan
{ss}
{'–'*5}
## Zettelkasten Statistics
       ★★★★★ 
{twords} Total word count
{tlinks-len(os.listdir(zettelkasten))} Total link count
{len(os.listdir(zettelkasten))} Total zettel count
       ★★★★★
"""
print(f'{output}')


# Print the trending results
print(f'{current[2]}-day trend: {current[0]}/{current[1]} {current[3]}')
print(f'{past[2]}-day trend: {past[0]}/{past[1]} {past[3]}')
print(f"{calculate_avg_notes_per_day(zettelkasten)} notes/day since day zero (20181114).")
# proofing_count = count_proofing_files(zettelkasten)
print(f"We have {count_target_occurrences('#proofing')} notes in the proofing oven.")

## Print the list of files produced in the last 10 days and their subatomic lines.
print(f'\n–––––')
print(f'## {current[0]} new notes have been created in the last ten days. \n')
for entry in current[4]:
    subatomic_line = daily_results.get_subatomic_line(zettelkasten+"/"+entry)
    print(f'- [{entry[:-7]}](thearchive://match/›[[{entry[-15:-3]})\n\t- {subatomic_line[11:]}')