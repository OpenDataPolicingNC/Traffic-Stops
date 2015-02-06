// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; try { args.callee = f.caller } catch(e) {}; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};

// make it safe to use console.log always
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

// printf helper function for strings
String.prototype.printf = function(){
    //http://stackoverflow.com/questions/610406/
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number){
        return typeof args[number] !== 'undefined' ? args[number] : match;
    });
};

// Traffic Stops global defaults
var Stops = {
  start_year: 2002,                    // start-year for reporting requirement
  races: [
    'white',
    'black',
    'native_american',
    'asian',
    'other'
  ],
  race_pprint: d3.map({
    'white': 'White',
    'black': 'Black',
    'native_american': 'Native American',
    'asian': 'Asian',
    'other': 'Other'
  }),
  ethnicities: [
    'hispanic',
    'non-hispanic'
  ],
  ethnicity_pprint: d3.map({
    'hispanic': 'Hispanic',
    'non-hispanic': 'Non-hispanic'
  }),
  colors: [
    "#fdae61",
    "#a6d96a",
    "#1a9641",
    "#d7191c",
    "#2BC2F0"
  ],
  single_color: "#5C0808",
  purpose_order: d3.map({
    'Driving While Impaired': 0,
    'Safe Movement Violation': 1,
    'Vehicle Equipment Violation': 2,
    'Other Motor Vehicle Violation': 3,
    'Investigation': 4,
    'Stop Light/Sign Violation': 5,
    'Speed Limit Violation': 6,
    'Vehicle Regulatory Violation': 7,
    'Seat Belt Violation': 8,
    'Checkpoint': 9  // todo: use a list and indexOf instead of map
  })
  };


// data handlers to get raw-data
DataHandlerBase = Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.get_data();
  },
  get_data: function(){
    var self = this;
    d3.json(this.get("url"), function(error, data) {
      if(error) return self.trigger("dataRequestFailed");
      self.set("raw_data", data);
      self.set("data", undefined);
      self.clean_data();
      self.trigger("dataLoaded", self.get("data"));
    });
  },
  clean_data: function(){
    throw "abstract method: requires override";
  }
});

CensusHandler  = DataHandlerBase.extend({
  clean_data: function(){
    // temporary for dummy census data
    var agency = this.get('agency'),
        data = this.get("raw_data").filter(function(d){return d.agency===agency;});
    if(data.length>0){
      data = d3.map(data[0]);
      this.set("data", data);
    } else {
      $('#census_row').remove();
    }
  }
});

StopsHandler = DataHandlerBase.extend({
  clean_data: function(){

    var data = this.get("raw_data"),
        total = {};

    // build a "Totals" year which sums by race/ethnicity for all years
    if (data.length>0){
      // create new totals object, and reset values
      total = _.clone(data[0]);
      _.keys(total).forEach(function(key){
        total[key] = 0;
      });

      // sum data from all years
      data.forEach(function(year){
        _.keys(year).forEach(function(key){
          total[key] += year[key];
        });
      });
      total["year"] = "Total";
    }

    // build-data for pie-chart
    var pie = d3.map();
    data.forEach(function(v){
      if (v.year>=Stops.start_year) pie.set(v.year, d3.map(v));
    });
    pie.set("Total", d3.map(total));

    // build data for line-chart

    var line = d3.map(),
        get_total_by_race = function(yr){
          var total = 0;
          Stops.races.forEach(function(race){
            total += yr[race];
          });
          return total;
        };
    Stops.races.forEach(function(v){
      line.set(v, []);
    });
    data.forEach(function(yr){
      if (yr.year>=Stops.start_year){
        var total = get_total_by_race(yr);
        Stops.races.forEach(function(race){
          line.get(race).push({x: yr.year, y:yr[race]/total});
        });
      }
    });

    // set object data
    this.set("data",
      {
        pie: pie,
        line: line
      });
  }
});

SearchHandler = StopsHandler.extend({});
UseOfForceHandler = StopsHandler.extend({});

