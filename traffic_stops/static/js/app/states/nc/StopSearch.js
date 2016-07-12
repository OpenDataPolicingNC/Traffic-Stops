import AggregateDataHandlerBase from '../../base/AggregateDataHandlerBase.js';
import TableBase from '../../base/TableBase.js';
import { StopRatioTimeSeries } from './Stops.js';
import Stops from './defaults.js';

import * as C from '../../common/StopSearch.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

const StopSearchHandler = C.StopSearchHandlerBase.extend({
  Stops: Stops,

  major_type: Stops.races,

  types: [Stops.races, Stops.ethnicities],

  _pprint: (d) => Stops.pprint.get(d)
});

var StopSearchTimeSeries = StopRatioTimeSeries.extend({
  setDefaultChart: function(){
    this.chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year');

    this.chart.yAxis
        .tickFormat(d3.format('%'));
  },
  _formatData: function(){

    var data = StopSearchTimeSeries.__super__._formatData.call(this),
        total = this.data.line.get('total'),
        defaultEnabled = ["Total", "White", "Black", "Hispanic", "Non-hispanic"];

    // add total-line
    data.push({
      key: "Total",
      values: total,
      color: Stops.baseline_color,
      disabled: false
    });

    // predefine enabled/disabled lines on chart
    _.each(data, function(d){
      d.disabled = defaultEnabled.indexOf(d.key) === -1;
    });

    return data;
  },
});

var StopSearchTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    rows.push(this.data.table_headers);

    // create data rows
    _.each(this.data.table, function(k, v){
      rows.push(k)
    });

    return rows;
  }
});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
