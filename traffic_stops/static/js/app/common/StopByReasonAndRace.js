import _ from 'underscore';
import d3 from 'd3';

import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';

export const SRRTimeSeriesBase = VisualBase.extend({
  Stops: { }, // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _pprint: function () { throw "abstract method: requires override"; },

  setDefaultChart: function () {
    this.chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format('.0d'));

    this.chart.yAxis
        .axisLabel('Number of stops by race')
        .tickFormat(d3.format('.0d'));
  },

  drawStartup: function () {
    var $selector = $('<select>');
    var purposes = d3.set(_.pluck(this.data.raw.stops, 'purpose'));
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
      .appendTo(this.div);

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

  _years: _.memoize(function () {
    var years_all = d3.set(_.pluck(this.data.raw.stops, 'year')).values();
    var years = _.without(years_all, 'Total');
    return years;
  }),

  _getByPurpose: _.memoize(function (purpose) {
    var types = this._items();
    var years = this._years();
    var raw_data, data;

    if (purpose === 'All') {
      raw_data = this._purposeAll();
    } else {
      raw_data = this.data.raw.stops;
    }

    var data = types.map((type, i) => ({
      key: this._pprint(type)
    , values: years.map((year) => ({
        x: year
      , y: (_.find(raw_data, (stop) => (
          String(stop.year) === year
            && stop.purpose === purpose
        )) || {})[type] || 0
    }))
    , color: this.Stops.colors[i]
    }));

    return this._checkThreshold(data);
  }),

  _checkThreshold: function (data_) {
    var data = _.clone(data_);
    var values = _.flatten(data.map((type) => (type.values.map((value) => value.y))));
    var overall_max = d3.max(values);

    data.forEach((datum) => {
      var local_max = d3.max(datum.values.map((v) => v.y));
      if ((local_max / overall_max) < 0.1) {
        datum.disabled = true;
      }
    });

    return data;
  },

  _purposeAll: _.memoize(function () {
    var data = [];
    var years = this._years();

    years.forEach((year) => {
      var totals = {
        year
      , purpose: 'All'
      };

      var stops = _.filter(
        this.data.raw.stops
      , (stop) => (String(stop.year) === year)
      );

      stops.forEach((stop) => {
        var keys = _.chain(stop)
          .keys()
          .without('year', 'purpose').
          value();

        keys.forEach((k) => {
          if (typeof totals[k] === 'undefined') {
            totals[k] = 0;
          }

          totals[k] += stop[k];
        });
      });

      data.push(totals);
    });

    return data;
  })
});

export const SRRTableBase = TableBase.extend({});
