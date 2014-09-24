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

/*
 * Dashboard plot-objects
 */
var StopRatioDonut = function(selector, agencyID){
    var self = this,
        w = 300,
        h = 300;

    nv.addGraph(function() {
        var chart = nv.models.pie()
            .values(function(d) { return d; })
            .width(w)
            .height(h)
            .showLabels(true)
            .labelType("percent")
            .donutRatio(0.35)
            .donut(true);

        d3.select(selector)
            .datum(self.getData(agencyID))
          .transition().duration(1200)
            .attr('width', "100%")
            .attr('height', "100%")
            .attr('preserveAspectRatio', "none")
            .attr('viewBox', '0 0 {0} {1}'.printf(w, h))
            .call(chart);

        return chart;
    });
};

StopRatioDonut.prototype.getData = function(agencyID){
    // should execute a GET call to fetch data
    return [stop_data_donut];
};


var StopRatioTimeSeries = function(selector, agencyID){
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

StopRatioTimeSeries.prototype.getData = function(agencyID){
    // should execute a GET call to fetch data
    return sinAndCos();
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
