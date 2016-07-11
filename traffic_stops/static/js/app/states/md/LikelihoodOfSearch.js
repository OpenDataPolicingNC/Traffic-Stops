import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import * as C from '../../common/LikelihoodOfSearch.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var LikelihoodSearchHandler = C.LikelihoodSearchHandlerBase.extend({
  types: [Stops.ethnicities],
  defaults: Stops
});

var LikelihoodOfSearch = C.LikelihoodOfSearchBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375,
    Stops: Stops
  },

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

  triggerRaceToggle: () => null
});

var LikelihoodSearchTable = C.LikelihoodSearchTableBase.extend({
  types: [Stops.ethnicities],

  defaults: Stops,

  _get_header_rows: function () {
    return Stops.ethnicities
  }
});

export default {
  LikelihoodSearchHandler,
  LikelihoodOfSearch,
  LikelihoodSearchTable
};
