import _ from 'underscore';
import d3 from 'd3';

import { get_years, get_totals, toTitleCase } from '../util.js';
import DataHandlerBase from '../base/DataHandlerBase.js';
import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';

/*
  NOTE: This should really be used by the StopByReasonAndRace graphs
  instead of the LikelihoodOfSearch handler, but since that
  would add an additional API hit, let's leave it for now.
  For the time being it is used only in the SearchByType graphs.
*/
export const IRRHandlerBase = DataHandlerBase.extend({
  types: [], // abstract property, requires override
  defaults: {}, // abstract property, requires override
  Stops: {}, // abstract property, requires override
  reason_type: '', // abstract property, requires override

  clean_data: function () {
    let raw = this.get("raw_data");
    let years = get_years(raw, this.Stops);

    if (raw.stops && raw.stops.length>0) {
      raw.stops = get_totals(raw.stops, this.types, this.reason_type);
    }

    if (raw.searches && raw.searches.length > 0 ) {
      raw.searches = get_totals(raw.searches, this.types);
    }

    if (!(raw.stops || raw.searches)) {
      raw = get_totals(raw, this.types, this.reason_type);
    }

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});

export const IRRTimeSeriesBase = VisualBase.extend({
  Stops: { }, // abstract property, requires override
  incident_type: '', // abstract property, requires override
  incident_type_plural: '', // abstract property, requires override
  reason_type: '', // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _pprint: function () { throw "abstract method: requires override"; },
  _raw_data: function () { throw "abstract method: requires override"; },

  setDefaultChart: function () {
    this.chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .forceY(0)
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format('.0d'));

    this.chart.yAxis
        .axisLabel('Number of ' + self.incident_type_plural + ' by race')
        .tickFormat(d3.format(',.0d'));
  },

  drawStartup: function () {
    var $selector = $('<select>');
    var reasons = d3.set(_.pluck(this._raw_data(), this.reason_type));
    var $opts = [$('<option value="All">All</option>')].concat(
      reasons
        .values()
        .sort()
        .map((p) => $(`<option value="${p}">${p}</option>`))
    )
    var update = () => {
      var val = $selector.val() || 'All';
      this.dataset = this._getByReason(val);
      this.drawChart();
    }

    $selector
      .append($opts)
      .val('All')
      .on('change', update);

    $('<div class="selector-container">')
      .html($selector)
      .prependTo(this.div);

    update();
  },

  drawChart: function () {
    var data = this.dataset;

    nv.addGraph(() => {
        d3.select(this.svg[0])
          .datum(data)
          .attr('width', "100%")
          .attr('height', "100%")
          .style({ width:  `${this.div.width()}px`
                 , height: `${ (this.get('height') / this.get('width')) * this.div.width() }px` })
          .attr('preserveAspectRatio', "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
      });
  },

  /***
   * Function to return array of years present in dataset.
   */
  _years: function () {
    var years_all = d3.set(_.pluck(this._raw_data(), 'year')).values();
    var years = _.without(years_all, 'Total');
    return years;
  },

  /***
   * Function to return the dataset sorted by "type" and incident reason.
   */
  _getByReason: function (reason) {
    var types = this._items();
    var years = this._years();
    var raw_data, data;

    /***
     * "All" is not a reason found in the data, so we compute it on the fly
     * using the helper method _reasonAll.
     */
    if (reason === 'All') {
      raw_data = this._reasonAll();
    } else {
      raw_data = this._raw_data();
    }

    /***
     * Resulting data shape:

      [
        {
          key: "name of race/ethnicity",
          values: [
            {
              x: 2016,
              y: 123
            }
          ],
          color: '#ffffff'
        }
      ]
     */
    var data = types.map((type, i) => ({
      key: this._pprint(type)
    , values: years.map((year) => ({
        x: year
      , y: (_.find(raw_data, (incident) => (
          String(incident.year) === year
            && incident[this.reason_type] === reason
        )) || {})[type] || 0
    }))
    , color: this.Stops.colors[i]
    }));

    return this._checkThreshold(data);
  },

  /***
   * Helper function to identify data that should not be displayed on
   * initial graph draw because its count is too low.
   *
   * This implementation suppresses data whose max value is less than 5%
   * of the overall max value.
   */
  _checkThreshold: function (data_) {
    var data = _.clone(data_);
    var values = _.flatten(data.map((type) => (type.values.map((value) => value.y))));
    var overall_max = d3.max(values);

    data.forEach((datum) => {
      var local_max = d3.max(datum.values.map((v) => v.y));
      if ((local_max / overall_max) < 0.05) {
        datum.disabled = true;
      }
    });

    return data;
  },

  /***
   * Function to create a virtual "All" reason data object for each year.
   * Iterates through each year returned by _years and sums up the counts for
   * each race/ethnicity.
   */
  _reasonAll: function () {
    var data = [];
    var years = this._years();

    years.forEach((year) => {
      var totals = {
        year,
        [this.reason_type]: 'All'
      };

      var incidents = _.filter(
        this._raw_data(),
        (incident) => (String(incident.year) === year)
      );

      incidents.forEach((incident) => {
        var keys = _.chain(incident)
          .keys()
          .without('year', this.reason_type).
          value();

        keys.forEach((k) => {
          if (typeof totals[k] === 'undefined') {
            totals[k] = 0;
          }

          totals[k] += incident[k];
        });
      });

      data.push(totals);
    });

    return data;
  }
});

export const IRRTableBase = TableBase.extend({
  Stops: { }, // abstract property, requires override
  incident_type: '', // abstract property, requires override
  incident_type_plural: '', // abstract property, requires override
  reason_type: '', // abstract property, requires override
  reason_order_key: '', // abstract property, requires override
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },
  _raw_data: function () { throw "abstract method: requires override"; },

  draw_table: function () {
    TableBase.prototype.draw_table.apply(this, arguments);
    this.add_select();
  },

  _reasons: function () {
    return d3.set(_.pluck(this._raw_data(), this.reason_type));
  },

  add_select: function () {
    let div = $(this.get("selector"));

    // select input  only needs to be added once
    if (div.find('select').length) { return true; }

    let $selector = $(`<select id="${this.get('selector').replace('#', '')}_select">`);
    let reasons = this._reasons();
    let $opts = [$('<option value="All">All</option>')].concat(
      reasons
        .values()
        .sort()
        .map((p) => $(`<option value="${p}">${p}</option>`))
    )

    let update = () => {
      let $window = $(window);
      let initial_scrollpoint = $selector.offset().top - $window.scrollTop();

      let val = $selector.val() || 'All';
      this.set('filter', val);
      this.draw_table();
      /***
       * to prevent disorienting experience of scroll position no longer
       * corresponding to location of selector on the screen.
       */
      $(window).scrollTop($selector.offset().top - initial_scrollpoint);
    }

    $selector
      .append($opts)
      .val('All')
      .on('change', update);

    $('<div class="selector-container">')
      .html($selector)
      .appendTo(div);
  },

  get_tabular_data: function () {
    let reason_filter = (reason) =>
      !this.get('filter')
      || this.get('filter') === 'All'
      || reason === this.get('filter');

    // create row with initial header row
    let rows = [
      ["Year", toTitleCase(this.incident_type) + "-reason", ...this._get_header_rows()]
    ];

    let reasons = this.Stops[this.reason_order_key].keys().filter(reason_filter);
    let incidents = this._raw_data();

    function create_cell (incident_counts={}, race) {
      let incident_count = incident_counts[race] || 0;

      return incident_count.toLocaleString();
    }

    // create data rows
    this.data.years.forEach((yr) => {
      let incidents_by_yr = incidents.filter((d) => d.year == yr);

      reasons.forEach((reason) => {
        let row = [yr, reason];
        let incident_counts = _.find(incidents_by_yr, (d) =>  d[this.reason_type] == reason);

        this.types.forEach((type) => {
          type.forEach((race) => {
            row.push(create_cell(incident_counts, race));
          })
        })

        rows.push(row);
      });
    });

    return rows;
  }
});
