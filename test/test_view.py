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

import stat
import unittest

class AbstractViewTest(unittest.TestCase):

    def validateView(self, view, path):
        attr = view.getattr(path)

        self.assertTrue(attr)

        if (attr.st_mode | stat.S_IFDIR > 0):
            # path is a directory

            # TODO implement propper offset handling
            dir = view.readdir(path, 0)

            # TODO self.assertTrue(dir)
        else:
            self.fail('Unknown attributes ' + attr)


class AbstractPatternViewTest(AbstractViewTest):

    def validatePatternView(self, view, matchPath, notMatchPath):
        self.validateView(view, matchPath)

        self.assertTrue(view.canHandlePath(matchPath))
        self.assertFalse(view.canHandlePath(notMatchPath))

if __name__ == "__main__":
    import brainfs

    unittest.main()
