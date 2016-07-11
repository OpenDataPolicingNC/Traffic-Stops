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
  defaults: Stops
});

export const StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    width: 300,
    height: 300
  },

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (x) {
    return x;
  }

  triggerRaceToggle: () => null
});

export const StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  _formatData: function(){
    let data = [],
        items = Stops.ethnicities,
        subset = [],
        i = 0,
        disabled;

    this.data.line.forEach((key, vals) => {
      if (items.indexOf(key) < 0) return;
      // disable by default if maximum value < 5%
      disabled = d3.max(vals, (d) => d.y)<0.05;
      data.push({
        key: key,
        values: vals,
        color: Stops.colors[i],
        disabled: disabled
      });
      i += 1;
    });

    return data;
  },

  triggerRaceToggle: () => null
});

export const StopsTable = C.StopsTableBase.extend({
  get_tabular_data: function(){
    let rows = [];

    // create header
    let header = ["Year"];
    header.push.apply(header, Stops.ethnicities);
    rows.push(header);

    return this.add_data_rows(rows, [Stops.ethnicities]);
  }
});

export default {
  StopsHandler,
  StopRatioDonut,
  StopRatioTimeSeries,
  StopsTable
};
