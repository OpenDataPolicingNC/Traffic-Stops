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
    'Checkpoint': 9
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

LikelihoodSearchHandler  = DataHandlerBase.extend({
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

    getTotals(raw.stops);
    getTotals(raw.searches);

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
          key: "{0} vs. White".printf(Stops.race_pprint[race]),
          values: []
      };

      // build a bar for each violation
      Stops.purpose_order.forEach(function(purpose){
        // optional reporting requirement; remove as it's generally unreported
        if (purpose === "Checkpoint") return;

        // calculate percent-difference of stops which led to searches by race,
        // in comparison to white-baseline
        var w_se = searches.get(purpose).white,
            w_st = stops.get(purpose).white,
            w_ra = w_se/w_st,
            r_se = searches.get(purpose)[race],
            r_st = stops.get(purpose)[race],
            r_ra = r_se/r_st,
            rate = (r_ra-w_ra)/w_ra;

        // add purpose to list of values
        bar.values.push({
          label: purpose,
          value: rate,
          order: Stops.purpose_order.get(purpose)
        });
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

ContrabandHitRateBar = LikelihoodOfSearch.extend({});
