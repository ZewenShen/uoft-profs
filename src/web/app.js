var express = require("express");
var app = express();
var bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");

app.get("/", function(req, res) {
	res.send("home page");
});

app.listen(3000, "127.0.0.1", function() {
	console.log("Server starts...");
});
