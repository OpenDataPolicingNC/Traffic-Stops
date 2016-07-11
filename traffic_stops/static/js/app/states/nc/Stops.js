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
  types: [Stops.races, Stops.ethnicities],
  defaults: Stops
});

export const StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    showEthnicity: false,
    width: 300,
    height: 300
  },

  _items: function () {
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: function (e, v) {
    this.set('showEthnicity', v);
    this.drawChart();
  }
});

export const StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    showEthnicity: false,
    width: 750,
    height: 375
  },

  _formatData: function(){
    let data = [],
        items = (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races,
        subset = [],
        i = 0,
        disabled;

    this.data.line.forEach((key, vals) => {
      if (items.indexOf(key) < 0) return;
      // disable by default if maximum value < 5%
      disabled = d3.max(vals, (d) => d.y)<0.05;
      data.push({
        key: Stops.pprint.get(key),
        values: vals,
        color: Stops.colors[i],
        disabled: disabled
      });
      i += 1;
    });
    return data;
  },
  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.drawChart();
  }
});

export const StopsTable = C.StopsTableBase.extend({
  get_tabular_data: function(){
    let rows = [];

    // create header
    let header = ["Year"];
    header.push.apply(header, Stops.pprint.values());
    rows.push(header);

    return this.add_data_rows(rows, [Stops.races, Stops.ethnicities])
  }
});

export default {
  Stops,
  StopsHandler,
  StopRatioDonut,
  StopRatioTimeSeries,
  StopsTable
};
