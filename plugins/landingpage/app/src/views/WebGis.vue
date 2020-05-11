<template>
  <div class="wrapper">
    <b-alert :show="error.length > 0" dismissible variant="danger">{{ error }}</b-alert>
    <LayerTree :project="project" v-on:toggleLayer="toggleLayer" />
    <div id="map">
      <l-map @ready="setMap">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          v-if="project.capabilities && project.capabilities.wmsOutputCrsList.includes('EPSG:3857')"
        ></l-tile-layer>
      </l-map>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import LayerTree from "@/components/LayerTree.vue";
import { LMap, LTileLayer } from "vue2-leaflet";
//import WMS from "../../node_modules/leaflet-wms/leaflet.wms.js";
import WMS from "leaflet-wms/leaflet.wms.js";
import "leaflet/dist/leaflet.css";
import { latLng, Polygon } from "leaflet";

export default {
  name: "WebGis",
  props: { projectId: String },
  components: {
    LayerTree,
    LMap,
    LTileLayer
  },
  data: function() {
    return {
      map: {},
      project: {},
      wms_source: {},
      error: ``,
      status: `loading` // [loading,project]
    };
  },
  mounted() {
    fetch(Vue.config.qgisUrl + `/map/` + this.projectId + `.json`)
      .then(this.handleErrors)
      .then(response => response.json())
      .then(json => {
        this.project = json.project;
        this.loadMap(this.project);
      })
      .then(() => {
        let layers = this.project.wms_root_name;
        if (!layers) {
          let _layers = [];
          Object.values(this.project.wms_layers_map).forEach(layer_id =>
            _layers.push(layer_id)
          );
          layers = _layers.join(`,`);
        }
        let toc_url = `/project/${this.project.id}/?SERVICE=WMS&REQUEST=GetLegendGraphics&LAYERS=${layers}&FORMAT=application/json`;
        fetch(Vue.config.qgisUrl + toc_url)
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
            this.error = error.message;
          });
      })
      .catch(error => {
        this.error = error.message;
      });
  },
  methods: {
    setMap(map) {
      this.map = map;
    },
    /**
     * Toggles a layer by typename
     */
    toggleLayer(typename) {
      if (typename in this.wms_source._subLayers) {
        this.wms_source.removeSubLayer(typename);
      } else {
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
            new_sub_layers[_type_name] = this.wms_source._subLayers[_type_name];
          }
        }
        this.wms_source._subLayers = new_sub_layers;
        this.wms_source.refreshOverlay();
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

      this.wms_source = WMS.source(
        Vue.config.qgisUrl + `/project/` + project.id + `/?`,
        {
          tileSize: 512,
          transparent: true,
          format: "image/png",
          dpi: window.devicePixelRatio * 96
        }
      ).addTo(this.map);
    }
  }
};
</script>

<style scoped>
.wrapper {
  height: calc(100vh - 3.5em);
}

.alert-danger {
  position: absolute;
  top: 4em;
  margin: 0 8em;
  z-index: 10000;
}

#map {
  width: 100%;
  height: 100%;
}
</style>