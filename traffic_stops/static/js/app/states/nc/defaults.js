// Traffic Stops global defaults
export default {
  start_year: 2002,     // start-year for reporting requirement
  end_year: new Date().getUTCFullYear(),       // end-date for latest dataset
  races: [
    'white',
    'black',
    'native_american',
    'asian',
    'other'
  ],
  ethnicities: [
    'hispanic',
    'non-hispanic'
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
  colors: [
    "#1C9647", // dark green
    "#3F5EAB", // dark blue
    "#A7D16B", // light green
    "#66ACDD", // light blue
    "#DC8F27", // orange
  ],
  baseline_color: "black",
  single_color: "#5C0808",
  purpose_order: d3.map({
    'Driving While Impaired': 0,
    'Safe Movement Violation': 1,
    'Vehicle Equipment Violation': 2,
    'Other Motor Vehicle Violation': 3,
    'Investigation': 4,
    'Stop Light/Sign Violation': 5,
    'Speed Limit Violation': 6,
    'Vehicle Regulatory Violation': 7,
    'Seat Belt Violation': 8,
    'Checkpoint': 9  // todo: use a list and indexOf instead of map
  }),
};
