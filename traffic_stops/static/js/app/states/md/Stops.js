import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import * as C from '../../common/Stops.js';

import Backbone from 'backbone';
import _ from 'underscore';
import d3 from 'd3';
import $ from 'jquery';
Backbone.$ = $;

export const StopsHandler = C.StopsHandlerBase.extend({
  types: [Stops.ethnicities],
  Stops: Stops
});

export const StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    width: 300,
    height: 300
  },

  Stops: Stops,

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (x) {
    return x;
  },

  triggerRaceToggle: () => null
});

export const StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375,
  },

  Stops: Stops,

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (x) {
    return x;
  },

  triggerRaceToggle: () => null
});

export const StopsTable = C.StopsTableBase.extend({
  types: [Stops.ethnicities],

  _get_header_rows: function () {
    return Stops.ethnicities;
  }
});

export default {
  StopsHandler,
  StopRatioDonut,
  StopRatioTimeSeries,
  StopsTable
};
