import Stops from './defaults.js';
import * as C from '../../common/Stops.js';

export const StopsHandler = C.StopsHandlerBase.extend({
  types: [Stops.races, Stops.ethnicities],
  Stops: Stops
});

export const StopRatioDonut = C.StopRatioDonutBase.extend({
  defaults: {
    showEthnicity: false,
    width: 300,
    height: 300
  },

  Stops: Stops,

  _items: function () {
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: function (e, v) {
    this.set('showEthnicity', v);
    this.drawChart();
  }
});

export const StopRatioTimeSeries = C.StopRatioTimeSeriesBase.extend({
  defaults: {
    showEthnicity: false,
    width: 750,
    height: 375
  },

  Stops: Stops,

  _items: function () {
    return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.drawChart();
  }
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
