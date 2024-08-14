var express = require("express");
var router = express.Router();

// Todo: update so it's projects/301 instead
router.get("/dashboard", function (req, res, next) {
  res.render("projects/dashboard", { title: "Dashboard" });
});

module.exports = router;
