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

prefix = /usr/local
bindir = $(prefix)/bin
docdir = $(prefix)/share/doc/brainfs
installdirs = $(bindir) $(docdir)

srcdir = .

testmntdir = $(shell pwd)/mnt

pymoddir = $(srcdir)/src/modules

PYTHON = python
INSTALL = install
INSTALL_DATA = $(INSTALL) -m 644
INSTALL_PROGRAM = $(INSTALL)

DOCS = AUTHORS COPYING README

.PHONY: all
all:
	@echo "42. That's all."
	@echo "Try 'make mounttest' for something more interesting."

.PHONY: clean
clean:
	find $(srcdir) -name '*.pyc' -type f -exec rm {} \;
	@if test "`mount | grep -e 'brainfs.*on.*$(testmntdir)'`"; then \
		echo "brainfs mounted on '$(testmntdir)' -- keeping it."; \
	elif test -d '$(testmntdir)'; then \
		echo 'removing $(testmntdir)'; \
		rmdir '$(testmntdir)'; \
	fi

.PHONY: test
test:
	$(PYTHON) $(srcdir)/test/test_all.py

$(installdirs):
	$(INSTALL) -d $(installdirs)

.PHONY: install
install: $(installdirs)
	$(INSTALL_PROGRAM) $(srcdir)/src/brainfs $(bindir)/brainfs
	$(INSTALL_DATA) $(DOCS) $(docdir)

.PHONY: uninstall
uninstall:
	rm -- $(bindir)/brainfs
	rm -r -- $(docdir)

$(testmntdir):
	mkdir -p $@

.PHONY: mounttest
mounttest: $(testmntdir)
	PYTHONPATH=$(pymoddir):$(PYTHONPATH) \
		$(PYTHON) $(srcdir)/src/brainfs $(testmntdir)

.PHONY: unmounttest
unmounttest:
	fusermount -u $(testmntdir)
	rmdir -- $(testmntdir)

.PHONY: umounttest
umounttest: unmounttest

.PHONY: mt
mt: mounttest

.PHONY: umt
umt: unmounttest
