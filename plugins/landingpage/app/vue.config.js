const path = require("path");

module.exports = {
  configureWebpack: {
    devtool: "source-map",
  },
  runtimeCompiler: true,
  // Set the page title in index.html
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "QGIS Server Catalog";
      return args;
    });
  },
};
