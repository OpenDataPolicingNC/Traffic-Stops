import Stops from './Stops.js';
import Search from './Search.js';

if (typeof window.MD === 'undefined') window.MD = {};

Object.assign(window.MD,
  Stops,
  Search
)
