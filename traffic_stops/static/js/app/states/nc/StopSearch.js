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
    showEthnicity: false,
    width: 750,
    height: 375
  },

  Stops: Stops,

  defaultEnabled: ["Total", "White", "Black", "Hispanic", "Non-hispanic"],

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

var StopSearchTable = C.StopSearchTableBase.extend({});

export default {
  StopSearchHandler,
  StopSearchTimeSeries,
  StopSearchTable
};
