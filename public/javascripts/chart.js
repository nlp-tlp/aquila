// chart.js, by Michael Stewart
// (not to be confused with the chart library of the same name)





function updateChart(granularity) {
	//chartInfo = getChartInfo(granularity);
	earliest = new Date(chartInfo["earliest"])
	latest   = new Date(chartInfo["latest"])
	/*
	function getDateX(d) {
		switch(granularity) {
			case "Days": 	return d["date"];
			case "Weeks": 	return getLastSunday(d["date"]);
			case "Months": 	return (new Date(d["date"].getFullYear(), d["date"].getMonth(), 1));
			case "Years": 	return (new Date(d["date"].getFullYear(), 0, 1));
		}
	}*/

	var svg = d3.select('svg');

	var width = chartInfo[granularity].width,
		    height = 900,
		    margin = {top: Math.max(80, 200), right: 70, bottom: Math.max(80, height - 700), left:95}

	var x = d3.time.scale()
		    .domain([d3.time.day.offset(earliest, - chartInfo[granularity].offset[0]), d3.time.day.offset(latest, chartInfo[granularity].offset[1])])
		    .rangeRound([0, width - margin.left - margin.right]);

	function getXAxis(granularity) {
		var xAxis = d3.svg.axis()
		    .scale(x)
		    .orient('bottom')
		switch(granularity) {
			case "Days": 	return 	xAxis.ticks(d3.time.days, 1).tickFormat(d3.time.format('%d')).tickSize(4).tickPadding(4);
			case "Weeks": 	return 	xAxis.ticks(d3.time.weeks, 1).tickFormat(d3.time.format('%d')).tickSize(4).tickPadding(4);
			case "Months": 	return 	xAxis.ticks(d3.time.months, 1).tickFormat(d3.time.format('%B %Y')).tickSize(4).tickPadding(4);
			case "Years": 	return 	xAxis.ticks(d3.time.years, 1).tickFormat(d3.time.format('%Y')).tickSize(4).tickPadding(4);

		}
	};

	/*var width = chartInfo[granularity].width,
	    height = height = window.innerHeight - 120,
	    margin = {top: Math.max(80, window.innerHeight - 120 - 700), right: 70, bottom: Math.max(80, height - 700), left:95}*/




	var xAxis = getXAxis(granularity);

	var xAxisMonths = d3.svg.axis()
	    .scale(x)
	    .ticks(d3.time.months, 1)
	    .tickFormat(d3.time.format('%B %Y'))

	var y = d3.scale.linear()
   		.domain([0, chartInfo[granularity].maxY])
    	.range([height - margin.top - margin.bottom, 0]);

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient('left')
	    .tickPadding(8);

	svg.selectAll("circle")		    
	    .transition()
	    .duration(500)
	    .attr("cy", function (d) { return d3.select(this).attr("data-y-" + granularity.toLowerCase()); })
	    .transition()
	    .duration(500)
	    .attr("cx", function (d) { return d3.select(this).attr("data-x-" + granularity.toLowerCase()); })
	 	.attr("r", chartInfo[granularity].circleRadius)


	svg.select('.x.axis')
		.transition()
		.duration(500)
		.call(xAxis);

	svg.select('.y.axis')
		.transition()
		.duration(500)
		.call(yAxis);

	if(granularity != "Months" && granularity != "Years") {
		svg.select('.x.axis.line-hidden')
			.transition()
			.duration(500)
			.attr('opacity', '1')
			.call(xAxisMonths);
	} else {
		svg.select('.x.axis.line-hidden')
			.transition()
			.duration(500)
			.attr('opacity', '0')
			.call(xAxisMonths);
	}

	d3.select('svg')
		.transition()
		.duration(500)
		.attr('width', width)
		.attr('height', height)

}

document.getElementById("granularity-select").onchange = function(e) {
	var granularity = convertIntegerToGranularity(this.selectedIndex);
	//getChartInfo(granularity);
	updateChart(granularity);
}

// Converts an integer to a granularity (time)
 function convertIntegerToGranularity(integer) {
	switch(integer) {
		case 0: return "Days";
		case 1: return "Weeks";
		case 2: return "Months";
		case 3: return "Years";
	}
}



window.onload = function() {

	var svg = d3.select('svg');
	svg.selectAll('circle')
		.transition()
		.duration(500)
		.attr("cy", function () { return d3.select(this).attr("data-y-days") })


	var g = d3.select('g');

	var text = d3.selectAll('text');

	svg.call(d3.behavior.zoom()
		.on("zoom", function () {
			g.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
			text.attr("transform", "scale(" + 1/(0.2+d3.event.scale/5*4) + ")");
			document.getElementById("chart").classList.add("grabbing");
		})
		.on("zoomend", function() {
			document.getElementById("chart").classList.remove("grabbing");
		}))


	var tip = d3.tip()
		  .attr('class', 'd3-tip')
		  .offset(function(d) {
			var coordinates = [0, 0];
			coordinates = d3.mouse(document.body);
			var mouseX = coordinates[0];

		  	if(mouseX > 1500) return [0, -10]
		  	else return [0, 10]
		  })
		  .direction(function(d) {
			var coordinates = [0, 0];
			coordinates = d3.mouse(document.body);
			var mouseX = coordinates[0];

		  	if(mouseX > 1500) return 'w'
		  	else return 'e'
		  })
		  .html(function(d) {
		  	return  d3.select(this).attr("data-tip");
		  });

	g.call(tip);

	svg.selectAll("circle")
		.on('mouseover', tip.show)
		.on('mouseout', tip.hide)



	window.onresize = function() {
		var height = window.innerHeight - 120;
		var svg = d3.select('svg')
		    .attr('height', height);
	}

}