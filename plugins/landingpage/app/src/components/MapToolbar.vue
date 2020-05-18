 <template>
  <!--v-toolbar light floating-->
  <v-layout column>
    <v-btn dark fab small @click="map.zoomIn()" color="orange">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-btn class="mt-1" dark fab small @click="map.zoomOut()" color="orange">
      <v-icon>mdi-minus</v-icon>
    </v-btn>
    <v-btn class="mt-3" dark fab small color="blue">
      <v-icon>mdi-information-outline</v-icon>
    </v-btn>
    <v-btn class="mt-1" dark fab small @click="map._onResize()" color="blue">
      <v-icon>mdi-selection-drag</v-icon>
    </v-btn>
  </v-layout>
  <!--/v-toolbar-->
</template>

<style lang="scss" scoped>
</style>

<script>
export default {
  name: "MapToolbar",
  props: {
    map: Object
  }
};
</script>