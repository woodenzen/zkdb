#!/usr/bin/env python3
# encoding: utf-8

from __future__ import absolute_import
from Foundation import NSData
from Foundation import NSPropertyListMutableContainers
from Foundation import NSPropertyListSerialization
import os
import sys
from urllib.parse import urlparse


class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass


class NSPropertyListSerializationException(FoundationPlistException):
    """Read/parse error for plists"""
    pass


class TheArchive:
    @staticmethod
    def path():
        archive_url = TheArchive.setting('archiveURL')
        path = urllib2.unquote(archive_url[len("file://"):])
        return path

    @staticmethod
    def plist():
        bundle_id = "de.zettelkasten.TheArchive"
        team_id = "FRMDA3XRGC"
        filepath = os.path.expanduser(
            "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
        if os.path.exists(filepath):
            plistData = NSData.dataWithContentsOfFile_(filepath)
            data, dummy_plistFormat, error = (
                NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                    plistData, NSPropertyListMutableContainers, None, None
                )
            )
            if data is None:
                if error:
                    error = error.encode('ascii', 'ignore')
                else:
                    error = "Unknown error"
                raise NSPropertyListSerializationException(
                    "{0} in file {1}".format(error, filepath))
            else:
                return data
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


path = TheArchive.path()
sys.stdout.write(path)
