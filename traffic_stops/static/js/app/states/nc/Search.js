import { StopsHandler, StopRatioDonut, StopRatioTimeSeries, StopsTable } from './Stops.js';
import * as C from '../../common/Search.js';

const SearchHandler = C.createSearchHandlerBase(StopsHandler);

const SearchRatioDonut = StopRatioDonut.extend({});
const SearchRatioTimeSeries = StopRatioTimeSeries.extend({});
const SearchTable = StopsTable.extend({});

export default {
  SearchHandler,
  SearchRatioDonut,
  SearchRatioTimeSeries,
  SearchTable
};
