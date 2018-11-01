import _ from 'underscore';
import d3 from 'd3';

import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';

export const IRRTimeSeriesBase = VisualBase.extend({
  Stops: { }, // abstract property, requires override
  _incident_type: '', // abstract property, requires override
  _incident_type_plural: '', // abstract property, requires override
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
    var purposes = d3.set(_.pluck(this._raw_data(), 'purpose'));
    var $opts = [$('<option value="All">All</option>')].concat(
      purposes
        .values()
        .sort()
        .map((p) => $(`<option value="${p}">${p}</option>`))
    )
    var update = () => {
      var val = $selector.val() || 'All';
      this.dataset = this._getByPurpose(val);
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
   * Pure function to return array of years present in dataset.
   */
  _years: _.memoize(function () {
    var years_all = d3.set(_.pluck(this._raw_data(), 'year')).values();
    var years = _.without(years_all, 'Total');
    return years;
  }),

  /***
   * Pure function to return the dataset sorted by "type" and stop purpose.
   */
  _getByPurpose: _.memoize(function (purpose) {
    var types = this._items();
    var years = this._years();
    var raw_data, data;

    /***
     * "All" is not a purpose found in the data, so we compute it on the fly
     * using the helper method _purposeAll.
     */
    if (purpose === 'All') {
      raw_data = this._purposeAll();
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
            && incident.purpose === purpose
        )) || {})[type] || 0
    }))
    , color: this.Stops.colors[i]
    }));

    return this._checkThreshold(data);
  }),

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
   * Pure function to create a virtual "All" purpose data object for each year.
   * Iterates through each year returned by _years and sums up the counts for
   * each race/ethnicity.
   */
  _purposeAll: _.memoize(function () {
    var data = [];
    var years = this._years();

    years.forEach((year) => {
      var totals = {
        year
      , purpose: 'All'
      };

      var incidents = _.filter(
        this._raw_data()
      , (incident) => (String(incident.year) === year)
      );

      incidents.forEach((incident) => {
        var keys = _.chain(incident)
          .keys()
          .without('year', 'purpose').
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
  })
});

export const IRRTableBase = TableBase.extend({
  Stops: { }, // abstract property, requires override
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },

  draw_table: function () {
    TableBase.prototype.draw_table.apply(this, arguments);
    this.add_select();
  },

  _purposes: _.memoize(function () {
    return d3.set(_.pluck(this._raw_data(), 'purpose'));
  }),

  add_select: function () {
    let div = $(this.get("selector"));

    // select input  only needs to be added once
    if (div.find('select').length) { return true; }

    let $selector = $('<select id="srr-table-select">');
    let purposes = this._purposes();
    let $opts = [$('<option value="All">All</option>')].concat(
      purposes
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
    let purpose_filter = (purpose) =>
      !this.get('filter')
      || this.get('filter') === 'All'
      || purpose === this.get('filter');

    // create row with initial header row
    let rows = [
      ["Year", this.incident_type.charAt(0).toUpperCase() + this.incident_type.slice(1) + "-reason", ...this._get_header_rows()]
    ];

    let purposes = this.Stops.purpose_order.keys().filter(purpose_filter);
    let incidents = this._raw_data();

    function create_cell (incident_counts={}, race) {
      let incident_count = incident_counts[race] || 0;

      return incident_count.toLocaleString();
    }

    // create data rows
    this.data.years.forEach((yr) => {
      let incidents_by_yr = incidents.filter((d) => d.year == yr);

      purposes.forEach((purp) => {
        let row = [yr, purp];
        let incident_counts = _.find(incidents_by_yr, (d) =>  d.purpose == purp);

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
