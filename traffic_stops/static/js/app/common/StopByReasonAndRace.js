import _ from 'underscore';
import d3 from 'd3';

import VisualBase from '../base/VisualBase.js';
import TableBase from '../base/TableBase.js';

export const SRRTimeSeriesBase = VisualBase.extend({
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
        .axisLabel('Number of stops by race')
        .tickFormat(d3.format('%'));
  },

  drawStartup: function () {
    var $selector = $('<select>');
    var purposes = d3.set(_.pluck(this.data.raw.stops, 'purpose'));
    var $opts = purposes.values().map((p) => $(`<option value="${p}">${p}</option>`));

    $selector
      .append($opts)
      .val('Seat Belt Violation');

    $('<div class="selector-container">')
      .html($selector)
      .appendTo(this.div);
  },

  drawChart: function () {
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

  _formatData: function () {
    return [];
  }
});

export const SRRTableBase = TableBase.extend({});
