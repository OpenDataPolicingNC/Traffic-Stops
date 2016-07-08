import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var ContrabandHitRateHandler = DataHandlerBase.extend({
  clean_data: function () {

    var years,
        raw = this.get("raw_data");

    // get available years
    years = d3.set(raw.searches.map((v) => v.year)).values();
    years.filter((v) => (v >= Stops.start_year));
    years.push("Total");

    // build totals for all years
    var getTotals = (arr) => {
      var total = _.clone(arr[0]);
      _.keys(total).forEach((key) => {
        total[key] = 0;
      });

      // sum data from all years
      arr.forEach((year) => {
        _.keys(year).forEach((key) => {
          total[key] += year[key];
        });
      });

      // push to end of array
      total["year"] = "Total";
      arr.push(total);
    };

    if (raw.searches.length>0) getTotals(raw.searches);
    if (raw.contraband.length>0) getTotals(raw.contraband);

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});

// dashboard visuals

var ContrabandHitRateBar = VisualBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375
  },

  setDefaultChart: function () {
    this.chart = nv.models.multiBarHorizontalChart()
      .x((d) => d.label)
      .y((d) => d.value)
      .barColor((d, i) => Stops.colors[1])
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .forceY([0, 1])
      .showLegend(false)
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false);

    this.chart.yAxis
        .axisLabel('Searches resulting in contraband-found')
        .tickFormat(d3.format('%'));

    this.chart.valueFormat(d3.format('%'));
  },

  drawStartup: function () {
    // get year options for pulldown menu
    var selector = $('<select>'),
        year_options = this.data.years,
        opts = year_options.map((v) => `<option value="${v}">${v}</option>`),
        getData = () => {
          var year = selector.val();
          year = parseInt(year, 10) || year;
          this.dataset =  this._getDataset(year);
          this.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData)
      .trigger('change');

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    this.selector = selector;
  },

  drawChart: function () {

    d3.select(this.svg[0])
            .datum(this.dataset)
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },

  _getDataset: function (year) {
    var raw = this.data.raw,
        searches_arr = raw.searches.filter((v) => v.year===year),
        contraband_arr = raw.contraband.filter((v) => v.year===year),
        dataset = {
            color: Stops.single_color,
            key: "Contraband hit-rates",
            values: []
        },
        items = Stops.ethnicities,
        ratio;

    if (searches_arr.length===1 && contraband_arr.length===1){

      searches_arr = searches_arr[0];
      contraband_arr = contraband_arr[0];

      // build a bar for each ethnicity
      items.forEach((ethnicity, i) => {
        ratio = (contraband_arr[ethnicity] / searches_arr[ethnicity]) || 0;
        if (!isFinite(ratio)) ratio = undefined;
        dataset.values.push({
          "label": ethnicity,
          "value": ratio
        });
      });

    }
    return [dataset];
  },

  triggerRaceToggle: () => null
});

var ContrabandTable = TableBase.extend({
  get_tabular_data: function () {
    var header, row, rows = [], se, cb;

    // create header
    header = ["Year"];
    header.push.apply(header, Stops.ethnicities);
    rows.push(header);

    var raw = this.data.raw,
        searches = _.object(_.pluck(raw.searches, 'year'), raw.searches),
        contrabands = _.object(_.pluck(raw.contraband, 'year'), raw.contraband);

    _.keys(searches).forEach((yr) => {
      se = searches[yr];
      cb = contrabands[yr] || {};
      row = [yr];
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
