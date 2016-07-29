import Backbone from 'backbone';
import $ from 'jquery';

export default Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.listenTo(this.get("handler"), "dataLoaded", this.update);
    this.listenTo(this.get("handler"), "dataRequestFailed", this.showError);
    this.setDOM();
    this.loader_show();
    this.setDefaultChart();

    $(window).on('resize', this.onResize.bind(this))
  },
  setDOM: function(){
    this.svg = $(this.get("selector"));
    this.div = $(this.svg).parent();
  },
  onResize: function () {
    d3.select(this.svg[0])
      .style({ width:  `${this.div.width()}px`
             , height: `${ (this.get('height') / this.get('width')) * this.div.width() }px` });
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
    $(document).on('raceToggle.change', this.triggerRaceToggle.bind(this));
  },
  drawStartup: function(){
    /* istanbul ignore next */
    throw "abstract method: requires override";
  },
  drawChart: function(){
    /* istanbul ignore next */
    throw "abstract method: requires override";
  },
  setDefaultChart: function(){
    /* istanbul ignore next */
    throw "abstract method: requires override";
  },
  triggerRaceToggle: function(e, v){}
});
