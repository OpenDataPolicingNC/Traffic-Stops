import Stops from './defaults.js';
import StopsGraphs from './Stops.js';
import StopSearch from './StopSearch.js';
import Search from './Search.js';
import LikelihoodOfSearch from './LikelihoodOfSearch.js';
import ContrabandHitRate from './ContrabandHitRate.js';
import Census from './Census.js';

if (typeof window.MD === 'undefined') window.MD = {};

Object.assign(window.MD,
  {Stops},
  StopsGraphs,
  StopSearch,
  Search,
  LikelihoodOfSearch,
  ContrabandHitRate,
  Census
)