LikelihoodSearchHandler = DataHandlerBase.extend({
  clean_data: function(){

    var years,
        raw = this.get("raw_data");

    // get available years
    years = d3.set(raw.stops.map(function(v){return v.year;})).values();
    years.filter(function(v){return (v >= Stops.start_year);});
    years.push("Total");

    // get total searches/stops for all years by purpose
    var getTotals = function(arr){
      // calculate total for all years by purpose; push to array
      var purposes = d3.nest()
                       .key(function(d) { return d.purpose; })
                       .entries(arr);

      purposes.forEach(function(v){
        // create new totals object, and reset race/ethnicity-values
        var total = _.clone(v.values[0]);

        _.keys(total).forEach(function(key){
          if ((Stops.races.indexOf(key)>=0) ||
              (Stops.ethnicities.indexOf(key)>=0)) {
            total[key] = 0;
          }
        });

        // sum data from all years
        v.values.forEach(function(year){
          _.keys(year).forEach(function(key){
            if ((Stops.races.indexOf(key)>=0) ||
                (Stops.ethnicities.indexOf(key)>=0)) {
              total[key] += year[key];
            }
          });
        });
        total["year"] = "Total";
        arr.push(total);
      });
    };

    if (raw.stops.length>0) getTotals(raw.stops);
    if (raw.searches.length>0) getTotals(raw.searches);

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});

ContrabandHitRateHandler = DataHandlerBase.extend({
  clean_data: function(){

    var years,
        raw = this.get("raw_data");

    // get available years
    years = d3.set(raw.searches.map(function(v){return v.year;})).values();
    years.filter(function(v){return (v >= Stops.start_year);});
    years.push("Total");

    // build totals for all years
    var getTotals = function(arr){
      var total = _.clone(arr[0]);
      _.keys(total).forEach(function(key){
        total[key] = 0;
      });

      // sum data from all years
      arr.forEach(function(year){
        _.keys(year).forEach(function(key){
          total[key] += year[key];
        });
      });

      // push to end of array
      total["year"] = "Total";
      arr.push(total);
    };

    if (raw.searches.length>0) getTotals(raw.searches);
    if (raw.contraband.length>0) getTotals(raw.contraband);

    // set cleaned-data to handler
    this.set("data", {
      years: years,
      raw: raw
    });
  }
});


// dashboard visuals
VisualBase = Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.listenTo(this.get("handler"), "dataLoaded", this.update);
    this.listenTo(this.get("handler"), "dataRequestFailed", this.showError);
    this.setDOM();
    this.loader_show();
    this.setDefaultChart();
  },
  setDOM: function(){
    this.svg = $(this.get("selector"));
    this.div = $(this.svg).parent();
  },
  loader_show: function(){
    this.loader_div = $('<div>')
          .append('<p>Loading ... <i class="fa fa-cog fa-spin"></i></p>')
          .prependTo(this.div);
  },
  showError: function(){
    this.loader_hide();
    this.error_div = $('<div class="bg-warning">')
          .append('<p>An error occurred in fetching the data.</p>')
          .prependTo(this.div);
  },
  loader_hide: function(){
    this.loader_div.remove();
  },
  update: function(data){
    if(data===undefined) return;  // temporary for dummy census data
    this.data = data;
    this.loader_hide();
    this.drawStartup();
    this.drawChart();
  },
  drawStartup: function(){
    throw "abstract method: requires override";
  },
  drawChart: function(){
    throw "abstract method: requires override";
  },
  setDefaultChart: function(){
    throw "abstract method: requires override";
  }
});

CensusRatioDonut = VisualBase.extend({
  defaults: {
    width: 300,
    height: 300
  },
  setDefaultChart: function(){
    this.chart = nv.models.pie()  // change to pie-chart
      .x(function(d){ return d.key; })
      .y(function(d){ return d.value; })
      .color(function(d){ return d.data.color; })
      .width(this.get("width"))
      .height(this.get("height"))
      .showLabels(true)
      .labelType("percent")
      .donutRatio(0.35)
      .labelThreshold(0.05)
      .donut(true);
  },
  drawStartup: function(){},
  drawChart: function(){
    var self = this,
        data = this._formatData();

    nv.addGraph(function() {
      d3.select(self.svg[0])
          .datum(data)
        .transition().duration(1200)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', '0 0 {0} {1}'.printf(self.get("width"), self.get("height")))
          .call(self.chart);
    });
  },
  _formatData: function(){
    var data = [],
        raw = this.data;

    // build data specifically for this pie chart
    Stops.races.forEach(function(race, i){
        data.push({
          "key": Stops.race_pprint.get(race),
          "value": raw.get(race),
          "color": Stops.colors[i]
        });
    });

    return [data];
  }
});

