import $ from 'jquery';
import Backbone from 'backbone';

// dashboard tables
export default Backbone.Model.extend({
  constructor: function(){
    Backbone.Model.apply(this, arguments);
    this.listenTo(this.get("handler"), "dataLoaded", this.update);
    this.listenTo(this.get("handler"), "dataRequestFailed", this.showError);
  },
  update: function(data){
    if(data===undefined) return;  // temporary for dummy census data
    this.data = data;
    this.draw_table();
  },
  get_tabular_data: function(){
    // should return list of lists, one list per row
    throw "abstract method: requires override";
  },
  showError: function(){
    var div = $(this.get("selector")),
        error_div = $('<div class="bg-warning">')
          .append('<p>An error occurred in fetching the data.</p>')
          .prependTo(div);
  },
  draw_table: function(){
    var div = $(this.get("selector")),
        matrix = this.get_tabular_data(),
        resp = $('<div class="table-responsive">'),
        tbl = $('<table class="table">').attr("class", "table table-striped table-condensed dash-tables"),
        tbody = $('<tbody>');

    matrix.forEach(function(row, i){
      var tr = $('<tr>');
      row.forEach(function(d){
        var cell = (i === 0) ? $('<th>') : $('<td>');
        tr.append(cell.append(d));
      });
      tbody.append(tr);
    });
    resp.append(tbl);
    tbl.append(tbody);
    div.prepend(resp);
  }
});
