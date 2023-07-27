import os
import re
from plistlib import load
from urllib.parse import urlparse, unquote
import glob
import time
startTime = time.time()

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


def get_uuid(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        match = re.search(r'(?<=›\[\[)\d{12}', text)
        if match:
            return match.group(0)
        else:
            return None

def get_word_count(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        word_count = len(text.split())
        return word_count        

def get_date_created(uuid): 
    date_created = uuid[:8]
    return date_created
    
def get_link_count(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        link_count = len(re.findall(r' \[\[', text))
        return link_count

def get_list_of_links(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        links = re.findall(r'(?<= \[\[)[^\]]+', text)
        return links    

def get_note_title(file_path):
    title = os.path.basename(file_path)
    return title


    
zettlekasten_path = TheArchivePath()
notes = glob.glob(os.path.join(zettlekasten_path, '*.md'))


# Create Dictionary
zk_dict = {}
for file_name in notes:
    file_path = os.path.join(TheArchivePath(), file_name)
    uuid = get_uuid(file_path)
    if uuid:
        if uuid not in zk_dict:
            zk_dict[uuid] = {}
            zk_dict[uuid]['wc'] = get_word_count(file_path)
            zk_dict[uuid]['birthed'] = get_date_created(uuid)
            zk_dict[uuid]['link_count'] = get_link_count(file_path)
            zk_dict[uuid]['link_list'] = get_list_of_links(file_path)
            zk_dict[uuid]['title'] = get_note_title(file_path)

# print(zk_dict["201912270640"])

match_uuid = '20230724'  
for uuid in zk_dict:
    if uuid[:8] == match_uuid:
        title = zk_dict[uuid]['title']
        print(uuid, title, zk_dict[uuid]['wc'])

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))        