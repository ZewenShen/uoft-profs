var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var querystring = require("querystring");
var spawn = require("child_process").spawn;
var exec = require("child_process").exec;
var util = require("util");

app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");

app.get("/", function(req, res) {
	res.send("homepage");
});

app.get("/profanalysis", function(req, res) {
	instructor = req.query.instructor;
	course = req.query.course;
	if (instructor === undefined || course === undefined) {
		res.render("profanalysis", {imgTag: ''});
	} else {
		var pythonPath = util.format("python3 %s '%s' %s", '../analysis/analyze_prof.py', instructor, course);
		exec(pythonPath, function(err, stdout, stderr) {
			if (err) {
				console.log('get plot err:' + stderr);
				res.render("profanalysis", {imgTag: ''});
			} else {
				res.render("profanalysis", {imgTag: stdout});
			}
		});
		/*
		var pythonProcess = spawn('python3', ['../analysis/analyze_prof.py', "'" + req.query.instructor + "'", req.query.course]);
		pythonProcess.stdout.on('data', function (data) {
			console.log("Enter python");
			imgTag = data.toString();
			res.render("profanalysis", {imgTag: imgTag});
		});
		*/
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
