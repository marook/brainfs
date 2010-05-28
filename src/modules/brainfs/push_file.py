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

import dom
import log
import errno
import fuse
import stat
import view

class PushNode(object):

    def __init__(self, subjects):
        self.subjects = subjects

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFCHR | 0555
        a.st_nlink = 2

        return a

    def read(self, path, len, offset):
        # TODO
        return 'todo'

class RootNode(object):

    def __init__(self, subjects):
        self.subjects = subjects

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFDIR | 0555
        a.st_nlink = 2

        return a

    def getChildNode(self, name):
        return PushNode(self.subjects)

class PushFileView(view.NodeView):

    def __init__(self, subjects):
        view.NodeView.__init__(self, '^/[.]push$')

        self.subjects = subjects

    def getRootNode(self):
        return RootNode(self.subjects)
