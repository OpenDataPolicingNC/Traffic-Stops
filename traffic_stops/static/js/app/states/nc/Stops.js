import Stops from './defaults.js';
import * as C from '../../common/Stops.js';

export const StopsHandler = C.StopsHandlerBase.extend({
  types: [Stops.races],
  Stops: Stops
});

export const StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    width: 300,
    height: 300
  },

  Stops: Stops,

  _items: function () {
    return Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },
});

export const StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  Stops: Stops,

  _items: function () {
    return Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },
});

export const StopsTable = C.StopsTableBase.extend({
  types: [Stops.races],

  _get_header_rows: function () {
    return Stops.pprint.values();
  }
});

export default {
  Stops,
  StopsHandler,
  StopRatioDonut,
  StopRatioTimeSeries,
  StopsTable
};
