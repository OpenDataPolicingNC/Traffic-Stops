import _ from 'underscore';

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
