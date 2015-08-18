# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for qutebrowser.browser.commands."""

import collections

import pytest
from PyQt5.QtNetwork import (QNetworkCookieJar, QAbstractNetworkCache,
                             QNetworkCacheMetaData)

from qutebrowser.browser import commands
from qutebrowser.mainwindow import tabbedbrowser
from qutebrowser.utils import objreg
from qutebrowser.keyinput import modeman


ObjectsRet = collections.namedtuple('Dispatcher', ['tb', 'cd'])

class FakeNetworkCache(QAbstractNetworkCache):

    def cacheSize(self):
        return 0

    def data(self, _url):
        return None

    def insert(self, _dev):
        pass

    def metaData(self, _url):
        return QNetworkCacheMetaData()

    def prepare(self, _metadata):
        return None

    def remove(self, _url):
        return False

    def updateMetaData(self, _url):
        pass


@pytest.yield_fixture(autouse=True)
def cookiejar_and_cache():
    """Fixture providing a fake cookie jar and cache."""
    jar = QNetworkCookieJar()
    cache = FakeNetworkCache()
    objreg.register('cookie-jar', jar)
    objreg.register('cache', cache)
    yield
    objreg.delete('cookie-jar')
    objreg.delete('cache')


@pytest.yield_fixture
def objects(qtbot, default_config, key_config_stub, tab_registry,
            host_blocker_stub):
    """Fixture providing a CommandDispatcher and a fake TabbedBrowser."""
    win_id = 0
    modeman.init(win_id, parent=None)
    tabbed_browser = tabbedbrowser.TabbedBrowser(win_id)
    qtbot.add_widget(tabbed_browser)
    objreg.register('tabbed-browser', tabbed_browser, scope='window',
                    window=win_id)
    dispatcher = commands.CommandDispatcher(win_id, tabbed_browser)
    objreg.register('command-dispatcher', dispatcher, scope='window',
                    window=win_id)
    yield ObjectsRet(tabbed_browser, dispatcher)


@pytest.mark.skipif(True, reason="Work in progress")
def test_openurl(objects):
    objects.cd.openurl('localhost')