import d3 from 'd3';

// Traffic Stops global defaults
export default {
  start_year: 2012,     // start-year for reporting requirement
  end_year: new Date().getUTCFullYear(),       // end-date for latest dataset
  ethnicities: [
    'White',
    'Black',
    'Native American',
    'Hispanic',
    'Asian',
    'Unknown',
  ],
  colors: [
    "#1a9641",
    "#0571b0",
    "#a6d96a",
    "#66ADDD",
    "#3cd6c4",
    "#F2AC29",
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
