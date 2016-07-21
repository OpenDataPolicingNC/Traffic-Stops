import DataHandlerBase from '../base/DataHandlerBase.js';
import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';
import d3 from 'd3';
import _ from 'underscore';
import $ from 'jquery';

export function get_years (raw, Stops) {
  let years = d3.set(raw.searches.map((v) => v.year)).values();

  years.filter((v) => (v >= Stops.start_year));
  years.push("Total");

  return years;
}

export function get_totals (xs) {
  let arr = _.clone(xs);
  let total = _.clone(arr[0]);

  _.keys(total).forEach((key) => {
    total[key] = 0;
  });

  // sum data from all years
  arr.forEach((year) => {
    _.keys(year).forEach((key) => {
      total[key] += year[key];
    });
  });

  // push to end of array
  total["year"] = "Total";
  arr.push(total);

  return arr;
}

export const ContrabandHitRateHandlerBase = DataHandlerBase.extend({
  clean_data: function () {

    let raw = this.get("raw_data");
    let years = get_years(raw, this.Stops);

    if (raw.searches.length > 0) {
      raw.searches = get_totals(raw.searches);
    }

    if (raw.contraband.length > 0) {
      raw.contraband = get_totals(raw.contraband);
    }

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});

export const ContrabandHitRateBarBase = VisualBase.extend({
  Stops: { }, // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _pprint: function () { throw "abstract method: requires override"; },
  triggerRaceToggle: function () { throw "abstract method: requires override"; },

  setDefaultChart: function () {
    this.chart = nv.models.multiBarHorizontalChart()
      .x((d) => d.label)
      .y((d) => d.value)
      .barColor((d, i) => this.Stops.colors[1])
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .forceY([0, 1])
      .showLegend(false)
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false);

    this.chart.yAxis
        .axisLabel('Searches resulting in contraband-found')
        .tickFormat(d3.format('%'));

    this.chart.valueFormat(d3.format('%'));
  },

  drawStartup: function () {
    // get year options for pulldown menu
    let selector = $('<select>'),
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

  drawChart: function(){
    d3.select(this.svg[0])
            .datum(this.dataset)
            .attr('width', "100%")
            .attr('height', "100%")
            .style({ width:  `${this.get('width')}px`
                   , height: `${this.get('height')}px` })
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },

  _getDataset: function (year) {
    let raw = this.data.raw,
        searches_arr = raw.searches.filter((v) => v.year === year),
        contraband_arr = raw.contraband.filter((v) => v.year === year),
        dataset = {
            color: this.Stops.single_color,
            key: "Contraband hit-rates",
            values: []
        },
        items = this._items(),
        ratio;

    if (searches_arr.length === 1 && contraband_arr.length === 1) {

      searches_arr = searches_arr[0];
      contraband_arr = contraband_arr[0];

      // build a bar for each type
      items.forEach((type, i) => {
        ratio = (contraband_arr[type] / searches_arr[type]) || 0;
        if (!isFinite(ratio)) ratio = 0;
        dataset.values.push({
          "label": this._pprint(type),
          "value": ratio
        });
      });

    }
    return [dataset];
  }
});

export const ContrabandTableBase = TableBase.extend({
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },

  get_tabular_data: function () {
    var header, row, rows = [], se, cb;

    // create header
    header = ["Year"];
    header.push.apply(header, this._get_header_rows());
    rows.push(header);

    var raw = this.data.raw,
        searches = _.object(_.pluck(raw.searches, 'year'), raw.searches),
        contrabands = _.object(_.pluck(raw.contraband, 'year'), raw.contraband);

    _.keys(searches).forEach((yr) => {
      se = searches[yr];
      cb = contrabands[yr] || {};
      row = [yr];
      this.types.forEach((type) => {
        type.forEach(function(e){
          row.push((cb[e]||0).toLocaleString() + "/" + (se[e]||0).toLocaleString());
        });
      })
      rows.push(row);
    });

    return rows;
  }
});
