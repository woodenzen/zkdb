
import os, re, random, pathlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from plistlib import load
from urllib.parse import urlparse


####
# Get folder size
####
def getFolderSize(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):#not sub folders
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)   
    return total_size
    
####
# Human readable single folder size
####

def sizeof_fmt(num, suffix='bytes'):
    for unit in ['',' Kilo',' Mega',' Giga',' Tera',' Peta',' Exa',' Zetta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return

if __name__ == '__main__':
    print(sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten')))
    print('-'*40) 

####
# Function for finding the path to The Archive
#####
def TheArchivePath():
    """
    Find the path to The Archive's plist file.

    Returns:
        A string representing the path to The Archive.
    """
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    #`fileName` is the path to the plist file that contains the path to the ZK.
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        # load is a special function for use with a plist
        pl = load(fp) 
        # 'archiveURL' is the key that pairs with the zk path
        path = urlparse(pl['archiveURL']) 
    # path is the part of the path that is formatted for use as a path.
    return (path.path) 

if __name__ == "__main__":
    zettelkasten = pathlib.Path(TheArchivePath())
    print(f'The Current ZK Directory. {zettelkasten}')
    print(f'## {len(os.listdir(zettelkasten))} notes in the archive.')   
    subfolders = [ f.path for f in os.scandir(zettelkasten) if f.is_dir() ]
    for i in subfolders:
        print(f'## {len(os.listdir(i))} files in {i}.')
        print(f'## {sizeof_fmt(getFolderSize(i))} in {i}.')
        print('-'*40) 


#####
# Function for finding a string in a line of a file
#####
def lines_that_contain(string, fp):
    """
    Find lines in a file that contain a given string.

    Args:
        string: A string to search for in the file.
        fp: A file object representing the file to search.

    Returns:
        A list of strings representing the lines in the file that contain the given string.
    """
    return [line for line in fp if string in line]
    
#####
# Function for getting a list of random files in the ZK 
#####
    
def zkrand(number):
    target_dir = TheArchivePath()
    counter = 0
    # Set counter to the number of notes wanted to be returned.
    print(f'## {number} random notes from the past.')
    while counter < number:
        # Create a variable "random+file" that contains a randomixed list of the files,
        random_file=random.choices(os.listdir(target_dir))
        # d = a year month day
        d = re.compile('.* (\d{8})')
        zkdate = d.match(str(random_file))[1]
        f = re.compile("\[['\"](.*\d{12})")
        year=zkdate[:4]
        zktitle = f.match(str(random_file))[1]
        #  Set "date" to a string now minus x years
        date = datetime.now() - relativedelta(years=0)
        date = date.strftime('%Y%m%d')
        # Compare current date (minus x years) with the file date and print if less than. And then update counter and do it all again,
        if date >= zkdate:
                UUID = zktitle[-12:]
                zettelname = zktitle[:-13]
                #  Print MMD formatted links
                print(f'{year} [{zettelname}](thearchive://match/{zettelname} {UUID})')
                counter += 1
                    
if __name__ == "__main__":
    print(zkrand(10))    

    
#####
# Function for determining if the ZK is growing or shrinking
##### 

import os
import fnmatch
from datetime import datetime as dt
from datetime import timedelta
zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def trend(length):
    """
    Returns the number of files in the zettelkasten directory that match a date pattern
    for the last n days, where n is the length parameter. This is uesd to calculate the trend.
        
    The date pattern is YYYYMMDD, and the files are markdown files.

    The function returns a tuple of the number of files that match the pattern and the length parameter.    
    """
    # calculate date range for the last ten days
    today = dt.today()
    ten_days_ago = today - timedelta(days=length)
    date_range = [ten_days_ago + timedelta(days=x) for x in range(length)]

    # use fnmatch to filter the file names based on a pattern that matches the date string
    count = 0
    for root, dirs, files in os.walk(zettelkasten):
        for date in date_range:
            date_str = date.strftime("%Y%m%d")
            for file in fnmatch.filter(files, f"*{date_str}*.md"):
                count += 1
    return count, length

if __name__ == "__main__":

    # if the trend is zero, the number of files is the same
    # if the trend is positive, the number of files is increasing
    # if the trend is negative, the number of files is decreasing
    # the direction variable is used to indicate the direction of the trend

    direction = '⎯'
    if trend(9) > trend(10):
        direction = '⬆︎'
    elif trend(99) < trend(100) :
        direction = '⬇︎'

    # print the trend for the last 10 days and the last 100 days    

    print(f'{trend(10)[1]} day tend: {trend(10)[0]}/{trend(10+1)[0]} {direction}')
    print(f'{trend(100)[1]} day trend: {trend(100)[0]}/{trend(100+1)[0]} {direction}')

 
    
#####
# Function for getting a list of random files in the ZK that are more than 1000 words
##### 
 
import os, re, random
from datetime import datetime
from dateutil.relativedelta import relativedelta

####
# Get a random file from the zettelkasten folder with more than 1000 words
####
   
def large_note_rand(minsize, maxsize, notenumber):
    target_dir = TheArchivePath()
    files = os.listdir(target_dir)
    files = [f for f in files if f.endswith('.md')]
    zettel=0
    print(f'## {notenumber} random notes for review & atomizing, between {minsize} and {maxsize} words.')    
    while zettel < notenumber:
        # open a random file
        random.shuffle(files)
        file_name, file_ext = os.path.splitext(os.path.basename(files[0]))
        d = re.compile('.* (\d{8})')
        zkdate = d.match(str(file_name))[1]
        year=zkdate[:4]
        with open(f'{target_dir}/{files[0]}', 'r') as file:
            data = file.read()
            words = data.split()
            if len(words) > minsize and len(words) < maxsize:
                zettel+=1   
                # print(f"{file_name} has {len(words)} words.")
                # add leading spaces
                # print(f'{len(words)} [{file_name}](thearchive://match/{file_name})')
                print(f'{year} {str(len(words)).ljust(4)} [{file_name}](thearchive://match/{file_name})')
        continue            
    return 

if __name__ == "__main__":
    large_note_rand(500, 1500, 10)
    
####
# Function that returns the time it takes to run a function
# Is used as a decorator
#####     
    
import os
import sys
from datetime import timedelta
from timeit import time

def stopwatch(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        duration = timedelta(seconds=te - ts)
        print(f"{method.__name__}: {duration}")
        return result
    return timed

if __name__ == "__main__":
    @stopwatch
    def test():
        return sum(range(1000000))
    test()
    
####
# Regex search of file names in the ZK
####    

import os
import re
import glob
    
def filepaths_search(root_path: str, file_regex: str):
    return glob.glob(os.path.join(root_path, file_regex))

if __name__ == "__main__":
    print(filepaths_search(zettelkasten, "*20221218*.md"))

####
# Function for bookography progress
####    

import re
import datetime

def bookography(goal):
    """
    Calculates the progress towards a reading goal based on the number of books read compared to the years week number.

    Args:
        goal (int): The number of books to read in a year.
    
    Returns:
        tuple:
        - int: The highest book number read.
        - int: The current week of the year.
        - int: The goal for the year.
    
    Returns a tuple containing the highest book number read, the current week of the year, and the goal for the year.
    """
    # Variables
    # User needs to change this to the path of their Bookography file
    bookography = "/Users/will/Dropbox/zettelkasten/Bookography 2023 202301021454.md"
    current_date = datetime.date.today()
    current_week = current_date.isocalendar()[1]
    
    # Read the entire file
    with open(bookography, 'r') as file:
        content = file.read()
    # Search for ordered list items and extract numbers
    # regex pattern looks for lines that start with a number followed by a period
    pattern = r"^\s*\d+\."
    matches = re.findall(pattern, content, re.MULTILINE)
    # Convert matches to integers and remove the period
    numbers = [int(match.strip(".")) for match in matches]

    # Find the highest number
    if numbers:
        highest_number = max(numbers)
    else:
        highest_number = 0

    return highest_number, current_week, goal

if __name__ == "__main__":
    highest_number, current_week, goal = bookography(52)
    print(f"**I've read {highest_number} books so far this year.** \n**It is week {current_week} of my one-book-per-week challenge.**\n**My goal is to read {goal} books this year.**\n\n")