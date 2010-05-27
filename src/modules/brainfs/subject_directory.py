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

class ContentLinkNode(object):

    def __init__(self, subject):
        self.subject = subject

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFLNK | 0555
        a.st_nlink = 2

        return a

    def readlink(self, path):
        # TODO
        return 'bla'

class SubjectDirectoryNode(object):

    def __init__(self, subject):
        self.subject = subject
    
    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFDIR | 0555
        a.st_nlink = 2

        return a

    def readdir(self, path, offset):
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')

        # TODO calculate extention dynamically
        yield fuse.Direntry('content.jpg')

    def getChildNode(self, name):
        if name == 'content.jpg':
            return ContentLinkNode(self.subject)

        return None

class RootNode(object):

    def __init__(self, subjects):
        self.subjects = subjects
    
    def getSubjectForName(self, name):
        # TODO introduce dict for subjects

        for s in self.subjects:
            if s.name == name:
                return s

        return None

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFDIR | 0555
        a.st_nlink = 2

        return a

    def symlink(self, path, linkPath):
        s = dom.FileSubject(path)

        self.subjects.append(s)

    def getChildNode(self, name):
        s = self.getSubjectForName(name)

        if not s:
            return None

        return SubjectDirectoryNode(s)
        

class SubjectDirectoryView(view.NodeView):

    def __init__(self, subjects):
        view.NodeView.__init__(self, '^/(.+)$')

        self.subjects = subjects

    def getRootNode(self):
        return RootNode(self.subjects)
