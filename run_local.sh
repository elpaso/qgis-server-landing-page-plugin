QGIS_PLUGINPATH=plugins \
    QGIS_SERVER_DISABLED_APIS="Landing Page" \
    QGIS_SERVER_IGNORE_BAD_LAYERS=1 \
    QGIS_SERVER_LANDING_PAGE_PROJECTS_DIRECTORIES="plugins/landingpage/tests/projects2" \
    QGIS_SERVER_LANDING_PAGE_PROJECTS_PG_CONNECTIONS="postgresql://localhost:5432?sslmode=disable&dbname=landing_page_test&schema=public" \
    QGIS_SERVER_LANDINGPAGE_DEBUG=1 \
    qgis_mapserver -l 0 0.0.0.0:8001