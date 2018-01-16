import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import { StopRatioDonut, StopsTable } from './Stops.js';
import Stops from './defaults.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var UseOfForceHandler = DataHandlerBase.extend({
  clean_data: function(){

    var data = this.get("raw_data"),
        pie = d3.map(),
        line = d3.map(),
        total = {};

    // build a "Totals" year which sums by race/ethnicity for all years
    if (data.length>0){
      // create new totals object, and reset values
      total = _.clone(data[0]);
      _.keys(total).forEach(function(key){
        total[key] = 0;
      });

      // sum data from all years
      data.forEach(function(year){
        _.keys(year).forEach(function(key){
          total[key] += year[key];
        });
      });
      total["year"] = "Total";
    }

    // build-data for pie-chart
    data.forEach(function(v){
      if (v.year>=Stops.start_year) pie.set(v.year, d3.map(v));
    });
    pie.set("Total", d3.map(total));

    // build data for line-chart
    [Stops.races].forEach(function(dataType){
      dataType.forEach(function(v){
        line.set(v, []);
      });
      data.forEach(function(yr){
        if (yr.year>=Stops.start_year){
          dataType.forEach(function(race){
            line
              .get(race)
              .push({
                x: yr.year,
                y: (yr[race] > 0 ? yr[race] : 0)
              })
            ;
          });
        }
      });
    });

    // set object data
    this.set("data", {
      type: "stop",
      raw: this.get("raw_data"),
      pie: pie,
      line: line
    });
  }
});

var UseOfForceDonut = StopRatioDonut.extend({});
var UseOfForceBarChart = VisualBase.extend({
  defaults: {
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.multiBarChart()
      .transitionDuration(350)
      .reduceXTicks(false)
      .rotateLabels(0)
      .showControls(true)
      .groupSpacing(0.1)
      .width(this.get("width"))
      .height(this.get("height"))
      .tooltipContent((key, y, e, graph) => `
        <h3 class="stops donut-label">${ key }</h3>
        <p>${ e } in ${ y }</p>
      `);

    this.chart.xAxis
        .axisLabel('Year');

    this.chart.yAxis
        .axisLabel('Number stops by race')
        .tickFormat(d3.format('d'));
  },
  drawStartup: function(){},
  drawChart: function(){
    var data = this._formatData();

    nv.addGraph(() => {
        d3.select(this.svg[0])
          .datum(data)
          .attr('width', "100%")
          .attr('height', "100%")
          .style({ width:  `${this.div.width()}px`
                 , height: `${ (this.get('height') / this.get('width')) * this.div.width() }px` })
          .attr('preserveAspectRatio', "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
        this.svg
          .find(".nv-x .tick line")
          .css("opacity", "0");
      });
  },
  _formatData: function(){
    var items = Stops.races,
        subset = [],
        i = 0,
        data = [],
        disabled;

    this.data.line.forEach(function(key, vals){
      if (items.indexOf(key) < 0) return;
      // disable by default if maximum value 1
      disabled = d3.max(vals, function(d){return d.y;})<1;
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
});

var UseOfForceTable = StopsTable.extend({});

export default {
  UseOfForceHandler,
  UseOfForceDonut,
  UseOfForceBarChart,
  UseOfForceTable
};
