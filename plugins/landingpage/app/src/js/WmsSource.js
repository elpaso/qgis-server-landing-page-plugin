/**
 * Override leaflet WMS for custom get feature info
 */
import L from "leaflet";
import WMS from "leaflet-wms/leaflet.wms.js";

var WmsSource = WMS.Source.extend({
  getFeatureInfo: function(point, latlng, layers, callback) {
    // Request WMS GetFeatureInfo and call callback with results
    // (split from identify() to faciliate use outside of map events)
    var params = this.getFeatureInfoParams(point, layers),
      url = this._url + L.Util.getParamString(params, this._url);

    this.showWaiting();
    this.ajax(url, done);

    function done(result) {
      this.hideWaiting();
      var text = this.parseFeatureInfo(result, url);
      callback.call(this, latlng, text);
    }
  },
  showFeatureInfo: function(latlng, info) {
    console.log(info);
  },
});

export default {
  source(url, options) {
    return new WmsSource(url, options);
  },
};
