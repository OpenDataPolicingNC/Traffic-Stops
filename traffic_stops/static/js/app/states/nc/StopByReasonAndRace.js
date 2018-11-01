import Stops from './defaults.js';
import * as C from '../../common/StopByReasonAndRace.js';

export const SRRTimeSeries = C.SRRTimeSeriesBase.extend({
  Stops: Stops,

  defaults: {
    width: 750,
    height: 375,
  },

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  }
});

const SRRTable = C.SRRTableBase.extend({
  types: [Stops.ethnicities],

  Stops: Stops,

  _get_header_rows: function () {
    return Stops.ethnicities
  }
});


export default {
  SRRTimeSeries,
  SRRTable
};
