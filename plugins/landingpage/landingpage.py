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

from qgis.PyQt.QtCore import QBuffer, QIODevice, QTextStream, QRegularExpression
from qgis.server import (
    QgsServiceRegistry,
    QgsService,
    QgsServerOgcApi,
    QgsServerOgcApiHandler,
    QgsServerProjectUtils,
    QgsServerFilter,
)

from qgis.core import (
    QgsProject, QgsMessageLog
)

from qgis.PyQt.QtCore import Qt


def projects():
    """Returns a list of available projects

    :return: hash of project paths (or other storage identifiers) with a digest key
    :rtype: dict
    """
    projects = {}
    if not os.environ.get('QGIS_SERVER_PROJECTS_DIRECTORY', False):
        return projects

    for f in os.listdir(os.environ.get('QGIS_SERVER_PROJECTS_DIRECTORY')):
        if f.upper().endswith('.QGS') or f.upper().endswith('.QGZ'):
            project_key = hashlib.md5(f.encode('utf8')).hexdigest()
            projects[project_key] = os.path.join(os.environ.get('QGIS_SERVER_PROJECTS_DIRECTORY'), f)

    return projects

def project_info(project_path):
    """Extract project information and returns it as a dictionary"""

    info = {}
    p = QgsProject()
    if p.read(project_path):

        ####################################################
        # Main section

        info['title'] = p.title()


        ####################################################
        # Metadata section
        m = p.metadata()
        metadata = {}
        for prop in (
            'title',
            'identifier',
            'parentIdentifier',
            'abstract',
            'author',
            'language',
            'categories',
            'history',
            'type',
        ):
            metadata[prop] = getattr(m, prop)()
        # links array
        metadata['links'] = []
        for l in m.links():
            metadata['links'].append({
                'name': l.name,
                'description': l.description,
                'url': l.url,
                'size': l.size,
                'mimeType': l.mimeType,
            })
        # contacts array
        metadata['contacts'] = []
        for c in m.contacts():
            metadata['contacts'].append({
                'name': c.name,
                'role': c.role,
                'email': c.email,
                'fax': c.fax,
                'voice': c.voice,
                'organization': c.organization,
                'position': c.position,
                'addresses': [{
                    'address': a.address,
                    'city': a.city,
                    'country': a.country,
                    'postalCode': a.postalCode,
                    'type': a.type,
                    'administrativeArea': a.administrativeArea,
                } for a in c.addresses],
            })

        metadata['creationDateTime'] = m.creationDateTime().toString(Qt.ISODate)
        info['metadata'] = metadata

        ####################################################
        # WMS Service Capabilities section

        capabilities = {}
        for c in (
            'owsServiceAbstract',
            'owsServiceAccessConstraints',
            'owsServiceCapabilities',
            'owsServiceContactMail',
            'owsServiceContactOrganization',
            'owsServiceContactPerson',
            'owsServiceContactPhone',
            'owsServiceContactPosition',
            'owsServiceFees',
            'owsServiceKeywords',
            'owsServiceOnlineResource',
            'owsServiceTitle',
            'wcsLayerIds',
            'wcsServiceUrl',
            'wfsLayerIds',
            'wfsServiceUrl',
            'wfstDeleteLayerIds',
            'wfstInsertLayerIds',
            'wfstUpdateLayerIds',
            'wmsDefaultMapUnitsPerMm',
            'wmsExtent',
            'wmsFeatureInfoAddWktGeometry',
            'wmsFeatureInfoDocumentElement',
            'wmsFeatureInfoDocumentElementNs',
            'wmsFeatureInfoLayerAliasMap',
            'wmsFeatureInfoPrecision',
            'wmsFeatureInfoSchema',
            'wmsFeatureInfoSegmentizeWktGeometry',
            'wmsImageQuality',
            'wmsInfoFormatSia2045',
            'wmsInspireActivate',
            'wmsInspireLanguage',
            'wmsInspireMetadataDate',
            'wmsInspireMetadataUrl',
            'wmsInspireMetadataUrlType',
            'wmsInspireTemporalReference',
            'wmsMaxAtlasFeatures',
            'wmsMaxHeight',
            'wmsMaxWidth',
            'wmsOutputCrsList',
            'wmsRestrictedComposers',
            'wmsRestrictedLayers',
            'wmsRootName',
            'wmsServiceUrl',
            'wmsTileBuffer',
            'wmsUseLayerIds',
            'wmtsServiceUrl'
        ):
            capabilities[c] = getattr(QgsServerProjectUtils, c)(p)

        ####################################################
        # WFS Layers section TODO
        # WMS Layers section TODO

        info['capabilities'] = capabilities

    return info


class LandingPageApiHandler(QgsServerOgcApiHandler):
    """Project listing handler"""

    def __init__(self):
        super().__init__()
        self.setContentTypes([QgsServerOgcApi.HTML])

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
        return os.path.join(os.path.dirname(__file__), 'landingpage.html')

    def parameters(self, context):
        return []


class LandingPageApi(QgsServerOgcApi):
    """Overrides accept to only trigger on /"""

    def accept(self, url):
        return url.path() == '/' or url.path() == ''


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
        self.handler = LandingPageApiHandler()
        self.api.registerHandler(self.handler)
        serverIface.serviceRegistry().registerApi(self.api)
        self.loader_filter = ProjectLoaderFilter(serverIface)
        serverIface.registerFilter( self.loader_filter, 1)

