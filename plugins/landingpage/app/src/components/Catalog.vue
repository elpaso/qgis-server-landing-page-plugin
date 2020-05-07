<template>
  <div id="catalog" class="container">
    <!-- TODO: empty -->
    <div class="mb-4" :key="project.identifier" v-for="project in projects">
      <b-card no-body header-tag="h2" :header="project.title">
        <b-card-body class="description" v-if="project.description">{{ project.description }}</b-card-body>
        <l-map :ref="'mapid-'+project.id" @ready="loadMap(project, $event)">
          <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            v-if="project.capabilities.wmsOutputCrsList.includes('EPSG:3857')"
          ></l-tile-layer>
        </l-map>
        <b-card-footer>
          <b-button variant="primary" v-b-toggle="'metadata-' + project.id" role="button">Metadata</b-button>
          <b-button
            variant="primary"
            role="button"
            :href="qgisUrl('/project/' + project.id + '/map/' + project.id)"
          >Map</b-button>
          <b-button
            variant="link"
            role="button"
            :href="qgisUrl('/project/' + project.id + '/wfs3')"
          >OAPIF/WFS3</b-button>
          <b-button
            variant="link"
            role="button"
            :href="qgisUrl('/project/' + project.id + '/?SERVICE=WFS&amp;REQUEST=GetCapabilities')"
          >WFS GetCapabilities</b-button>
          <b-button
            variant="link"
            role="button"
            :href="qgisUrl('/project/' + project.id + '/?SERVICE=WMS&amp;REQUEST=GetCapabilities')"
          >WMS GetCapabilities</b-button>
          <b-collapse :id="'metadata-' + project.id" class="mt-2">
            <Metadata :project="project" />
          </b-collapse>
        </b-card-footer>
      </b-card>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { LMap, LTileLayer } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import { latLng, Polygon } from "leaflet";
import WMS from "../../node_modules/leaflet-wms/leaflet.wms.js";
import Metadata from "./Metadata.vue";

export default {
  name: "Catalog",
  components: {
    LMap,
    LTileLayer,
    Metadata
  },
  data() {
    return { projects: [] };
  },
  mounted() {
    fetch(Vue.config.qgisUrl + `/index.json`)
      .then(response => response.json())
      .then(json => {
        this.projects = json.projects;
      });
  },
  methods: {
    loadMap(project, map) {
      let west = project.geographic_extent[0];
      let south = project.geographic_extent[1];
      let east = project.geographic_extent[2];
      let north = project.geographic_extent[3];
      let p1 = new latLng(south, west);
      let p2 = new latLng(north, west);
      let p3 = new latLng(north, east);
      let p4 = new latLng(south, east);
      let polygonPoints = [p1, p2, p3, p4];
      let jl = new Polygon(polygonPoints, { fill: false }).addTo(map);
      map.setView(jl.getBounds().getCenter());
      if (
        jl.getBounds().getEast() != jl.getBounds().getWest() &&
        jl.getBounds().getNorth() != jl.getBounds().getSouth()
      ) {
        map.fitBounds(jl.getBounds());
      }
      WMS.overlay(Vue.config.qgisUrl + "/project/" + project.id + "/?", {
        layers: project.wms_root_name,
        transparent: true,
        format: "image/png"
      }).addTo(map);
    },
    qgisUrl(url) {
      return Vue.config.qgisUrl + url;
    }
  }
};
</script>

<style scoped>
.leaflet-container {
  height: 20rem;
}
.card-footer .btn {
  margin-right: 0.5em;
}
</style>