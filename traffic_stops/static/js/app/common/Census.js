import DataHandlerBase from '../base/DataHandlerBase.js';
import TableBase from '../base/TableBase.js';
import VisualBase from '../base/VisualBase.js';
import d3 from 'd3';
import $ from 'jquery';

export const CensusHandlerBase = DataHandlerBase.extend({
  clean_data: function () {
    // temporary for dummy census data
    let agency = this.get('agency');
    let raw_data = this.get('raw_data');
    let data;

    if (raw_data instanceof Array) {
      /***
       * If raw_data is an array, then we have probably grabbed a list
       * of agencies with associated census data, which is what
       * census.temporary.json gives us. In that case, we need to filter down
       * the list by the provided agency name to find our agency; this will
       * give us the appropriate data.
       */
      data = raw_data.filter((d) => d.agency === agency)[0];
    } else if (typeof raw_data.census_profile === 'object') {
      /***
       * If raw_data is *not* an array, then it is probably the serialization
       * of a single agency, and it will probably have a census_profile attribute
       * containing the data we're interested in.
       */
      data = raw_data.census_profile;
    } else {
      /***
       * Otherwise, we're in some unknown situation, and we might as well
       * throw an error to signal to the developer that something is up.
       */
      throw 'Census data not recognized'
    }

    if (d3.keys(data).length > 0) {
      let data_map = d3.map(data);
      this.set("data", data_map);
      $('#census_row').show();
      $('#census-link-item').show();
    }

    $('body').scrollspy('refresh');
  }
});

export const CensusRatioDonutBase = VisualBase.extend({
  defaults: {
    showEthnicity: false,
    width: 300,
    height: 300
  },

  Stops: { }, // abstract property, requires override
  _items: function () { throw "abstract method: requires override"; },
  _pprint: function () { throw "abstract method: requires override"; },
  _process_key: function () { throw "abstract method: requires override"; },
  triggerRaceToggle: function () { throw "abstract method: requires override"; },

  setDefaultChart: function () {
    this.chart = nv.models.pieChart()
      .x((d) => d.key)
      .y((d) => d.value)
      .color((d) => d.data.color)
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

  drawStartup: function () {},

  drawChart: function () {
    let data = this._formatData();

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
    let data = [];
    let raw = this.data;
    let items = this._items();

    // build data specifically for this pie chart
    items.forEach((item, i) => {
      data.push({
        "key": this._pprint(item),
        "value": raw.get(this._process_key(item)),
        "color": this.Stops.colors[i]
      });
    });

    return data;
  }
});

export const CensusTableBase = TableBase.extend({
  types: [],
  _get_header_rows: function () { throw "abstract method: requires override"; },
  _process_key: function () { throw "abstract method: requires override"; },

  get_tabular_data: function () {
    let rows = [];
    let data = this.data;
    let fmt = d3.format('.1%');
    let counts = [];
    let percents = [];

    // create header
    {
      let row = [""];
      row.push.apply(row, this._get_header_rows());
      rows.push(row);
    }

    this.types.forEach((type) => {
      let type_counts = type.map((e) => data.get(this._process_key(e)) || 0);
      let sum = d3.sum(type_counts);
      let type_percents = type_counts.map((d) => fmt(d/sum));

      counts.push(type_counts);
      percents.push(type_percents);
    })

    {
      let row = ["Population"];
      counts.forEach((count) => {
        row.push.apply(row, count);
      })
      rows.push(row.map((d) => d.toLocaleString() ));
    }

    {
      let row = ["Percent"];
      percents.forEach((percent) => {
        row.push.apply(row, percent);
      })
      rows.push(row.map((d) => d.toLocaleString() ));
    }

    return rows;
  },

  update: function () {
    TableBase.prototype.update.apply(this, arguments);

    if (this.data === undefined) {
      return;
    }  // temporary for dummy census data

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
