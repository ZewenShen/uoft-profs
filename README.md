# uoft-courses

This library intends to offer course selection advice to students at UofT, e.g., whether the prof is good, whether the course is difficult, etc. Moreover, it automates the generation of one's timetable based on one's course selection.

## Functions to implement ...
  - [ ] Scrape all the course evaluation data from blackboard
  - [ ] Given all the courses one want to take in a semester, return a best time table based on time conflicts, course evaluation, etc.
  - [ ] Recommend courses in one's free time slots
  - [ ] Publish this service to the Internet

## Table of Contents
- [Requirements](#requirements)
- [Library Reference](#library-reference)
	- [CourseSpider](#coursespider)

## Requirements
 - [python3](https://www.python.org/downloads/release/python-352/)
 - [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
 - [requests](http://docs.python-requests.org/en/master/user/install/)
 - [pymysql](https://github.com/PyMySQL/PyMySQL)

## Library Reference

### CourseSpider
```shell
echo "host\nuser\npasssword\nport" > database.info
cd src/spider/coursespider/ 
python3 main.py 
```
Then all the data of courses currently offered at UofT will be sent to the given database, in table "Course" of the new created database "uoftcourses"

#### Schema of the table:
Course(<u>cID</u>, cName, credits, campus, department, <u>term</u>, division, prerequisites, exclusion, br, <u>lecNum</u>, lecTime, instructor, location, size, currentEnrollment)

#### Note:
host: ip address of the SQL server

user: user name of the SQL server

password: password of the user 

port: the port number that the SQL server is listening to

##### Example:
```shell
cat database.info
127.0.0.1
root
123456
3306
```

#### Demo:
![database](https://github.com/Walden-Shen/uoft-courses/blob/master/img/database_example.png?raw=true)
