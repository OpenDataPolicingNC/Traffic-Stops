import DataHandlerBase from './DataHandlerBase.js';
import _ from 'underscore';

export default DataHandlerBase.extend({
  get_data: function () {
    if (typeof this._data_promise === 'undefined') {
      this._data_promise = new Promise((resolve, reject) => {
        Promise.all(this.get('handlers').map((h) => h.get_data()))
          .then((datas) => {
            this.set('raw_data', datas);
            this.set('data', undefined);
            this.clean_data();

            resolve(this.get('data'));
          })
          .catch(reject);
      });
    }

    return this._data_promise;
  }
});
