# coding=utf-8
""""API Handlers for Landing Page plugin

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

"""

__author__ = 'elpaso@itopen.it'
__date__ = '2020-04-28'
__copyright__ = 'Copyright 2020, ItOpen'

import os
import re

from qgis.PyQt.QtCore import (
    QBuffer,
    QIODevice,
    QTextStream,
    QRegularExpression,
    QMimeDatabase,
)

from qgis.server import (
    QgsServerOgcApiHandler,
    QgsServerOgcApi,
)

from .utils import project_info, projects

class LandingPageApiHandler(QgsServerOgcApiHandler):
    """Project listing handler"""

    def __init__(self):
        super().__init__()
        self.setContentTypes([QgsServerOgcApi.HTML, QgsServerOgcApi.JSON])

    def path(self):
        return QRegularExpression("/")

    def operationId(self):
        return "Landing Page API"

    def summary(self):
        return "Shows an home page with a list of projects"

    def description(self):
        return "Shows an home page with a list of projects"

    def linkTitle(self):
        return "Shows an home page with a list of projects"

    def linkType(self):
        return QgsServerOgcApi.items

    def handleRequest(self, context):
        """List projects"""

        html_metadata = {
            "pageTitle": "QGIS Server Home Page",
            "navigation": []
        }

        projects_data = []
        for project_id, project_identifier in projects().items():
            data = project_info(project_identifier)
            data['id'] = project_id
            projects_data.append(data)

        self.write({
                'links': [],
                'projects': projects_data
            },
            context,
            html_metadata)

    def templatePath(self, context):
        return os.path.join(os.path.dirname(__file__), 'templates', 'landingpage.html')

    def parameters(self, context):
        return []


class MapApiHandler(QgsServerOgcApiHandler):
    """Project map handler"""

    project_id_re = re.compile(r'/map/([a-f0-9]{32})')

    def __init__(self):
        super().__init__()
        self.setContentTypes([QgsServerOgcApi.HTML, QgsServerOgcApi.JSON])

    def path(self):
        return QRegularExpression("/map/[a-z0-9]{32}.*")

    def operationId(self):
        return "Map Browser API"

    def summary(self):
        return "Shows a map for a given project"

    def description(self):
        return self.summary()

    def linkTitle(self):
        return self.summary()

    def linkType(self):
        return QgsServerOgcApi.items

    def handleRequest(self, context):
        """Makes the map"""

        html_metadata = {
            "pageTitle": "QGIS Server Project Map",
            "navigation": [] # TODO
        }

        project_identifier = self.project_id_re.findall(context.request().url().toString())[0]
        # TODO: cache this thing!
        project_data = project_info(projects()[project_identifier])

        self.write({
                'links': [],
                'project': project_data
            },
            context,
            html_metadata)

    def templatePath(self, context):
        return os.path.join(os.path.dirname(__file__), 'templates', 'map.html')

    def parameters(self, context):
        return []


class StaticApiHandler(QgsServerOgcApiHandler):
    """Static files handler"""

    def __init__(self):
        super().__init__()
        self.setContentTypes([QgsServerOgcApi.HTML, QgsServerOgcApi.JSON])

    def path(self):
        return QRegularExpression("/static/.*")

    def operationId(self):
        return "Static handler"

    def summary(self):
        return "Serve static files"

    def description(self):
        return self.summary()

    def linkTitle(self):
        return self.summary()

    def linkType(self):
        return QgsServerOgcApi.JSON

    def handleRequest(self, context):
        """Serve static files from 'static' directory"""

        path = os.path.join(os.path.dirname(__file__), context.request().url().path()[1:])
        if not os.path.exists(path):
            raise Exception('Not found!')

        with open(path, 'rb') as f:
            content = f.read()
            size = len(content)

        mimeType = QMimeDatabase().mimeTypeForFile( path )
        context.response().setHeader("Content-Type", mimeType.name())
        context.response().setHeader("Content-Length", str(size))
        context.response().write(content)

    def parameters(self, context):
        return []

