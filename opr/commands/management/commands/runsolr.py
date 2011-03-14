#/usr/bin/env python2.6

__authors__ = [
        '"Ben Ripkens" <bripkens.dev@gmail.com>',
]

from django.core.management.base import NoArgsCommand
from django.conf import settings
import os

class Command(NoArgsCommand):
    """
    Useful command to start up the solr server.

    This requires the SOLR_START_COMMAND and SOLR_WORKING_DIRECTORY setting.

    """
    help = 'Convert scss to css'

    def handle_noargs(self, **options):
        command = settings.SOLR_START_COMMAND
        os.chdir(settings.SOLR_WORKING_DIRECTORY)
        print "Starting development solr instance with command '%s'" % command
        os.system(command)
