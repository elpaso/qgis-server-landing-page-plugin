<template>
  <v-app id="app">
    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
.v-app-bar.v-app-bar--fixed,
.v-footer {
  z-index: 10000 !important;
}
</style>
