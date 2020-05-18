import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    catalog: [],
    projects: {},
    tocs: {},
    error: "",
    status: "loading",
  },
  mutations: {
    setCatalog(state, payload) {
      state.catalog = payload;
    },
    setStatus(state, payload) {
      console.log(`Mutate status: ${payload}`);
      state.status = payload;
    },
    setError(state, payload) {
      console.log(`Mutate error: ${payload}`);
      state.error = payload;
    },
    clearError(state) {
      console.log(`Mutate clear error`);
      state.error = "";
    },
    setProject(state, project) {
      console.log(`Mutate set project ${project.id}`);
      Vue.set(state.projects, project.id, project);
    },
    setToc(state, { projectId, toc }) {
      console.log(`Mutate set toc ${projectId}`);
      Vue.set(state.tocs, projectId, toc);
    },
  },
  actions: {
    clearError({ commit }) {
      commit("clearError");
    },
    async getCatalog({ commit }) {
      try {
        fetch(`/index.json`)
          .then((response) => {
            if (!response) {
              throw Error(`Error fetching data from QGIS Server`);
            }
            if (!response.ok) {
              throw Error(response.statusText);
            }
            return response;
          })
          .then((response) => response.json())
          .then((json) => {
            json.projects.forEach((element) => {
              element.show = false;
            });
            commit("setCatalog", json.projects);
            commit("setStatus", json.projects.length ? `projects` : `empty`);
          })
          .catch((error) => {
            commit("setError", error.message);
          });
      } catch (error) {
        commit("setError", error.message);
      }
    },
    async getProject({ commit }, projectId) {
      try {
        console.log(`Inside getProject ${projectId}`);
        fetch(`/map/${projectId}.json`)
          .then((response) => {
            if (!response) {
              throw Error(`Error fetching data from QGIS Server`);
            }
            if (!response.ok) {
              throw Error(response.statusText);
            }
            return response;
          })
          .then((response) => response.json())
          .then((json) => {
            commit("setProject", json.project);
            commit("setStatus", `project`);
          })
          .catch((error) => {
            commit("setError", error.message);
          });
      } catch (error) {
        commit("setError", error.message);
      }
    },
    setStatus({ commit }, status) {
      commit("setStatus", status);
    },
    async getToc({ commit }, payload) {
      let toc_url = `/project/${payload.projectId}/?SERVICE=WMS&REQUEST=GetLegendGraphics&LAYERS=${payload.layers}&FORMAT=application/json`;
      fetch(toc_url)
        .then(this.handleErrors)
        .then((response) => response.json())
        .then((toc) => {
          commit("setToc", { projectId: payload.projectId, toc });
        })
        .catch((error) => {
          //this.error = error.message;
          console.log(error);
        });
    },
  },
});
