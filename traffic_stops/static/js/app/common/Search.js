export function createSearchHandlerBase (StopsHandler) {
  return StopsHandler.extend({
    clean_data: function () {
      StopsHandler.prototype.clean_data.bind(this)();
      var data = this.get("data");
      data.type = "search";
      this.set("data", data);
    }
  });
}
