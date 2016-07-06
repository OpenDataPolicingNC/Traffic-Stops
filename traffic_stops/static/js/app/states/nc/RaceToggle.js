var _ = require('underscore');
var $ = require('jquery');

var RaceToggle = function(updateUrl, showEthnicity){
  this.updateUrl = updateUrl;
  this.showEthnicity = showEthnicity;
}
_.extend(RaceToggle.prototype, {
  render: function($div){
    var id,
        inpDiv = $('<div class="radio">')
          .append('<label><input type="radio" name="raceType" id="raceTypeRace" value="race">Race &nbsp;</label>')
          .append('<label><input type="radio" name="raceType" id="raceTypeEthnicity" value="ethnicity">Ethnicity</label>'),
        container = $('<div class="raceSelector pull-right">')
          .append('<strong>View results by:</strong>')
          .append(inpDiv)
          .insertBefore($div);

    id = (this.showEthnicity) ? "#raceTypeEthnicity" : "#raceTypeRace";
    inpDiv.find(id).prop("checked", true);

    inpDiv.find('input').on('change', (e) => {
      this.showEthnicity = $(e.target).val()==="ethnicity";
      $.post(this.updateUrl, {"showEthnicity": this.showEthnicity});
      $(document).trigger('raceToggle.change', this.showEthnicity);
    });
  }
});

if (typeof window.NC === 'undefined') window.NC = {};

Object.assign(window.NC, {
  RaceToggle
});
