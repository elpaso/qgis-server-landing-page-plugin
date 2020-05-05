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
    QgsMapLayerType,
    QgsLegendRenderer,
    QgsRenderContext,
    QgsLegendModel,
    QgsLegendSettings,
    QgsProviderRegistry,
    QgsApplication,
    QgsDataSourceUri,
)

def projects():
    """Returns a list of available projects from various sources:

    - QGIS_SERVER_PROJECTS_DIRECTORIES directories
    - QGIS_SERVER_PROJECTS_PG_CONNECTIONS postgres connections

    :return: hash of project paths (or other storage identifiers) with a digest key
    :rtype: dict
    """
    projects = {}

    if os.environ.get('QGIS_SERVER_PROJECTS_DIRECTORIES', False):
        for directory in os.environ.get('QGIS_SERVER_PROJECTS_DIRECTORIES').split('||'):
            for f in os.listdir(directory):
                if f.upper().endswith('.QGS') or f.upper().endswith('.QGZ'):
                    project_key = hashlib.md5(f.encode('utf8')).hexdigest()
                    projects[project_key] = os.path.join(directory, f)

    if os.environ.get('QGIS_SERVER_PROJECTS_PG_CONNECTIONS', False):
        md = QgsProviderRegistry.instance().providerMetadata('postgres')
        for pg_connection in os.environ.get('QGIS_SERVER_PROJECTS_PG_CONNECTIONS').split('||'):
            conn = md.createConnection(pg_connection, {})
            # List projects
            app = QgsApplication.instance()
            reg = app.projectStorageRegistry()
            assert reg.projectStorages() != []
            storage = reg.projectStorageFromType('postgresql')
            uri = QgsDataSourceUri(pg_connection)
            for project in storage.listProjects(pg_connection):
                project_key = hashlib.md5((project + pg_connection).encode('utf8')).hexdigest()
                projects[project_key] = pg_connection + "&project=" + project

    return projects


def get_toc(project):
    """Get the WMS TOC information for the project"""

    use_ids = QgsServerProjectUtils.wmsUseLayerIds(project)
    wmsRestrictedLayers = QgsServerProjectUtils.wmsRestrictedLayers(project)

    def _harvest(node, parent_id=None):
        node_name = node.name() if parent_id is not None else 'root'
        rec = {
            'title': node_name,  # Override with title for layers
            'name': node_name,
            'expanded': node.isExpanded(),
            'visible': node.isVisible(),
        }
        try:
            rec['id'] = node.layerId()
            short_name = node.layer().shortName() if node.layer().shortName() else node.layer().name()
            rec['typename'] = node.layer().id() if use_ids else short_name
            # Override title
            if node.layer().title():
                rec['title'] = node.layer().title()
            if node.layer().type() not in (QgsMapLayerType.VectorLayer, QgsMapLayerType.RasterLayer):
                raise Exception
            rec['layer_type'] = 'vector' if node.layer().type() == QgsMapLayerType.VectorLayer else 'raster'
            rec['has_scale_based_visibility'] = node.layer().hasScaleBasedVisibility()
            if rec['has_scale_based_visibility']:
                rec['min_scale'] = node.layer().minimumScale()
                rec['max_scale'] = node.layer().maximumScale()
            rec['is_layer'] = True
        except AttributeError:
            rec['is_layer'] = False

        rec['tree_id'] = ( parent_id + '.' + rec['title'] ) if parent_id is not None else 'root'
        rec['tree_id_hash'] = hashlib.md5(rec['tree_id'].encode('utf8')).hexdigest()

        children = []
        for cn in [n for n in node.children() if n.name() not in wmsRestrictedLayers]:
            try:
                children.append(_harvest(cn, rec['tree_id']))
            except:
                pass

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
        if not info['title']:
            info['title'] = p.baseName()

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

        info['wms_root_name'] = capabilities['wmsRootName'] if capabilities['wmsRootName'] else p.title()
        restricted_wms = capabilities['wmsRestrictedLayers']
        wms_layers = {}
        use_ids = capabilities['wmsUseLayerIds']
        # Map layer title to layer name (or id if use_ids)
        wms_layers_map = {}

        for l in p.mapLayers().values():
            if l.name() not in restricted_wms:
                wms_layers[l.id()] = layer_info(l)
                name = l.title() if l.title() else l.name()
                short_name = l.shortName() if l.shortName() else l.name()
                wms_layers_map[name] = l.id() if use_ids else short_name

        info['wms_layers'] = wms_layers
        info['wms_layers_map'] = wms_layers_map

        ####################################################
        # TOC tree (WMS published only)
        info['toc'] = get_toc(p)

    return info
