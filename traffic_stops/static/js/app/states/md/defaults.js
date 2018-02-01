import d3 from 'd3';

// Traffic Stops global defaults
export default {
  start_year: 2013,     // start-year for reporting requirement
  end_year: new Date().getUTCFullYear(),       // end-date for latest dataset
  races: [
    'white',
    'black',
    'native_american',
    'asian',
    'other'
  ],
  census_ethnicities: [
    'hispanic',
    'non_hispanic'
  ],
  pprint: d3.map({
    'white': 'White',
    'black': 'Black',
    'native_american': 'Native American',
    'asian': 'Asian',
    'other': 'Other',
    'hispanic': 'Hispanic',
    'non-hispanic': 'Non-hispanic'
  }),
  ethnicities: [
    'White',
    'Black',
    'Native American',
    'Hispanic',
    'Asian',
    'Unknown',
  ],
  colors: [
    "#1C9647", // dark green
    "#3F5EAB", // dark blue
    "#A7D16B", // light green
    "#66ACDD", // light blue
    "#7A76B7", // purple
    "#DC8F27", // orange
  ],
  baseline_color: "black",
  single_color: "#5C0808",
  purpose_order: d3.map({ // strings must match PURPOSE_CHOICES
    'Driving While Impaired': 0,
    'Safe Movement Violation': 1,
    'Vehicle Equipment Violation': 2,
    'Other Motor Vehicle Violation': 3,
    'Stop Light/Sign Violation': 4,
    'Speed Limit Violation': 5,
    'Vehicle Regulatory Violation': 6,
    'Seat Belt Violation': 7,
    'Non-motor Vehicle Violations': 8,
    'Other/Unknown': 9  // todo: use a list and indexOf instead of map
  }),
};
