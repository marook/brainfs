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

    def validateSubject(self, s):
        c = s.connection

        data = c.read()

        c.close()

        self.assertTrue(len(data) > 0)
        

class TestFileSubject(AbstractSubjectTest):

    def testReadData(self):
        """Tries to read data from a FileSubject
        """

        s = dom.FileSubject('/vmlinuz')

        self.validateSubject(s)

class TestHttpSubject(AbstractSubjectTest):

    def testReadData(self):
        """Tries to read data from a HttpSubject
        """

        s = dom.HttpSubject('/', 'www.heise.de')

        self.validateSubject(s)


if __name__ == "__main__":
    import brainfs

    unittest.main()
