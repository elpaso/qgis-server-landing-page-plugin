module.exports = {
  "configureWebpack": {
    "devtool": "source-map",
    "optimization": {
      "splitChunks": {
        "chunks": "all"
      }
    }
  },
  "runtimeCompiler": true,
  "devServer": {
    "proxy": "http://192.168.99.46:8001"
  },
  "transpileDependencies": [
    "vuetify"
  ]
}