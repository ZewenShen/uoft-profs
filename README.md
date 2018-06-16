# uoft-courses

This library intends to offer course selection advice to students at UofT, e.g., whether the prof is good, whether the course is difficult, etc. Moreover, it automates the generation of one's timetable based on one's course selection.

## Functions to implement ...
  - [x] Scrape all the course evaluation data from Blackboard
  - [ ] Given all the courses one want to take in a semester, return a best time table based on time conflicts, course evaluation, etc.
  - [ ] Recommend courses in one's free time slots
  - [x] Analyze course evaluation data from BlackBoard
  - [x] Publish this service to the Internet

## Table of Contents
- [Requirements](#requirements)
- [Library Reference](#library-reference)
	- [Spider](#spider)
		- [CourseSpider](#coursespider)
		- [EvalSpider](#evalspider)
	- [AnalyzeProf](#analyzeprof)
	- [Web](#web)

## Requirements
 - [python3](https://www.python.org/downloads/release/python-352/)
 - [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
 - [requests](http://docs.python-requests.org/en/master/user/install/)
 - [pymysql](https://github.com/PyMySQL/PyMySQL)
 - [lxml](http://lxml.de/index.html#download)
 - [numpy](https://www.scipy.org/scipylib/download.html)
 - [matplotlib](https://matplotlib.org/users/installing.html)
 - [pandas](https://pandas.pydata.org/getpandas.html)

## Library Reference

### Spider

#### Usage
```shell
echo -e "host\nuser\npasssword\nport" > database.info
cd src/spider/
python3 main.py -h
usage: main.py [-h] [-i] [-c] [-e]

optional arguments:
  -h, --help    show this help message and exit
  -i, --init    initialize the database
  -c, --course  scrape courses offered at uoft
  -e, --eval    scrape eval data from uoft blackboard
```

#### database.info Example:
```shell
cat database.info
127.0.0.1
root
123456
3306
```

#### Note:
host: ip address of the SQL server

user: user name of the SQL server

password: password of the user 

port: the port number that the SQL server is listening to

### CourseSpider

#### Data source:
[Course Finder](http://coursefinder.utoronto.ca)

#### Schema of the table Course:
Course(<u>cID</u>, cName, credits, campus, department, <u>term</u>, division, prerequisites, exclusion, br, <u>lecNum</u>, lecTime, instructor, location, size, currentEnrollment)

#### Demo:
![courseTable](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/course_table_example.png?raw=true)

### EvalSpider

#### Data source:
[Faculty of Arts & Science Course Evaluations](https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=seipDRPeug8Eu)

#### Schema of the table:
Eval(department, <u>cID</u>, <u>cName</u>, <u>lecNum</u>, campus, term, instructor, <u>instructorFullName</u>, intellectuallySimulating, deeperUnderstanding, courseAtmosphere, homeworkQuality, homeworkFairness, overallQuality, enthusiasm, workload, recommend, numInvited, numResponded)

#### Demo:
![evalTable](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/eval_table_example.png?raw=true)

### AnalyzeProf

#### Usage

```shell
cd src/analysis/
python3 analyze_prof.py -h
usage: analyze_prof.py [-h] [-p] instructor courseID campus

positional arguments:
  instructor  The full name of an instructor
  courseID    The id of a course, e.g., CSC240
  campus	  The campus where the instructor stays

optional arguments:
  -h, --help  show this help message and exit
  -p, --plot  Plot the graph in GUI mod (if this flag is not set on, an html 
		      img tag will be printed to stdout)
```
#### Demo:

![profAnalyze](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/prof_analyze_example.png?raw=true)

### Web

Powered by Express.js and Bootstrap.

#### Demo:

[webpage](http://uoftprofs.com)

![webAnalysis](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/web_analysis_example.png?raw=true)
