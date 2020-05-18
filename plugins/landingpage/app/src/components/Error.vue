<template>
  <v-card class="mx-auto" max-width="600">
    <v-card-title>
      <v-icon color="red" large>mdi-emoticon-sad</v-icon>Epic failure
    </v-card-title>
    <v-card-text>
      <v-alert type="error">{{ error }}</v-alert>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    error: String
  }
};
</script>