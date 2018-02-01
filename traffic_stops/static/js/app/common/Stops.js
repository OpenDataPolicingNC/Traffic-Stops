import _ from 'underscore';
import d3 from 'd3';

import DataHandlerBase from '../base/DataHandlerBase.js';
import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';

/***
 * StopsHandler data processing helper functions
 */
export function build_totals (data) {
  let total = {};
  // build a 'Totals' year which sums by ethnicity for all years
  if (data.length > 0) {
    // create new totals object, and reset values
    total = _.clone(data[0]);

    _.keys(total).forEach((key) => {
      total[key] = 0;
    });

    // sum data from all years
    data.forEach((year) => {
      _.keys(year).forEach((key) => {
        if (key === 'OTHER') return; // ignore 'OTHER' from bad API output
        if (typeof total[key] === 'undefined') total[key] = 0;
        total[key] += (typeof year[key] === 'undefined') ? 0 : year[key];
      });
    });

    total['year'] = 'Total';
  }

  return total;
}

export function build_pie_data (data, total, Stops) {
  let pie = d3.map();

  data.forEach((v) => {
    if (v.year >= Stops.start_year) pie.set(v.year, d3.map(v));
  });

  pie.set('Total', d3.map(total));

  return pie;
}

export function get_total_by_type (dataType, yr) {
  var total = 0;
  dataType.forEach((type) => {
    total += (typeof yr[type] === 'undefined') ? 0 : yr[type];
  });
  return total;
}

export function build_line_data (data, types, Stops) {
  var line = d3.map();

  types.forEach((dataType) => {
    dataType.forEach((v) => {
      line.set(v, []);
    });
    data.forEach((yr) => {
      if (yr.year >= Stops.start_year) {
        var total = get_total_by_type(dataType, yr);
        dataType.forEach((type) => {
          line.get(type).push({x: yr.year, y:(yr[type] > 0 ? yr[type]/total : 0)});
        })
      }
    })
  });

  return line;
}

export const StopsHandlerBase = DataHandlerBase.extend({
  types: [],
  Stops: {},

  clean_data: function () {

    // build totals
    let data = this.get('raw_data');
    let total = build_totals(data);

    // build data for pie-chart
    let pie = build_pie_data(data, total, this.Stops);

    // build data for line-chart
    let line = build_line_data(data, this.types, this.Stops);

    // set object data
    this.set('data', {
      type: 'stop',
      raw: this.get('raw_data'),
      pie: pie,
      line: line
    });
  }
})

export const StopRatioDonutBase = VisualBase.extend({
  Stops: { }, // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _pprint: function () { throw "abstract method: requires override"; },

  setDefaultChart: function(){
    this.chart = nv.models.pieChart()
      .x(function(d){ return d.key; })
      .y(function(d){ return d.value; })
      .color(function(d){ return d.data.color; })
      .width(this.get("width"))
      .height(this.get("height"))
      .showLabels(true)
      .labelType("percent")
      .donutRatio(0.35)
      .labelThreshold(0.05)
      .donut(true)
      .tooltipContent((key, y, e, graph) => (
        `<h3 class="stops donut-label">${ key }</h3><p>${ y.replace(/\.\d*/, '') }</p>`
      ));
  },

  drawStartup: function () {

    // get year options for pulldown menu
    var selector = $('<select>'),
        year_options = this.data.pie.keys(),
        opts = year_options.map((v) => `<option value="${v}">${v}</option>`),
        getData = () => {
          var value = selector.val();
          this.dataset =  this.data.pie.get(value);
          this.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData);

    $('<div class="selector-container">')
      .html(selector)
      .appendTo(this.div);

    getData();
  },


  drawChart: function(){
    var data = this._formatData();

    nv.addGraph(() => {
      d3.select(this.svg[0])
          .datum(data)
          .attr('width', "100%")
          .attr('height', "100%")
          .style({ width:  `${this.div.width()}px`
                 , height: `${ (this.get('height') / this.get('width')) * this.div.width() }px` })
        .transition().duration(1200)
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
    });
  },

  _formatData: function () {
    let data = [],
        selected = this.dataset,
        items = this._items();

    // build data specifically for this pie chart
    items.forEach((d, i) => {
      if (!d) return;
      data.push({
        "key": this._pprint(d),
        "value": selected.get(d) || 0,
        "color": this.Stops.colors[i]
      });
    });

    return data;
  }
});

export const StopRatioTimeSeriesBase = VisualBase.extend({
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
                  .forceY([0, 1])
                  .width(this.get("width"))
                  .height(this.get("height"));

    this.chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format('.0d'));

    this.chart.yAxis
        .axisLabel('Percentage of stops by race')
        .tickFormat(d3.format('%'));
  },

  drawStartup: function () {},

  drawChart: function(){
    var data = this._formatData();

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


  _formatData: function(){
    let data = [],
        items = this._items(),
        subset = [],
        i = 0,
        disabled;

    this.data.line.forEach((key, vals) => {
      if (items.indexOf(key) < 0) return;
      // disable by default if maximum value < 5%
      disabled = d3.max(vals, (d) => d.y) < 0.05;
      data.push({
        key: this._pprint(key),
        values: vals,
        color: this.Stops.colors[i],
        disabled: disabled
      });
      i += 1;
    });

    return data;
  },
});


export const StopsTableBase = TableBase.extend({
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },

  add_data_rows: function (rows = [], categories) {
    // create data rows
    this.data.pie.forEach((k, v) => {
      let row = [k];
      categories.forEach((type) => {
        type.forEach((r) => {
          row.push(
            (v.get(r) || 0).toLocaleString()
          );
        });
      })
      rows.push(row);
    });

    return rows;
  },

  get_tabular_data: function(){
    let rows = [];

    // create header
    let header = ["Year"];
    header.push.apply(header, this._get_header_rows());
    rows.push(header);

    return this.add_data_rows(rows, this.types)
  }
});
