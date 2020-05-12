const path = require("path");

module.exports = {
  configureWebpack: {
    devtool: "source-map",
    /*
    optimization: {
      splitChunks: {
        minSize: 10000,
        maxSize: 250000,
      },
    },*/
    optimization: {
      splitChunks: {
        chunks: "all",
      },
    },
  },
  runtimeCompiler: true,
  // Set the page title in index.html
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "QGIS Server Catalog";
      return args;
    });
  },
  // Use QGIS Server on host port 8001
  // You can change this to reflect your development setup
  devServer: {
    proxy: "http://192.168.99.46:8001",
  },
};
