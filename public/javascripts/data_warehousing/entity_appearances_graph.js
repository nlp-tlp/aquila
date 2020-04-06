// Creates the bar chart.
// Entries name is either "entries" or "rules" depending on the page that renders the js.
function makeHierarchicalBarChart(data_source, entries_name) {

	// Majority of code found here:
	// Modified in November 2016.
	// Released under the GNU General Public License: https://opensource.org/licenses/GPL-3.0
	//https://bl.ocks.org/mbostock/1283663

	var margin = {top: 40, right: 40, bottom: 0, left: 160},
	    width = 600 - margin.left - margin.right,
	    height = 800 - margin.top - margin.bottom;

	var x = d3.scale.linear()
	    .range([0, width]);

	var barHeight = 26;

	var color = d3.scale.ordinal()
	    .range(["steelblue", "#ccc"]);

	var duration = 400,
	    delay = 10;

	var partition = d3.layout.partition()
	    .value(function(d) { return d.size; })		
	    .sort(function comparator(a, b) {
		  return b.size - a.size;
		});


	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("top");

	var svg = d3.select("#bar-chart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	svg.append("rect")
	    .attr("class", "background")
	    .attr("width", width)
	    .attr("height", height)
	    .on("click", up);

	svg.append("g")
	    .attr("class", "x axis");

	svg.append("g")
	    .attr("class", "y axis")
	  .append("line")
	    .attr("y1", "100%");

	d3.json(data_source, function(error, root) {
	  if (error) throw error;

	  partition.nodes(root);
	  x.domain([0, root.size]).nice();
	  down(root, 0);
	});




	function appendLoadingText() {
	  // Append loading message 
	  $("#erc-table-container").addClass("loading");
	  $("#loading-message").addClass("loading");
	  $("#loading-overlay").css("top", $("#erc-table-container").scrollTop());
	}

	function removeLoadingText() {
	    // Remove loading message 
		$("#erc-table-container").removeClass("loading");
		$("#loading-message").removeClass("loading");
	}


	var originalFilterHtml = $("#filter-info").html();
	function filterTable(category, category_id) {
		if(category == "all_entities") {
	 	 	$("#entity-recognition-table tbody tr").show();
	 	 	$("#filter-info").html(originalFilterHtml);
		 } else {
		  $("#entity-recognition-table tbody tr").hide();

		  //var category = $("#jstree").jstree().get_selected(true)[0].a_attr["data-category"]
		  //var bgcolor = $("#" + $("#jstree").jstree().get_selected(true)[0].id).find("a").css("background").split(")")[0]; // amazing

		 // console.log(bgcolor);

		 console.log(category);

		  if(entityAppearances.hasOwnProperty(category)) {
			  var entries = entityAppearances[category];
			  console.log(entityAppearances);

			  for(var i = 0; i < entries.length; i++) {
			  	$("#row-" + entries[i]).show();
			  	//console.log(entries[i]);
			  }
		  } else {
		  	entries = [];
		  }
		  $("#filter-info").html("Showing <b>" + entries.length + "</b> " + entries_name + " containing the category <span class=\"tag category-" + category_id + "\"" + "\">\"" + category + "\"</span>.");
		  $("#erc-table-container").scrollTop(0);


	  }

	  removeLoadingText();
	 // console.log(entries);

	}






	function down(d, i) {
	  if (!d.children || this.__transition__) return;


	  appendLoadingText();




	  var end = duration + d.children.length * delay;

	  // Mark any currently-displayed bars as exiting.
	  var exit = svg.selectAll(".enter")
	      .attr("class", "exit");

	  // Entering nodes immediately obscure the clicked-on bar, so hide it.
	  exit.selectAll("rect").filter(function(p) { return p === d; })
	      .style("fill-opacity", 1e-6);

	  // Enter the new bars for the clicked-on data.
	  // Per above, entering bars are immediately visible.
	  var enter = bar(d)
	      .attr("transform", stack(i))
	      .style("opacity", 1);

	  // Have the text fade-in, even though the bars are visible.
	  // Color the bars as parents; they will fade to children if appropriate.
	  enter.select("text").style("fill-opacity", 1e-6);
	  //enter.select("rect").style("fill", color(true));		 
	  enter.select("rect").attr("class", function(d) { return "category-" + d.class_id; }, true )
	  //enter.select("rect").classed("has-children", function(d) { return !!d.children; } )
	  enter.select("rect").style("fill-opacity", function(d) { if(d.children) { return 1 } else { return 0.5 } });	

	  // Update the x-scale domain.
	  x.domain([0, d3.max(d.children, function(d) { return d.size; })]).nice();

	  // Update the x-axis.
	  svg.selectAll(".x.axis").transition()
	      .duration(duration)
	      .call(xAxis);

	  // Transition entering bars to their new position.
	  var enterTransition = enter.transition()
	      .duration(duration)
	      .delay(function(d, i) { return i * delay; })
	      .attr("transform", function(d, i) { return "translate(0," + barHeight * i * 1.2 + ")"; });

	  // Transition entering text.
	  enterTransition.select("text")
	      .style("fill-opacity", 1);

	  // Transition entering rects to the new x-scale.
	  enterTransition.select("rect")
	      .attr("width", function(d) { return x(d.size); })
	      .style("fill-opacity", function(d) { if(d.children) { return 1 } else { return 0.5 } });

	  // Transition exiting bars to fade out.
	  var exitTransition = exit.transition()
	      .duration(duration)
	      .style("opacity", 1e-6)
	      .remove();
	      

	  // Transition exiting bars to the new x-scale.
	  exitTransition.selectAll("rect")
	      .attr("width", function(d) { return x(d.value); });

	  // Rebind the current node to the background.
	  svg.select(".background")
	      .datum(d)
	    .transition()
	      .duration(end)
	      .each("end", function() { filterTable(d.name, d.class_id) } );

	  d.index = i;
	}

	function up(d) {
	  if (!d.parent || this.__transition__) return;
	  var end = duration + d.children.length * delay;

	  appendLoadingText();

	  // Mark any currently-displayed bars as exiting.
	  var exit = svg.selectAll(".enter")
	      .attr("class", "exit");

	  // Enter the new bars for the clicked-on data's parent.
	  var enter = bar(d.parent)
	      .attr("transform", function(d, i) { return "translate(0," + barHeight * i * 1.2 + ")"; })
	      .style("opacity", 1e-6)
	      

	  // Color the bars as appropriate.
	  // Exiting nodes will obscure the parent bar, so hide it.
	  enter.select("rect")
	      //.style("fill", function(d) { return color(!!d.children); })
	      .attr("class", function(d) { return "category-" + d.class_id; }, true )
	      .classed("has-children", function(d) { return !!d.children; })
	      .style("fill-opacity", function(d) { if(d.children) { return 1 } else { return 0.5 } })	 	
	    .filter(function(p) { return p === d; })
	      .style("fill-opacity", 1e-6);

	  // Update the x-scale domain.
	  //console.log(d.parent)
	  console.log(d.parent.size);
	  x.domain([0, d.parent.size]).nice();

	  // Update the x-axis.
	  svg.selectAll(".x.axis").transition()
	      .duration(duration)
	      .call(xAxis);

	  //x.domain([0, d3.max(d.children, function(d) { return d.size; })]).nice();

	  // Transition entering bars to fade in over the full duration.
	  var enterTransition = enter.transition()
	      .duration(end)
	      .style("opacity", 1);

	  // Transition entering rects to the new x-scale.
	  // When the entering parent rect is done, make it visible!
	  enterTransition.select("rect")
	      .attr("width", function(d) { return x(d.size); })
	      .each("end", function(p) { if (p === d) d3.select(this).style("fill-opacity", null); });

	  // Transition exiting bars to the parent's position.
	  var exitTransition = exit.selectAll("g").transition()
	      .duration(duration)
	      .delay(function(d, i) { return i * delay; })
	      .attr("transform", stack(d.index));

	  // Transition exiting text to fade out.
	  exitTransition.select("text")
	      .style("fill-opacity", 1e-6);

	  // Transition exiting rects to the new scale and fade to parent color.
	  exitTransition.select("rect")
	      .attr("width", function(d) { return x(d.size); })
	      //.style("fill", color(true));
	      .style("fill-opacity", 1);

	  // Remove exiting nodes when the last child has finished transitioning.
	  exit.transition()
	      .duration(end)
	      .remove();

	  // Rebind the current parent to the background.
	  svg.select(".background")
	      .datum(d.parent)
	    .transition()
	      .duration(end)
	      .each("end", function(d) { filterTable(d.name, d.class_id) } );
	}

	// Creates a set of bars for the given data node, at the specified index.
	function bar(d) {
	  var bar = svg.insert("g", ".y.axis")
	      .attr("class", "enter")
	      .attr("transform", "translate(0,5)")
	    .selectAll("g")
	      .data(d.children)
	    .enter().append("g")
	      .style("cursor", function(d) { return !d.children ? null : "pointer"; })
	      .on("click", down);

	  bar.append("text")
	      .attr("x", -6)
	      .attr("y", barHeight / 2)
	      .attr("dy", ".35em")
	      .style("text-anchor", "end")
	      .text(function(d) { return d.name; });

	  bar.append("rect")
	      .attr("width", function(d) { return 0; })
	      .attr("height", barHeight)
	      //.on("click", function(d) { if(d.children) { filterTable(d.name, d.class_id) } });

	  return bar;
	}

	// A stateful closure for stacking bars horizontally.
	function stack(i) {
	  var x0 = 0;
	  return function(d) {
	    var tx = "translate(" + x0 + "," + barHeight * i * 1.2 + ")";
	    x0 += 0; //x(d.size);
	    return tx;
	  };
	}
}