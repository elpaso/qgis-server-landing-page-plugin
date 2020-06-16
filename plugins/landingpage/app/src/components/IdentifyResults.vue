<template>
  <v-container class="mx-auto">
    <template>
      <v-row v-if="identifyResults.features">
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
      <v-row v-else>
        <v-progress-linear indeterminate query></v-progress-linear>
      </v-row>
    </template>
  </v-container>
</template>

<script>
export default {
  name: "IdentifyResults",
  props: {
    drawer: null
  },
  computed: {
    identifyResults() {
      console.log("Computed", this.$store.state.identifyResults.features);
      return this.$store.state.identifyResults;
    }
  }
};
</script>