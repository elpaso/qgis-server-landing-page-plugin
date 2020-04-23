
FROM ubuntu:18.04

RUN chmod 777 /tmp && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install wget gpg && \
    wget -O - https://qgis.org/downloads/qgis-2019.gpg.key | gpg --import && \
    gpg --export --armor 51F523511C7028C3 | apt-key add - && \
    echo 'deb http://qgis.org/ubuntu bionic main' > /etc/apt/sources.list.d/ubuntu-qgis.list

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y qgis-server xvfb && \
    apt-get clean

CMD ["/usr/bin/xvfb-run", "/usr/bin/qgis_mapserver", "${QGIS_SERVER_HOSTNAME_PORT}"]