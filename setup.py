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

from distutils.core import setup, Command
import sys
import os
from os.path import (
        basename,
        dirname,
        abspath,
        splitext,
        join as pjoin
)
from glob import glob
from unittest import TestLoader, TextTestRunner

projectdir = dirname(abspath(__file__))
srcdir = pjoin(projectdir, 'src')
moddir = pjoin(srcdir, 'modules')
testdir = pjoin(projectdir, 'test')

class test(Command):
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        self._cwd = os.getcwd()
        self._verbosity = 2

    def finalize_options(self): pass

    def run(self):
        tests = ['.'.join([
                basename(testdir), splitext(basename(f))[0]
        ]) for f in glob(pjoin(
                testdir, '*.py'
        )) if not f.endswith('__init__.py')]

        print "..using:"
        print "  testdir:", testdir
        print "  tests:", tests
        print "  sys.path:", sys.path
        print
        sys.path.insert(0, moddir)
        sys.path.insert(0, srcdir)

        if 'DEBUG' in os.environ:
            from brainfs.brainfs import setUpLogging
            setUpLogging()

        suite = TestLoader().loadTestsFromNames(tests)
        TextTestRunner(verbosity=self._verbosity).run(suite)


# Overrides default clean (which cleans from build runs)
# This clean should probably be hooked into that somehow.
class clean_pyc(Command):
    description = 'remove *.pyc files from source directory'
    user_options = []

    def initialize_options(self):
        self._delete = []
        for cwd, dirs, files in os.walk(projectdir):
            self._delete.extend(
                pjoin(cwd, f) for f in files if f.endswith('.pyc')
            )

    def finalize_options(self): pass

    def run(self):
        for f in self._delete:
            try:
                os.unlink(f)
            except OSError, e:
                print "Strange '%s': %s" % (f, e)
                # Could be a directory.
                # Can we detect file in use errors or are they OSErrors
                # as well?
                # Shall we catch all?

setup(
    cmdclass = {
        'test': test,
        'clean_pyc': clean_pyc,
    },
    name = 'brainfs',
    version = '0.1',
    url = 'http://github.com/marook/brainfs',
    description = '',
    long_description = '',
    author = 'Markus Pielmeier',
    author_email = 'markus.pielmeier@gmx.de',
    license = 'GPLv3',
    platforms = 'Linux',
    requires = [],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Filesystems'
    ],
    data_files = [
        (pjoin('share', 'doc', 'brainfs'), ['AUTHORS', 'COPYING', 'README'])
    ],
    scripts = [pjoin('src', 'brainfs')],
    packages = ['brainfs'],
    package_dir = {'': pjoin('src', 'modules')},
)
