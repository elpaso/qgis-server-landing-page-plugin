# coding=utf-8
""""Test for landing page plugin

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Note: QGIS_SERVER_LANDING_PAGE_PG_TEST defines a PG connection to be used for
          testing projects stored in the database. For example (default value):
          "host=localhost port=5432"
          The test database name is landing_page_test, it will be dropped and recreated
          on each test run.

"""

__author__ = 'elpaso@itopen.it'
__date__ = '2020-04-24'
__copyright__ = 'Copyright 2020, ItOpen'

import os
import re
import hashlib
from qgis.core import QgsApplication, QgsProject
from qgis.server import QgsServer, QgsBufferServerRequest, QgsBufferServerResponse
from qgis.testing import TestCase, unittest, start_app
from landingpage.landingpage import LandingPageApiLoader
from landingpage.utils import (
    projects,
    project_info,
    project_wms,
    layer_info,
    get_toc,
)

from qgis.server import (
    QgsServerProjectUtils,
)
from qgis.core import QgsProviderRegistry, QgsDataSourceUri

start_app()


class TestLandingPageFileSystemLoader(TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['QGIS_SERVER_PROJECTS_DIRECTORIES'] = os.path.join(os.path.dirname(
            __file__), 'projects') + '||' + os.path.join(os.path.dirname(__file__), 'projects2')
        os.environ['QGIS_SERVER_PROJECTS_PG_CONNECTIONS'] = os.path.join(os.path.dirname(
            __file__), 'projects') + '||' + os.path.join(os.path.dirname(__file__), 'projects2')
        cls.server = QgsServer()
        cls.api = LandingPageApiLoader(cls.server.serverInterface())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_projects(self):
        _projects = '|'.join(projects())
        self.assertTrue(hashlib.md5(
            'Project1.qgs'.encode('utf8')).hexdigest() in _projects)
        self.assertTrue(hashlib.md5(
            'Project2.qgz'.encode('utf8')).hexdigest() in _projects)

    def test_project_info(self):
        path = sorted(projects().values())[1]
        info = project_info(path)
        self.assertEqual(info['title'], 'Project2 Title')
        self.assertEqual(info['toc']['children'][0]['name'], 'points_3857')
        self.assertEqual(len(info['toc']['children']), 1)

    def test_layer_info(self):
        p = QgsProject()
        p.read(list(projects().values())[1])
        info = layer_info(p.mapLayer(
            'points_842425df_7f45_4091_a6c9_086e1dc1edd1'))
        self.assertEqual(info['name'], 'points')
        self.assertEqual(
            info['id'], 'points_842425df_7f45_4091_a6c9_086e1dc1edd1')
        self.assertEqual(info['metadata']['categories'], [
                         'Geoscientific Information', 'Imagery Base Maps Earth Cover'])
        self.assertEqual(info['metadata']['contacts'][0], {'name': 'Layer Metadata Contact Name', 'role': 'distributor', 'email': 'Layer Metadata Contact Email', 'fax': 'Layer Metadata Contact Fax', 'voice': 'Layer Metadata Contact Voice',
                                                           'organization': 'Layer Metadata Contact Organization', 'position': 'Layer Metadata Contact Position', 'addresses': [{'address': 'street 1', 'city': 'Milan', 'country': 'Italy', 'postalCode': '10021', 'type': 'postal', 'administrativeArea': 'Lombardy'}]})
        self.assertEqual(info['fields'], {'fid': {'type': 'Integer64',
                                                  'label': 'fid',
                                                  'precision': 0,
                                                  'length': 0,
                                                  'not_null': True,
                                                  'unique': True,
                                                  'has_expression': False,
                                                  'default': 'Autogenerate',
                                                  'expression': '',
                                                  'editable': False},
                                          'name': {'type': 'String',
                                                   'label': 'name',
                                                   'precision': 0,
                                                   'length': 0,
                                                   'not_null': False,
                                                   'unique': False,
                                                   'has_expression': False,
                                                   'default': '',
                                                   'expression': '',
                                                   'editable': True}})

    def test_project_wms(self):
        p0 = QgsProject()
        p0.read(sorted(list(projects().values()))[0])
        p1 = QgsProject()
        p1.read(sorted(list(projects().values()))[1])

        # Check that project3 from second directory is in the list
        self.assertTrue(
            'projects2/project3.qgz' in '||'.join(list(projects().values())))

        # p0 is not restricted and does not use layer ids
        extent, layers = project_wms(p0, 'EPSG:4326')
        self.assertEqual(layers, ['points'])
        # Extent is WMS advertized
        self.assertEqual(re.sub(r'(\.\d{2})\d+', r'\1', extent.asWktPolygon(
        )), 'POLYGON((-1.12 43.23, 11.12 43.23, 11.12 52.26, -1.12 52.26, -1.12 43.23))')

        # p1 is restricted and does use layer ids
        extent, layers = project_wms(p1, 'EPSG:4326')
        self.assertEqual(
            layers, ['points_3857_6c1395a0_1065_41f7_9cf4_8109e268ac84'])
        # Extent is from the only published layer
        self.assertEqual(re.sub(r'(\.\d{2})\d+', r'\1', extent.asWktPolygon(
        )), 'POLYGON((-25.49 41.98, 38.23 41.98, 38.23 55.95, -25.49 55.95, -25.49 41.98))')

    def test_landing_page(self):
        request = QgsBufferServerRequest('/')
        response = QgsBufferServerResponse()
        self.server.handleRequest(request, response)
        self.assertTrue(b'html' in bytes(response.body()), response.body())
        self.assertEqual(response.statusCode(), 200)

    def test_get_toc(self):
        p = QgsProject()
        path = os.path.join(os.path.dirname(__file__), 'projects',
                            'test_project_wms_grouped_nested_layers.qgs')
        info = project_info(path)
        toc = info['toc']
        self.assertTrue('osm' in [l['title'] for l in toc['children']])
        osm = toc['children'][-1]
        self.assertEqual(osm['layer_type'], 'raster')
        self.assertEqual(osm['tree_id'], 'root.osm')
        boundaries = toc['children'][0]
        cdb_lines = boundaries['children'][0]
        self.assertTrue(cdb_lines['typename'], 'CDB_Lines_Server_Short_Name')
        self.assertTrue(cdb_lines['title'], 'CDB Lines Server Title')
        self.assertTrue(cdb_lines['name'], 'CDB Lines')


class TestLandingPagePostgresLoader(TestCase):

    @classmethod
    def setUpClass(cls):
        # Make sure there are no other loaders
        del os.environ['QGIS_SERVER_PROJECTS_DIRECTORIES']
        cls.pg_conn = os.environ.get('QGIS_SERVER_LANDING_PAGE_PG_TEST', False)
        if not cls.pg_conn:  # default
            cls.pg_conn = "host=localhost port=5432 schema=public"

        # Use QGIS API to create the test data
        md = QgsProviderRegistry.instance().providerMetadata('postgres')
        conn = md.createConnection(cls.pg_conn, {})
        conn.executeSql('DROP DATABASE landing_page_test')
        conn.executeSql('CREATE DATABASE landing_page_test')

        # Add DB to conn string
        cls.pg_conn = "dbname=landing_page_test " + cls.pg_conn
        conn = md.createConnection(cls.pg_conn, {})
        conn.executeSql(open(os.path.join(os.path.dirname(
            __file__), 'landing_page_test.sql'), 'rt').read())

        uri = QgsDataSourceUri(cls.pg_conn)
        cls.pg_storage_conn = "postgresql://{host}:{port}?sslmode=disable&dbname=landing_page_test&schema=public".format(
            host=uri.host(), port=uri.port())
        os.environ['QGIS_SERVER_PROJECTS_PG_CONNECTIONS'] = cls.pg_storage_conn
        cls.server = QgsServer()
        cls.api = LandingPageApiLoader(cls.server.serverInterface())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_projects(self):
        _projects = '|'.join(projects().values())
        self.assertTrue('PGProject1' in _projects)
        self.assertTrue('PGProject2' in _projects)
        self.assertTrue('my as areas project' in _projects)

    def test_project_extent(self):
        p = QgsProject()
        p.read(sorted(list(projects().values()))[2])
        self.assertTrue(QgsServerProjectUtils.wmsExtent(p).isNull())
        info = project_info(sorted(list(projects().values()))[2])
        self.assertEqual(re.sub(
            r'(\.\d{2})\d+', r'\1', str(info['geographic_extent'])), '[10.68, 52.41, 10.74, 52.45]')


if __name__ == '__main__':
    unittest.main()
