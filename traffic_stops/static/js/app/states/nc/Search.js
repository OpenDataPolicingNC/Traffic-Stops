import { StopsHandler, StopRatioDonut, StopRatioTimeSeries, StopsTable } from './Stops.js';

var SearchHandler = StopsHandler.extend({
  clean_data: function(){
    SearchHandler.__super__.clean_data.call(this);
    var data = this.get("data");
    data.type = "search";
    this.set("data", data);
  }
});

var SearchRatioDonut = StopRatioDonut.extend({});
var SearchRatioTimeSeries = StopRatioTimeSeries.extend({});
var SearchTable = StopsTable.extend({});

if (typeof window.NC === 'undefined') window.NC = {};

Object.assign(window.NC, {
  SearchHandler,
  SearchRatioDonut,
  SearchRatioTimeSeries,
  SearchTable
});
