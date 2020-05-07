<template>
  <div id="app">
    <NavBar />
    <div id="main" class="mt-4">
      <Catalog />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import Catalog from "./components/Catalog.vue";

export default {
  name: "App",
  components: {
    NavBar,
    Catalog
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
