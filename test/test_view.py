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
import logging
import stat
import unittest
from brainfs import view

class FSAttributesTest(unittest.TestCase):

    def testStr(self):
        """Test the FSAttributes.__str__ method
        """

        a = view.FSAttributes()

        self.assertTrue(len(str(a)) > 0)

        logging.debug('Test attributes are ' + str(a))

class AbstractViewTest(unittest.TestCase):

    def validateView(self, view, path):
        attr = view.getattr(path)

        self.assertNotEquals(-errno.ENOSYS, attr,
                              msg = 'Expected attributes for path ' + path + ' but was ' + str(attr))
        self.assertNotEquals(-errno.ENOENT, attr,
                              msg = 'Expected attributes for path ' + path + ' but was ' + str(attr))

        if (attr.st_mode & stat.S_IFDIR == stat.S_IFDIR):
            # path is a directory

            # TODO implement propper offset handling
            for entry in view.readdir(path, 0):
                self.assertTrue(entry != None)

            r = view.symlink('the file', path + '/the link')
        elif (attr.st_mode & stat.S_IFLNK == stat.S_IFLNK):
            l = view.readlink(path)

            self.assertNotEquals(-errno.ENOENT, l)

            self.assertTrue(len(l) > 0)
        elif (attr.st_mode & stat.S_IFCHR == stat.S_IFCHR):
            self.assertTrue(attr.st_size >= 0)

            content = view.read(path, min(attr.st_size, 100), 0)

            self.assertNotEquals(-errno.ENOSYS, content)
            self.assertNotEquals(-errno.ENOENT, content)

            self.assertTrue(content != None)

            logging.debug('Content: ' + str(content))

            # TODO validate block file
            
            pass
        else:
            self.fail('Unknown attributes ' + str(attr))


class AbstractPatternViewTest(AbstractViewTest):

    def validatePatternView(self, view, matchPath, notMatchPath = None):
        self.validateView(view, matchPath)

        self.assertTrue(view.canHandlePath(matchPath))

        if notMatchPath:
            self.assertFalse(view.canHandlePath(notMatchPath))

class AbstractNodeViewTest(AbstractPatternViewTest):

    def validateNode(self, node, path):
        attr = node.getattr(path)

        self.assertNotEquals(-errno.ENOSYS, attr)
        self.assertNotEquals(-errno.ENOENT, attr)

        # TODO

    def validateNodeView(self, view, matchPath, notMatchPath = None):
        self.validatePatternView(view, matchPath, notMatchPath)

        self.validateNode(view.getRootNode(), '/')
        

if __name__ == "__main__":
    import brainfs

    unittest.main()
