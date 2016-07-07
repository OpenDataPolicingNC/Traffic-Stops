import DataHandlerBase from './DataHandlerBase.js';
import _ from 'underscore';

export default DataHandlerBase.extend({
  get_data: function(){
    var datas = [],
        checkIfComplete = (data) => {
          this.numRemaining = this.numRemaining - 1;
          datas.push(data);
          if(this.numRemaining === 0){
            this.set("raw_data", datas);
            this.set("data", undefined);
            this.clean_data();
            this.trigger("dataLoaded", this.get("data"));
          }
        };

    this.numRemaining = this.get("handlers").length;
    _.each(this.get("handlers"), function(handler){
      this.listenTo(handler, "dataLoaded", checkIfComplete);
      this.listenTo(handler, "dataRequestFailed", this.showError);
    }, this);
  }
});