StopRatioDonut = VisualBase.extend({
  defaults: {
    width: 300,
    height: 300
  },
  setDefaultChart: function(){
    this.chart = nv.models.pie()
      .x(function(d){ return d.key; })
      .y(function(d){ return d.value; })
      .color(function(d){ return d.data.color; })
      .width(this.get("width"))
      .height(this.get("height"))
      .showLabels(true)
      .labelType("percent")
      .donutRatio(0.35)
      .labelThreshold(0.05)
      .donut(true);
  },
  drawStartup: function(){

    // get year options for pulldown menu
    var self = this,
        selector = $('<select>'),
        year_options = this.data.pie.keys(),
        opts = year_options.map(function(v){return '<option value="{0}">{0}</option>'.printf(v);}),
        getData = function(){
          var value = selector.val();
          self.dataset =  self.data.pie.get(value);
          self.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData);

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    getData();
  },
  drawChart: function(){
    var self = this,
        data = this._formatData();

    nv.addGraph(function() {
      d3.select(self.svg[0])
          .datum(data)
        .transition().duration(1200)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', '0 0 {0} {1}'.printf(self.get("width"), self.get("height")))
          .call(self.chart);
    });
  },
  _formatData: function(){
    var data = [],
        selected = this.dataset;

    // build data specifically for this pie chart
    Stops.races.forEach(function(race, i){
        data.push({
          "key": Stops.race_pprint.get(race),
          "value": selected.get(race),
          "color": Stops.colors[i]
        });
    });

    return [data];
  }
});

StopRatioTimeSeries = VisualBase.extend({
  defaults: {
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
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
        .axisLabel('Year');

    this.chart.yAxis
        .axisLabel('Percentage of stops by race')
        .tickFormat(d3.format('%'));
  },
  drawStartup: function(){},
  drawChart: function(){
    var self = this,
        data = this._formatData();

    nv.addGraph(function() {
        d3.select(self.svg[0])
          .datum(data)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr('preserveAspectRatio', "xMinYMin")
          .attr('viewBox', "0 0 {0} {1}".printf(self.get("width"), self.get("height")))
          .call(self.chart);
      });
  },
  _formatData: function(){

    var data = [];

    this.data.line.entries().forEach(function(v, i){
      data.push({
        key: Stops.race_pprint.get(v.key),
        values: v.value,
        color: Stops.colors[i]
      });
    });
    return data;
  }
});

