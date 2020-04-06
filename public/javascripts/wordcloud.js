// wordcloud.js, by Michael Stewart
var MULTIPLIER = 2; // Chart size multiplier

function getDataset(chartName) {
	if(chartName == "noun") {
		dataset = npcData;
	} else if (chartName == "relation") {
		dataset = rpcData;
	}
	
	return dataset;
}

function redrawChart(entryNumber, chartName) {
	dataset = getDataset(chartName);
	datasetLength = dataset.length;	

	var svg = d3.select('#chart-' + chartName);		
	svg.selectAll("text")
	    .transition()
	    .duration(200)
		.style("font-size", function(d) { 
			var w = dataset[d.index].freqs[entryNumber];
			if(w == 0 ) return "0px";
			else return 12 * (1 + dataset[d.index].freqs[entryNumber] / datasetLength * MULTIPLIER) + "px";
		 })		
}

function wordCloud(chartName) {

	dataset = getDataset(chartName);	
	datasetLength = dataset.length;	

	if(chartName == "noun") {
		phraseName = "Noun Phrase"
	} else if (chartName == "relation") {
		phraseName = "Relation Phrase"
	}

	var svg, cloud;
	var fill = d3.scale.category20();
	var numEntries = dataset[0]["freqs"].length	


	function createChart(entryNumber, chartName) {

		var height = 700;
		var width = 730;
		var initialScale = 1;
		var leftMargin = 80;
		var topMargin = -20;
		if(chartName == "relation") {
			initialScale = 1.2;
		}

		svg = d3.select('#chart-' + chartName)
		    .attr('height', height);

		weightedWordsMapped = dataset.map(function(d) {
		    return {index: dataset.indexOf(d), text: d[phraseName], size: 12 * (1 + d.freqs[entryNumber] / datasetLength * MULTIPLIER) };
		});

		
		cloud = d3.layout.cloud().size([width, height])
		      .words(weightedWordsMapped)
		      .padding(5)
		      .rotate(function() { return ~~(Math.random() * 4) * 45; })
		      .font("Impact")
		      .fontSize(function(d) { return d.size; })
		      .index(function(d) { return d.index; })
		      .on("end", draw)
		      .start();

		function draw(words) {
			svg
				.call(d3.behavior.zoom()
				.on("zoom", function () {					
					svg.select('g').attr("transform", "translate(" + (d3.event.translate[0] + leftMargin + (width) * (d3.event.scale/2)) + ", "  +  (d3.event.translate[1] + topMargin + (width) *(d3.event.scale /2)) + ") scale(" + (d3.event.scale * initialScale)+ ")");
					svg.attr("class", "chart grabbing");

				})
				.on("zoomend", function() {
					svg.attr("class", "chart");
				}))
			.append("g")
			.attr("transform", "translate(" + (width * 0.5 + leftMargin ) + ", " + (width * 0.5 + topMargin) + ") scale(" + initialScale + ")")		
			.selectAll("text")
			.data(words)
			.enter().append("text")	      	
			.style("font-size", 0)
			.style("font-family", "Impact")
			.style("fill", function(d, i) { return fill(i); })
			.attr("text-anchor", "middle")
			.attr("transform", function(d) {
				return "translate(" + [d.x + 10, d.y + 10] + ")rotate(" + d.rotate + ")";
			})		
		    .transition()
		    .duration(500)
		    .style("font-size", function(d) { return d.size + "px"; })
			.text(function(d) { return d.text; });
		}

		slider = d3.slider().axis(true).min(1).max(numEntries).step(4).value(numEntries);
		sliderEle = d3.select('#wordcloud-slider-' + chartName).call(slider);
	}


	createChart(numEntries - 1, chartName);
}


window.onload = function() {
	a = wordCloud("noun");
	b = wordCloud("relation");

	// Remove the loading screen once loaded
	var loadingScreen = document.getElementById("loading-screen");
	loadingScreen.classList.add("hide");
	var killLoadingScreen = window.setTimeout(function() {
		loadingScreen.classList.add("gone");
	}, 200);
}