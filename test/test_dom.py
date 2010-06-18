#!/usr/bin/env python
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

import unittest
from brainfs import dom

class AbstractSubjectTest(unittest.TestCase):

    def validateSubjectConnection(self, s):
        c = s.connection

        data = c.read()

        c.close()

        self.assertTrue(len(data) > 0)

    def validateSubjectName(self, s):
        n = s.name

        self.assertTrue(len(n) > 0)

    def validateSubject(self, s):
        self.validateSubjectConnection(s)
        self.validateSubjectName(s)

class TestFileSubject(AbstractSubjectTest):

    def testReadData(self):
        """Tries to read data from a FileSubject
        """

        s = dom.FileSubject('src/brainfs')

        self.validateSubject(s)

        self.assertEqual('brainfs', s.name)

    def testFromUrl(self):
        """Creates a FileSubject from an URL
        """

        s = dom.fromUrl('file:///usr')

        self.validateSubject(s)

        self.assertEquals('/usr', s.fileName)

class TestHttpSubject(AbstractSubjectTest):

    def testReadData(self):
        """Tries to read data from a HttpSubject
        """

        s = dom.HttpSubject('/index.html', 'localhost')

        self.validateSubject(s)

        self.assertEqual('localhost_index.html', s.name)

    def testFromUrl(self):
        """Creates a HttpSubject from an URL
        """

        s = dom.fromUrl('http://localhost')

        self.validateSubject(s)

        self.assertEquals('localhost', s.host)
        self.assertEquals('', s.path)
        self.assertEquals('GET', s.method)


if __name__ == "__main__":
    import brainfs

    unittest.main()
