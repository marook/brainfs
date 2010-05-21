#
# Copyright 2010 Markus Pielmeier
#
# This file is part of brainfs.
#
# brainfs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# brainfs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with brainfs.  If not, see <http://www.gnu.org/licenses/>.
#

#====================================================================
# first set up exception handling and logging

import logging
import sys

def setUpLogging():
    def exceptionCallback(eType, eValue, eTraceBack):
        import cgitb

        txt = cgitb.text((eType, eValue, eTraceBack))

        logging.fatal(txt)
    
        # sys.exit(1)

    # configure file logger
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s %(levelname)s %(message)s',
                        filename = '/tmp/brainfs.log',
                        filemode = 'a')
    
    # configure console logger
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    
    consoleFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    consoleHandler.setFormatter(consoleFormatter)
    logging.getLogger().addHandler(consoleHandler)

    # replace default exception handler
    sys.excepthook = exceptionCallback
    
    logging.debug('Logging and exception handling has been set up')

if __name__ == '__main__':
    from os import environ as env

    if 'DEBUG' in env:
        setUpLogging()

#====================================================================
# here the application begins

import errno
import fuse
import root_directory
import subject_directory

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

class BrainFS(fuse.Fuse):

    def __init__(self, initwd, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)

        self.views = [
            root_directory.RootDirectoryView(),
            subject_directory.SubjectDirectoryView()
            ]

    def findView(self, path):
        for view in self.views:
            if not view.canHandlePath(path):
                continue

            return view

        return None

    def getattr(self, path):
        view = self.findView(path)

        if not view:
            logging.info('No View for path ' + path)

            return -errno.ENOENT

        return view.getattr(path)

    def readdir(self, path, offset):
        pass
            
    def readlink(self, path):
        return -errno.ENOENT

    def open(self, path, flags):
        return -errno.ENOENT

    def read(self, path, size, offset):
        return -errno.ENOENT

def main():
    import os

    fs = BrainFS(os.getcwd(),
            version = "%prog " + fuse.__version__,
            dash_s_do = 'setsingle')

    fs.parse(errex = 1)
    opts, args = fs.cmdline

    return fs.main()

if __name__ == '__main__':
    import sys
    sys.exit(main())
