import Vue from "vue";
import VueRouter from "vue-router";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import App from "./App.vue";

// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.config.productionTip = false;
// From the environment
Vue.config.qgisUrl = process.env.VUE_APP_QGIS_SERVER_API_ENDPOINT;

// Routing
Vue.use(VueRouter);

import WebGis from "@/views/WebGis.vue";
import Catalog from "@/views/Catalog.vue";

const routes = [
  { path: "/", name: "catalog", component: Catalog },
  { path: "/map/:projectId", name: "map", component: WebGis, props: true },
];

const router = new VueRouter({
  routes, // short for `routes: routes`
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
