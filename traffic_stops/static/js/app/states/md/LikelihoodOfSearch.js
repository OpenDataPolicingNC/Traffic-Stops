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
  types: [Stops.ethnicities],
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
    return Stops.ethnicities;
  },

  _base: function () {
    return "White";
  },

  _defRace: function () {
    return "Black";
  },

  _pprint: function (type) {
    return type;
  },

  triggerRaceToggle: () => null
});

var LikelihoodSearchTable = TableBase.extend({
  get_tabular_data: function () {
    var header, row, rows = [];

    // create header
    header = ["Year", "Stop-reason"];
    header.push.apply(header, Stops.ethnicities);
    rows.push(header);

    var stop, search, stop_purp, search_purp, v1, v2,
        purposes = Stops.purpose_order.keys(),
        stops = this.data.raw.stops,
        searches = this.data.raw.searches,
        get_row = (stops, searches, term) => {
          var stop = (stops !== undefined) ? stops[term] : 0,
              search = (searches !== undefined) ? searches[term] : 0;
          return `${search}/${stop}`;
        };

    // create data rows
    this.data.years.forEach((yr) => {
        stop = stops.filter((d) => d.year == yr);
        search = searches.filter((d) => d.year == yr);
        purposes.forEach((purp) => {
          row = [yr, purp];
          stop_purp = (stop.length>0) ? stop.filter((d) => d.purpose == purp): undefined;
          search_purp = (search.length>0) ? search.filter((d) => d.purpose == purp) : undefined;
          stop_purp = (stop_purp && stop_purp.length === 1) ? stop_purp[0] : undefined;
          search_purp = (search_purp && search_purp.length === 1) ? search_purp[0] : undefined;

          Stops.ethnicities.forEach((e) => {
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
