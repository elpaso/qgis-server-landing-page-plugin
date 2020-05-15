 <template>
  <!--v-toolbar light floating-->
  <v-layout column>
    <v-btn dark fab small color="orange">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-btn class="mt-1" dark fab small color="orange">
      <v-icon>mdi-minus</v-icon>
    </v-btn>
    <v-btn class="mt-3" dark fab small color="blue">
      <v-icon>mdi-information-outline</v-icon>
    </v-btn>
    <v-btn class="mt-1" dark fab small color="blue">
      <v-icon>mdi-selection-drag</v-icon>
    </v-btn>
    {{ mapObject }}
  </v-layout>
  <!--/v-toolbar-->
</template>

<style lang="scss" scoped>
</style>

<script>
export default {
  name: "MapToolbar",
  props: {
    mapObject: {}
  }
};
</script>