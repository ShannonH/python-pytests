# How to install

_These tests can be run on most popular operating systems. Required software is just Python 3_

1. Download and install Python for your system: https://www.python.org/downloads/
1. Install pytest using pip (Python package manager)  
 `pip install -U pytest`
1. Install the requests module using pip  
`pip install -U requests`
1. Install the oauth modules using pip  
`pip install -U requests_oauthlib`

# How to get test files

Download a zipped file of all test files:  
1. Click the download button in toolbar  
1. Unzip the file to your machine

### Before moving on, you will need to obtain proper Learn creds (logins and key/secret combinations) and have data available to query. Plug these into the proper variables in the tests.

# How to run the tests:
1. Open terminal or command prompt
1. Change directories to the python-pytests location  
`cd ~/python-pytests` or `cd C:\Users\user\Desktop\python-pytests`
* To run all tests in the directory  
`python -m pytest`
* To run all tests in a specific test file  
`python -m pytest test_Advise_API.py`
* To run specific tests using a keyword in the test name (example using keyword student)   
`python -m pytest -k student`
* To run specific tests using keywords in specific test files (example using keyword student)  
`python -m pytest test_Advise_API.py -k student`
* To run tests and view all output in the terminal/command prompt  
`python -m pytest -s`
* To run tests and view each test name with pass/fail result
`python -m pytest -v`
* To run tests and view both output and pass/fail results:
`python -m pytest -v -s`
* To run tests in a single file and view all output and pass/fail results:
`python -m pytest -v -s test_Telemetry_API.py`

More ways to invoke pytest can be found at http://doc.pytest.org/en/latest/usage.html

# Running Telemetry tests against other environments (under construction)

By default, these tests will run against https://ultra-integ.int.bbpd.io  
There's a command line switch that allows running against other environments:
* The switch is `--test_server`
* Make sure to enter a fully qualified domain name
  * `--test_server=https://learn.blackboard.com`    

# Reading pytest output

#### Sample output from `python -m pytest`:  
```
=========================== test session starts ============================
platform darwin -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
rootdir: /Users/sharris/python-pytests, inifile: 
collected 58 items 

test_Advise_API.py ...........x...x.......x............x.....
test_Predict_API.py ....
test_Telemetry_API.py ............

================== 54 passed, 4 xfailed in 44.34 seconds ===================
```

* You can see that 58 tests were collected out of all 3 test files in the python-pytests directory
* Each file shows its own results
* A `.` represents a passed test
* An `x` represents a test that was expected to fail (if you look at the tests in the code, you see a reason for each marked test)
* The total number of passes, fails, xfails and the amount of time taken to complete the run

#### Sample output from `python -m pytest -s`:  
```
=========================== test session starts ============================
platform darwin -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
rootdir: /Users/sharris/python-pytests, inifile: 
collected 58 items 

test_Advise_API.py ...Ascending order: 0.03  0.04  0.06  0.07  0.08  0.09  0.095  0.105  0.1433333333  0.15  
.Descending order: 0.99  0.99  0.99  0.98  0.97  0.96  0.935  0.925  0.9166666667  0.9133333333  
.Ascending order: 0.01  0.01  0.01  0.02  0.03  0.04  0.065  0.075  0.08333333333  0.08666666667  
.Descending order: 0.97  0.96  0.94  0.93  0.92  0.91  0.905  0.895  0.8566666667  0.85  
.Ascending order: 10003461  10007596  10008677  10017790  10019945  10020607  10020626  10026009  10028431  10029113  
.Descending order: 10998767  10995255  10991881  10988822  10988237  10988004  10984626  10984570  10983281  10979946  
...x...x.Ascending order: 10003461  10007596  10008677  10017790  10019945  10020607  10020626  10026009  10028431  10029113  
.Descending order: 10998767  10995255  10991881  10988822  10988237  10988004  10984626  10984570  10983281  10979946  
.Ascending order: Ada  Adam  Alan  Albert  Albert  Albert  Alberto  Alecia  Alejandro  Alfred  
.Descending order: Zachariah  Yvonne  Yong  Wilma  William  William  William  William  William  William  
.Ascending order: Abbott  Acosta  Adams  Agar  Aguilar  Alexander  Alexander  Alfaro  Allen  Alligood  
.Descending order: Zimmermann  Ziemer  Ziegler  Young  Wyatt  Wyatt  Wong  Wolff  Wolfe  Winn  
.x............x.....
test_Predict_API.py ....
test_Telemetry_API.py ............

================== 54 passed, 4 xfailed in 15.06 seconds ===================
```

* This output includes all of the same text as before, but will include any data that was set to print out in the tests
* In this example, Advise tests include tests for ordering, so they are set to print out the values returned from the API call so you can visually verify the order

#### Sample output from `python -m pytest` that has a failed test:  
```
=========================== test session starts ============================
platform darwin -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
rootdir: /Users/sharris/python-pytests, inifile: 
collected 58 items 

test_Advise_API.py ...........x...x.......x............x.....
test_Predict_API.py ....
test_Telemetry_API.py .F..........

================================= FAILURES =================================
___________________ test_2_discussion_activity_per_user ____________________

    def test_2_discussion_activity_per_user():
        url = "https://{}/learn/api/v1/courses/_47312_1/contents/_291295_1\
    /telemetry/reports/discussionActivity/_768903_1".format(str(base_url))
        response = session.get(url)
    
>       assert response.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404]>.status_code

test_Telemetry_API.py:36: AssertionError
============= 1 failed, 53 passed, 4 xfailed in 12.42 seconds ==============
```

* In this output, you can see an `F` which indicates a failed test in the test_Telemetry_API file
* After the run summary, failures are printed, including the entire test block and why it failed
* In this example, the test for discussion activity failed because the status code that got returned was not 200, it was 404
* The end line shows 1 failure, 53 passed tests and 4 expected failures; the entire test run was 12.42 seconds

#### Sample output from `python -m pytest -v test_Telemetry_API.py`:
```
============================= test session starts ==============================
platform darwin -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0 -- /usr/local/bin/python3.5
cachedir: .cache
rootdir: /Users/sharris/python-pytests, inifile: 
collected 12 items 

test_Telemetry_API.py::test_1_get_instructor_cookie PASSED
test_Telemetry_API.py::test_2_discussion_activity_per_item PASSED
test_Telemetry_API.py::test_3_discussion_activity_per_user PASSED
test_Telemetry_API.py::test_4_student_content_activity_in_detail PASSED
test_Telemetry_API.py::test_5_activity_vs_grade PASSED
test_Telemetry_API.py::test_6_course_activity PASSED
test_Telemetry_API.py::test_7_course_grades PASSED
test_Telemetry_API.py::test_8_student_activity PASSED
test_Telemetry_API.py::test_9_student_grades PASSED
test_Telemetry_API.py::test_10_student_multimedia_activity_in_detail PASSED
test_Telemetry_API.py::test_11_student_multimedia_statistics PASSED
test_Telemetry_API.py::test_do_logout PASSED

========================== 12 passed in 1.84 seconds ===========================
```

* In this output, each line indicates a test within the test_Telemetry_API.py file
* The line shows test_file_name::test_name  PASSED or FAILED