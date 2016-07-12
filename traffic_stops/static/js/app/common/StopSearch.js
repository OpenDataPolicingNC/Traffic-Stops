import AggregateDataHandlerBase from '../base/AggregateDataHandlerBase.js';
import { StopRatioTimeSeriesBase } from './Stops.js';
import _ from 'underscore';
import d3 from 'd3';

export const StopSearchHandlerBase = AggregateDataHandlerBase.extend({
  clean_data: function () {

    var stops = _.findWhere(this.get("raw_data"), {"type": "stop"}).raw,
        searches = _.findWhere(this.get("raw_data"), {"type": "search"}).raw,
        years = _.chain(stops).pluck('year')
                 .filter((yr) => yr >= this.Stops.start_year)
                 .sort().value(),
        lines = d3.map(),
        tables = [],
        stop, search, row, st, se, headers;

    // get total by race
    _.each([stops, searches], (data) => {
      _.each(data, (yr) => {
        yr.total = d3.sum(_.map(this.major_type, (type) => yr[type] || 0));
      });
    });

    // set defaults
    _.each(this.types.concat([["total"]]), (dataType) => {
      _.each(dataType, (type) => {
        lines.set(type, []);
      });
    });

    // get values for table and for each line
    headers = _.clone(this.types);
    var headerArr = _.chain(headers).flatten().map(this._pprint).value();
    headerArr.unshift("Year");
    headerArr.push("Total");
    headers.push(["total"]);

    _.each(years, (yr) => {
      stop = _.findWhere(stops, {"year": yr});
      search = _.findWhere(searches, {"year": yr});
      row = [yr];
      _.each(headers, (dataType) => {
        _.each(dataType, (type) => {
          st = stop && stop[type] || 0;
          se = search && search[type] || 0;
          if (st === 0){
            row.push("-");
            lines.get(type).push({x:yr , y:undefined});
          } else {
            row.push(`${se}/${st}`);
            lines.get(type).push({x:yr , y:se/st});
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

export const StopSearchTimeSeriesBase = StopRatioTimeSeriesBase.extend({
  setDefaultChart: function () {
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

    var data = StopRatioTimeSeriesBase.prototype._formatData.bind(this)(),
        total = this.data.line.get('total'),
        defaultEnabled = this.defaultEnabled;

    // add total-line
    data.push({
      key: "Total",
      values: total,
      color: this.Stops.baseline_color,
      disabled: false
    });

    // predefine enabled/disabled lines on chart
    _.each(data, (d) => {
      d.disabled = defaultEnabled.indexOf(d.key) === -1;
    });

    return data;
  }
});
