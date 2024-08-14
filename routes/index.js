var express = require("express");
var router = express.Router();
var path = require("path");

var csrf = require("csurf");
var csrfProtection = csrf({ cookie: true });

var reportData = {
	"Acronym Replacement":
		require("../nlp/data/reports/acronym_replacement.js").data(),
	"Capitalisation Normalisation":
		require("../nlp/data/reports/capitalisation_normalisation.js").data(),
	"Common Acronyms": require("../nlp/data/reports/common_acronyms.js").data(),
	"Spelling Errors": require("../nlp/data/reports/spelling_errors.js").data(),
	"Error Words": require("../nlp/data/reports/error_words.js").data(),
	"Entity Recognition": require("../nlp/data/reports/prelim_tagging.js").data(),
	"Association Rule Mining":
		require("../nlp/data/reports/association_rule_mining_data.js").data(),
};

var timelineChartHelper = require("../helpers/timeline_chart_helper.js");

function buildRoute(path, action, variables) {
	router.get(path, csrfProtection, function (req, res, next) {
		res.render(action, variables); // Add the path to the response so it's easy to program the sidenav
	});
}

router.get("/", function (req, res) {
	res.redirect("/projects/dashboard");
});

router.get("/dashboard", function (req, res, next) {
	res.redirect("projects/dashboard");
});

//buildRoute('/',									'landing_page', {title: 'Home'})

// A separate path to show the progress of the Python code.
//buildRoute('/generator/running',	'generator_running', 	{ title: 'Generator - Running' });

buildRoute("/timeline", "visualisations/timeline", {
	title: "Timeline",
	showChartControls: true,
	chart: timelineChartHelper.getChart(),
});
buildRoute("/wordcloud", "visualisations/wordcloud", {
	title: "Word Cloud",
	showLoadingScreen: true,
});
// buildRoute('/wordcloud_words', 	'wordcloud_words', 	{ title: 'Word Cloud', 	showLoadingScreen: true, bodyWhiteBackground: true,  overflowHidden: true  });
buildRoute("/category-tree", "visualisations/category_tree", {
	title: "Category Tree",
	showDownloadYAML: true,
});

// Reports

buildRoute("/reports/spelling-errors-report", "reports/generic_report", {
	title: "Spelling Errors Report",
	data: reportData["Spelling Errors"],
});

buildRoute(
	"/entity-recognition-report",
	"visualisations/entity_recognition_report",
	{
		title: "Entity Recognition Report",
		data: reportData["Entity Recognition"],
		overflowHidden: true,
	},
);
buildRoute(
	"/association-rule-mining",
	"visualisations/association_rule_mining",
	{
		title: "Association Rule Mining",
		data: reportData["Association Rule Mining"],
		overflowHidden: true,
	},
);

buildRoute("/entity-linking-graph", "visualisations/entity_linking_graph", {
	title: "Entity Linking Graph",
	bodyWhiteBackground: true,
});

buildRoute("/entity-category-graph", "visualisations/entity_category_graph", {
	title: "Entity Category Graph",
	bodyWhiteBackground: true,
});
buildRoute("/decision-tree", "visualisations/decision_tree", {
	title: "Decision Tree",
	bodyWhiteBackground: true,
});

module.exports = router;
