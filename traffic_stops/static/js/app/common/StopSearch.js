import AggregateDataHandlerBase from '../base/AggregateDataHandlerBase.js';
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
