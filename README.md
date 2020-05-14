# qgis-server-standalone-docker

QGIS Server Standalone Docker

## Sample .env file

```bash
DOCKER_SHARED_VOLUME=/home/dev/Dockers/qgis-server-standalone-docker/shared-volume
POSTGRES_DBNAME=geo
POSTGRES_USER=geo
POSTGRES_PASS=geo
# 2 is critical 3 is no logs
QGIS_SERVER_LOG_LEVEL=0
PUBLIC_HOSTNAME=test_qgis_server
PLUGINS_VOLUME=/home/dev/Dockers/qgis-server-standalone-docker/plugins
PUBLIC_PORT=8002
# Can be overridden, default to /usr/share/qgis/resources/server/api/
QGIS_SERVER_API_RESOURCES_DIRECTORY=/usr/share/qgis/resources/server/api/
# Landing page plugin (container paths, separated by || if more than one)
QGIS_SERVER_PROJECTS_DIRECTORIES=/plugins/landingpage/tests/projects||/plugins/landingpage/tests/projects2
```

`QGIS_SERVER_LANDINGPAGE_DEBUG` when activated will print all json information inside the templates.

## TODO

- PG PKI certs
- Map footer with CRS, scale etc. (zoom to predefined scale?)
- Metadata formatting
- Feature table (dependent onf WFW3 active)
- Relations and joins? (dependent onf WFW3 active)
- Searches
- BBOX selection
- map themese
- base maps switcher
- open QgsProject without loading layers
