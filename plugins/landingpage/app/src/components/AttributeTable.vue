<template>
  <v-card level="2">
    <v-card-text>
      <v-progress-linear v-if="!tableHeaders" indeterminate query></v-progress-linear>

      <v-btn class="btn-close" color="red" icon @click="onCloseButtonClicked">
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-data-table dense :headers="tableHeaders" :items="tableData" :items-per-page="5"></v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "AttributeTable",
  props: {
    project: null
  },
  computed: {
    /**
     * Layer identifier for WFS3: layer id or short name or name
     */
    typename() {
      return this.$store.state.attributeTableTypename;
    }
  },
  data() {
    return {
      error: null,
      tableData: [],
      tableHeaders: []
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    onCloseButtonClicked() {
      this.$store.commit("clearAttributeTableTypename");
    },
    /**
     * Load table data from WFS3
     */
    async loadData() {
      try {
        fetch(
          `/project/${this.project.id}/wfs3/collections/${this.typename}/items.json`
        )
          .then(response => {
            if (!response) {
              throw Error(
                `Error fetching attribute table data from QGIS Server`
              );
            }
            if (!response.ok) {
              throw Error(response.statusText);
            }
            return response;
          })
          .then(response => response.json())
          .then(json => {
            if (json.features) {
              let headers = [];
              for (let k in json.features[0].properties) {
                headers.push({ text: k, value: k });
              }
              console.log(headers);
              this.tableHeaders = headers;
              let data = [];
              for (let i = 0; i < json.features.length; i++) {
                data.push(json.features[i].properties);
              }
              this.tableData = data;
            }
          })
          .catch(error => {
            this.error = error.message;
          });
      } catch (error) {
        this.error = error.message;
      }
    }
  }
};
</script>

<style scoped>
.btn-close {
  float: right;
}
</style>