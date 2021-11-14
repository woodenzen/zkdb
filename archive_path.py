#!/usr/bin/env python3
# encoding: utf-8

# Credit for the class "TheArchive" goes to @pryley, the developer of the code.
# Our friend over on the zettelkasten.de/forums

from plistlib import load
from urllib.parse import unquote
import os
import sys


class TheArchive:
    @staticmethod
    def path():
        archive_url = TheArchive.setting('archiveURL')
        path = unquote(archive_url[len("file://"):])
        return path

    @staticmethod
    def plist():
        bundle_id = "de.zettelkasten.TheArchive"
        team_id = "FRMDA3XRGC"
        filepath = os.path.expanduser(
            "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
        if os.path.exists(filepath):
            with open(filepath, 'rb') as fp:
                return load(fp)
        else:
            raise Exception("Error: Cannot find The Archive plist.")

    @staticmethod
    def setting(key):
        data = TheArchive.plist()
        try:
            return data[key]
        except KeyError:
            raise Exception(
                u"Warning: Cannot get The Archive setting: {0}".format(key))


if __name__ == "__main__":
    path = TheArchive.path()
    sys.stdout.write(path)
