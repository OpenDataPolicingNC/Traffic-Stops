import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import AggregateDataHandlerBase from '../../base/AggregateDataHandlerBase.js';
import Stops from './defaults.js';

import { StopsHandler, StopRatioDonut, StopRatioTimeSeries, StopsTable } from './Stops.js';
import './Stops.js';
import './Search.js';
import './Census.js';
import './StopSearch.js';
import './LikelihoodOfSearch.js';

var _ = require('underscore');
var d3 = require('d3');
var Backbone = require('backbone');
var $ = require('jquery');
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
    [Stops.races, Stops.ethnicities].forEach(function(dataType){
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

var ContrabandHitRateHandler = DataHandlerBase.extend({
  clean_data: function(){

    var years,
        raw = this.get("raw_data");

    // get available years
    years = d3.set(raw.searches.map(function(v){return v.year;})).values();
    years.filter(function(v){return (v >= Stops.start_year);});
    years.push("Total");

    // build totals for all years
    var getTotals = function(arr){
      var total = _.clone(arr[0]);
      _.keys(total).forEach(function(key){
        total[key] = 0;
      });

      // sum data from all years
      arr.forEach(function(year){
        _.keys(year).forEach(function(key){
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

var UseOfForceDonut = StopRatioDonut.extend({});
var UseOfForceBarChart = VisualBase.extend({
  defaults: {
    showEthnicity: false,
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
      .height(this.get("height"));

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
          .attr('preserveAspectRatio', "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
        this.svg
          .find(".nv-x .tick line")
          .css("opacity", "0");
      });
  },
  _formatData: function(){
    var items = (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races,
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
  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.drawChart();
  }
});

var ContrabandHitRateBar = VisualBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.multiBarHorizontalChart()
      .x(function(d){ return d.label; })
      .y(function(d){ return d.value; })
      .barColor(function(d,i){return Stops.colors[1];})
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
  drawStartup: function(){
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
  drawChart: function(){

    d3.select(this.svg[0])
            .datum(this.dataset)
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },
  _getDataset: function(year){
    var raw = this.data.raw,
        searches_arr = raw.searches.filter(function(v){return v.year===year;}),
        contraband_arr = raw.contraband.filter(function(v){return v.year===year;}),
        dataset = {
            color: Stops.single_color,
            key: "Contraband hit-rates",
            values: []
        },
        items = (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races,
        ratio;

    if (searches_arr.length===1 && contraband_arr.length===1){

      searches_arr = searches_arr[0];
      contraband_arr = contraband_arr[0];

      // build a bar for each race
      items.forEach(function(race, i){
        ratio = contraband_arr[race] / searches_arr[race];
        if (!isFinite(ratio)) ratio = undefined;
        dataset.values.push({
          "label": Stops.pprint.get(race),
          "value": ratio
        });
      });

    }
    return [dataset];
  },
  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.selector.trigger('change');
  }
});

var UseOfForceTable = StopsTable.extend({});

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

var RaceToggle = function(updateUrl, showEthnicity){
  this.updateUrl = updateUrl;
  this.showEthnicity = showEthnicity;
}
_.extend(RaceToggle.prototype, {
  render: function($div){
    var id,
        inpDiv = $('<div class="radio">')
          .append('<label><input type="radio" name="raceType" id="raceTypeRace" value="race">Race &nbsp;</label>')
          .append('<label><input type="radio" name="raceType" id="raceTypeEthnicity" value="ethnicity">Ethnicity</label>'),
        container = $('<div class="raceSelector pull-right">')
          .append('<strong>View results by:</strong>')
          .append(inpDiv)
          .insertBefore($div);

    id = (this.showEthnicity) ? "#raceTypeEthnicity" : "#raceTypeRace";
    inpDiv.find(id).prop("checked", true);

    inpDiv.find('input').on('change', (e) => {
      this.showEthnicity = $(e.target).val()==="ethnicity";
      $.post(this.updateUrl, {"showEthnicity": this.showEthnicity});
      $(document).trigger('raceToggle.change', this.showEthnicity);
    });
  }
});

if (typeof window.NC === 'undefined') window.NC = {};

Object.assign(window.NC, {
  UseOfForceHandler,
  ContrabandHitRateHandler,
  ContrabandHitRateBar,
  ContrabandTable,
  UseOfForceDonut,
  UseOfForceBarChart,
  UseOfForceTable,
  RaceToggle
});
