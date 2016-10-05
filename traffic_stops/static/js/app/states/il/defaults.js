import d3 from 'd3';

// Traffic Stops global defaults
export default {
  start_year: 2005,     // start-year for reporting requirement
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
    'Hispanic',
    'Unknown',
  ],
  colors: [
    "#1C9647", // dark green
    "#3F5EAB", // dark blue
    "#A7D16B", // light green
    "#66ACDD", // light blue
  ],
  baseline_color: "black",
  single_color: "#5C0808",
  purpose_order: d3.map({ // strings must match PURPOSE_CHOICES
    'Equipment': 0,
    'Moving Violation': 1,
    'Registration': 2,
  }),
};
