import Stops from './defaults.js';
import StopSearch from './StopSearch.js';
import Search from './Search.js';
import LikelihoodOfSearch from './LikelihoodOfSearch.js';
import ContrabandHitRate from './ContrabandHitRate.js';

if (typeof window.MD === 'undefined') window.MD = {};

Object.assign(window.MD,
  {Stops},
  StopSearch,
  Search,
  LikelihoodOfSearch,
  ContrabandHitRate
)
