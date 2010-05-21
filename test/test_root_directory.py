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
import test_view
from brainfs import root_directory

class RootDirectoryViewTest(test_view.AbstractPatternViewTest):

    def testInterface(self):
        """Validate View interface for RootDirectoryView
        """

        view = root_directory.RootDirectoryView()

        self.validatePatternView(view,
                                 '/',
                                 '/00_IMG008')

if __name__ == "__main__":
    import brainfs

    unittest.main()
