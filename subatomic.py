#!/usr/bin/python3
# encoding: utf-8
import os
from plistlib import load
from urllib.parse import urlparse


#####
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

def check(token):
    with open(os.environ["KMVAR_fname"]) as f:
        datafile = f.readlines()
    for line in datafile:
        if token in line:
            # print(line.partition("Subatomic: ")[2])   
            return line.partition("Subatomic: ")[2]
    return False  # Because you finished the search without finding
     
    # Use    
if __name__ == "__main__":
    output = (f'\t\t {check("Subatomic: ")}')  
    print(output)

