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
import logging
import errno
import fuse
import os
import stat
import view

class GenericContentNode(object):

    def __init__(self, subject):
        self.subject = subject
        self.content = None

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFREG | 0444
        a.st_nlink = 2
        a.st_uid = os.getuid()
        a.st_gid = os.getgid()
        a.st_size = len(self.getContent())

        return a

    def getContent(self):
        if self.content == None:
            logging.debug('Reading content for subject %s', self.subject)

            c = self.subject.connection

            self.content = c.read()

            c.close()

        return self.content

    def open(self, path, flags):
        pass

    def read(self, path, len, offset):
        c = self.getContent()

        return c[offset:len - offset]

class FileSubjectContentNode(object):

    def __init__(self, subject):
        self.subject = subject

    def getattr(self, path):
        a = view.FSAttributes()
        a.st_mode = stat.S_IFLNK | 0555
        a.st_nlink = 2
        a.st_uid = os.getuid()
        a.st_gid = os.getgid()

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
        a.st_uid = os.getuid()
        a.st_gid = os.getgid()

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
        a.st_mode = stat.S_IFREG | 0644
        a.st_nlink = 1
        a.st_uid = os.getuid()
        a.st_gid = os.getgid()
        a.st_size = len('hello')

        return a

    def open(self, path, flags):
        # TODO validate read/write/append request
        pass

    def read(self, path, len, offset):
        return 'hello'

    def write(self, path, data, pos):
        i = data.index('\n')

        url = data[0:i]

        # TODO create FileSubject or HttpSubject based on URI
        s = dom.fromUrl(url)

        logging.debug('Parsed subject %s from URL %s' % (s, url))

        self.subjects.append(s)

        return i + 1

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
        a.st_mode = stat.S_IFDIR | 0755
        a.st_nlink = 2
        a.st_uid = os.getuid()
        a.st_gid = os.getgid()

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