LikelihoodOfSearch = VisualBase.extend({
  defaults: {
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.multiBarHorizontalChart()
      .x(function(d){ return d.label; })
      .y(function(d){ return d.value; })
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false);

    this.chart.yAxis
        .axisLabel('Additional percentage or search by search-cause')
        .tickFormat(d3.format('%'));

    this.chart.valueFormat(d3.format('%'));
  },
  drawStartup: function(){
    // get year options for pulldown menu
    var self = this,
        selector = $('<select>'),
        year_options = this.data.years,
        opts = year_options.map(function(v){return '<option value="{0}">{0}</option>'.printf(v);}),
        getData = function(){
          var year = selector.val();
          year = parseInt(year, 10) || year;
          self.dataset =  self._getDataset(year);
          self.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData);

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    getData();
  },
  drawChart: function(){

    d3.select(this.svg[0])
            .datum(this.dataset)
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', "0 0 {0} {1}".printf(this.get("width"), this.get("height")))
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },
  _getDataset: function(year){
    var dataset = [],
        raw = this.data.raw,
        stops_arr = raw.stops.filter(function(v){return v.year===year;}),
        searches_arr = raw.searches.filter(function(v){return v.year===year;}),
        stops = d3.map(),
        searches = d3.map();

    // turn arrays into maps with purpose as the key
    stops_arr.forEach(function(v){
      stops.set(v.purpose, v);
    });
    searches_arr.forEach(function(v){
      searches.set(v.purpose, v);
    });

    // build a set of bars for each race, except for white
    Stops.races.forEach(function(race, i){
      if(race === "white") return;

      var bar = {
          color: Stops.colors[i],
          key: "{0} vs. White".printf(Stops.race_pprint.get(race)),
          values: []
      };

      // build a bar for each violation
      Stops.purpose_order.forEach(function(purpose){
        // optional reporting requirement; remove as it's generally unreported
        if (purpose === "Checkpoint") return;

        // calculate percent-difference of stops which led to searches by race,
        // in comparison to white-baseline
        var search = searches.get(purpose),
            stop  = stops.get(purpose);

        if (search && stop){

          var rate, w_rate, r_rate,
              w_se = search.white || 0,
              w_st = stop.white || 0,
              r_se = search[race] || 0,
              r_st = stop[race] || 0;

          w_rate = w_se/w_st;
          r_rate = r_se/r_st;
          rate = (r_rate-w_rate)/w_rate;

          // add purpose to list of values
          bar.values.push({
            label: purpose,
            value: rate,
            order: Stops.purpose_order.get(purpose)
          });

        }
      });

      // sort bars and then push race to list
      bar.values.sort(function(a,b){return a.order-b.order;});
      dataset.push(bar);
    });

    return dataset;
  }
});

SearchRatioDonut = StopRatioDonut.extend({});
SearchRatioTimeSeries = StopRatioTimeSeries.extend({});

UseOfForceDonut = StopRatioDonut.extend({});
UseOfForceTimeSeries = StopRatioTimeSeries.extend({});

ContrabandHitRateBar = VisualBase.extend({
  defaults: {
    width: 750,
    height: 375
  },
  setDefaultChart: function(){
    this.chart = nv.models.multiBarHorizontalChart()
      .x(function(d){ return d.label; })
      .y(function(d){ return d.value; })
      .width(this.get("width"))
      .height(this.get("height"))
      .margin({top: 20, right: 50, bottom: 20, left: 180})
      .showValues(true)
      .tooltips(true)
      .transitionDuration(350)
      .showControls(false);

    this.chart.yAxis
        .axisLabel('Searches resulting in contraband-found')
        .tickFormat(d3.format('%'));

    this.chart.valueFormat(d3.format('%'));
  },
  drawStartup: function(){
    // get year options for pulldown menu
    var self = this,
        selector = $('<select>'),
        year_options = this.data.years,
        opts = year_options.map(function(v){return '<option value="{0}">{0}</option>'.printf(v);}),
        getData = function(){
          var year = selector.val();
          year = parseInt(year, 10) || year;
          self.dataset =  self._getDataset(year);
          self.drawChart();
        };

    selector
      .append(opts)
      .val("Total")
      .on('change', getData);

    $('<div>')
      .html(selector)
      .appendTo(this.div);

    getData();
  },
  drawChart: function(){

    d3.select(this.svg[0])
            .datum(this.dataset)
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', "0 0 {0} {1}".printf(this.get("width"), this.get("height")))
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },
  _getDataset: function(year){
    var raw = this.data.raw,
        searches_arr = raw.searches.filter(function(v){return v.year===year;}),
        contraband_arr = raw.contraband.filter(function(v){return v.year===year;}),
        dataset = {
            color: Stops.single_color,
            key: "Contraband hit-rates",
            values: []
        };

    if (searches_arr.length===1 && contraband_arr.length===1){

      searches_arr = searches_arr[0];
      contraband_arr = contraband_arr[0];

      // build a bar for each race
      Stops.races.forEach(function(race, i){
        var ratio = contraband_arr[race] / searches_arr[race];
        dataset.values.push({
          "label": Stops.race_pprint.get(race),
          "value": ratio
        });
      });

    }

    return [dataset];
  }
});

