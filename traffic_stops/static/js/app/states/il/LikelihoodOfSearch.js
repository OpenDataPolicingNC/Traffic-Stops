import Stops from './defaults.js';
import * as C from '../../common/LikelihoodOfSearch.js';

const LikelihoodSearchHandler = C.LikelihoodSearchHandlerBase.extend({
  types: [Stops.ethnicities],
  Stops: Stops
});

const LikelihoodOfSearch = C.LikelihoodOfSearchBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375
  },

  Stops: Stops,

  _items: function () {
    return Stops.ethnicities;
  },

  _base: function () {
    return "White";
  },

  _defRace: function () {
    return "Black";
  },

  _pprint: function (type) {
    return type;
  },
});

const LikelihoodSearchTable = C.LikelihoodSearchTableBase.extend({
  types: [Stops.ethnicities],

  Stops: Stops,

  _get_header_rows: function () {
    return Stops.ethnicities
  }
});

export default {
  LikelihoodSearchHandler,
  LikelihoodOfSearch,
  LikelihoodSearchTable
};
