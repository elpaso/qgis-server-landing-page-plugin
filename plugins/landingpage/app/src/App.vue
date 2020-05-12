<template>
  <v-app id="app">
    <router-view></router-view>
    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
//import NavBar from "./components/NavBar.vue";
export default {
  name: "App",
  components: {
    //NavBar
  }
};
</script>

<style>
.v-app-bar.v-app-bar--fixed {
  z-index: 10000 !important;
}
</style>
