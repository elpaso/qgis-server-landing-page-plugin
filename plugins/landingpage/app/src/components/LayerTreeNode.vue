<template>
  <li :id="node.tree_id_hash">
    <div v-if="node.is_layer && node.layer_type == 'vector'">
      <i
        data-toggle="collapse"
        :aria-expanded="node.expanded ? 'true' : 'false'"
        aria-controls="'node-' + node.tree_id_hash"
        :class="'group-toggle fa fa-caret-' + (node.expanded ? 'down' : 'right')"
        @click="node.expanded = !node.expanded"
        v-if="node.children.length"
      ></i>
      <i
        v-b-tooltip.hover
        title="Toggle layer visibility"
        :class="'node-check fa ' + (node.visible ? 'fa-check-square-o visible' : 'fa-square-o')"
        @click="toggleLayer(node.typename)"
      ></i>
      <template v-if="node.layer_type=='vector' && node.children.length">
        <b-button
          class="group-title"
          variant="link"
          v-b-toggle="'node-' + node.tree_id_hash"
        >{{ node.title }}</b-button>
        <b-collapse
          tag="ul"
          :id="'node-' + node.tree_id_hash"
          class="list list-unstyled layer-legend"
          v-for="child in node.children"
          :key="child.title"
          v-model="node.expanded"
        >
          <li>
            <img class="symbol" :src="`data:image/png;base64,${child.icon}`" />
            {{ child.title }}
          </li>
        </b-collapse>
      </template>
      <span v-else>{{ node.title }}</span>
    </div>
    <div v-else>
      <!-- it's a group -->
      <i
        data-toggle="collapse"
        :aria-expanded="node.expanded ? 'true' : 'false'"
        :class="'group-toggle fa fa-caret-' + (node.expanded ? 'down' : 'right')"
        aria-controls="'node-' + node.tree_id_hash"
        @click="node.expanded = !node.expanded"
      ></i>
      <i
        v-b-tooltip.hover
        title="Toggle group visibility"
        :class="'node-check fa ' + (node.visible ? 'fa-check-square-o visible' : 'fa-square-o')"
        @click="toggleGroup(node.tree_id_hash)"
      ></i>
      <b-button
        class="group-title"
        variant="link"
        v-b-toggle="'node-' + node.tree_id_hash"
      >{{ node.title }}</b-button>
      <b-collapse
        tag="ul"
        :id="'node-' + node.tree_id_hash"
        class="list list-unstyled layer-group"
        v-model="node.expanded"
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

i.group-toggle,
i.node-check {
  cursor: pointer;
  width: 1em;
}

i.node-check {
  margin-right: 0.25em;
}
button.group-title {
  padding: 0;
}

ul.layer-legend {
  margin-left: 1em;
}
</style>