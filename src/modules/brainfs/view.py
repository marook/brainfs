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
import log

class FSAttributes(object):
    
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

    def __str__(self):
        return '[' + ', '.join([field + ': ' + str(self.__dict__[field]) for field in self.__dict__]) + ']'
    

class NodeView(object):
    """Abstract View which implements Node based paths.

    Extending classes must implement def getRootNode(self). getRootDef(...)
    returns a Node.
    """

    def getNode(self, path):
        n = self.getRootNode()

        for e in path.split('/')[1:]:
            if e == '':
                continue

            n = n.getChildNode(e)

            if not n:
                # it seems like we are trying to fetch a node for an illegal
                # path

                break

        return n

    @log.logCall
    def getattr(self, path):
        n = self.getNode(path)

        if not n:
            return -errno.ENOENT

        return n.getattr(path)

    @log.logCall
    def readdir(self, path, offset):
        n = self.getNode(path)

        if not n:
            return -errno.ENOENT

        return n.readdir(path, offset)

    @log.logCall
    def readlink(self, path):
        n = self.getNode(path)

        if not n:
            return -errno.ENOENT

        return n.readlink(path)

    @log.logCall
    def symlink(self, path, linkPath):
        n = self.getNode(path)

        if not n:
            return -errno.ENOENT

        return n.symlink(path, linkPath)

    @log.logCall
    def read(self, path, len, offset):
        n = self.getNode(path)

        if not n:
            return -errno.ENOENT

        return n.read(path, len, offset)
