# coding=utf-8
""""Utilities for Landing Page plugin

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

"""

__author__ = 'elpaso@itopen.it'
__date__ = '2020-04-28'
__copyright__ = 'Copyright 2020, ItOpen'

import os
import hashlib

from qgis.server import (
    QgsServerProjectUtils,
)

from qgis.PyQt.QtCore import Qt

from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
)

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


def get_toc(project, restricted_wms):

    def _harvest(node):
        rec = {
            'name': node.name(),
            'expanded': node.isExpanded(),
            'visible': node.isVisible(),
        }
        try:
            rec['layer_id'] = node.layerId()
            rec['is_layer'] = True
        except AttributeError:
            rec['is_layer'] = False
        children = []
        for cn in node.children():
            c = _harvest(cn)
            if c['is_layer'] and c['name'] not in restricted_wms:
                children.append(c)
        rec['children'] = children
        return rec

    return _harvest(project.layerTreeRoot())

def project_wms(project, crs):
    """Calculate the extent from WMS advertized (if defined) or from
        WMS published layers.

    :param project: [description]
    :type project: [type]
    :returns: a tuple with WMS extent and list of published WMS typenames
    :rtype: tuple
    """

    wms_typenames = []
    extent = ''

    restricted_wms = QgsServerProjectUtils.wmsRestrictedLayers(project)
    use_ids = QgsServerProjectUtils.wmsUseLayerIds(project)

    for l in project.mapLayers().values():
        if l.name() not in restricted_wms:
            lid = l.id() if use_ids else l.name()
            wms_typenames.append(lid)

    extent = QgsServerProjectUtils.wmsExtent(project)
    if extent.isNull():
        target_crs = QgsCoordinateReferenceSystem.fromEpsgId(int(crs.split(':')[1]))
        for l in project.mapLayers().values():
            if l.name() not in restricted_wms:
                l_extent = l.extent()
                if l.crs() != target_crs:
                    ct = QgsCoordinateTransform(l.crs(), target_crs, project.transformContext())
                    l_extent = ct.transform(l_extent)
                extent.combineExtentWith(l_extent)
    else:
        if crs != project.crs().authid():
            target_crs = QgsCoordinateReferenceSystem.fromEpsgId(int(crs.split(':')[1]))
            ct = QgsCoordinateTransform(project.crs(), target_crs, project.transformContext())
            extent = ct.transform(extent)

    return extent, wms_typenames


def _read_links(metadata):
    links = []
    for l in metadata.links():
        links.append({
            'name': l.name,
            'description': l.description,
            'url': l.url,
            'size': l.size,
            'mimeType': l.mimeType,
        })
    return links

def _read_constraints(metadata):
    constraints = []
    for l in metadata.constraints():
        constraints.append({
            'constraint': l.constraint,
            'type': l.type,
        })
    return constraints


def _read_contacts(metadata):
    contacts = []
    for c in metadata.contacts():
        contacts.append({
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
    return contacts

def layer_info(layer):
    """Extracts layer information from the layer object"""

    info = {
        'name': layer.name(),
        'id': layer.id(),
        'crs': layer.crs().authid(),
    }
    extent = layer.extent()
    info['extent'] = [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]

    ####################################################
    # Metadata section
    m = layer.metadata()
    metadata = {}
    for prop in (
        'abstract',
        'categories',
        'contacts',
        'encoding',
        'fees',
        'history',
        'identifier',
        'keywordVocabularies',
        'keywords',
        'language',
        'licenses',
        'links',
        'parentIdentifier',
        'rights',
        'title',
        'type',
    ):
        metadata[prop] = getattr(m, prop)()

    # links array
    metadata['links'] = _read_links(m)
    # contacts array
    metadata['contacts'] = _read_contacts(m)
    # constraints array
    metadata['constraints'] = _read_constraints(m)
    metadata['crs'] = m.crs().authid()
    info['metadata'] = metadata

    return info

def project_info(project_path):
    """Extracts project information and returns it as a dictionary"""

    info = {}
    p = QgsProject()
    if p.read(project_path):

        ####################################################
        # Main section

        info['title'] = p.metadata().title()
        if not info['title']:
            info['title'] = QgsServerProjectUtils.owsServiceTitle(p)
        if not info['title']:
            info['title'] = p.title()

        info['description'] = p.metadata().abstract()
        if not info['description']:
            info['description'] = QgsServerProjectUtils.owsServiceAbstract(p)

        # Extent, CRS and published WMS layers typenames
        wmsOutputCrsList = QgsServerProjectUtils.wmsOutputCrsList(p)
        info['crs'] = 'EPSG:4326' if 'EPSG:4326' in wmsOutputCrsList else wmsOutputCrsList[0]
        extent, info['wms_layers'] = project_wms(p, info['crs'])
        info['extent'] = [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]
        geographic_extent = extent
        if info['crs'] != 'EPSG:4326':
            extent_crs = QgsCoordinateReferenceSystem.fromEpsgId(int(info['crs'].split(':')[1]))
            ct = QgsCoordinateTransform(extent_crs, QgsCoordinateReferenceSystem.fromEpsgId(4326), p.transformContext())
            geographic_extent = ct.transform(info['geographic_extent'])
        info['geographic_extent'] = [geographic_extent.xMinimum(), geographic_extent.yMinimum(), geographic_extent.xMaximum(), geographic_extent.yMaximum()]

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
        metadata['links'] = _read_links(m)
        # contacts array
        metadata['contacts'] = _read_contacts(m)
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

        info['capabilities'] = capabilities

        ####################################################
        # WMS Layers section

        info['wms_root_name'] = capabilities['wmsRootName'] if capabilities['wmsRootName'] else p.name()
        restricted_wms = capabilities['wmsRestrictedLayers']
        wms_layers = {}
        wms_layers_map = {}
        use_ids = capabilities['wmsUseLayerIds']

        for l in p.mapLayers().values():
            if l.name() not in restricted_wms:
                wms_layers[l.id()] = layer_info(l)
                wms_layers_map[l.displayName()] = l.id() if use_ids else l.displayName()

        info['wms_layers'] = wms_layers
        info['wms_layers_map'] = wms_layers_map

        ####################################################
        # WFS Layers section TODO

        ####################################################
        # TOC tree
        info['toc'] = get_toc(p, restricted_wms)

    return info
