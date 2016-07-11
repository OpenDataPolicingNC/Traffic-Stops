import { StopsHandler, StopRatioDonut, StopRatioTimeSeries, StopsTable } from './Stops.js';
import * as C from '../../common/Search.js';

var SearchHandler = C.createSearchHandlerBase(StopsHandler);

var SearchRatioDonut = StopRatioDonut.extend({});
var SearchRatioTimeSeries = StopRatioTimeSeries.extend({});
var SearchTable = StopsTable.extend({});

export default {
  SearchHandler,
  SearchRatioDonut,
  SearchRatioTimeSeries,
  SearchTable
};
