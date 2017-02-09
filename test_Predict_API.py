import requests


def login_as_advisor():
    url = "https://ultra-integ.int.bbpd.io/webapps/login/"
    querystring = {"user_id": "alpha", "action": "login", "password": "alpha"}
    payload = ""
    response = session.post(url, data=payload, params=querystring)

    assert response.status_code == 200
    return url


def get_student():
    url = "https://ultra-integ.int.bbpd.io/telemetry/api/v1/predict/students?advisor=alpha/\
&availability=CURRENT&availability=FUTURE&availability=RECENT&limit=1&sort=goodProbability(asc)"
    response = session.get(url)
    json_data = response.json()

    return json_data['results'][0]["lmsId"]


def get_course():
    url = "https://ultra-integ.int.bbpd.io/telemetry/api/v1/predict/students"
    querystring = {"advisor": "alpha", "availability": ["CURRENT", "FUTURE", "RECENT"], "limit": "1",
                   "sort": "goodProbability(asc)"}
    response = session.get(url, params=querystring)

    return response.json()['results'][0]['courses'][0]['lmsId']


def test_1_student_profile_request():
    url = "https://ultra-integ.int.bbpd.io/telemetry/api/v1/predict/students"
    querystring = {"fields": "courseInstructors", "studentId": test_student}
    response = session.get(url, params=querystring)

    assert response.status_code == 200


def test_2_advisor_course_data():
    url = "https://ultra-integ.int.bbpd.io/telemetry/api/v1/predict/courses/{}".format(test_course)
    response = session.get(url)

    assert response.status_code == 200


def test_3_advise_student_data_per_course():
    url = "https://ultra-integ.int.bbpd.io/telemetry/api/v1/predict/courses/{course}/\
students/{student}".format(course=test_course, student=test_student)
    response = session.get(url)

    assert response.status_code == 200


def test_do_logout():
    url = "https://ultra-integ.int.bbpd.io/webapps/login/"
    querystring = {"action": "logout"}
    logout = session.post(url, params=querystring)

    assert logout.status_code == 200

session = requests.Session()
test_advisor = login_as_advisor()
test_student = get_student()
test_course = get_course()
