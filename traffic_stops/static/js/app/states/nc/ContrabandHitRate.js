import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import * as C from '../../common/ContrabandHitRate.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

const ContrabandHitRateHandler = C.ContrabandHitRateHandlerBase.extend({
  Stops: Stops
});

// dashboard visuals

const ContrabandHitRateBar = C.ContrabandHitRateBarBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375
  },

  Stops: Stops,

  _items: function () {
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.selector.trigger('change');
  }
});

const ContrabandTable = C.ContrabandTableBase.extend({
  _get_header_rows: function () {
    return Stops.pprint.values();
  },

  types: [Stops.races, Stops.ethnicities]
});

export default {
  ContrabandHitRateHandler,
  ContrabandHitRateBar,
  ContrabandTable
};
