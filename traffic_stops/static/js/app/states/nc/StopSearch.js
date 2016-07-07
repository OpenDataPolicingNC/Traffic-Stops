import AggregateDataHandlerBase from '../../base/AggregateDataHandlerBase.js';
import TableBase from '../../base/TableBase.js';
import { StopRatioTimeSeries } from './Stops.js';
import Stops from './defaults.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var StopSearchHandler = AggregateDataHandlerBase.extend({
  clean_data: function(){

    var stops = _.findWhere(this.get("raw_data"), {"type": "stop"}).raw,
        searches = _.findWhere(this.get("raw_data"), {"type": "search"}).raw,
        years = _.chain(stops).pluck('year')
                 .filter(function(yr){return yr>=Stops.start_year})
                 .sort().value(),
        lines = d3.map(),
        tables = [],
        stop, search, row, st, se, headers;

    // get total by race
    _.each([stops, searches], function(data){
      _.each(data, function(yr){
        yr.total = d3.sum(_.map(Stops.races, function(race){return yr[race] || 0;}));
      });
    });

    // set defaults
    _.each([Stops.races, Stops.ethnicities, ["total"]], function(dataType){
      _.each(dataType, function(race){
        lines.set(race, []);
      });
    });

    // get values for table and for each line
    headers = [Stops.races, Stops.ethnicities];
    var headerArr = _.chain(headers).flatten().map(function(d){return Stops.pprint.get(d);}).value();
    headerArr.unshift("Year");
    headerArr.push("Total");
    headers.push(["total"]);

    _.each(years, function(yr){
      stop = _.findWhere(stops, {"year": yr});
      search = _.findWhere(searches, {"year": yr});
      row = [yr];
      _.each(headers, function(dataType){
        _.each(dataType, function(race){
          st = stop && stop[race] || 0;
          se = search && search[race] || 0;
          if (st===0){
            row.push("-");
            lines.get(race).push({x:yr , y:undefined});
          } else {
            row.push(`${se}/${st}`);
            lines.get(race).push({x:yr , y:se/st});
          }
        });
      });
      tables.push(row);
    });

    // set object data
    this.set("data", {
      line: lines,
      table: tables,
      table_headers: headerArr,
    });
  }
});

var StopSearchTimeSeries = StopRatioTimeSeries.extend({
  setDefaultChart: function(){
    this.chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year');

    this.chart.yAxis
        .tickFormat(d3.format('%'));
  },
  _formatData: function(){

    var data = StopSearchTimeSeries.__super__._formatData.call(this),
        total = this.data.line.get('total'),
        defaultEnabled = ["Total", "White", "Black", "Hispanic", "Non-hispanic"];

    // add total-line
    data.push({
      key: "Total",
      values: total,
      color: Stops.baseline_color,
      disabled: false
    });

    // predefine enabled/disabled lines on chart
    _.each(data, function(d){
      d.disabled = defaultEnabled.indexOf(d.key) === -1;
    });

    return data;
  },
});

var StopSearchTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    rows.push(this.data.table_headers);

    // create data rows
    _.each(this.data.table, function(k, v){
      rows.push(k)
    });

    return rows;
  }
});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
