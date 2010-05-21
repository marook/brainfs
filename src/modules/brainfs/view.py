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

import errno

class View(object):
    """Abstract base class for all views.

    A View needs to implement the following defs:

    def canHandlePath(self, path): This method returns wheather the supplied
    path can be handled by this view.
    """

    def getattr(self, path):
        return -errno.ENOENT

    def readdir(self, path, offset):
        pass
            
    def readlink(self, path):
        return -errno.ENOENT

    def open(self, path, flags):
        return -errno.ENOENT

    def read(self, path, size, offset):
        return -errno.ENOENT

class PatternView(View):
    """Abstract View which implements pattern based path handling.
    """

    def __init__(self, pathPattern):
        import re

        self.pathRegEx = re.compile(pathPattern)

    def canHandlePath(self, path):
        return (self.pathRegEx.match(path) != None)
