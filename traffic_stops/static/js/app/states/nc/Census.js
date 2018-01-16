import Stops from './defaults.js';
import * as C from '../../common/Census.js';

const CensusHandler = C.CensusHandlerBase;

function process_key (key) {
  return key.replace('-', '_')
}

const CensusRatioDonut = C.CensusRatioDonutBase.extend({
  Stops: Stops,

  _items: function () {
    return Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  _process_key: process_key,
});

var CensusTable = C.CensusTableBase.extend({
  _get_header_rows: function () {
    return Stops.pprint.values();
  },

  _process_key: process_key,

  types: [Stops.races, Stops.ethnicities]
});

export default {
  CensusHandler,
  CensusRatioDonut,
  CensusTable
};
