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
var Stops = {};

Stops.start_year = 2001;
Stops.max_year = new Date().getFullYear();
Stops.years = Stops.max_year - Stops.start_year + 1;
Stops.races = {
  'A': 'Asian',
  'B': 'Black',
  'I': 'Native American',
  'U': 'Other/Unknown',
  'W': 'White'
};
Stops.colors = ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"];

var StopsHandler = function(url){
  var self = this;

  this.data = {};
  this.observers = [];

  d3.json(url, function(error, data) {
    if(error) return console.warn(error);
    self.data = data;
    self.clean_data();
    self.notify_observers();
  });
};

StopsHandler.prototype.add_observer = function(observer){
  this.observers.push(observer);
};

StopsHandler.prototype.notify_observers = function(){
  var self = this;
  this.observers.forEach(function(v){
    v.update(self);
  });
};

StopsHandler.prototype.clean_data = function(){
  // make sure all years represented, and counts for each race exist
  var years = [],
      by_year = {},
      totals = {},
      by_race = {};

  // make a blank-template for totals
  for(var key in Stops.races){
    totals[Stops.races[key]] = 0;
    by_race[Stops.races[key]] = Array.apply(null, new Array(Stops.years)).map(Number.prototype.valueOf,0);
  }
  by_race["Total"] = Array.apply(null, new Array(Stops.years)).map(Number.prototype.valueOf,0);

  // copy blank-template to all years
  for(var i = Stops.start_year; i<=Stops.max_year; i++){
    years.push(i);
    by_year[i] = $.extend({}, totals);
  }

  // apply data to template
  this.data.forEach(function(v){

    var obj = by_year[v.year];
    for(var key in v){
      var match = Stops.races[key];
      if (match){
        obj[match] = v[key];
        by_race[match][v.year-Stops.start_year] = v[key];
        by_race["Total"][v.year-Stops.start_year] += v[key];
        totals[match] += v[key];
      }
    }

  });
  by_year["Total"] = totals;

  this.years = years;
  this.by_year = by_year;
  this.by_race = by_race;
};


/*
 * Dashboard plot-objects
 */
var StopRatioDonut = function(selector, options){
  options = options || {};
  this.w = options.width || 300;
  this.h = options.height || 300;

  this.selector = selector;
  this.svg = $(selector);
  this.div = $(this.svg).parent();
  this.selector_div = $('<div>').appendTo(this.div);

  this.chart = nv.models.pie()
    .x(function(d){ return d.key; })
    .y(function(d){ return d.value; })
    .color(function(d){ return d.data.color; })
    .width(this.w)
    .height(this.h)
    .showLabels(true)
    .labelType("percent")
    .donutRatio(0.35)
    .labelThreshold(0.05)
    .donut(true);

  this._drawLoading();
};

StopRatioDonut.prototype.update = function(dataHandler){
  this.data = dataHandler;
  this.loader_div.remove();
  this._drawSelector();
  this._drawChart();
};

StopRatioDonut.prototype._drawSelector = function(){
  var self = this,
      selector = $('<select>'),
      opts = this.data.years.map(function(v){return '<option value="{0}">{0}</option>'.printf(v);}),
      getData = function(){
        var value = selector.val();
        self.dataset =  self.data.by_year[value];
        self._drawChart();
      };

  selector
    .append('<option value="Total">Total</option>')
    .append(opts)
    .on('change', getData);

  this.selector_div.html(selector);
  getData();
};

StopRatioDonut.prototype._drawLoading = function(){
  this.loader_div = $('<div>').prependTo(this.div);
  this.loader_div.append('<p>Loading ... <i class="fa fa-cog fa-spin"></i></p>');
};

StopRatioDonut.prototype._drawChart = function(){
  var self = this,
      ds = [],
      color_idx = 0;

  for(var key in this.dataset){
    ds.push({"key": key,
             "value": this.dataset[key],
             "color": Stops.colors[color_idx]
    });
    color_idx += 1;
  }

  nv.addGraph(function() {

      d3.select(self.svg[0])
          .datum([ds])
        .transition().duration(1200)
          .attr('width', "100%")
          .attr('height', "100%")
          .attr("preserveAspectRatio", "xMinYMin")
          .attr('viewBox', '0 0 {0} {1}'.printf(self.w, self.h))
          .call(self.chart);

      return self.chart;
  });
};


var StopRatioTimeSeries = function(selector, options){
  options = options || {};
  this.w = options.width || 750;
  this.h = options.height || 375;

  this.svg = $(selector);
  this.div = $(this.svg).parent();

  this.chart = nv.models.lineChart()
                .useInteractiveGuideline (true)
                .transitionDuration(350)
                .showLegend(true)
                .showYAxis(true)
                .showXAxis(true)
                .forceY([0, 1])
                .width(this.w)
                .height(this.h);

  this.chart.xAxis
      .axisLabel('Year');

  this.chart.yAxis
      .axisLabel('Fraction of stops by race')
      .tickFormat(d3.format('%'));

  this._drawLoading();
};

StopRatioTimeSeries.prototype.update = function(dataHandler){
  this.data = dataHandler;
  this.loader_div.remove();
  this._drawChart();
};

StopRatioTimeSeries.prototype._drawChart = function(){
  var self = this,
      ds = [],
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

    ds.push(obj);
  }

  nv.addGraph(function() {
      d3.select(self.svg[0])
        .datum(ds)
        .attr('width', "100%")
        .attr('height', "100%")
        .attr('preserveAspectRatio', "xMinYMin")
        .attr('viewBox', "0 0 {0} {1}".printf(self.w, self.h))
        .call(self.chart);
    });
};

StopRatioTimeSeries.prototype._drawLoading = function(){
  this.loader_div = $('<div>').prependTo(this.div);
  this.loader_div.append('<p>Loading ... <i class="fa fa-cog fa-spin"></i></p>');
};

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


var LikelihoodOfStop = function(selector, whichChart){
    var self = this;

    nv.addGraph(function() {
      var chart = nv.models.multiBarHorizontalChart()
          .x(function(d) { return d.label; })
          .y(function(d) { return d.value; })
          .margin({top: 20, right: 50, bottom: 20, left: 150})
          .showValues(true)
          .tooltips(true)
          .transitionDuration(350)
          .showControls(false);

      chart.yAxis
          .tickFormat(d3.format(',.2f'));

      d3.select(selector)
          .datum(self.getData(whichChart))
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
  });
};

LikelihoodOfStop.prototype.getData = function(whichChart){
    // should execute a GET call to fetch data
    if (whichChart){
      return barData;
    } else {
      return barData2;
    }
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
