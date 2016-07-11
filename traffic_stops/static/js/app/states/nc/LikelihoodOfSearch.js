import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import * as C from '../../common/LikelihoodOfSearch.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var LikelihoodSearchHandler = C.LikelihoodSearchHandlerBase.extend({
  types: [Stops.races, Stops.ethnicities],
  defaults: Stops
});

var LikelihoodOfSearch = VisualBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.multiBarHorizontalChart()
      .x(function(d){ return d.label; })
      .y(function(d){ return d.value; })
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false);

    this.chart.yAxis
        .axisLabel('Additional percentage or search by search-cause')
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
    var dataset = [],
        raw = this.data.raw,
        stops_arr = raw.stops.filter(function(v){return v.year===year;}),
        searches_arr = raw.searches.filter(function(v){return v.year===year;}),
        stops = d3.map(),
        searches = d3.map(),
        items = (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races,
        base = (this.get('showEthnicity')) ? "non-hispanic" : "white",
        defRace = (this.get('showEthnicity')) ? "hispanic" : "black",
        baseUpper = function(d){return d.charAt(0).toUpperCase() + d.slice(1);}(base);

    // turn arrays into maps with purpose as the key
    stops_arr.forEach(function(v){
      stops.set(v.purpose, v);
    });
    searches_arr.forEach(function(v){
      searches.set(v.purpose, v);
    });

    // build a set of bars for each race, except for base
    items.forEach(function(race, i){
      if(race === base) return;

      var bar = {
          color: Stops.colors[i],
          key: `${Stops.pprint.get(race)} vs. ${baseUpper}`,
          values: [],
          disabled: (race !== defRace)
      };

      // build a bar for each violation
      Stops.purpose_order.forEach(function(purpose){
        // optional reporting requirement; remove as it's generally unreported
        if (purpose === "Checkpoint") return;

        // calculate percent-difference of stops which led to searches by race,
        // in comparison to base-baseline
        var search = searches.get(purpose),
            stop  = stops.get(purpose);

        if (search && stop){

          var rate, base_rate, r_rate,
              base_se = search[base] || 0,
              base_st = stop[base] || 0,
              r_se = search[race] || 0,
              r_st = stop[race] || 0;

          base_rate = base_se/base_st;
          r_rate = r_se/r_st;
          rate = (r_rate-base_rate)/base_rate;
          if(!r_rate || !isFinite(rate)) rate = 0;

          // add purpose to list of values
          bar.values.push({
            label: purpose,
            value: rate,
            order: Stops.purpose_order.get(purpose)
          });
        }
      });

      // sort bars and then push race to list
      bar.values.sort(function(a,b){return a.order-b.order;});
      dataset.push(bar);
    });

    return dataset;
  },
  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.selector.trigger('change');
  }
});

var LikelihoodSearchTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    header = ["Year", "Stop-reason"];
    header.push.apply(header, Stops.pprint.values());
    rows.push(header);

    var stop, search, stop_purp, search_purp, v1, v2,
        purposes = Stops.purpose_order.keys(),
        stops = this.data.raw.stops,
        searches = this.data.raw.searches,
        get_row = function(stops, searches, term){
          var stop = (stops !== undefined) ? stops[term] : 0,
              search = (searches !== undefined) ? searches[term] : 0;
          return `${search}/${stop}`;
        };

    // create data rows
    this.data.years.forEach(function(yr){
        stop = stops.filter(function(d){return d.year == yr;});
        search = searches.filter(function(d){return d.year == yr;});
        purposes.forEach(function(purp){
          row = [yr, purp];
          stop_purp = (stop.length>0) ? stop.filter(function(d){return d.purpose == purp;}): undefined;
          search_purp = (search.length>0) ? search.filter(function(d){return d.purpose == purp;}) : undefined;
          stop_purp = (stop_purp && stop_purp.length === 1) ? stop_purp[0] : undefined;
          search_purp = (search_purp && search_purp.length === 1) ? search_purp[0] : undefined;

          Stops.races.forEach(function(r){
            row.push(get_row(stop_purp, search_purp, r));
          });

          Stops.ethnicities.forEach(function(e){
            row.push(get_row(stop_purp, search_purp, e));
          });

          rows.push(row);
        });
    });

    return rows;
  }
});

export default {
  LikelihoodSearchHandler,
  LikelihoodOfSearch,
  LikelihoodSearchTable
};
