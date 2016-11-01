import d3 from 'd3';
import Backbone from 'backbone';

export default Backbone.Model.extend({
  get_data: function () {
    if (typeof this._data_promise === 'undefined') {
      this._data_promise = new Promise((resolve, reject) => {
        d3.json(this.get("url"), (error, data) => {
          if (error) {
            reject(error);
            return error;
          }

          this.set("raw_data", data);
          this.set("data", undefined);
          this.clean_data();

          resolve(this.get('data'));
        });
      });
    }

    return this._data_promise;
  },

  clean_data: function () {
    throw "abstract method: requires override";
  }
});
