<template>
  <v-app id="project">
    <v-app-bar app dense collapse-on-scroll clipped-left color="green" dark v-if="project">
      <v-app-bar-nav-icon @click.stop="expandedToc = !expandedToc"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ project.title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon title="Home Page" to="/">
        <v-icon>mdi-home-circle</v-icon>
      </v-btn>
    </v-app-bar>
    <LayerTree
      :project="project"
      :drawer="expandedToc"
      v-on:setLayerVisibility="setLayerVisibility"
    />
    <v-content>
      <v-container id="map" class="fill-height" fluid>
        <!--v-alert :show="error.length > 0" dismissible variant="danger">{{ error }}</v-alert-->
        <v-layout>
          <l-map ref="map" v-resize="onResize" @ready="setMap" style="z-index: 0;">
            <l-tile-layer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              v-if="project && project.capabilities.wmsOutputCrsList.includes('EPSG:3857')"
            ></l-tile-layer>
          </l-map>
        </v-layout>
      </v-container>
    </v-content>
    <MapToolbar class="map-toolbar" :map="map" />
  </v-app>
</template>

<script>
import LayerTree from "@/components/LayerTree.vue";
import MapToolbar from "@/components/MapToolbar.vue";
import { LMap, LTileLayer } from "vue2-leaflet";
import WmsSource from "@/js/WmsSource.js";
import "leaflet/dist/leaflet.css";
import { latLng, Polygon } from "leaflet";
import L from "leaflet";

L.Control.include({
  _refocusOnMap: L.Util.falseFn // Do nothing.
});

export default {
  name: "WebGis",
  props: { projectId: String },
  components: {
    LayerTree,
    LMap,
    LTileLayer,
    MapToolbar
  },
  data: function() {
    return {
      map: {},
      wms_source: {},
      expandedToc: false
    };
  },
  computed: {
    project() {
      return this.$store.state.projects[this.projectId];
    },
    status() {
      return this.$store.state.status;
    },
    error() {
      let error = this.$store.state.error;
      this.$store.dispatch("clearError");
      return error;
    }
  },
  watch: {
    project() {
      this.initializeMap();
    }
  },
  mounted() {
    this.$store.dispatch("setStatus", `loading`);

    if (!this.project) {
      this.$store.dispatch("getProject", this.projectId);
    } else {
      console.log("Project already loaded ...");
      this.initializeMap();
    }
  },
  methods: {
    setMap() {
      this.map = this.$refs["map"].mapObject;
    },
    /**
     * Called when project has been fetched
     */
    initializeMap() {
      console.log(`Watched project changed ${this.project.id}`);
      this.loadMap(this.project);
      Object.keys(this.project.wms_layers_map)
        .reverse()
        .forEach(title => {
          let node = this.findLayerNode(title, this.project.toc.children);
          if (node && node.visible) {
            console.log(`Loading layer ${title}`);
            this.wms_source._subLayers[
              node.typename
            ] = this.wms_source.getLayer(node.typename);
          } else if (!node) {
            console.log(`Could not find layer node: ${title}`);
          } else if (!node.visible) {
            console.log(`Not loading layer (not visible): ${title}`);
          }
        });
      this.wms_source.refreshOverlay();
      let layers = this.project.wms_root_name;
      if (!layers) {
        let _layers = [];
        Object.values(this.project.wms_layers_map).forEach(layer_id =>
          _layers.push(layer_id)
        );
        layers = _layers.join(`,`);
      }
      let toc_url = `/project/${this.project.id}/?SERVICE=WMS&REQUEST=GetLegendGraphics&LAYERS=${layers}&FORMAT=application/json`;
      fetch(toc_url)
        .then(this.handleErrors)
        .then(response => response.json())
        .then(json => {
          json.nodes.forEach(layer => {
            let node = this.findLayerNode(
              layer.title,
              this.project.toc.children
            );
            if (node) {
              if (layer.icon) {
                node.children.push(layer);
              } else {
                layer.symbols.forEach(symbol => node.children.push(symbol));
              }
            }
          });
        })
        .catch(error => {
          //this.error = error.message;
          console.log(error);
        });
      this.$nextTick(() => {
        this.map.zoomControl.remove();
      });
    },
    onResize() {
      if (this.map) {
        this.map._onResize();
      }
    },
    /**
     * Toggles a layer by typename
     */
    setLayerVisibility(typename, visible) {
      if (typename in this.wms_source._subLayers && !visible) {
        console.log(`Removing layer: ${typename}`);
        this.wms_source.removeSubLayer(typename);
      } else if (visible && !(typename in this.wms_source._subLayers)) {
        // We need to respect drawing order!
        this.wms_source._subLayers[typename] = this.wms_source.getLayer(
          typename
        );
        let new_sub_layers = {};
        for (const _type_name of Object.values(
          this.project.wms_layers_map
        ).reverse()) {
          //let _type_name = this.project.wms_layers_map[title];
          if (_type_name in this.wms_source._subLayers) {
            console.log(`Adding layer: ${typename}`);
            new_sub_layers[_type_name] = this.wms_source._subLayers[_type_name];
          }
        }
        this.wms_source._subLayers = new_sub_layers;
        this.wms_source.refreshOverlay();
      } else {
        console.log(`Nothing to do for: ${typename} - ${visible}`);
      }
    },
    /**
     * Find a layer by title
     */
    findLayerNode(title, children) {
      if (children) {
        for (let i = 0; i < children.length; ++i) {
          if (children[i].title == title) {
            return children[i];
          }
          let res = this.findLayerNode(title, children[i].children);
          if (res) {
            return res;
          }
        }
      }
    },
    /**
     * Handles ajax errors
     */
    handleErrors(response) {
      if (!response) {
        throw Error(`Error fetching data from QGIS Server`);
      }
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response;
    },
    /**
     * Loads map
     */
    loadMap(project) {
      let west = project.geographic_extent[0];
      let south = project.geographic_extent[1];
      let east = project.geographic_extent[2];
      let north = project.geographic_extent[3];
      let p1 = new latLng(south, west);
      let p2 = new latLng(north, west);
      let p3 = new latLng(north, east);
      let p4 = new latLng(south, east);
      let polygonPoints = [p1, p2, p3, p4];
      let jl = new Polygon(polygonPoints, { fill: false }); // Don't: .addTo(this.map);
      this.map.setView(jl.getBounds().getCenter());
      if (
        jl.getBounds().getEast() != jl.getBounds().getWest() &&
        jl.getBounds().getNorth() != jl.getBounds().getSouth()
      ) {
        this.map.fitBounds(jl.getBounds());
      }
      this.wms_source = WmsSource.source(`/project/` + project.id + `/?`, {
        tileSize: 512,
        transparent: true,
        format: "image/png",
        dpi: window.devicePixelRatio * 96
      }).addTo(this.map);
    }
  }
};
</script>

<style scoped>
#wrapper {
  height: 100%;
}

.alert-danger {
  position: absolute;
  top: 4em;
  margin: 0 8em;
  z-index: 10000;
}

#map {
  padding: 0;
}

.v-content {
  padding-bottom: 0 !important;
}

.map-toolbar {
  position: fixed;
  top: 90px;
  right: 30px;
}
</style>