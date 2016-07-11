import Stops from './Stops.js';
import Search from './Search.js';
import LikelihoodOfSearch from './LikelihoodOfSearch.js';
import ContrabandHitRate from './ContrabandHitRate.js';

if (typeof window.MD === 'undefined') window.MD = {};

Object.assign(window.MD,
  Stops,
  Search,
  LikelihoodOfSearch,
  ContrabandHitRate
)
