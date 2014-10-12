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


// global website defaults
var Stops = {
  start_year: 2001,
  max_year: new Date().getFullYear(),
  races: d3.map({
    'A': 'Asian',
    'B': 'Black',
    'I': 'Native American',
    'U': 'Other/Unknown',
    'W': 'White'
  }),
  colors: [
    "#d7191c",
    "#fdae61",
    "#ffffbf",
    "#a6d96a",
    "#1a9641"
  ],
  violations: d3.map({
    1: 'Speed Limit Violation',
    2: 'Stop Light/Sign Violation',
    3: 'Driving While Impaired',
    4: 'Safe Movement Violation',
    5: 'Vehicle Equipment Violation',
    6: 'Vehicle Regulatory Violation',
    7: 'Seat Belt Violation',
    8: 'Investigation',
    9: 'Other Motor Vehicle Violation',
    10: 'Checkpoint'
  })
};
Stops.years = Stops.max_year - Stops.start_year + 1;


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
    // make sure all years represented, and counts for each race exist
    var years = [],
        by_year = {},
        totals = {},
        by_race = {},
        data = this.get('raw_data');

    // make a blank-template for totals
    Stops.races.keys().forEach(function(key){
      totals[Stops.races.get(key)] = 0;
      by_race[Stops.races.get(key)] = Array.apply(null, new Array(Stops.years)).map(Number.prototype.valueOf,0);
    });
    by_race["Total"] = Array.apply(null, new Array(Stops.years)).map(Number.prototype.valueOf,0);

    // copy blank-template to all years
    for(var i = Stops.start_year; i<=Stops.max_year; i++){
      years.push(i);
      by_year[i] = $.extend({}, totals);
    }

    // apply data to template
    data.forEach(function(v){

      var obj = by_year[v.year];
      for(var key in v){
        var match = Stops.races.get(key);
        if (match){
          obj[match] = v[key];
          by_race[match][v.year-Stops.start_year] = v[key];
          by_race["Total"][v.year-Stops.start_year] += v[key];
          totals[match] += v[key];
        }
      }

    });
    by_year["Total"] = totals;

    this.set("data",
      {
        years:   years,
        by_year: by_year,
        by_race: by_race
      });
  }
});

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
    var self = this,
        selector = $('<select>'),
        opts = this.data.years.map(function(v){return '<option value="{0}">{0}</option>'.printf(v);}),
        getData = function(){
          var value = selector.val();
          self.dataset =  self.data.by_year[value];
          self.drawChart();
        };

    selector
      .append('<option value="Total">Total</option>')
      .append(opts)
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
        color_idx = 0;

    for(var key in this.dataset){
      data.push({"key": key,
               "value": this.dataset[key],
               "color": Stops.colors[color_idx]
      });
      color_idx += 1;
    }
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
  drawStartup: function(){
  },
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
    var data = [],
        color_idx = 0,
        totals = this.data.by_race["Total"];

    for(var race in this.data.by_race){

      if (race === "Total") continue;

      var obj = {
        values: [],
        key: race,
        color: Stops.colors[color_idx]
      };
      color_idx += 1;

      this.data.by_race[race].forEach(function(v, i){
        var val = (totals[i]>0) ? v / totals[i] : NaN;
        obj.values.push({x: Stops.start_year+i, y: val});
      });

      data.push(obj);
    }
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
  },
  drawStartup: function(){
  },
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
        wcol = this.data.cols.get("White"),
        d = this.data;

    this.data.cols.keys().forEach(function(v, i){
      if(v !== "White"){
        var formatted = {
          color: Stops.colors[i],
          key: v + " vs. White",
          values: []
        }, col = self.data.cols.get(v);

        self.data.rows.forEach(function(v){
          var row = d.rows.get(v),
              rate = d.data[row][col]/d.data[row][wcol] || 0;

          rate = (rate) ? rate -1 : undefined;

          formatted.values.push({
            label: Stops.violations.get(v),
            value: rate
          });
        });
        data.push(formatted);
      }
    });

    return data;
  }
});







var UseOfForceTimeSeries = function(selector, agencyID){
  var self = this,
      w = 750,
      h = 375;

  nv.addGraph(function() {
    var chart = nv.models.lineChart()
                  .useInteractiveGuideline (true)
                  .transitionDuration(350)
                  .showLegend(true)
                  .showYAxis(true)
                  .showXAxis(true)
                  .width(w)
                  .height(h);

    chart.xAxis
        .axisLabel('Year');

    chart.yAxis
        .axisLabel('Fraction of stops by race')
        .tickFormat(d3.format('.02f'));

    d3.select(selector)
      .datum(self.getData())
      .attr('width', "100%")
      .attr('height', "100%")
      .attr('preserveAspectRatio', "none")
      .attr('viewBox', "0 0 {0} {1}".printf(w, h))
      .call(chart);
  });
};

