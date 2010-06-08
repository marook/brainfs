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

class GenericContentNode(object):

    def __init__(self, subject):
        self.subject = subject

class FileSubjectContentNode(object):

    def __init__(self, subject):
        self.subject = subject

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFLNK | 0555
        a.st_nlink = 2

        return a

    def readlink(self, path):
        return self.subject.fileName

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

    def getContentNode(self):
        if isinstance(self.subject, dom.FileSubject):
            return FileSubjectContentNode(self.subject)

        return GenericContentNode(self.subject)

    def getChildNode(self, name):
        if name == 'content.jpg':
            return self.getContentNode()

        return None

class PushNode(object):

    def __init__(self, subjects):
        self.subjects = subjects

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFCHR | 0777
        a.st_nlink = 2

        return a

    def read(self, path, len, offset):
        # TODO
        return 'todo'

class RootNode(object):

    def __init__(self, subjects):
        self.subjects = subjects
        self.pushNodeName = '.push'
    
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

    def readdir(self, path, offset):
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')

        yield fuse.Direntry(self.pushNodeName)

        for s in self.subjects:
            yield fuse.Direntry(s.name)

    def symlink(self, path, linkPath):
        # TODO strip last part from link path (strip '/' from '/path')
        s = dom.FileSubject(linkPath)

        self.subjects.append(s)

    def getChildNode(self, name):
        if name == self.pushNodeName:
            return PushNode(self.subjects)

        s = self.getSubjectForName(name)

        if s:
            return SubjectDirectoryNode(s)

        return None
        

class SubjectDirectoryView(view.NodeView):

    def __init__(self, subjects):
        view.NodeView.__init__(self)

        self.subjects = subjects

    def getRootNode(self):
        return RootNode(self.subjects)
