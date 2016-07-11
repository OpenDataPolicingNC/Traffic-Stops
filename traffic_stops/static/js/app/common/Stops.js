import _ from 'underscore';
import d3 from 'd3';

/***
 * StopsHandler data processing helper functions
 */
export function build_totals (data) {
  let total = {};
  // build a 'Totals' year which sums by ethnicity for all years
  if (data.length > 0) {
    // create new totals object, and reset values
    total = _.clone(data[0]);

    _.keys(total).forEach((key) => {
      total[key] = 0;
    });

    // sum data from all years
    data.forEach((year) => {
      _.keys(year).forEach((key) => {
        if (key === 'OTHER') return; // ignore 'OTHER' from bad API output
        if (typeof total[key] === 'undefined') total[key] = 0;
        total[key] += (typeof year[key] === 'undefined') ? 0 : year[key];
      });
    });

    total['year'] = 'Total';
  }

  return total;
}

export function build_pie_data (data, total, Stops) {
  let pie = d3.map();

  data.forEach((v) => {
    if (v.year >= Stops.start_year) pie.set(v.year, d3.map(v));
  });

  pie.set('Total', d3.map(total));

  return pie;
}

export function get_total_by_type (dataType, yr) {
  var total = 0;
  dataType.forEach((type) => {
    total += (typeof yr[type] === 'undefined') ? 0 : yr[type];
  });
  return total;
}

export function build_line_data (data, types, Stops) {
  var line = d3.map();

  types.forEach((dataType) => {
    dataType.forEach((v) => {
      line.set(v, []);
    });
    data.forEach((yr) => {
      if (yr.year >= Stops.start_year) {
        var total = get_total_by_type(dataType, yr);
        dataType.forEach((type) => {
          line.get(type).push({x: yr.year, y:(yr[type] > 0 ? yr[type]/total : 0)});
        })
      }
    })
  });

  return line;
}
