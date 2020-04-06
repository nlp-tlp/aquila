var tooltipTimeout;
var tooltip = document.getElementById("tooltip");
var tooltip_heading = tooltip.getElementsByTagName("h2")[0];
var tooltip_content = tooltip.getElementsByTagName("p")[0];
var modules = document.getElementsByClassName("has-tooltip");
var tooltipTimeoutOpen;
var tooltipTimeoutClose;
for(var i = 0; i < modules.length; i++) {
	modules[i].onmouseover = function(ele) {
		tooltip.classList.remove('no-display');
		window.clearInterval(tooltipTimeoutClose);
		tooltipTimeoutOpen = window.setTimeout(function() {
			tooltip.classList.add('show');
		}, 500);
		tooltip_heading.innerHTML = this.dataset.ttheading;//('data-ttheading');
		tooltip_content.innerHTML = this.dataset.ttcontent;//this.attr('data-ttcontent');
	}
	modules[i].onmouseleave = function() {
		tooltip.classList.remove('show');
		window.clearInterval(tooltipTimeoutOpen);
		tooltipTimeoutClose = window.setTimeout(function() {
			tooltip.classList.add('no-display');
		}, 200);			
	}
}
document.onmousemove = function(e) {
	var xOffset = 20;
	if(e.pageX > (window.innerWidth - 560)) {
		xOffset = -540;
	}

	tooltip.style.left = e.pageX + xOffset + "px";
	tooltip.style.top = e.pageY + 20 + "px";
}		
		