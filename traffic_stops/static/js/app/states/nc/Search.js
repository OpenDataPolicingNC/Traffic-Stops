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

export default {
  SearchHandler,
  SearchRatioDonut,
  SearchRatioTimeSeries,
  SearchTable
};
