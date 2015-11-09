var viz = function(build) {

  if (!build.colors) build.colors = staticColors.viz.defaults;

  build.viz = d3plus.viz()
    .background("transparent")
    .container(build.container)
    .error("Please Wait")
    .draw();

  if (build.highlight) {

    build.viz.class(function(d, viz){
      return build.highlight === "01000US" || d[viz.id.value] === build.highlight ? "highlight" : "";
    });

  }

  viz.loadCoords(build);

  return build;

};

viz.finish = function(build) {

  var source_text = d3plus.string.list(d3plus.util.uniques(build.sources).reduce(function(arr, s, i){
    if (s) arr.push(s.dataset);
    return arr;
  }, []));

  if (location.href.indexOf("/profile/") > 0) {
    d3.select(build.container.node().parentNode).select(".source")
      .text(source_text);
  }
  else {
    build.viz.footer(source_text);
  }

  if (!build.config.color) {
    if (build.viz.attrs()[build.highlight]) {
      build.config.color = function(d, viz) {
        return build.highlight === "01000US" || d[viz.id.value] === build.highlight ? build.colors.pri : build.colors.sec;
      };
    }
    else {
      build.config.color = function(d, viz) {
        return build.colors.pri;
      };
    }
    build.config.legend = false;
  }
  else if (build.config.color in staticColors) {
    build.color = build.config.color;
    build.config.color = function(d) {
      return staticColors[build.color][d[build.color]];
    };
  }

  var default_config = viz.defaults(build),
      type_config = viz[build.config.type](build);

  build.viz
    .config(default_config)
    .config(type_config)
    .config(build.config)
    .depth(build.config.depth)
    .error(false)
    .draw();

};

viz.redraw = function(build) {
  build.viz.error(false).draw();
};
