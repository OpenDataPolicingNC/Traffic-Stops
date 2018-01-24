import Stops from './defaults.js';
import * as C from '../../common/LikelihoodOfSearch.js';

const LikelihoodSearchHandler = C.LikelihoodSearchHandlerBase.extend({
  types: [Stops.ethnicities],
  Stops: Stops
});

const LikelihoodOfSearch = C.LikelihoodOfSearchBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  Stops: Stops,

  _items: function () {
    return Stops.ethnicities;
  },

  _base: function () {
    return "white"
  },

  _defRace: function () {
    return "black"
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: () => null
});

const LikelihoodSearchTable = C.LikelihoodSearchTableBase.extend({
  types: [Stops.ethnicities],

  Stops: Stops,

  _get_header_rows: function () {
    return Stops.pprint.values();
  }
});

export default {
  LikelihoodSearchHandler,
  LikelihoodOfSearch,
  LikelihoodSearchTable
};
