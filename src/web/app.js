var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var querystring = require("querystring");
var exec = require("child_process").exec;
var spawn = require("child_process").spawn;
var util = require("util");

var ANALYZE_PROF_PATH = '../analysis/analyze_prof.py'
var COURSE_LIST_PATH = '../analysis/get_course_list_by_instructor.py'

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('public'))
app.set("view engine", "ejs");

app.get("/", function(req, res) {
	res.send("homepage");
});

app.get("/profanalysis", function(req, res) {
	instructor = req.query.instructor;
	course = req.query.course;
	campus = req.query.campus;
	if (instructor == undefined || course == undefined || !/^[A-Za-z\s]*$/.test(instructor) || !/^[A-Z]{3}\d?\d?\d?$/.test(course) || (campus != 'St. George' && campus != 'Mississauga')) {
		res.render("profanalysis", {imgTag: ''});
	} else {
		courseDataString = '';
		courseListPY = spawn('python3', [COURSE_LIST_PATH, instructor, campus]);
		courseListPY.stdout.on('data', function(data) {
			courseDataString += data.toString();
		});
		var courseList = [];
		courseListPY.stdout.on('end', function() {
			courseList = JSON.parse(courseDataString);
		});
		/*
		var courseListTerminal = util.format("python3 %s '%s' '%s'", COURSE_LIST_PATH, instructor, campus);
		exec(courseListTerminal, function(err, stdout, stderr) {
			if (err) {
				console.log('get course list err:' + stderr);
			} else {
				courseList = JSON.parse(stdout);
			}
		});
		*/

		var plotTerminal = util.format("python3 %s '%s' %s '%s'", ANALYZE_PROF_PATH, instructor, course, campus);
		exec(plotTerminal, function(err, stdout, stderr) {
			if (err) {
				console.log('get plot err:' + stderr);
				res.render("profanalysis", {imgTag: '', courseList: courseList});
			} else {
				res.render("profanalysis", {imgTag: stdout, courseList: courseList});
			}
		});
	}
});

app.post("/analyzeprof", function(req, res) {
	var profInput = {instructor: req.body.instructor, course: req.body.course, campus: req.body.campus};
	var query = querystring.stringify(profInput);
	res.redirect("/profanalysis?" + query);
});


app.listen(3000, "127.0.0.1", function() {
	console.log("Server starts...");
});
