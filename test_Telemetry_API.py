import requests
from conftest import test_server


def login_as_instructor():
    url = "https://{}/webapps/login/".format(str(base_url))
    querystring = {"user_id": "alpha", "action": "login", "password": "abcd1234"}
    payload = ""
    session.post(url, data=payload, params=querystring)

    return url


def set_discussion_student_id():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{discussion}\
/telemetry/reports/discussionActivity".format(site=str(base_url), course=telem_course_id, discussion=discussion_id)
    response = session.get(url)

    if len(response.json()['topParticipants']) > 0:
        student_id = response.json()['topParticipants'][0]['user']['id']
    else:
        student_id = response.json()['nonParticipants'][0]['id']

    return student_id


def test_1_get_instructor_cookie():
    url = "https://{}/webapps/login/".format(str(base_url))
    querystring = {"user_id": "alpha", "action": "login", "password": "abcd1234"}
    payload = ""
    response = session.post(url, data=payload, params=querystring)

    assert response.status_code == 200
    return url


def test_2_discussion_activity_per_item():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{discussion}\
/telemetry/reports/discussionActivity".format(site=str(base_url), course=telem_course_id, discussion=discussion_id)
    response = session.get(url)
    jsondata = response.json()

    assert response.status_code == 200
    assert jsondata['courseId'] is not ''
    assert jsondata['contentId'] is not ''
    assert jsondata['avgCommentsPerStudent'] > 0
    assert jsondata['avgWordCountPerStudent'] > 0
    assert jsondata['avgGrade'] > 0

    if len(jsondata['topParticipants']) > 0:
        assert jsondata['topParticipants'][0]['user']['id'] is not ''
        assert jsondata['topParticipants'][0]['user']['userName'] is not ''
        assert jsondata['topParticipants'][0]['user']['avatarUrl'] is not ''
        assert jsondata['topParticipants'][0]['user']['givenName'] is not ''
        assert jsondata['topParticipants'][0]['user']['familyName'] is not ''
        assert jsondata['topParticipants'][0]['numComments'] > 0


def test_3_discussion_activity_per_user():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{discussion}\
/telemetry/reports/discussionActivity/{discussion_user}".format(site=str(base_url), course=telem_course_id,
                                                                discussion=discussion_id,
                                                                discussion_user=discussion_user_id)
    response = session.get(url)

    assert response.status_code == 200


def test_4_student_content_activity_in_detail():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{activity}/\
telemetry/reports/studentContentActivityInDetail".format(site=str(base_url), course=telem_course_id,
                                                         activity=activity_id)
    response = session.get(url)

    assert response.status_code == 200


def test_5_activity_vs_grade():
    url = "https://{site}/learn/api/v1/courses/{course}/telemetry/reports/\
activityVsGrade".format(site=str(base_url), course=telem_course_id)
    response = session.get(url)

    assert response.status_code == 200


def test_6_course_activity():
    url = "https://{site}/learn/api/v1/courses/{course}/telemetry/reports/\
activityVsGrade".format(site=str(base_url), course=telem_course_id)
    response = session.get(url)

    assert response.status_code == 200


def test_7_course_grades():
    url = "https://{site}/learn/api/v1/courses/{course}/telemetry/reports/courseGrades".format(site=str(base_url),
                                                                                               course=telem_course_id)
    response = session.get(url)

    assert response.status_code == 200


def test_8_student_activity():
    url = "https://{site}/learn/api/v1/courses/{course}/telemetry/\
reports/studentActivity".format(site=str(base_url), course=telem_course_id)
    querystring = {"userId": student_user_id}
    response = session.get(url, params=querystring)

    assert response.status_code == 200


def test_9_student_grades():
    url = "https://{site}/learn/api/v1/courses/{course}/telemetry/reports/studentGrades".format(site=str(base_url),
                                                                                                course=telem_course_id)
    querystring = {"userId": student_user_id}
    response = session.get(url, params=querystring)

    assert response.status_code == 200


def test_10_student_multimedia_activity_in_detail():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{activity}/\
telemetry/reports/studentMultimediaActivityInDetail".format(site=str(base_url), course=multimedia_course_id,
                                                            activity=multimedia_id)
    response = session.get(url)

    assert response.status_code == 200


def test_11_student_multimedia_statistics():
    url = "https://{site}/learn/api/v1/courses/{course}/contents/{activity}/\
telemetry/reports/studentMultimediaStatistics".format(site=str(base_url), course=multimedia_course_id,
                                                      activity=multimedia_id)
    response = session.get(url)

    assert response.status_code == 200


def test_do_logout():
    url = "https://{}/webapps/login/".format(str(base_url))
    querystring = {"action": "logout"}
    logout = session.post(url, params=querystring)

    assert logout.status_code == 200


# Flags
base_url = test_server
session = requests.Session()
telem_course_id = "_47312_1"
multimedia_course_id = "_47156_1"
discussion_id = "_291295_1"
activity_id = "_290905_1"
multimedia_id = "_288995_1"
student_user_id = "_76906_1"
test_instructor_id = login_as_instructor()
discussion_user_id = set_discussion_student_id()
