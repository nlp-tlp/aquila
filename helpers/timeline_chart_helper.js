var d3 = require("../public/javascripts/d3/d3.min.js");
var jsdom = require("jsdom");
var doc = jsdom.jsdom();
var data = require("../nlp/data/timeline_chart_data").data();

// These dates should be updated whenever an earlier, or later, date is found in the dataset.
// It could be done automatically but not yet.

//earliest = new Date(2014, 7, 5);
//latest   = new Date(2019, 6, 30);
earliest = new Date(2013, 6, 1);
latest = new Date(2013, 12, 30);

var getChart = function (params) {
	//var CATEGORICAL_FIELDNAME = "FinalRiskConsequence"
	var CATEGORICAL_FIELDNAME = "Severity"; // The categorical field name, for example "Severity" or "FinalRiskConsequence"

	//var ACCIDENT_CATEGORIES = ["1 Catastrophic", "2 Major", "3 Moderate", "4 Minor", "5 No Significant Effect"];
	var ACCIDENT_CATEGORIES = ["Minor", "Serious", "Fatal", "NDI"]; // A list of the caterogies present in the CATEGORICAL_FIELDNAME column

	//var DATE_FIELDNAME = "dateofevent"
	var DATE_FIELDNAME = "Date Of Accident"; // The field name of the date column

	//var DESCRIPTION_FIELDNAME = "Briefdescriptionofevent"
	var DESCRIPTION_FIELDNAME = "Detailed Description"; // The textual field name

	// No need to change this one:
	var GRANULARITIES = ["Days", "Weeks", "Months", "Years"];

	// Gets the previous sunday (for use with weeks)
	function getLastSunday(d) {
		var t = new Date(d);
		t.setDate(t.getDate() - t.getDay());
		return t;
	}

	// Parse data and generate correct event numbers and properly-represented dates
	// To do this, it divides the data into the four severity categories, and then goes through
	// each category to assign an 'event number'. This 'event number' corresponds to the event's
	// position on the y axis.
	// Without scanning through severity categories first, it's not possible to order the events
	// based on their severity.
	function parseData() {
		// Initialise dates, categorised into different granularities of time
		dates = [];
		for (var g in GRANULARITIES) dates[GRANULARITIES[g]] = [];

		// Set up severity categories (manually, as there are only four).
		severityCategorisedData = {};
		for (var ac in ACCIDENT_CATEGORIES)
			severityCategorisedData[ACCIDENT_CATEGORIES[ac]] = [];

		// Place data into severity categories
		for (i = 0, len = data.length; i < len; i++) {
			severityCategorisedData[data[i][CATEGORICAL_FIELDNAME]].push(data[i]);
		}

		// Reset the data variable, so we can push categorised data to it in the following steps
		data = [];

		// Iterate through each severity category, allowing for the ordering of events along the
		// y-axis, based on their severity.
		for (var category in severityCategorisedData) {
			if (severityCategorisedData.hasOwnProperty(category)) {
				sCData = severityCategorisedData[category];
				for (i = 0, len = sCData.length; i < len; i++) {
					// Convert the date of the event into an array, so it may be converted into a Javascript date
					var str = sCData[i][DATE_FIELDNAME];
					//console.log(sCData[i])
					var arr = str.split("/");

					// Parse the date of the event and update the earliest and latest dates if necessary
					var date = new Date(arr[2], arr[1] - 1, arr[0]);
					if (date < earliest) earliest = date;
					if (date > latest) latest = date;

					//console.log(arr, date)
					// Create a new field, "date", in the data to hold the Javascript date
					sCData[i]["date"] = date;

					// Create a new fieled, "eventNumber", in the data to hold the ordering of the event in relation to other events
					// that occured in the same level of time granularity (e.g. all events on that day, week, etc)
					var eventNumber;
					sCData[i]["eventNumber"] = [];

					// Calculate the event number for each event within each level of time granularity
					for (var g in GRANULARITIES) {
						gi = GRANULARITIES[g];

						// Get an index of a date with a particular granularity.
						function getDate(granularity, date) {
							switch (gi) {
								case "Days":
									return (
										"" +
										date.getDate() +
										"/" +
										date.getMonth() +
										"/" +
										date.getFullYear()
									);
									break;
								case "Weeks":
									var lastSunday = getLastSunday(date);
									return (
										"" +
										lastSunday.getDate() +
										"/" +
										lastSunday.getMonth() +
										"/" +
										lastSunday.getFullYear()
									);
									break;
								case "Months":
									return "" + date.getMonth() + "/" + date.getFullYear();
									break;
								case "Years":
									return "" + date.getFullYear();
									break;
							}
						}

						var dateG = getDate(gi, date);

						// Check if there are any events within this date granularity already.

						if (dates[gi][dateG]) {
							dates[gi][dateG].push(sCData[i]);
							eventNumber = dates[gi][dateG].length;
						} else {
							eventNumber = 1;
							dates[gi][dateG] = [];
							dates[gi][dateG].push(sCData[i]);
						}

						sCData[i]["eventNumber"][gi] = eventNumber;
					}
				}
				for (i = 0, len = sCData.length; i < len; i++) {
					data.push(sCData[i]);
				}
			}
		}
	}

	//  Creates the chart, and renders it to the svg element.
	//  Granularity may be either:
	/*
		"Days"
		"Weeks"
		"Months"
		"Years"
	*/

	function getChartInfo(granularity) {
		chartInfo = function () {
			chartInfo = {};
			var keyLength = Object.keys(dates["Days"]).length;
			chartInfo["Days"] = {
				offset: [1, 0],
				width: keyLength * 50,
				circleRadius: 14,
				maxY: Math.max(
					10,
					d3.max(data, function (d) {
						return d.eventNumber["Days"];
					}),
				),
			};
			keyLength = Object.keys(dates["Weeks"]).length;
			chartInfo["Weeks"] = {
				offset: [7, 0],
				width: keyLength * 50,
				circleRadius: 8,
				maxY: Math.max(
					10,
					d3.max(data, function (d) {
						return d.eventNumber["Weeks"];
					}),
				),
			};
			keyLength = Object.keys(dates["Months"]).length;
			chartInfo["Months"] = {
				offset: [7, 0],
				width: keyLength * 130,
				circleRadius: 4,
				maxY: Math.max(
					10,
					d3.max(data, function (d) {
						return d.eventNumber["Months"];
					}),
				),
			};
			keyLength = Object.keys(dates["Years"]).length;
			chartInfo["Years"] = {
				offset: [365, 1],
				width: keyLength * 500,
				circleRadius: 4,
				maxY: Math.max(
					10,
					d3.max(data, function (d) {
						return d.eventNumber["Years"];
					}),
				),
			};
			chartInfo["earliest"] = earliest;
			chartInfo["latest"] = latest;
			return chartInfo;
		}.call();
		return chartInfo;
	}

	function createChart(granularity) {
		chartInfo = getChartInfo(granularity);

		var width = chartInfo[granularity].width,
			height = 900,
			margin = {
				top: Math.max(80, 200),
				right: 70,
				bottom: Math.max(80, height - 700),
				left: 95,
			};

		var x = d3.time
			.scale()
			.domain([
				d3.time.day.offset(earliest, -chartInfo[granularity].offset[0]),
				d3.time.day.offset(latest, chartInfo[granularity].offset[1]),
			])
			.rangeRound([0, width - margin.left - margin.right]);

		function getXAxis(granularity) {
			var xAxis = d3.svg.axis().scale(x).orient("bottom");
			switch (granularity) {
				case "Days":
					return xAxis
						.ticks(d3.time.days, 1)
						.tickFormat(d3.time.format("%d"))
						.tickSize(4)
						.tickPadding(4);
				case "Weeks":
					return xAxis
						.ticks(d3.time.weeks, 1)
						.tickFormat(d3.time.format("%d"))
						.tickSize(4)
						.tickPadding(4);
				case "Months":
					return xAxis
						.ticks(d3.time.months, 1)
						.tickFormat(d3.time.format("%B %Y"))
						.tickSize(4)
						.tickPadding(4);
				case "Years":
					return xAxis
						.ticks(d3.time.years, 1)
						.tickFormat(d3.time.format("%Y"))
						.tickSize(4)
						.tickPadding(4);
			}
		}

		var y = d3.scale
			.linear()
			.domain([0, chartInfo[granularity].maxY])
			.range([height - margin.top - margin.bottom, 0]);

		var xAxis = getXAxis(granularity);

		var xAxisMonths = d3.svg
			.axis()
			.scale(x)
			.orient("bottom")
			.ticks(d3.time.months, 1)
			.tickFormat(d3.time.format("%B %Y"))
			.tickSize(0)
			.tickPadding(8);

		var yAxis = d3.svg
			.axis()
			.scale(y)
			.ticks(chartInfo[granularity].maxY)
			.orient("left")
			.tickPadding(8);

		var svg = d3
			.select(doc.body)
			.append("svg")
			.attr("id", "chart")
			.attr("class", "shadow")
			.attr("width", width)
			.attr("height", height);

		var g = svg
			.append("g")
			.attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

		g.append("text")
			.attr("class", "y label y-axis-label")
			.attr("text-anchor", "end")
			.attr("x", -165)
			.attr("y", -38)
			.text("Accidents");

		g.append("g")
			.attr("class", "x axis")
			.attr(
				"transform",
				"translate(0, " + (height - margin.top - margin.bottom) + ")",
			)
			.call(xAxis);

		if (granularity != "Months" && granularity != "Years")
			g.append("g")
				.attr("class", "x axis line-hidden")
				.attr(
					"transform",
					"translate(0, " + (height - margin.top - margin.bottom + 30) + ")",
				)
				.call(xAxisMonths);

		g.append("g").attr("class", "y axis").call(yAxis);

		function getDateX(d, granularity) {
			switch (granularity) {
				case "Days":
					return d["date"];
				case "Weeks":
					return getLastSunday(d["date"]);
				case "Months":
					return new Date(d["date"].getFullYear(), d["date"].getMonth(), 1);
				case "Years":
					return new Date(d["date"].getFullYear(), 0, 1);
			}
		}

		function getXScale(d, granularity) {
			var width = chartInfo[granularity].width;
			x = d3.time
				.scale()
				.domain([
					d3.time.day.offset(earliest, -chartInfo[granularity].offset[0]),
					d3.time.day.offset(latest, chartInfo[granularity].offset[1]),
				])
				.rangeRound([0, width - margin.left - margin.right]);
			return x(getDateX(d, granularity));
		}
		function getYScale(d, granularity) {
			y = d3.scale
				.linear()
				.domain([0, chartInfo[granularity].maxY])
				.range([height - margin.top - margin.bottom, 0]);
			return y(d["eventNumber"][granularity]);
		}

		g.selectAll("circle")
			.data(data)
			.enter()
			.append("circle")
			.attr("class", function (d) {
				return (
					"colour-" +
					(ACCIDENT_CATEGORIES.indexOf(d[CATEGORICAL_FIELDNAME]) + 1)
				);
			})
			.attr("cx", function (d) {
				return x(getDateX(d, granularity));
			})
			.attr("cy", 0)
			.attr("r", chartInfo[granularity].circleRadius)
			.attr("data-x-Days", function (d) {
				return getXScale(d, "Days");
			})
			.attr("data-x-Weeks", function (d) {
				return getXScale(d, "Weeks");
			})
			.attr("data-x-Months", function (d) {
				return getXScale(d, "Months");
			})
			.attr("data-x-Years", function (d) {
				return getXScale(d, "Years");
			})
			.attr("data-y-Days", function (d) {
				return getYScale(d, "Days");
			})
			.attr("data-y-Weeks", function (d) {
				return getYScale(d, "Weeks");
			})
			.attr("data-y-Months", function (d) {
				return getYScale(d, "Months");
			})
			.attr("data-y-Years", function (d) {
				return getYScale(d, "Years");
			})
			.attr("data-tip", function (d) {
				return (
					"<strong>Date: </strong>" +
					d[DATE_FIELDNAME] +
					"<br/>" +
					"<strong>Area: </strong>" +
					d["Area"] +
					"<br/>" +
					"<strong>Place of Injury: </strong>" +
					d["Place Of Injury"] +
					"<br/>" +
					"<strong>" +
					CATEGORICAL_FIELDNAME +
					': </strong> <span class="text colour-' +
					(ACCIDENT_CATEGORIES.indexOf(d[CATEGORICAL_FIELDNAME]) + 1) +
					'">' +
					d[CATEGORICAL_FIELDNAME] +
					"</span><br/><hr/>" +
					d[DESCRIPTION_FIELDNAME]
				);
			});

		return svg.node().outerHTML;
	}

	parseData();
	var svg = createChart("Days");
	return { svg: svg, chartInfo: "chartInfo = " + JSON.stringify(chartInfo) };
};

module.exports = {
	getChart: getChart,
};
