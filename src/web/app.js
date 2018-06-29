var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var querystring = require("querystring");
var exec = require("child_process").exec;
var util = require("util");
var program = require("commander");

program
	.version('0.0.1')
	.option('-t, --test', 'Test mode for Travis')
	.parse(process.argv);

var ANALYZE_PROF_PATH = '../analysis/analyze_prof.py'

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('public'))
app.set("view engine", "ejs");

app.get("/|/profanalysis", function(req, res) {
	instructor = req.query.instructor;
	course = req.query.course;
	campus = req.query.campus;
	if (instructor == undefined || course == undefined || !/^[A-Za-z\s\.\-]*$/.test(instructor) || !/^[A-Z]{3}\d?\d?\d?$/.test(course) || (campus != 'St. George' && campus != 'Mississauga')) {
		res.render("profanalysis", {imgTag: ''});
	} else {
		var plotTerminal = util.format("python3 %s '%s' %s '%s'", ANALYZE_PROF_PATH, instructor, course, campus);
		exec(plotTerminal, function(err, stdout, stderr) {
			if (err) {
				console.log('get plot err:' + stderr);
				res.render("profanalysis", {imgTag: ''});
			} else {
				res.render("profanalysis", {imgTag: stdout});
			}
		});
	}
});

app.get("*", function(req, res) {
	res.redirect("/");
});

app.post("/analyzeprof", function(req, res) {
	var profInput = {instructor: req.body.instructor, course: req.body.course, campus: req.body.campus};
	var query = querystring.stringify(profInput);
	res.redirect("/?" + query);
});

if (program.test) {
	return 0;
} else {
	app.listen(3000, "127.0.0.1", function() {
		console.log("Server starts...");
	});
}