// dashboard tables
TableBase = Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.listenTo(this.get("handler"), "dataLoaded", this.update);
    this.listenTo(this.get("handler"), "dataRequestFailed", this.showError);
  },
  update: function(data){
    if(data===undefined) return;  // temporary for dummy census data
    this.data = data;
    this.draw_table();
  },
  get_tabular_data: function(){
    // should return list of lists, one list per row
    throw "abstract method: requires override";
  },
  showError: function(){
    var div = $(this.get("selector")),
        error_div = $('<div class="bg-warning">')
          .append('<p>An error occurred in fetching the data.</p>')
          .prependTo(div);
  },
  draw_table: function(){
    var div = $(this.get("selector")),
        matrix = this.get_tabular_data(),
        tbl = $('<table>').attr("class", "table table-striped table-condensed dash-tables");

    matrix.forEach(function(row, i){

      if(i===0){
        var cols = $('<colgroup>');

      }

      var tr = $('<tr>');
      row.forEach(function(d){
        var cell = (i === 0) ? $('<th>') : $('<td>');
        tr.append(cell.append(d));
      });
      tbl.append(tr);
    });
    div.prepend(tbl);
  }
});

CensusTable = TableBase.extend({
  get_tabular_data: function(){
    var row, rows = [], data = this.data, fmt = d3.format('.1%'),
        nRaces, nEthnicities, totalRace, totalEthnicity, pRaces, pEthnicities;

    // create header
    row = [""];
    row.push.apply(row, Stops.race_pprint.values());
    row.push.apply(row, Stops.ethnicity_pprint.values());
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

StopsTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    header = ["Year"];
    header.push.apply(header, Stops.race_pprint.values());
    header.push.apply(header, Stops.ethnicity_pprint.values());
    rows.push(header);

    // create data rows
    this.data.pie.forEach(function(k, v){
      row = [k];
      Stops.races.forEach(function(r){ row.push((v.get(r)||0).toLocaleString()); });
      Stops.ethnicities.forEach(function(e){ row.push((v.get(e)||0).toLocaleString()); });
      rows.push(row);
    });

    return rows;
  }
});

SearchTable = StopsTable.extend({});
UseOfForceTable = StopsTable.extend({});

ContrabandTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    header = ["Year"];
    header.push.apply(header, Stops.race_pprint.values());
    header.push.apply(header, Stops.ethnicity_pprint.values());
    rows.push(header);

    // create data rows
    this.data.raw.contraband.forEach(function(v){
      row = [v.year];
      Stops.races.forEach(function(r){ row.push(v[r]||0).toLocaleString(); });
      Stops.ethnicities.forEach(function(e){ row.push(v[e]||0).toLocaleString(); });
      rows.push(row);
    });

    return rows;
  }
});

LikelihoodSearchTable = TableBase.extend({
  get_tabular_data: function(){
    var header, row, rows = [];

    // create header
    header = ["Year", "Stop-reason"];
    header.push.apply(header, Stops.race_pprint.values());
    header.push.apply(header, Stops.ethnicity_pprint.values());
    rows.push(header);

    var stop, search, stop_purp, search_purp, v1, v2,
        purposes = Stops.purpose_order.keys(),
        stops = this.data.raw.stops,
        searches = this.data.raw.searches,
        get_row = function(stops, searches, term){
          var stop = (stops !== undefined) ? stops[term] : 0,
              search = (searches !== undefined) ? searches[term] : 0;
          return "{0}/{1}".printf(search, stop);
        };

    // create data rows
    this.data.years.forEach(function(yr){
        stop = stops.filter(function(d){return d.year == yr;});
        search = searches.filter(function(d){return d.year == yr;});
        purposes.forEach(function(purp){
          row = [yr, purp];
          stop_purp = (stop.length>0) ? stop.filter(function(d){return d.purpose == purp;}): undefined;
          search_purp = (search.length>0) ? search.filter(function(d){return d.purpose == purp;}) : undefined;
          stop_purp = (stop_purp && stop_purp.length === 1) ? stop_purp[0] : undefined;
          search_purp = (search_purp && search_purp.length === 1) ? search_purp[0] : undefined;

          Stops.races.forEach(function(r){
            row.push(get_row(stop_purp, search_purp, r));
          });

          Stops.ethnicities.forEach(function(e){
            row.push(get_row(stop_purp, search_purp, e));
          });

          rows.push(row);
        });
    });

    return rows;
  }
});
