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

var LikelihoodOfSearch = C.LikelihoodOfSearchBase.extend({
  defaults: {
    showEthnicity: true,
    width: 750,
    height: 375,
    Stops: Stops
  },

  _items: function () {
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _base: function () {
    return (this.get('showEthnicity')) ? "non-hispanic" : "white"
  },

  _defRace: function () {
    return (this.get('showEthnicity')) ? "hispanic" : "black"
  },

  _pprint: function (type) {
    return this.defaults.Stops.pprint.get(type);
  },

  triggerRaceToggle: function (e, v) {
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
