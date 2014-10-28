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
  race_pprint: {
    'white': 'White',
    'black': 'Black',
    'native_american': 'Native American',
    'asian': 'Asian',
    'other': 'Other'
  },
  ethnicities: [
    'hispanic',
    'non-hispanic'
  ],
  colors: [
    "#fdae61",
    "#a6d96a",
    "#1a9641",
    "#d7191c",
    "#2BC2F0"
  ],
  violations: d3.map({
    1:  {order: 6, label: 'Speed Limit Violation'},
    2:  {order: 5, label: 'Stop Light/Sign Violation'},
    3:  {order: 0, label: 'Driving While Impaired'},
    4:  {order: 1, label: 'Safe Movement Violation'},
    5:  {order: 2, label: 'Vehicle Equipment Violation'},
    6:  {order: 7, label: 'Vehicle Regulatory Violation'},
    7:  {order: 8, label: 'Seat Belt Violation'},
    8:  {order: 4, label: 'Investigation'},
    9:  {order: 3, label: 'Other Motor Vehicle Violation'},
    10: {order: 9, label: 'Checkpoint'}
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
      if(error) return console.warn(error);
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

LikelihoodStopsHandler  = DataHandlerBase.extend({
  clean_data: function(){
    // create 2-D array of the data, each row is a stop-reason and column is
    // race. Also create d3.map for columns
    var rows = d3.map(),
        cols = d3.map(),
        data = [];

    var len = Stops.races.keys().length;
    // make zeroed array-template, set rows
    Stops.violations.keys().forEach(function(key, i){
      rows.set(key, i);
      data.push(Array.apply(null, new Array(len)).map(Number.prototype.valueOf,0));
    });

    // set columns
    Stops.races.keys().forEach(function(key, i){
      cols.set(Stops.races.get(key), i);
    });

    // apply data to template
    this.get("raw_data").forEach(function(v){
      v = d3.map(v);
      var row = rows.get(v.get('purpose'));
      v.keys().forEach(function(key){
        var col = cols.get(Stops.races.get(key));
        if(col) data[row][col] = v.get(key);
      });
    });

    this.set("data", {
      rows: rows,
      cols: cols,
      data: data
    });
  }
});


// dashboard visuals
VisualBase = Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.listenTo(this.get("handler"), "dataLoaded", this.update);
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
  loader_hide: function(){
    this.loader_div.remove();
  },
  update: function(data){
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
          "key": Stops.race_pprint[race],
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
        key: Stops.race_pprint[v.key],
        values: v.value,
        color: Stops.colors[i]
      });
    });
    return data;
  }
});

LikelihoodOfStop = VisualBase.extend({
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
  drawStartup: function(){},
  drawChart: function(){
    d3.select(this.svg[0])
            .datum(this._formatData())
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "xMinYMin")
            .attr('viewBox', "0 0 {0} {1}".printf(this.get("width"), this.get("height")))
            .call(this.chart);

    nv.utils.windowResize(this.chart.update);
  },
  _formatData: function(){
    var self = this,
        data = [],
        base_col = this.data.cols.get("White"),
        d = this.data;  // sorting order (based on SME feedback)

    this.data.cols.keys().forEach(function(v, i){
      if(v !== "White"){
        var formatted = {
          color: Stops.colors[i],
          key: v + " vs. White",
          values: []
        }, col = self.data.cols.get(v);

        self.data.rows.forEach(function(v){
          var row = d.rows.get(v),
              rate = d.data[row][col]/d.data[row][base_col] || 0;

          rate = (rate) ? rate -1 : undefined;

          formatted.values.push({
            label: Stops.violations.get(v).label,
            value: rate,
            order: Stops.violations.get(v).order
          });
        });

        formatted.values.sort(function(a,b){return a.order-b.order;});

        // remove final "Checkpoint", optional reporting in regulation, based on SME feedback
        formatted.values.pop();

        data.push(formatted);
      }
    });

    return data;
  }
});

SearchRatioDonut = StopRatioDonut.extend({});
SearchRatioTimeSeries = StopRatioTimeSeries.extend({});

UseOfForceDonut = StopRatioDonut.extend({});
UseOfForceTimeSeries = StopRatioTimeSeries.extend({});

ContrabandHitRateBar = LikelihoodOfStop.extend({});
