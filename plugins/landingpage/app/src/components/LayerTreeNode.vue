<template>
  <div :id="node.tree_id_hash">
    <div class="v-treeview-node" v-if="node.is_layer && node.layer_type == 'vector'">
      <div class="node-title">
        <v-icon
          data-toggle="collapse"
          :aria-expanded="node.expanded ? 'true' : 'false'"
          aria-controls="'node-' + node.tree_id_hash"
          @click="node.expanded = !node.expanded"
          v-if="node.children.length"
        >mdi-menu-{{ node.expanded ? `down` : `right` }}</v-icon>
        <v-tooltip top>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" icon @click="toggleLayer(node.tree_id_hash)">
              <v-icon>mdi-checkbox-{{ node.visible ? `marked` : `blank-outline` }}</v-icon>
            </v-btn>
          </template>
          Toggle layer visibility
        </v-tooltip>
        <v-tooltip top>
          <template v-slot:activator="{ on }">
            <span
              v-on="on"
              class="group-title"
              @click="node.expanded = ! node.expanded"
              @contextmenu.prevent.stop="showContextMenu($event, node.tree_id_hash)"
            >{{ node.title }}</span>
          </template>
          <div>
            {{ node.title }}
            <i>({{ node.typename }})</i>
          </div>
          <div v-if="node.description">{{ node.description }}</div>
        </v-tooltip>
      </div>

      <template v-if="node.layer_type=='vector' && node.children.length">
        <v-expand-transition>
          <div class="vector-legend" v-if="node.expanded" @contextmenu.prevent.stop="function(){}">
            <div
              :id="'node-' + node.tree_id_hash"
              class="v-treeview-node layer-legend"
              v-for="child in node.children"
              :key="child.title"
              :aria-expanded="node.expanded ? 'true' : 'false'"
            >
              <div class="v-treeview-node vector-legend-entry">
                <img class="symbol" :src="`data:image/png;base64,${child.icon}`" />
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <span v-on="on" @click="node.expanded = ! node.expanded">{{ child.title }}</span>
                  </template>
                  <div>{{ child.title }}</div>
                </v-tooltip>
              </div>
            </div>
          </div>
        </v-expand-transition>
      </template>
    </div>
    <div v-else>
      <!-- it's a group or a raster -->
      <v-icon
        @click="node.expanded = !node.expanded"
        v-if="node.layer_type != 'raster'"
      >mdi-menu-{{ node.expanded ? `down` : `right` }}</v-icon>
      <v-icon v-else color="light-green lighten-3">mdi-checkerboard</v-icon>
      <v-tooltip top>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon @click="toggleGroup(node.tree_id_hash)">
            <v-icon>mdi-checkbox-{{ node.visible ? `marked` : `blank-outline` }}</v-icon>
          </v-btn>
        </template>
        Toggle group visibility
      </v-tooltip>
      <v-tooltip top>
        <template v-slot:activator="{ on }">
          <span
            v-on="on"
            class="group-title"
            @click="node.expanded = ! node.expanded"
            @contextmenu.prevent.stop="function(){}"
          >{{ node.title }}</span>
        </template>
        <div>{{ node.title }}</div>
        <div v-if="node.description">{{ node.description }}</div>
      </v-tooltip>

      <v-expand-transition>
        <div
          :class="`group-container group-father-of-` + node.children.length"
          :id="'node-' + node.tree_id_hash"
          v-show="node.expanded"
        >
          <LayerTreeNode
            :node="child_node"
            v-on:toggleLayer="toggleLayer"
            v-on:toggleGroup="toggleGroup"
            v-for="child_node in node.children"
            :key="child_node.tree_id_hash"
          />
        </div>
      </v-expand-transition>
    </div>

    <!-- Context menu -->
    <v-menu
      v-model="showMenu"
      :close-on-content-click="true"
      :close-on-click="false"
      :position-x="x"
      :position-y="y"
      absolute
      offset-y
    >
      <v-list>
        <v-list-item
          v-for="item in options"
          :key="item.name"
          @click="onContextMenuOptionClicked(item.name, node.tree_id_hash)"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "LayerTreeNode",
  props: {
    node: {}
  },
  data() {
    return {
      x: 0,
      y: 0,
      showMenu: false,
      options: [
        {
          title: "Attribute Table",
          name: "attributes",
          icon: "mdi-table-large"
        },
        {
          title: "Download",
          name: "download",
          icon: "mdi-download"
        }
      ]
    };
  },
  methods: {
    toggleLayer(tree_id_hash) {
      this.$emit("toggleLayer", tree_id_hash);
    },
    toggleGroup(tree_id_hash) {
      this.$emit("toggleGroup", tree_id_hash);
    },
    onContextMenuOptionClicked(name, tree_id_hash) {
      console.log("onContextMenuOptionClicked", name, tree_id_hash);
      if (name == "attributes") {
        this.$store.commit("setShowAttributeTable", tree_id_hash);
      } else {
        console.log(name, tree_id_hash);
      }
    },
    showContextMenu(e, tree_id_hash) {
      e.preventDefault();
      this.showMenu = false;
      this.x = e.clientX;
      this.y = e.clientY;
      this.$nextTick(() => {
        console.log("Showing menu for", tree_id_hash);
        this.showMenu = true;
      });
    }
  }
};
</script>

<style scoped>
@import "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";

.group-title {
  cursor: pointer;
  overflow: hidden;
}

.group-container {
  margin-left: 2em;
}

.group-title,
.node-title,
.vector-legend-entry {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.vector-legend-entry span {
  margin-left: 10px;
}
.vector-legend {
  margin-left: 1.3em;
}

.layer-legend {
  margin-left: 16px;
}
</style>