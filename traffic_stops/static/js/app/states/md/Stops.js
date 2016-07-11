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

export var StopsHandler = DataHandlerBase.extend({
  clean_data: function () {

    // build totals
    var data = this.get('raw_data');
    var total = C.build_totals(data);

    // build data for pie-chart
    var pie = C.build_pie_data(data, total, Stops);

    // build data for line-chart
    var line = C.build_line_data(data, [Stops.ethnicities], Stops);

    // set object data
    this.set('data', {
      type: 'stop',
      raw: this.get('raw_data'),
      pie: pie,
      line: line
    });
  }
});

export var StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    width: 300,
    height: 300
  },

  _formatData: function () {
    var data = [],
        selected = this.dataset,
        items = Stops.ethnicities;

    // build data specifically for this pie chart
    items.forEach((d, i) => {
      if (!d) return;
      data.push({
        "key": d,
        "value": selected.get(d) || 0,
        "color": Stops.colors[i]
      });
    });

    return data;
  },

  triggerRaceToggle: () => null
});

export var StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  _formatData: function(){
    var data = [],
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

export var StopsTable = C.StopsTableBase.extend({
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
