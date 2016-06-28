import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import Backbone from 'backbone';
import _ from 'underscore';
import d3 from 'd3';
import $ from 'jquery';
Backbone.$ = $;

/***
 * StopsHandler data processing helper functions
 */
export function build_totals (data) {
  let total = {};
  // build a 'Totals' year which sums by ethnicity for all years
  if (data.length > 0) {
    // create new totals object, and reset values
    total = _.clone(data[0]);

    _.keys(total).forEach((key) => {
      total[key] = 0;
    });

    // sum data from all years
    data.forEach((year) => {
      _.keys(year).forEach((key) => {
        total[key] += year[key];
      });
    });

    total['year'] = 'Total';
  }

  return total;
}

export function build_pie_data (data, total, Stops) {
  let pie = d3.map();

  data.forEach((v) => {
    if (v.year >= Stops.start_year) pie.set(v.year, d3.map(v));
  });

  pie.set('Total', d3.map(total));

  return pie;
}

export function get_total_by_race (dataType, yr) {
  var total = 0;
  dataType.forEach((ethnicity) => {
    total += yr[ethnicity];
  });
  return total;
}

export function build_line_data (data, Stops) {
  var line = d3.map();

  Stops.ethnicities.forEach((v) => {
    line.set(v, []);
  });
  data.forEach((yr) => {
    if (yr.year >= Stops.start_year) {
      var total = get_total_by_race(Stops.ethnicities, yr);
      Stops.ethnicities.forEach((ethnicity) => {
        line.get(ethnicity).push({x: yr.year, y:yr[ethnicity]/total});
      })
    }
  })
  return line;
}

export var StopsHandler = DataHandlerBase.extend({
  clean_data: function () {

    // build totals
    var data = this.get('raw_data');
    var total = build_totals(data);

    // build-data for pie-chart
    var pie = build_pie_data(data, total, Stops);

    // build data for line-chart
    var line = build_line_data(data, Stops);

    // set object data
    this.set('data', {
      type: 'stop',
      raw: this.get('raw_data'),
      pie: pie,
      line: line
    });
  }
});

export var StopRatioDonut = VisualBase.extend({
  defaults: {
    width: 300,
    height: 300
  },

  setDefaultChart: function(){
    this.chart = nv.models.pieChart()
      .x((d) => d.key)
      .y((d) => d.value)
      .color((d) => d.data.color)
      .width(this.get("width"))
      .height(this.get("height"))
      .showLabels(true)
      .labelType("percent")
      .donutRatio(0.35)
      .labelThreshold(0.05)
      .donut(true);
  },
  drawStartup: function(){

    // get year options for pulldown menu
    var selector = $('<select>'),
        year_options = this.data.pie.keys(),
        opts = year_options.map((v) => `<option value="${v}">${v}</option>`),
        getData = () => {
          var value = selector.val();
          this.dataset =  this.data.pie.get(value);
          this.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData);

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    getData();
  },
  drawChart: function(){
    var data = this._formatData();

    nv.addGraph(() => {
      d3.select(this.svg[0])
          .datum(data)
        .transition().duration(1200)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
    });
  },
  _formatData: function(){
    var data = [],
        selected = this.dataset,
        items = Stops.ethnicities;

    // build data specifically for this pie chart
    items.forEach((d, i) => {
      if (!d) return;
      data.push({
        "key": Stops.pprint.get(d),
        "value": selected.get(d),
        "color": Stops.colors[i]
      });
    });

    return data;
  },
  triggerRaceToggle: () => null
});

var StopRatioTimeSeries = VisualBase.extend({
  defaults: {
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .forceY([0, 1])
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year');

    this.chart.yAxis
        .axisLabel('Percentage of stops by race')
        .tickFormat(d3.format('%'));
  },
  drawStartup: function(){},
  drawChart: function(){
    var data = this._formatData();

    nv.addGraph(() => {
        d3.select(this.svg[0])
          .datum(data)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr('preserveAspectRatio', "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
      });
  },
  _formatData: function(){
    var data = [],
        items = Stops.ethnicities,
        subset = [],
        i = 0,
        disabled;

    this.data.line.forEach(function(key, vals){
      if (items.indexOf(key) < 0) return;
      // disable by default if maximum value < 5%
      disabled = d3.max(vals, function(d){return d.y;})<0.05;
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
  triggerRaceToggle: () => null
});

var StopsTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    header = ["Year"];
    header.push.apply(header, Stops.pprint.values());
    rows.push(header);

    // create data rows
    this.data.pie.forEach(function(k, v){
      row = [k];
      Stops.ethnicities.forEach(function(e){ row.push((v.get(e)||0).toLocaleString()); });
      rows.push(row);
    });

    return rows;
  }
});

if (typeof window.MD === 'undefined') window.MD = {};

Object.assign(window.MD, {
  StopsHandler,
  StopRatioDonut,
  StopRatioTimeSeries,
  StopsTable
});
