import Stops from './defaults.js';
import * as C from '../../common/StopSearch.js';

const StopSearchHandler = C.StopSearchHandlerBase.extend({
  Stops: Stops,

  major_type: Stops.ethnicities,

  types: [Stops.ethnicities],

  _pprint: (d) => Stops.pprint.get(d)
});

const StopSearchTimeSeries = C.StopSearchTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  Stops: Stops,

  defaultEnabled: ["Total", "White", "Black", "Hispanic"],

  _items: function () {
    return Stops.ethnicities;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },

  triggerRaceToggle: () => null
});

var StopSearchTable = C.StopSearchTableBase.extend({});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
