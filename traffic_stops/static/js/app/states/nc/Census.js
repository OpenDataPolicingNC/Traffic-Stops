import Stops from './defaults.js';
import * as C from '../../common/Census.js';

const CensusHandler = C.CensusHandlerBase;

const CensusRatioDonut = C.CensusRatioDonutBase.extend({
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

var CensusTable = C.CensusTableBase.extend({
  _get_header_rows: function () {
    return Stops.pprint.values();
  },

  types: [Stops.races, Stops.ethnicities]
});

export default {
  CensusHandler,
  CensusRatioDonut,
  CensusTable
};
