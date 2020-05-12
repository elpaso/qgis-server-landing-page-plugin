<template>
  <v-app-bar app dense collapse-on-scroll clipped-left color="green" dark>
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title>QGIS Server</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon title="Home Page" :to="{ name: 'catalog' }">
      <v-icon>mdi-home-circle</v-icon>
    </v-btn>
  </v-app-bar>
</template>