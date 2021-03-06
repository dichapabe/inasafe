# coding=utf-8
"""
InaSAFE Disaster risk assessment tool developed by AusAid - **Help Class.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'tim@linfiniti.com'
__revision__ = '$Format:%H$'
__date__ = '20/01/2011'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

import sys
import os
import logging

from PyQt4 import (QtGui, QtCore)

from safe_qgis.exceptions import HelpFileMissingError

LOGGER = logging.getLogger('InaSAFE')


def show_context_help(context=None):
    """Show help using the user's web browser.

    :type context: str
    :param context: Page name (without path) of a document in the
       user-docs subdirectory. e.g. 'keywords'
    """

    try:
        _show_local_help(context)
    except HelpFileMissingError:
        _show_online_help(context)


def _show_local_help(context=None):
    """Show help using the user's web browser - uses local help file.

    :type context: str
    :param context: Page name (without path) of a document in the
       user-docs subdirectory. e.g. 'keywords'

    :raises: HelpFileMissingError
    """

    # First we try using local filesystem

    base_url = os.path.abspath(os.path.join(
        __file__, os.path.pardir, os.path.pardir, os.path.pardir, 'docs'
    ))

    # set default value for myLocale
    myLocale = 'en'
    if 'LANG' in os.environ:
        myLocale = os.environ['LANG']

    if myLocale not in ['id', 'en']:
        myLocale = 'en'

    base_url = os.path.join(base_url, myLocale)

    if context is not None:
        base_url = os.path.join(base_url, context + '.html')
        LOGGER.debug(os.path.isfile(base_url))
    else:
        base_url = os.path.join(base_url, 'index.html')

    if not os.path.exists(base_url):
        raise HelpFileMissingError('Help file not found: %s' % base_url)

    # Even on windows we need to use / for urls
    if 'win32' in sys.platform:
        drive, path = os.path.splitdrive(base_url)
        base_url = path.replace(os.path.sep, '/')
        base_url = drive + base_url
        base_url = 'file:///%s' % base_url
    else:
        base_url = 'file://%s' % base_url

    myUrl = QtCore.QUrl(base_url)
    # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
    QtGui.QDesktopServices.openUrl(myUrl)


def _show_online_help(context=None):
    """Show help using the user's web browser - uses inasafe web site.

    :type context: str
    :param context: Page name (without path) of a document in the
       user-docs subdirectory. e.g. 'keywords'
    """

    # First we try using local filesystem

    base_url = 'http://inasafe.linfiniti.com/'

    # set default value for myLocale
    myLocale = 'en'
    if 'LANG' in os.environ:
        myLocale = os.environ['LANG']

    if myLocale not in ['id', 'en']:
        myLocale = 'en'

    base_url += myLocale
    base_url += '/user-docs/'

    if context is not None:
        base_url += context + '.html'
        LOGGER.debug(os.path.isfile(base_url))
    else:
        base_url += 'index.html'
    myUrl = QtCore.QUrl(base_url)
    # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
    QtGui.QDesktopServices.openUrl(myUrl)
