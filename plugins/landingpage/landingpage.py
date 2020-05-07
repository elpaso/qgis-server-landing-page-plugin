# coding=utf-8
""""Landing page API plugin for QGIS Server

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

"""

__author__ = 'elpaso@itopen.it'
__date__ = '2020-04-24'
__copyright__ = 'Copyright 2020, ItOpen'


import json
import os
import re
import hashlib


from qgis.server import (
    QgsServerOgcApi,
    QgsServerFilter,
)

from qgis.core import (
    QgsProject, QgsMessageLog
)

from .handlers import (
    LandingPageApiHandler,
    StaticApiHandler,
    MapApiHandler,
)

from .utils import projects


class LandingPageApi(QgsServerOgcApi):
    """Overrides accept to only trigger on /"""

    def accept(self, url):
        return (
            url.path() == '/' or
            url.path() == '' or
            url.path().startswith('/static/') or
            url.path().startswith('/map/') or
            url.path().startswith('/index')
        )


class ProjectLoaderFilter(QgsServerFilter):
    """Load the specified project"""

    project_id_re = re.compile(r'/project/([a-f0-9]{32})')

    def requestReady(self):
        handler = self.serverInterface().requestHandler()
        project_dict = projects()
        try:
            os.environ['QGIS_PROJECT_FILE'] = project_dict[self.project_id_re.findall(handler.url())[0]]
        except Exception as ex:
            QgsMessageLog.logMessage('Could not get project from url: %s' % ex)


class LandingPageApiLoader():
    """The landing page plugin loader"""

    def __init__(self, serverIface):
        self.api = LandingPageApi(serverIface, '',
                              'Landing Page API', 'Landing Page API', '1.0')
        self.map_handler = MapApiHandler()
        self.api.registerHandler(self.map_handler)
        self.static_handler = StaticApiHandler()
        self.api.registerHandler(self.static_handler)
        self.handler = LandingPageApiHandler()
        self.api.registerHandler(self.handler)
        serverIface.serviceRegistry().registerApi(self.api)
        self.loader_filter = ProjectLoaderFilter(serverIface)
        serverIface.registerFilter( self.loader_filter, 1)

