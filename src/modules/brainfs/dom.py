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

class Subject(object):
    """Superclass for all subjects.

    All subjects must supply a connection parameter. This parameter returns
    a stream with the content of the subject.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '[' + ', '.join([field + ': ' + str(self.__dict__[field]) for field in self.__dict__]) + ']'

class FileSubject(Subject):
    
    def __init__(self, fileName):
        import os.path

        Subject.__init__(self, os.path.basename(fileName))

        self.fileName = fileName

    @property
    def connection(self):
        f = open(self.fileName, 'r')

        return f

    def __eq__(self, o):
        # TODO maybe we should match type of self and o too?

        if o == None:
            return False

        return (self.fileName == o.fileName)
        

class HttpSubject(Subject):

    def __init__(self, path, host, port = 80, method = 'GET'):
        # TODO create more sane subject name
        Subject.__init__(self, (host + path).replace('/', '_'))

        self.path = path
        self.host = host
        self.port = port
        self.method = method

    @property
    def connection(self):
        import httplib

        c = httplib.HTTPConnection(self.host, self.port)
        c.request(self.method, self.path)

        r = c.getresponse()

        class Connection(object):

            def read(self, amount = None):
                return r.read(amount)

            def close(self):
                c.close()

        return Connection()

class Predicate(object):
    
    def __init__(self, name, namespace):
        """Creates a Predicate

        @parameter name This is the short name of the predicate. It may appear
        in different predicates.
        @parameter namespace This is the unique name of this predicate. Should
        have URL syntax like 'http://www.bloab.com/image/width'.
        """
        self.name = name
        self.namespace = namespace

def fromUrl(url, method = 'GET'):
    import urlparse

    u = urlparse.urlparse(url)

    if u.scheme == 'file':
        return FileSubject(u.path)

    if u.scheme == 'http':
        return HttpSubject(u.path, u.hostname, u.port, method)

    # TODO raise error

    return None
