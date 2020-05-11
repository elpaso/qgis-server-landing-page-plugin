<template>
  <div>
    <div class="leaflet-left leaflet-top layertree-toggle-container">
      <div class="leaflet-touch">
        <div class="leaflet-control-layers leaflet-bar leaflet-control" aria-haspopup="true">
          <a
            id="layertree-toggle"
            v-b-toggle.layertree
            class="leaflet-control-layers-toggle"
            v-b-tooltip.hover
            title="Show Legend"
          ></a>
        </div>
      </div>
    </div>
    <b-sidebar id="layertree" title="Legend" shadow>
      <div class="px-3 py-2" v-if="project.toc">
        <ul
          class="list list-unstyled layer-group"
          v-for="(element, entry) in project.toc.children"
          :key="uniqueKey(entry)"
        >
          <LayerTreeNode
            :node="element"
            v-on:toggleLayer="toggleLayer"
            v-on:toggleGroup="toggleGroup"
          />
        </ul>
      </div>
      <!-- TODO: else loading -->
    </b-sidebar>
  </div>
</template>

<script>
import LayerTreeNode from "@/components/LayerTreeNode.vue";
const uuidv4 = require("uuid/v4");
export default {
  name: "LayerTree",
  props: {
    projectId: String,
    project: Object
  },
  components: {
    LayerTreeNode
  },
  data: function() {
    return {
      uniqueKey: function() {
        return uuidv4();
      }
    };
  },
  methods: {
    /**
     * Find a layer node from typename and children
     */
    findLayerNode(typename, children) {
      if (children) {
        for (let i = 0; i < children.length; ++i) {
          if (children[i].typename == typename) {
            return children[i];
          }
          let res = this.findLayerNode(typename, children[i].children);
          if (res) {
            return res;
          }
        }
      }
    },
    /**
     * Find a group node from tree id hash and children
     */
    findGroupNode(tree_id_hash, children) {
      if (children) {
        for (let i = 0; i < children.length; ++i) {
          if (children[i].tree_id_hash == tree_id_hash) {
            return children[i];
          }
          let res = this.findGroupNode(tree_id_hash, children[i].children);
          if (res) {
            return res;
          }
        }
      }
    },
    /**
     * Toggle a single layer by typename
     */
    toggleLayer(typename) {
      let node = this.findLayerNode(typename, this.project.toc.children);
      if (node) {
        node.visible = !node.visible;
        this.$emit("toggleLayer", typename);
      }
    },
    /**
     * Toggle a group by tree id hash
     */
    toggleGroup(tree_id_hash) {
      let node = this.findGroupNode(tree_id_hash, this.project.toc.children);
      if (node) {
        this.setGroupNodeVisibility(node, !node.visible);
      }
    },
    /**
     * Recursively set a group node visibility
     */
    setGroupNodeVisibility(groupNode, visible) {
      groupNode.visible = visible;
      // Emit if it's a layer
      if (groupNode.is_layer) {
        this.$emit("toggleLayer", groupNode.typename);
      }
      if (groupNode.children) {
        for (let i = 0; i < groupNode.children.length; ++i) {
          this.setGroupNodeVisibility(groupNode.children[i], visible);
        }
      }
    }
  }
};
</script>

<style>
.leaflet-top.layertree-toggle-container {
  top: 8.5rem;
}

#layertree-toggle {
  cursor: pointer;
}

ul.layer-group {
  padding-left: 1em;
}

.b-sidebar-body > div > ul.layer-group {
  padding-left: 0;
}
</style>