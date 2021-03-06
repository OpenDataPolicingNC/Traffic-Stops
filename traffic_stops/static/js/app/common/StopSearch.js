import AggregateDataHandlerBase from '../base/AggregateDataHandlerBase.js';
import TableBase from '../base/TableBase.js';
import { StopRatioTimeSeriesBase } from './Stops.js';
import _ from 'underscore';
import d3 from 'd3';

export const StopSearchHandlerBase = AggregateDataHandlerBase.extend({
  _year_filter: function (yr) {
    return yr >= this.Stops.start_year;
  },

  clean_data: function () {

    var stops = _.findWhere(this.get("raw_data"), {"type": "stop"}).raw,
        searches = _.findWhere(this.get("raw_data"), {"type": "search"}).raw,
        years = _.chain(stops).pluck('year')
                 .filter(this._year_filter.bind(this))
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
          if (st === 0) {
            row.push("-");
            lines.get(type).push({x:yr , y:0});
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
                  .forceY(0)
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format('.0d'));

    this.chart.yAxis
        .tickFormat(d3.format('.1%'));
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
      // Strip key values of special characters before comparing
      d.disabled = defaultEnabled.indexOf(d.key.replace(/[^a-zA-Z ]/g, "")) === -1;
    });

    return data;
  }
});

export const StopSearchTableBase = TableBase.extend({
  get_tabular_data: function () {
    var header, row, rows = [];

    // create header
    rows.push(this.data.table_headers);

    // create data rows
    _.each(this.data.table, (k, v) => {
      rows.push(k)
    });

    return rows;
  }
});
