# #!/usr/bin/env python3
# # encoding: utf-8

# # Credit for the class "TheArchive" goes to @pryley, the developer of the code.
# # Our friend over on the zettelkasten.de/forums

# from plistlib import load
# from urllib.parse import unquote
# import os
# import sys


# class TheArchive:
#     @staticmethod
#     def path():
#         archive_url = TheArchive.setting('archiveURL')
#         path = unquote(archive_url[len("file://"):])
#         return path

#     @staticmethod
#     def plist():
#         bundle_id = "de.zettelkasten.TheArchive"
#         team_id = "FRMDA3XRGC"
#         filepath = os.path.expanduser(
#             "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
#         if os.path.exists(filepath):
#             with open(filepath, 'rb') as fp:
#                 return load(fp)
#         else:
#             raise Exception("Error: Cannot find The Archive plist.")

#     @staticmethod
#     def setting(key):
#         data = TheArchive.plist()
#         try:
#             return data[key]
#         except KeyError:
#             raise Exception(
#                 u"Warning: Cannot get The Archive setting: {0}".format(key))


# if __name__ == "__main__":
#     path = TheArchive.path()
#     sys.stdout.write(path)

# import os, pathlib
# import plistlib
# import sys

# def get_archive_directory():
#     filenname = os.path.expanduser(
#         "~/Library/Group Containers/FRMDA3XRGC.de.zettelkasten.TheArchive.prefs/"
#         "Library/Preferences/FRMDA3XRGC.de.zettelkasten.TheArchive.prefs.plist")
#     with open(filenname, 'rb') as fp:
#         pl = plistlib.load(fp)
#         return pl['archiveURL'] 

# if __name__ == "__main__":
#     path = pathlib.Path(get_archive_directory())
#     print(path)   

from urllib.parse import urlparse
import os, pathlib
from plistlib import load
    
def TheArchivePath():
#  Variables that ultimately revel The Archive's plist file.
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