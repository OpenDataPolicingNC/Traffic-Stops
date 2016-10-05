import Stops from './defaults.js';
import StopsGraphs from './Stops.js';

if (typeof window.IL === 'undefined') window.IL = {};

Object.assign(window.IL,
  {Stops},
  StopsGraphs,
  // StopSearch,
  // Search,
  // LikelihoodOfSearch,
  // ContrabandHitRate,
  // Census,
  // StopByReasonAndRace
)
