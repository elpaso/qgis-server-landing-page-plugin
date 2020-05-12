<template>
  <v-app id="catalog">
    <v-app-bar app dense hide-on-scroll color="green" dark>
      <v-toolbar-title>QGIS Server Catalog</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-content>
      <v-container id="catalog" class="fill-height" fluid>
        <b-alert :show="error.length > 0" dismissible variant="danger">{{ error }}</b-alert>
        <template div v-if="status == `loading`">
          <div class="row">
            <div class="col-sm-2">
              <b-spinner
                variant="info"
                style="width: 3rem; height: 3rem; text-align:center;"
                label="Large Spinner"
                type="grow"
              ></b-spinner>
            </div>
            <div class="col-sm-10">
              <h4 class="loading">Loading...</h4>
            </div>
          </div>
        </template>

        <b-jumbotron
          header="QGIS Server Projects Catalog"
          v-else-if="status == `empty`"
          lead="The catalog is empty"
        >
          <p>This QGIS Server catalog does not contain any project.</p>
        </b-jumbotron>
        <template v-else>
          <v-card
            class="mx-auto mb-4"
            max-width="800"
            min-width="400"
            :key="project.identifier"
            v-for="project in projects"
          >
            <l-map :ref="'mapid-'+project.id" @ready="loadMap(project, $event)">
              <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                v-if="project.capabilities.wmsOutputCrsList.includes('EPSG:3857')"
              ></l-tile-layer>
            </l-map>
            <v-card-title>{{ project.title }}</v-card-title>
            <v-card-subtitle
              class="description"
              v-if="project.description"
            >{{ project.description }}</v-card-subtitle>

            <v-card-actions>
              <v-btn color="orange" @click="project.show = !project.show" text>
                <v-icon>{{ project.show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>Metadata
              </v-btn>
              <v-btn
                color="orange"
                text
                :to="{ name: 'map', params: { projectId: project.id }}"
              >Browse</v-btn>
            </v-card-actions>
            <v-expand-transition>
              <div v-show="project.show">
                <v-divider></v-divider>
                <v-card-text>
                  <Metadata :project="project" />
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>
        </template>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { LMap, LTileLayer } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import { latLng, Polygon } from "leaflet";
import WMS from "leaflet-wms/leaflet.wms.js";
import Metadata from "@/components/Metadata.vue";

export default {
  name: "Catalog",
  components: {
    LMap,
    LTileLayer,
    Metadata
  },
  data() {
    return {
      projects: [],
      status: `loading`, // [loading,projects,empty]
      error: ``
    };
  },
  mounted() {
    fetch(`/index.json`)
      .then(this.handleErrors)
      .then(response => response.json())
      .then(json => {
        json.projects.forEach(element => {
          element.show = false;
        });
        this.projects = json.projects;
        this.status = this.projects.length ? `projects` : `empty`;
      })
      .catch(error => {
        this.error = error.message;
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
      WMS.overlay(`/project/${project.id}/?`, {
        layers: project.wms_root_name,
        transparent: true,
        format: "image/png"
      }).addTo(map);
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

h4.loading {
  margin-top: 0.35em;
}
</style>