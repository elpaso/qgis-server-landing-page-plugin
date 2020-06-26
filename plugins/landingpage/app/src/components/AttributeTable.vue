<template>
  <v-card level="2">
    <v-card-text>
      <v-btn class="btn-close" color="red" icon @click="onCloseButtonClicked">
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-data-table
        dense
        item-key="itemKeyInternalIdentifier"
        :page.sync="currentPage"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :server-items-length="numberMatched"
        :loading="tableHeaders.length == 0"
        :headers="tableHeaders"
        :items="tableData"
        :items-per-page="5"
        :footer-props="{
        itemsPerPageOptions: [5],
        itemsPerPageText: ''
      }"
      ></v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
const uuidv4 = require("uuid/v4");
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
      currentPage: 1,
      sortBy: null,
      sortDesc: null,
      tableData: [],
      tableHeaders: [],
      numberMatched: 0
    };
  },
  mounted() {
    this.loadData();
  },
  watch: {
    currentPage() {
      this.loadData();
    },
    sortBy() {
      this.loadData();
    },
    sortDesc() {
      this.loadData();
    }
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
        let offset = (this.currentPage - 1) * 5;
        let sorting = "";
        if (this.sortBy) {
          sorting = "&sortby=" + encodeURIComponent(this.sortBy);
          if (this.sortDesc) {
            sorting += "&sortdesc=1";
          }
        }
        fetch(
          `/project/${this.project.id}/wfs3/collections/${this.typename}/items.json?limit=5&offset=${offset}${sorting}`
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
              this.tableHeaders = headers;
              let data = [];
              for (let i = 0; i < json.features.length; i++) {
                let dataRow = json.features[i].properties;
                dataRow["itemKeyInternalIdentifier"] = uuidv4();
                data.push(dataRow);
              }
              this.tableData = data;
              this.numberMatched = json.numberMatched;
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