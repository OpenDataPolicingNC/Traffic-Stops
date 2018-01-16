import Stops from './defaults.js';
import * as C from '../../common/LikelihoodOfSearch.js';

const LikelihoodSearchHandler = C.LikelihoodSearchHandlerBase.extend({
  types: [Stops.races, Stops.ethnicities],
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
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _base: function () {
    return (this.get('showEthnicity')) ? "non-hispanic" : "white"
  },

  _defRace: function () {
    return (this.get('showEthnicity')) ? "hispanic" : "black"
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: function (e, v) {
    this.set('showEthnicity', v);
    this.selector.trigger('change');
  }
});

const LikelihoodSearchTable = C.LikelihoodSearchTableBase.extend({
  types: [Stops.races],

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
