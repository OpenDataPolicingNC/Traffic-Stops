import DataHandlerBase from '../../base/DataHandlerBase.js';
import VisualBase from '../../base/VisualBase.js';
import TableBase from '../../base/TableBase.js';
import Stops from './defaults.js';

import _ from 'underscore';
import d3 from 'd3';
import Backbone from 'backbone';
import $ from 'jquery';

Backbone.$ = $;

var CensusHandler = DataHandlerBase.extend({
  clean_data: function(){
    // temporary for dummy census data
    var agency = this.get('agency'),
        data = this.get("raw_data").filter(function(d){return d.agency===agency;});
    if(data.length>0){
      data = d3.map(data[0]);
      this.set("data", data);
      $('#census_row').show();
      $('#census-link-item').show();
    }

    $('body').scrollspy('refresh');
  }
});

var CensusRatioDonut = VisualBase.extend({
  defaults: {
    showEthnicity: false,
    width: 300,
    height: 300
  },
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
  drawStartup: function(){},
  drawChart: function(){
    var data = this._formatData();

    nv.addGraph(() => {
      d3.select(this.svg[0])
          .datum(data)
          .style({ width:  `${this.div.width()}px`
                 , height: `${this.div.width()}px` })
        .transition().duration(1200)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', `0 0 ${this.get('width')} ${this.get('height')}`)
          .call(this.chart);
    });
  },
  _formatData: function(){
    var data = [],
        raw = this.data,
        items = (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;

    // build data specifically for this pie chart
    items.forEach(function(race, i){
      data.push({
        "key": Stops.pprint.get(race),
        "value": raw.get(race),
        "color": Stops.colors[i]
      });
    });

    return data;
  },
  triggerRaceToggle: function(e, v){
    this.set('showEthnicity', v);
    this.drawChart();
  }
});

var CensusTable = TableBase.extend({
  get_tabular_data: function(){
    var row, rows = [], data = this.data, fmt = d3.format('.1%'),
        nRaces, nEthnicities, totalRace, totalEthnicity, pRaces, pEthnicities;

    // create header
    row = [""];
    row.push.apply(row, Stops.pprint.values());
    rows.push(row);

    nRaces = Stops.races.map(function(r){ return (data.get(r)||0); });
    nEthnicities = Stops.ethnicities.map(function(e){ return (data.get(e)||0); });

    totalRace = d3.sum(nRaces);
    totalEthnicity = d3.sum(nEthnicities);

    pRaces = nRaces.map(function(d){return fmt(d/totalRace);});
    pEthnicities = nEthnicities.map(function(d){return fmt(d/totalEthnicity);});

    // create data rows
    row = ["Population"];
    row.push.apply(row, nRaces);
    row.push.apply(row, nEthnicities);
    rows.push(row.map(function(d){return d.toLocaleString();}));

    row = ["Percent"];
    row.push.apply(row, pRaces);
    row.push.apply(row, pEthnicities);
    rows.push(row);

    return rows;
  },
  update: function(){
    TableBase.prototype.update.apply(this, arguments);
    if(this.data===undefined) return;  // temporary for dummy census data

    // add extra-styling to separate data-types
    $(this.get("selector"))
          .find('tr th:nth-child(1),td:nth-child(1)')
          .css("border-right", "1px solid #dddddd");
    $(this.get("selector"))
          .find('tr th:nth-child(6),td:nth-child(6)')
          .css("border-right", "1px solid #dddddd");

    // add help-text
    $('<p class="help-block">')
      .text(this.data.get('derivation_notes'))
      .appendTo($(this.get("selector")));
  }
});

export default {
  CensusHandler,
  CensusRatioDonut,
  CensusTable
};
