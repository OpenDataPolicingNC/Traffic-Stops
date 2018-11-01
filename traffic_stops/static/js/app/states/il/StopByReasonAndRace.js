import Stops from './defaults.js';
import * as C from '../../common/IncidentByReasonAndRace.js';

export const SRRTimeSeries = C.IRRTimeSeriesBase.extend({
  Stops: Stops,
  incident_type: 'stop',
  incident_type_plural: 'stops',

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
    return this.data.raw.stops;
  }
});

const SRRTable = C.IRRTableBase.extend({
  types: [Stops.ethnicities],
  incident_type: 'stop',
  incident_type_plural: 'stops',

  Stops: Stops,

  _get_header_rows: function () {
    return Stops.ethnicities
  },

  _raw_data: function () {
    return this.data.raw.stops;
  }
});


export default {
  SRRTimeSeries,
  SRRTable
};
