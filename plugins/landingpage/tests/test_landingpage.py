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
import hashlib
from qgis.core import QgsApplication
from qgis.server import QgsServer, QgsBufferServerRequest, QgsBufferServerResponse
from qgis.testing import TestCase, unittest
from landingpage.landingpage import LandingPageApi, projects, project_info

os.environ['QGIS_SERVER_PROJECTS_DIRECTORY'] = os.path.join(os.path.dirname(__file__), 'projects')

class TestLandingPage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QgsApplication([], False)
        cls.server = QgsServer()
        cls.api = LandingPageApi(cls.server.serverInterface())

    @classmethod
    def tearDownClass(cls):
        cls.app.exitQgis()

    def test_projects(self):
        _projects = '|'.join(projects())
        self.assertTrue(hashlib.md5('Project1.qgs'.encode('utf8')).hexdigest() in _projects)
        self.assertTrue(hashlib.md5('Project2.qgz'.encode('utf8')).hexdigest() in _projects)

    def test_project_info(self):
        path = sorted(projects().values())[0]
        info = project_info(path)
        self.assertEqual(info['title'], 'Project2 Title')

    def test_landing_page(self):
        request = QgsBufferServerRequest('/')
        response = QgsBufferServerResponse()
        self.server.handleRequest(request, response)
        self.assertTrue(b'html' in bytes(response.body()), response.body())
        self.assertEqual(response.statusCode(), 200)


if __name__ == '__main__':
    unittest.main()
