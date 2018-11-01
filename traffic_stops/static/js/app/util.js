import _ from 'underscore';
import d3 from 'd3';

/*
  Used by LikelihoodSearchHandlerBase and IRRHandlerBase
  to create the years for the "Total" rows for the data table.
*/
export function get_years (data, Stops) {
  let years = d3.set(data.map((v) => v.year)).values();

  years.filter((v) => (v >= Stops.start_year));
  years.push("Total");

  return years;
}

/*
  Used by LikelihoodSearchHandlerBase and IRRHandlerBase
  to fill in the data for the "Total" rows for the data table.
*/
export function get_totals (a, types, reason_type) {
  // calculate total for all years by purpose; push to array
  let arr = _.clone(a);

  var reasons = d3.nest()
                   .key((d) => d[reason_type])
                   .entries(arr);

  reasons.forEach((v) => {
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

export function toTitleCase (str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
