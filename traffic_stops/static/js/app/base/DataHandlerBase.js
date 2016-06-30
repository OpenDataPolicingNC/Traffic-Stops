import d3 from 'd3';
import Backbone from 'backbone';

export default Backbone.Model.extend({
  constructor: function (){
    Backbone.Model.apply(this, arguments);
    this.get_data();
  },

  get_data: function () {
    d3.json(this.get("url"), (error, data) => {
      if (error) return this.trigger("dataRequestFailed");
      this.set("raw_data", data);
      this.set("data", undefined);
      this.clean_data();
      this.trigger("dataLoaded", this.get("data"));
    });
  },

  clean_data: function () {
    throw "abstract method: requires override";
  }
});
