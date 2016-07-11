import DataHandlerBase from '../base/DataHandlerBase.js';
import d3 from 'd3';
import _ from 'underscore';

export function get_years (raw, Stops) {
  let years = d3.set(raw.searches.map((v) => v.year)).values();

  years.filter((v) => (v >= Stops.start_year));
  years.push("Total");

  return years;
}

export function get_totals (xs) {
  let arr = _.clone(xs);
  let total = _.clone(arr[0]);

  _.keys(total).forEach((key) => {
    total[key] = 0;
  });

  // sum data from all years
  arr.forEach((year) => {
    _.keys(year).forEach((key) => {
      total[key] += year[key];
    });
  });

  // push to end of array
  total["year"] = "Total";
  arr.push(total);

  return arr;
}

export const ContrabandHitRateHandlerBase = DataHandlerBase.extend({
  clean_data: function () {

    let raw = this.get("raw_data");
    let years = get_years(raw, this.defaults);

    if (raw.searches.length > 0) {
      raw.searches = get_totals(raw.searches);
    }

    if (raw.contraband.length > 0) {
      raw.contraband = get_totals(raw.contraband);
    }

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});
