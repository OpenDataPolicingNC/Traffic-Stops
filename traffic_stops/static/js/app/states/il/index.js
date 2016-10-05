import Stops from './defaults.js';
import StopsGraphs from './Stops.js';
import StopSearch from './StopSearch.js';
import Search from './Search.js';
import LikelihoodOfSearch from './LikelihoodOfSearch.js';
import ContrabandHitRate from './ContrabandHitRate.js';

if (typeof window.IL === 'undefined') window.IL = {};

Object.assign(window.IL,
  {Stops},
  StopsGraphs,
  StopSearch,
  Search,
  LikelihoodOfSearch,
  ContrabandHitRate,
  // Census,
  // StopByReasonAndRace
)
