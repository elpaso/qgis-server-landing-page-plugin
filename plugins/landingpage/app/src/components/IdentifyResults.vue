<template>
  <v-navigation-drawer
    absolute
    stateless
    right
    hide-overlay
    temporary
    width="300px"
    v-model="drawer"
  >
    <v-container class="mx-auto mt-10">
      <v-row>
        <v-col>
          <h3>Results</h3>
        </v-col>
        <v-col class="col-auto">
          <v-btn icon color="red" @click.stop="hideIdentifyResults()">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <template :v-if="identifyResults.features">
        <v-row>
          <v-col class="col-auto">
            <v-card
              hover
              class="mx-auto mb-4"
              v-for="feature in identifyResults.features"
              :key="feature.id"
            >
              <v-card-title>{{ feature.id }}</v-card-title>
              <v-simple-table dense>
                <template v-slot:default>
                  <tbody>
                    <tr v-for="(value, name) in feature.properties" :key="name">
                      <th>{{ name }}</th>
                      <td>{{ value }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "IdentifyResults",
  props: {
    drawer: null,
    identifyResults: {}
  },
  methods: {
    hideIdentifyResults() {
      this.$emit("hideIdentifyResults");
    }
  }
};
</script>