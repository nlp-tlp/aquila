//https://github.com/shprink/d3js-wordcloud/blob/master/word-cloud.js


var fill = d3.scale.category20();

var w = window.innerWidth,
        h = window.innerHeight;

var max,
        fontSize;

var layout = d3.layout.cloud()
        .timeInterval(Infinity)
        .size([w, h])
        .index(function(d) { return 0})
        .fontSize(function(d) {
            return fontSize(+d.Freq);
        })
        .text(function(d) {
            return d.Word;
        })
        .on("end", draw);

var svg = d3.select("#vis").append("svg")
        .attr("width", w)
        .attr("height", h);
        /*.call(d3.behavior.zoom()
        .on("zoom", function () {                   
            svg.select('g').attr("transform", "translate(" + (d3.event.translate[0] + 0 + (w) * (d3.event.scale/2)) + ", "  +  (d3.event.translate[1] + 0 + (w) *(d3.event.scale /2)) + ") scale(" + (d3.event.scale * 1)+ ")");
            svg.attr("class", "chart grabbing");

        })
        .on("zoomend", function() {
            svg.attr("class", "chart");
        }))*/

var vis = svg.append("g").attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

update();

window.onresize = function(event) {
    update();
};

function draw(data, bounds) {
    var w = window.innerWidth,
        h = window.innerHeight;

    svg.attr("width", w).attr("height", h);

    scale = bounds ? Math.min(
            w / Math.abs(bounds[1].x - w / 2),
            w / Math.abs(bounds[0].x - w / 2),
            h / Math.abs(bounds[1].y - h / 2),
            h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;

    var text = vis.selectAll("text")
            .data(data, function(d) {
                return d.text.toLowerCase();
            });
    text.transition()
            .duration(1000)
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            });
    text.enter().append("text")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            })
            .style("opacity", 1e-6)
            .transition()
            .duration(1000)
            .style("opacity", 1);
    text.style("font-family", function(d) {
        return d.font;
    })
            .style("fill", function(d) {
                return fill(d.text.toLowerCase());
            })
            .text(function(d) {
                return d.text;
            });

    vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
}

function update() {
    layout.font('impact').spiral('archimedean');
    fontSize = d3.scale['sqrt']().range([10, 100]);
    if (wcData.length){
        fontSize.domain([+wcData[wcData.length - 1].Freq || 1, +wcData[0].Freq]);
    }
    layout.stop().words(wcData).start();

    // Remove the loading screen once loaded
    var loadingScreen = document.getElementById("loading-screen");
    loadingScreen.classList.add("hide");
    var killLoadingScreen = window.setTimeout(function() {
        loadingScreen.classList.add("gone");
    }, 200);



}