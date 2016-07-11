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
  defaults: Stops
});

// dashboard visuals

var ContrabandHitRateBar = C.ContrabandHitRateBarBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375,
    Stops: Stops
  },

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

var ContrabandTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [], se, cb;

    // create header
    header = ["Year"];
    header.push.apply(header, Stops.pprint.values());
    rows.push(header);

    var raw = this.data.raw,
        searches = _.object(_.pluck(raw.searches, 'year'), raw.searches),
        contrabands = _.object(_.pluck(raw.contraband, 'year'), raw.contraband);

    _.keys(searches).forEach(function(yr){
      se = searches[yr];
      cb = contrabands[yr] || {};
      row = [yr];
      Stops.races.forEach(function(r){
        row.push((cb[r]||0).toLocaleString() + "/" + (se[r]||0).toLocaleString());
      });
      Stops.ethnicities.forEach(function(e){
        row.push((cb[e]||0).toLocaleString() + "/" + (se[e]||0).toLocaleString());
      });
      rows.push(row);
    });

    return rows;
  }
});

export default {
  ContrabandHitRateHandler,
  ContrabandHitRateBar,
  ContrabandTable
};
