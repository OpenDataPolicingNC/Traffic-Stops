import Stops from './defaults.js';
import * as C from '../../common/IncidentByReasonAndRace.js';

export const SRRTimeSeries = C.IRRTimeSeriesBase.extend({
  Stops: Stops,
  incident_type: 'stop',
  incident_type_plural: 'stops',
  reason_type: 'purpose',

  defaults: {
    width: 750,
    height: 375,
  },

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  _raw_data: function () {
    return this.data.raw.stops;
  }
});

const SRRTable = C.IRRTableBase.extend({
  types: [Stops.ethnicities],

  Stops: Stops,
  incident_type: 'stop',
  incident_type_plural: 'stops',
  reason_type: 'purpose',
  reason_order_key: 'purpose_order',

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
