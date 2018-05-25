var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var querystring = require("querystring");
var exec = require("child_process").exec;
var util = require("util");

var ANALYZE_PROF_PATH = '../analysis/analyze_prof.py'

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('public'))
app.set("view engine", "ejs");

app.get("/", function(req, res) {
	res.send("homepage");
});

app.get("/profanalysis", function(req, res) {
	instructor = req.query.instructor;
	course = req.query.course;
	if (instructor == undefined || course == undefined) {
		res.render("profanalysis", {imgTag: ''});
	} else {
		var pythonTerminal = util.format("python3 %s '%s' %s", ANALYZE_PROF_PATH, instructor, course);
		exec(pythonTerminal, function(err, stdout, stderr) {
			if (err) {
				console.log('get plot err:' + stderr);
				res.render("profanalysis", {imgTag: ''});
			} else {
				res.render("profanalysis", {imgTag: stdout});
			}
		});
	}
});

app.post("/analyzeprof", function(req, res) {
	var profInput = {instructor: req.body.instructor, course: req.body.course};
	var query = querystring.stringify(profInput);
	//console.log(query);
	res.redirect("/profanalysis?" + query);
});


app.listen(3000, "127.0.0.1", function() {
	console.log("Server starts...");
});
