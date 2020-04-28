# coding=utf-8
""""Test for landing page plugin

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

"""

__author__ = 'elpaso@itopen.it'
__date__ = '2020-04-24'
__copyright__ = 'Copyright 2020, ItOpen'

import os
import re
import hashlib
from qgis.core import QgsApplication, QgsProject
from qgis.server import QgsServer, QgsBufferServerRequest, QgsBufferServerResponse
from qgis.testing import TestCase, unittest
from landingpage.landingpage import LandingPageApiLoader
from landingpage.utils import projects, project_info, project_wms, layer_info

os.environ['QGIS_SERVER_PROJECTS_DIRECTORY'] = os.path.join(os.path.dirname(__file__), 'projects')

class TestLandingPage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QgsApplication([], False)
        cls.server = QgsServer()
        cls.api = LandingPageApiLoader(cls.server.serverInterface())

    @classmethod
    def tearDownClass(cls):
        cls.app.exitQgis()

    def test_projects(self):
        _projects = '|'.join(projects())
        self.assertTrue(hashlib.md5('Project1.qgs'.encode('utf8')).hexdigest() in _projects)
        self.assertTrue(hashlib.md5('Project2.qgz'.encode('utf8')).hexdigest() in _projects)

    def test_project_info(self):
        path = sorted(projects().values())[1]
        info = project_info(path)
        self.assertEqual(info['title'], 'Project2 Title')
        self.assertEqual(info['toc']['children'][0]['name'], 'points_3857')
        self.assertEqual(len(info['toc']['children']), 1)

    def test_layer_info(self):
        p = QgsProject()
        p.read(list(projects().values())[1])
        info = layer_info(p.mapLayer('points_842425df_7f45_4091_a6c9_086e1dc1edd1'))
        self.assertEqual(info['name'], 'points')
        self.assertEqual(info['id'], 'points_842425df_7f45_4091_a6c9_086e1dc1edd1')
        self.assertEqual(info['metadata']['categories'], ['Geoscientific Information', 'Imagery Base Maps Earth Cover'])
        self.assertEqual(info['metadata']['contacts'][0], {'name': 'Layer Metadata Contact Name', 'role': 'distributor', 'email': 'Layer Metadata Contact Email', 'fax': 'Layer Metadata Contact Fax', 'voice': 'Layer Metadata Contact Voice', 'organization': 'Layer Metadata Contact Organization', 'position': 'Layer Metadata Contact Position', 'addresses': [{'address': 'street 1', 'city': 'Milan', 'country': 'Italy', 'postalCode': '10021', 'type': 'postal', 'administrativeArea': 'Lombardy'}]})

    def test_project_wms(self):
        p0 = QgsProject()
        p0.read(list(projects().values())[0])
        p1 = QgsProject()
        p1.read(list(projects().values())[1])

        # p0 is restricted and does use layer ids
        extent, layers = project_wms(p0, 'EPSG:4326')
        self.assertEqual(layers, ['points_3857_6c1395a0_1065_41f7_9cf4_8109e268ac84'])
        # Extent is from the only published layer
        self.assertEqual(re.sub(r'(\.\d{2})\d+', r'\1', extent.asWktPolygon()), 'POLYGON((-25.49 41.98, 38.23 41.98, 38.23 55.95, -25.49 55.95, -25.49 41.98))')

        # p1 is not restricted and does not use layer ids
        extent, layers = project_wms(p1, 'EPSG:4326')
        self.assertEqual(layers, ['points'])
        # Extent is WMS advertized
        self.assertEqual(re.sub(r'(\.\d{2})\d+', r'\1', extent.asWktPolygon()), 'POLYGON((-1.12 43.23, 11.12 43.23, 11.12 52.26, -1.12 52.26, -1.12 43.23))')


    def test_landing_page(self):
        request = QgsBufferServerRequest('/')
        response = QgsBufferServerResponse()
        self.server.handleRequest(request, response)
        self.assertTrue(b'html' in bytes(response.body()), response.body())
        self.assertEqual(response.statusCode(), 200)


if __name__ == '__main__':
    unittest.main()
