import os, pathlib
from datetime import datetime, timedelta
from plistlib import load
from urllib.parse import urlparse, unquote

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
        path = urlparse(pl['archiveURL']).path
        decoded_path = unquote(path) 
    return unquote(path) 
 

if __name__ == "__main__":
    zettelkasten = pathlib.Path(TheArchivePath())
    print(f'The Current ZK Directory. {zettelkasten}')
    print(f'## {len(os.listdir(zettelkasten))} notes in the archive.')   
    subfolders = [ f.path for f in os.scandir(zettelkasten) if f.is_dir() ]
    for i in subfolders:
        print(f'## {len(os.listdir(i))} files in {i}.')
        print(f'## {sizeof_fmt(getFolderSize(i))} in {i}.')
        print('-'*40) 