# uoft-courses

This library intends to offer course selection advice to students at UofT, e.g., whether the prof is good, whether the course is difficult, etc. Moreover, it automates the generation of one's timetable based on one's course selection.

## Functions to implement ...
  - [x] Scrape all the course evaluation data from blackboard
  - [ ] Given all the courses one want to take in a semester, return a best time table based on time conflicts, course evaluation, etc.
  - [ ] Recommend courses in one's free time slots
  - [ ] Publish this service to the Internet

## Table of Contents
- [Requirements](#requirements)
- [Library Reference](#library-reference)
	- [Spider](#spider)
	- [CourseSpider](#coursespider)
	- [EvalSpider](#evalspider)

## Requirements
 - [python3](https://www.python.org/downloads/release/python-352/)
 - [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
 - [requests](http://docs.python-requests.org/en/master/user/install/)
 - [pymysql](https://github.com/PyMySQL/PyMySQL)
 - [lxml](http://lxml.de/index.html#download)

## Library Reference

### Spider
```shell
echo -e "host\nuser\npasssword\nport" > database.info
cd src/spider/
python3 main.py 
```
Then all the data of courses currently offered at UofT & all the evaluation data will be sent to the given database. Courses' data is in table "Course" and evaluation data is in table "Eval". The two tables are both under the new created database "uoftcourses"

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

```shell
echo "host\nuser\npasssword\nport" > database.info
cd src/spider/coursespider/
python3 cspider.py 
```

Use this if you only need course data.

#### Data source:
[Course Finder](http://coursefinder.utoronto.ca)

#### Schema of the table Course:
Course(<u>cID</u>, cName, credits, campus, department, <u>term</u>, division, prerequisites, exclusion, br, <u>lecNum</u>, lecTime, instructor, location, size, currentEnrollment)

#### Demo:
![courseTable](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/course_table_example.png?raw=true)

### EvalSpider

```shell
echo "host\nuser\npasssword\nport" > database.info
cd src/spider/evalspider/
python3 espider.py 
```

Use this if you only need course evaluation data.

#### Data source:
[Faculty of Arts & Science Course Evaluations](https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=seipDRPeug8Eu)

#### Schema of the table:
Eval(department, <u>cID</u>, <u>cName</u>, <u>lecNum</u>, campus, term, instructor, <u>instructorFullName</u>, intellectuallySimulating, deeperUnderstanding, courseAtmosphere, homeworkQuality, homeworkFairness, overallQuality, enthusiasm, workload, recommend, numInvited, numResponded)

#### Demo:
![evalTable](https://github.com/Walden-Shen/uoft-courses/blob/master/examples/images/eval_table_example.png?raw=true)
