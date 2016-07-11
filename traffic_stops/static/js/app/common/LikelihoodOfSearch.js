import DataHandlerBase from '../base/DataHandlerBase.js';
import d3 from 'd3';
import _ from 'underscore';

export function get_years (raw, Stops) {
  let years = d3.set(raw.stops.map((v) => v.year)).values();

  years.filter((v) => (v >= Stops.start_year));
  years.push("Total");

  return years;
}

export function get_totals (a, types) {
  // calculate total for all years by purpose; push to array
  let arr = _.clone(a);

  var purposes = d3.nest()
                   .key((d) => d.purpose)
                   .entries(arr);

  purposes.forEach((v) => {
    // create new totals object, and reset race/ethnicity-values
    var total = _.clone(v.values[0]);

    _.keys(total).forEach((key) => {
      if (_.some(types, (t) => t.indexOf(key) >= 0)) {
        total[key] = 0;
      }
    });

    // sum data from all years
    v.values.forEach((year) => {
      _.keys(year).forEach((key) => {
        if (_.some(types, (t) => t.indexOf(key) >= 0)) {
          total[key] += year[key];
        }
      });
    });

    total["year"] = "Total";
    arr.push(total);
  });

  return arr;
}

export const LikelihoodSearchHandlerBase = DataHandlerBase.extend({
  types: [],
  defaults: {},

  clean_data: function () {
    let raw = this.get("raw_data");
    let years = get_years(raw, this.defaults);

    if (raw.stops.length>0) {
      raw.stops = get_totals(raw.stops, this.types);
    }

    if (raw.searches.length > 0 ) {
      raw.searches = get_totals(raw.searches, this.types);
    }

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});
