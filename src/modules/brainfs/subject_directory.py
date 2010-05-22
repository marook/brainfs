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
import stat
import view

class SubjectDirectoryView(view.PatternView):

    def __init__(self, subjects):
        view.PatternView.__init__(self, '^/([^/]+)$')

        self.subjects = subjects

    def getSubjectName(self, path):
        m = self.pathRegEx.match(path)

        return m.group(1)

    def getSubjectForPath(self, path):
        name = self.getSubjectName(path)

        for s in self.subjects:
            if s.name == name:
                return s

        return None

    @log.logCall
    def getattr(self, path):
        s = self.getSubjectForPath(path)

        if s == None:
            return -errno.ENOENT

        a = view.FSAttributes()
        a.st_mode = stat.S_IFDIR | 0555
        a.st_nlink = 2

        return a

    @log.logCall
    def readdir(self, path, offset):
        # TODO implement me
        return []

    @log.logCall
    def symlink(self, path, linkPath):
        s = dom.FileSubject(path)

        self.subjects.append(s)

        return 0
