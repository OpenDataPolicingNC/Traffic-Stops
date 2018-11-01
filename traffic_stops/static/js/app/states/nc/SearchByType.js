import d3 from 'd3';

import DataHandlerBase from '../../base/DataHandlerBase.js';
import Stops from './defaults.js';
import { StopsHandler } from './Stops.js';
import * as C from '../../common/IncidentByReasonAndRace.js';

export const STHandler = C.IRRHandlerBase.extend({
  Stops: Stops,
  types: [Stops.ethnicities],
  reason_type: 'search_type'
});

export const STTimeSeries = C.IRRTimeSeriesBase.extend({
  Stops: Stops,
  incident_type: 'search',
  incident_type_plural: 'searches',
  reason_type: 'search_type',

  defaults: {
    width: 750,
    height: 375,
  },

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (x) {
    return x;
  },

  _raw_data: function () {
    return this.data.raw;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  }
});

const STTable = C.IRRTableBase.extend({
  types: [Stops.ethnicities],

  Stops: Stops,
  incident_type: 'search',
  incident_type_plural: 'searches',
  reason_type: 'search_type',
  reason_order_key: 'search_type_order',

  _get_header_rows: function () {
    return Stops.pprint.values();
  },

  _raw_data: function () {
    return this.data.raw;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  }
});


export default {
  STHandler,
  STTimeSeries,
  STTable
};
