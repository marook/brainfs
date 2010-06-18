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

from brainfs import dom
import unittest
import test_view
from brainfs import subject_directory

class SubjectDirectoryViewTest(test_view.AbstractNodeViewTest):

    def validatePushNode(self, subjects, view):
        host = 'localhost'
        path = ''

        url = 'http://' + host + path + '\n'

        # TODO maybe we should set the second param somehow specific?
        view.open('/.push', '32768')

        p = 0
        while p < len(url):
            l = view.write('/.push', url[p:len(url)], p)

            self.assertTrue(l > 0)

            p = p + l

        self.assertEquals(len(url), p)

        found = False
        for s in [s for s in subjects if isinstance(s, dom.HttpSubject)]:
            if not s.host == host:
                continue

            if not s.path == path:
                continue

            if not s.port == 80:
                continue

            if not s.method == 'GET':
                continue

            found = True

        if not found:
            self.fail(msg = 'Can\'t find pushed subject')


    def testInterface(self):
        """Validate View interface for SubjectDirectoryView
        """

        subjects = [
            dom.FileSubject('etc/demo_resources/00_IMG008.jpg')
            ]

        view = subject_directory.SubjectDirectoryView(subjects)

        self.validateNodeView(view, '/')


        self.validateNodeView(view, '/00_IMG008.jpg')

        r = view.symlink('../the file', '/the link')
        # TODO assert r's content

        self.validateNodeView(view, '/the link')

        self.validatePushNode(subjects, view)

if __name__ == "__main__":
    import brainfs

    unittest.main()
