<template>
  <li :id="node.tree_id_hash">
    <div v-if="node.is_layer && node.layer_type == 'vector'">
      <i
        data-toggle="collapse"
        :aria-expanded="node.expanded ? 'true' : 'false'"
        :class="'group-toggle fa fa-caret-' + (node.expanded ? 'down' : 'right')"
      ></i>
      <i
        v-b-tooltip.hover
        title="Toggle layer visibility"
        :class="'node-check fa ' + (node.visible ? 'fa-check-square-o visible' : 'fa-square-o')"
        @click="toggleLayer(node.typename)"
      ></i>
      {{ node.title }}
    </div>
    <div v-else>
      <!-- it's a group -->
      <i
        v-b-tooltip.hover
        title="Toggle group visibility"
        :class="'node-check fa ' + (node.visible ? 'fa-check-square-o visible' : 'fa-square-o')"
        @click="toggleGroup(node.tree_id_hash)"
      ></i>
      <b-button variant="link" v-b-toggle="'node-' + node.tree_id_hash">{{ node.title }}</b-button>
      <b-collapse
        tag="ul"
        :id="'node-' + node.tree_id_hash"
        class="list list-unstyled layer-group"
        :visible="node.expanded"
        v-for="child_node in node.children"
        :key="child_node.tree_id_hash"
      >
        <LayerTreeNode
          :node="child_node"
          v-on:toggleLayer="toggleLayer"
          v-on:toggleGroup="toggleGroup"
        />
      </b-collapse>
    </div>
  </li>
</template>

<script>
export default {
  name: "LayerTreeNode",
  props: {
    node: {}
  },
  methods: {
    toggleLayer(typename) {
      this.$emit("toggleLayer", typename);
    },
    toggleGroup(tree_id_hash) {
      this.$emit("toggleGroup", tree_id_hash);
    }
  },
  mounted() {
    if (this.node.is_layer && this.node.visible) {
      this.node.visible = false;
      this.$emit("toggleLayer", this.node.typename);
    }
  }
};
</script>

<style scoped>
@import "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";
</style>