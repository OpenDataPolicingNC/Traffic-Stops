import DataHandlerBase from '../base/DataHandlerBase.js';
import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';
import d3 from 'd3';
import _ from 'underscore';
import $ from 'jquery';

export function get_years (raw, Stops) {
  let years = d3.set(raw.stops.map((v) => v.year)).values();

  years.filter((v) => (v >= Stops.start_year));
  years.push("Total");

  return years;
}

export function get_totals (a, types) {
  // calculate total for all years by purpose; push to array
  let arr = _.clone(a);

  var purposes = d3.nest()
                   .key((d) => d.purpose)
                   .entries(arr);

  purposes.forEach((v) => {
    // create new totals object, and reset race/ethnicity-values
    var total = _.clone(v.values[0]);

    _.keys(total).forEach((key) => {
      if (_.some(types, (t) => t.indexOf(key) >= 0)) {
        total[key] = 0;
      }
    });

    // sum data from all years
    v.values.forEach((year) => {
      _.keys(year).forEach((key) => {
        if (_.some(types, (t) => t.indexOf(key) >= 0)) {
          total[key] += year[key];
        }
      });
    });

    total["year"] = "Total";
    arr.push(total);
  });

  return arr;
}

export const LikelihoodSearchHandlerBase = DataHandlerBase.extend({
  types: [],
  defaults: {},

  clean_data: function () {
    let raw = this.get("raw_data");
    let years = get_years(raw, this.Stops);

    if (raw.stops.length>0) {
      raw.stops = get_totals(raw.stops, this.types);
    }

    if (raw.searches.length > 0 ) {
      raw.searches = get_totals(raw.searches, this.types);
    }

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});

export const LikelihoodOfSearchBase = VisualBase.extend({
  defaults: { }, // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _base: function () { throw "abstract method: requires override"; },
  _defRace: function () { throw "abstract method: requires override"; },
  triggerRaceToggle: function () { throw "abstract method: requires override"; },

  setDefaultChart: function () {
    this.chart = nv.models.multiBarHorizontalChart()
      .x((d) => d.label)
      .y((d) => d.value)
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false)
      .tooltipContent((key, y, e, graph) => `
        <h3 class="stops donut-label">${ key }</h3>
        <p>${ y }</p>
        <p>${ e }</p>
      `);

    this.chart.yAxis
        .axisLabel('Additional percentage or search by search-cause')
        .tickFormat(d3.format('%'));

    this.chart.valueFormat(d3.format('%'));
  },

  drawStartup: function () {
    // get year options for pulldown menu
    var selector = $('<select>'),
        year_options = this.data.years,
        opts = year_options.map((v) => `<option value="${v}">${v}</option>`),
        getData = () => {
          var year = selector.val();
          year = parseInt(year, 10) || year;
          this.dataset =  this._getDataset(year);
          this.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData)
      .trigger('change');

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    this.selector = selector;
  },

  drawChart: function () {
    d3.select(this.svg[0])
      .datum(this.dataset)
      .attr('width', "100%")
      .attr('height', "100%")
      .style({ width:  `${this.div.width()}px`
             , height: `${ (this.get('height') / this.get('width')) * this.div.width() }px` })
      .attr('preserveAspectRatio', "xMinYMin")
      .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
      .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },

  _getDataset: function (year) {
    var dataset = [],
        raw = this.data.raw,
        stops_arr = raw.stops.filter((v) => v.year === year),
        searches_arr = raw.searches.filter((v) => v.year === year),
        stops = d3.map(),
        searches = d3.map(),
        items = this._items(),
        base = this._base(),
        defRace = this._defRace(),
        baseUpper = ((d) => d.charAt(0).toUpperCase() + d.slice(1))(base);

    // turn arrays into maps with purpose as the key
    stops_arr.forEach((v) => {
      stops.set(v.purpose, v);
    });
    searches_arr.forEach((v) => {
      searches.set(v.purpose, v);
    });

    // build a set of bars for each race, except for base
    items.forEach((race, i) => {
      if (race === base) return;

      var bar = {
          color: this.Stops.colors[i],
          key: `${this._pprint(race)} vs. ${baseUpper}`,
          values: [],
          disabled: (race !== defRace)
      };

      // build a bar for each violation
      this.Stops.purpose_order.forEach((purpose) => {
        // optional reporting requirement; remove as it's generally unreported
        if (purpose === "Checkpoint") return;

        // calculate percent-difference of stops which led to searches by race,
        // in comparison to base-baseline
        var search = searches.get(purpose),
            stop  = stops.get(purpose);

        if (search && stop){

          var rate, base_rate, r_rate,
              base_se = search[base] || 0,
              base_st = stop[base] || 0,
              r_se = search[race] || 0,
              r_st = stop[race] || 0;

          base_rate = base_se/base_st;
          r_rate = r_se/r_st;
          rate = (r_rate-base_rate)/base_rate;
          if(!r_rate || !isFinite(rate)) rate = 0;

          // add purpose to list of values
          bar.values.push({
            label: purpose,
            value: rate,
            order: this.Stops.purpose_order.get(purpose)
          });
        }
      });

      // sort bars and then push race to list
      bar.values.sort((a,b) => a.order - b.order);
      dataset.push(bar);
    });

    return dataset;
  }
});

export const LikelihoodSearchTableBase = TableBase.extend({
  Stops: { }, // abstract property, requires override
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },

  get_tabular_data: function () {
    // create row with initial header row
    let rows = [
      ["Year", "Stop-reason"].concat(this._get_header_rows())
    ];

    let purposes = this.Stops.purpose_order.keys();
    let stops = this.data.raw.stops;
    let searches = this.data.raw.searches;

    function create_cell (stop_counts={}, search_counts={}, race) {
      let stop_count = stop_counts[race] || 0;
      let search_count = search_counts[race] || 0;

      return `${search_count}/${stop_count}`;
    }

    // create data rows
    this.data.years.forEach((yr) => {
        let stops_by_yr = stops.filter((d) => d.year == yr);
        let searches_by_yr = searches.filter((d) => d.year == yr);

        purposes.forEach((purp) => {
          let row = [yr, purp];
          let stop_counts = _.find(stops_by_yr, (d) =>  d.purpose == purp);
          let search_counts = _.find(searches_by_yr, (d) => d.purpose == purp);

          this.types.forEach((type) => {
            type.forEach((race) => {
              row.push(create_cell(stop_counts, search_counts, race));
            })
          })

          rows.push(row);
        });
    });

    return rows;
  }
});
