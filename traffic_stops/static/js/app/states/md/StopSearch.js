import Stops from './defaults.js';
import * as C from '../../common/StopSearch.js';

const StopSearchHandler = C.StopSearchHandlerBase.extend({
  Stops: Stops,

  major_type: Stops.ethnicities,

  types: [Stops.ethnicities],

  _pprint: (d) => d
});

const StopSearchTimeSeries = C.StopSearchTimeSeriesBase.extend({
  defaults: {
    showEthnicity: false,
    width: 750,
    height: 375
  },

  Stops: Stops,

  defaultEnabled: ["Total", "White", "Black"],

  _items: () => Stops.ethnicities,

  _pprint: (d) => d,

  triggerRaceToggle: () => null
});

const StopSearchTable = C.StopSearchTableBase.extend({});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
