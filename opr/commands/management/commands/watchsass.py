#/usr/bin/env python2.6

__authors__ = [
        '"Ben Ripkens" <bripkens.dev@gmail.com>',
]

from django.core.management.base import NoArgsCommand
import os
import time
import datetime

class Command(NoArgsCommand):
    """
    Watch for changes in the common.scss file and convert it to common.css
    using sass. Sass needs to be on the path.

    http://sass-lang.com/

    """
    help = 'Convert scss to css'

    def handle_noargs(self, **options):
        scss = os.path.abspath("templates/resources/css/common.scss")
        css = os.path.abspath("templates/resources/css/common.css")

        command = "sass \"" + scss + "\":\"" + css + "\" --style compressed"

        print "Executing command '%s'" % command
        print "Sass watch parameter is not used due to some bug."

        last_update = os.stat(scss).st_mtime
        os.system(command)

        while True:
            if not last_update == os.stat(scss).st_mtime:
                os.system(command)
                last_update = os.stat(scss).st_mtime
                print "Updated stylesheet at %s" % datetime.datetime.now()
            time.sleep(0.5)