UseOfForceTimeSeries.prototype.getData = function(agencyID){
    // should execute a GET call to fetch data
    return sinAndCos();
};


var ContrabandHitRateBar = function(selector, agencyID){
  var self = this,
      w = 750,
      h = 375;

  nv.addGraph(function() {
      var chart = nv.models.multiBarChart()
        .transitionDuration(350)
        .reduceXTicks(true)
        .rotateLabels(0)
        .width(w)
        .height(h)
        .tooltips(true)
        .showControls(true)
        .groupSpacing(0.1);

      chart.xAxis
          .tickFormat(d3.format(',f'));

      chart.yAxis
          .tickFormat(d3.format(',.1f'));

      d3.select(selector)
          .datum(self.getData())
          .attr('width', "100%")
          .attr('height', "100%")
          .attr('preserveAspectRatio', "none")
          .attr('viewBox', "0 0 {0} {1}".printf(w, h))
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
  });
};

ContrabandHitRateBar.prototype.getData = function(agencyID){
  // should execute a GET call to fetch data
  return stream_layers(2,10+Math.random()*100,0.1).map(function(data, i) {
    return {
      key: 'Stream #' + i,
      values: data
    };
  });
};



/*
 * Placeholders for made-up data used for mockups
 */
var stop_data_donut  = [
    {
        key: "White",
        y: 88
    },
    {
        key: "Black",
        y: 131
    },
    {
        key: "Hispanic",
        y: 63
    }
], sinAndCos = function(){
  var sin = [],
      cos = [],
      baseline =[];

  //Data is represented as an array of {x,y} pairs.
  for (var i = 2000; i < 2015; i++) {
    sin.push({x: i, y: Math.sin(i/10)});
    baseline.push({x: i, y: 0})
    cos.push({x: i, y: 0.5 * Math.cos(i/10)});
  }

  //Line chart data should be sent as an array of series objects.
  return [
    {
      values: cos,
      key: 'Black vs Whites',
      color: '#2ca02c'
    },
    {
      values: baseline,
      key: 'Baseline',
      color: '#696969'
    },
    {
      values: sin,
      key: 'Hispanic vs Whites',
      color: '#7777ff',
    }
  ];
}, barData = [
  {
    "key": "Blacks vs Whites",
    "color": "#d67777",
    "values": [
      {
        "label" : "Driving impaired" ,
        "value" : 1.8746444827653
      } ,
      {
        "label" : "Safe movement" ,
        "value" : 8.0961543492239
      } ,
      {
        "label" : "Vehicle equipment" ,
        "value" : 0.57072943117674
      } ,
      {
        "label" : "Other violation" ,
        "value" : -2.4174010336624
      } ,
      {
        "label" : "Investigation" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Stop light/sign" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Speed limit" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Vehicle regulatory" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Seatbelt" ,
        "value" : -0.72009071426284
      }
    ]
  }
], barData2 = [
  {
    "key": "Hispanics vs. Non-hispanics",
    "color": "#16A720",
    "values": [
      {
        "label" : "Driving impaired" ,
        "value" : 1.8746444827653
      } ,
      {
        "label" : "Safe movement" ,
        "value" : 8.0961543492239
      } ,
      {
        "label" : "Vehicle equipment" ,
        "value" : 0.57072943117674
      } ,
      {
        "label" : "Other violation" ,
        "value" : -2.4174010336624
      } ,
      {
        "label" : "Investigation" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Stop light/sign" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Speed limit" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Vehicle regulatory" ,
        "value" : -0.72009071426284
      } ,
      {
        "label" : "Seatbelt" ,
        "value" : -0.72009071426284
      }
    ]
  }
], stream_layers = function(n, m, o) {
  if (arguments.length < 3) o = 0;
  function bump(a) {
    var x = 1 / (0.1 + Math.random()),
        y = 2 * Math.random() - 0.5,
        z = 10 / (0.1 + Math.random());
    for (var i = 0; i < m; i++) {
      var w = (i / m - y) * z;
      a[i] += x * Math.exp(-w * w);
    }
  }
  return d3.range(n).map(function() {
      var a = [], i;
      for (i = 0; i < m; i++) a[i] = o + o * Math.random();
      for (i = 0; i < 5; i++) bump(a);
      return a.map(stream_index);
    });
}, stream_index = function(d, i) {
  return {x: i, y: Math.max(0, d)};
};
