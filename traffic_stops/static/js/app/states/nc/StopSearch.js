import Stops from './defaults.js';
import * as C from '../../common/StopSearch.js';

const StopSearchHandler = C.StopSearchHandlerBase.extend({
  Stops: Stops,

  major_type: Stops.races,

  types: [Stops.races],

  _pprint: (d) => Stops.pprint.get(d)
});

const StopSearchTimeSeries = C.StopSearchTimeSeriesBase.extend({
  defaults: {
    width: 750,
    height: 375
  },

  Stops: Stops,

  defaultEnabled: ["Total", "White", "Black"],

  _items: function () {
    return Stops.races;
  },

  _pprint: function (type) {
    return Stops.pprint.get(type);
  },
});

var StopSearchTable = C.StopSearchTableBase.extend({});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
