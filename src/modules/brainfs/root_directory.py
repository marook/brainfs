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
import stat
import view

class RootDirectoryView(view.PatternView):

    def __init__(self):
        view.PatternView.__init__(self, '^/$')

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFDIR | 0555
        a.st_nlink = 2

        return -errno.ENOENT

    def readdir(self, path, offset):
        pass
