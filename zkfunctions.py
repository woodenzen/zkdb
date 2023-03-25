
import os, re, random, pathlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from plistlib import load
from urllib.parse import urlparse

####
# Function for finding the path to The Archive
#####
# Set the active archive path
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
    print(zettelkasten)
    
'''
Print a random list of notes from the past.
'''   
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
    zkrand(10)
    
'''
get folder size
'''
def getFolderSize(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):#not sub folders
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)   
    return total_size
    
'''
Human readable single folder size
'''

def sizeof_fmt(num, suffix='bytes'):
    for unit in ['',' Kilo',' Mega',' Giga',' Tera',' Peta',' Exa',' Zetta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return

if __name__ == '__main__':
    print(sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten/media/')))

