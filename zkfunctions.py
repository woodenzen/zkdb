
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
#  Variables that ultimately revel The Archive's plist file.
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        pl = load(fp) # load is a special function for use with a plist
        path = urlparse(pl['archiveURL']) # 'archiveURL' is the key that pairs with the zk path
    return (path.path) # path is the part of the path that is formatted for use as a path.

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
# Function for getting a list of random files in the ZK 
#####
    
def zkrand(number):
    target_dir = "/Users/will/Dropbox/zettelkasten"
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
from datetime import datetime, timedelta

zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def trend(days_ago, num_days):
    count = 0
    target_date = datetime.now() - timedelta(days=days_ago)
    target_date_str = target_date.strftime('%Y%m%d')
    for i in range(num_days):
        date = target_date - timedelta(days=i)
        date_str = date.strftime('%Y%m%d')
        for filename in os.listdir(zettelkasten):
            if date_str in filename:
                count += 1
    return count 

if __name__ == "__main__":
    result = '⬇︎' if trend(20, 10) <= trend(10, 10) else '⬆︎'
    print(result)
 
 

    
#####
# Function for getting a list of random files in the ZK that are more than 1000 words
##### 
 
 
import os, re, random
from datetime import datetime
from dateutil.relativedelta import relativedelta


####
# Get a random file from the zettelkasten folder with more than 1000 words
####
   
def large_note_rand(minsize, maxsize, target):
    target_dir = "/Users/will/Dropbox/zettelkasten"
    files = os.listdir(target_dir)
    files = [f for f in files if f.endswith('.md')]
    zettel=0
    print(f'## {target} random notes for atomizing, between {minsize} and {maxsize} words.')    
    while zettel < target:
        # open a random file
        random.shuffle(files)
        file_name, file_ext = os.path.splitext(os.path.basename(files[0]))
        with open(f'{target_dir}/{files[0]}', 'r') as file:
            data = file.read()
            words = data.split()
            if len(words) > minsize and len(words) < maxsize:
                zettel+=1   
                # print(f"{file_name} has {len(words)} words.")
                # add leading spaces
                # print(f'{len(words)} [{file_name}](thearchive://match/{file_name})')
                print(f'{str(len(words)).ljust(4)} [{file_name}](thearchive://match/{file_name})')
        continue            
    return 
if __name__ == "__main__":
    large_note_rand(800, 1600, 10)