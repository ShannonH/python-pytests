from requests_oauthlib import OAuth1Session
import pytest


# gets the first student Id returned from a list of student data
# Pre-requisites: The endpoint, GET /advise/api/public/v1/students, must be functional
# NOTE: This workaround exists because the current SIS Student Ids are flushed daily and assigned by random
#       It would take some metadata tweaking to the demo data on the snowflake side to have the Ids static
def get_integ_student_id():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students'
    response = integ_oauth.get(url)

    return response.json()['results'][0]['studentId']


# gets the id for known student with closed courses: Ruhan A
def get_dev_student_id():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students?sort=name.family(asc)&limit=6'
    response = dev_oauth.get(url)

    return response.json()['results'][3]['studentId']


# gets the total number of students with advise data for the site
# Pre-requisites: The endpoint, GET /advise/api/public/v1/students, must be functional
def get_student_num():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students?limit=1000'
    response = integ_oauth.get(url)
    json_data = response.json()

    student_number = len(json_data['results'])

    return student_number


# gets the number of students in a given course
# Pre-requisites: The endpoint, GET /advise/api/public/v1/courses/{courseId}/predictions, must be functional
def get_student_in_course_num():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions?limit=1000'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    course_number = len(json_data['results'])

    return course_number


# gets the number of courses for given student
# Pre-requisites: The endpoint, GET /advise/api/public/v1/students, must be functional
def get_student_course_num():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    student_course_number = len(json_data['results'])

    return student_course_number


# 1: Single student course prediction with invalid Course Id
def test_1_single_student_course_prediction_invalid_course_id():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions'.format('NVLD-404')
    response = integ_oauth.get(url)

    assert response.status_code == 404


# 2: Single student course prediction with valid Course Id
def test_2_single_student_course_prediction_valid_course_id():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions'.format(course_id)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 3: Single student course prediction with an unsupported parameter
def test_3_single_student_course_prediction_unsupported_parameter():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?hello=3'.format(course_id)
    response = integ_oauth.get(url)

    # the hello parameter is ignored
    assert response.status_code == 200


# 4: Single student course prediction with sort parameter: "positiveOutcomeProbability(asc)"
# Manual: Check results to see if positive outcome probability is sorted in ascending order
def test_4_single_student_course_prediction_pos_prob_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=positiveOutcomeProbability(asc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 probabilities
    for x in range(sort_range):
        print(str(json_data['results'][x]['positiveOutcomeProbability']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 5: Single student course prediction with sort parameter: "positiveOutcomeProbability(desc)"
# Manual: Check results to see if positive outcome probability is sorted in descending order
def test_5_single_student_course_prediction_pos_prob_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=positiveOutcomeProbability(desc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 probabilities
    for x in range(sort_range):
        print(str(json_data['results'][x]['positiveOutcomeProbability']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 6: Single student course prediction with sort parameter: "negativeOutcomeProbability(asc)"
# Manual: Check results to see if negative outcome probability is sorted in ascending order
def test_6_single_student_course_prediction_neg_prob_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=negativeOutcomeProbability(asc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 probabilities
    for x in range(sort_range):
        print(str(json_data['results'][x]['negativeOutcomeProbability']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 7: Single student course prediction with sort parameter: "negativeOutcomeProbability(desc)"
# Manual: Check results to see if negative outcome probability is sorted in descending order
def test_7_single_student_course_prediction_neg_prob_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=negativeOutcomeProbability(desc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 probabilities
    for x in range(sort_range):
        print(str(json_data['results'][x]['negativeOutcomeProbability']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 8: Single student course prediction with sort parameter: "studentId(asc)"
# Manual: Check results to see if student Id is sorted in ascending order
def test_8_single_student_course_prediction_student_id_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=studentId(asc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['studentId']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 9: Single student course prediction with sort parameter: "studentId(desc)"
# Manual: Check results to see if student Id is sorted in descending order
def test_9_single_student_course_prediction_student_id_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?sort=studentId(desc)'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['studentId']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 10: Single student course prediction returns default limit of 50
def test_10_single_student_course_prediction_limit_default():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 50


# 11: Single student course prediction with in range limit parameter: "limit=#"
def test_11_single_student_course_prediction_in_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?limit=5'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 5


# 12: Single student course prediction with limit parameter value that is not an integer: "limit=invalid"
@pytest.mark.xfail(reason='CADL-1962')
def test_12_single_student_course_prediction_invalid_limit_input():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?limit=invalid'.format(course_id)
    response = integ_oauth.get(url)

    assert response.status_code == 400


# 13: Single student course prediction with out of range limit parameter: "limit=#"
def test_13_single_student_course_prediction_out_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?limit=1001'.format(course_id)
    response = integ_oauth.get(url)

    assert response.status_code == 400


# 14: Single student course prediction with in range offset parameter: "offset=#"
# Pre-requisites: The endpoint must return at least 3 results
def test_14_single_student_course_prediction_in_range_result_offset():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions'.format(course_id)
    response = integ_oauth.get(url)
    json_data = response.json()
    offset_url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?offset=3'.format(course_id)
    offset_response = integ_oauth.get(offset_url)
    offset_json_data = offset_response.json()

    # compare unique Ids of third dataset and the first dataset where offset=3
    assert response.status_code == 200 and \
        offset_json_data['results'][0]['studentId'] == json_data['results'][3]['studentId']


# 15: Single student course prediction with out of range offset parameter: "offset=#"
def test_15_single_student_course_prediction_out_range_result_offset():
    offset_num = get_student_in_course_num() + 1
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{course}/predictions\
?offset={offset}'.format(course=course_id, offset=offset_num)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 16: Single student course prediction with invalid offset input type: "offset=invalid"
@pytest.mark.xfail(reason='CADL-1962')
def test_16_single_student_course_prediction_invalid_offset_input():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions\
?offset=invalid'.format(course_id)
    response = integ_oauth.get(url)

    assert response.status_code == 400


# 17: Student course Advise details
def test_17_student_course_advise_details():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students'
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 18: Student course Advise details with sort parameter: "studentId(asc)"
# Manual: Check results to see if student Id is sorted in ascending order
def test_18_student_course_advise_details_student_id_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=studentId(asc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['studentId']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 19: Student course Advise details with sort parameter: "studentId(desc)"
# Manual: Check results to see if student Id is sorted in descending order
def test_19_student_course_advise_details_student_id_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=studentId(desc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['studentId']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 20: Student course Advise details with sort parameter: "name.given(asc)"
# Manual: Check results to see if given name is sorted in ascending order
def test_20_student_course_advise_details_given_name_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=name.given(asc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['name']['given']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 21: Student course Advise details with sort parameter: "name.given(desc)"
# Manual: Check results to see if given name is sorted in descending order
def test_21_student_course_advise_details_given_name_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=name.given(desc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['name']['given']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 22: Student course Advise details with sort parameter: "name.family(asc)"
# Manual: Check results to see if family name is sorted in ascending order
def test_22_student_course_advise_details_family_name_asc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=name.family(asc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Ascending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['name']['family']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 23: Student course Advise details with sort parameter: "name.family(desc)"
# Manual: Check results to see if family name is sorted in descending order
def test_23_student_course_advise_details_family_name_desc():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=name.family(desc)'
    response = integ_oauth.get(url)
    json_data = response.json()

    print('Descending order:', end=' ')
    # gets the first 10 Ids
    for x in range(sort_range):
        print(str(json_data['results'][x]['name']['family']) + ' ', end=' ')
    print()

    assert response.status_code == 200 and manual_test_off


# 24: Student course Advise details with an unsupported sort value
@pytest.mark.xfail(reason='CADL-1962')
def test_24_student_course_advise_details_unsupported_sort_value():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?sort=invalid'
    response = integ_oauth.get(url)

    # the hello parameter is ignored
    assert response.status_code == 400


# 25: Student course Advise details with no limit specified returns default of 50
def test_25_student_course_advise_details_limit_default():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students'
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 50


# 26: Student course Advise details with in range limit parameter: "limit=#"
def test_26_student_course_advise_details_in_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?limit=5'
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 5


# 27: Student course Advise details with out of range limit parameter: "limit=#"
def test_27_student_course_advise_details_out_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?limit=1001'
    response = integ_oauth.get(url)

    assert response.status_code == 400


# 28: Student course Advise details with an unsupported parameter
def test_28_student_course_advise_details_unsupported_parameter():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?hello=3'
    response = integ_oauth.get(url)

    # the hello parameter is ignored
    assert response.status_code == 200


# 29: Student course Advise details with in range offset parameter: "offset=#"
# Pre-requisites: The endpoint must return at least 3 results
def test_29_student_course_advise_details_in_range_result_offset():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students'
    response = integ_oauth.get(url)
    json_data = response.json()
    offset_url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?offset=3'
    offset_response = integ_oauth.get(offset_url)
    offset_json_data = offset_response.json()

    # compare unique Ids of third dataset and the first dataset where offset=3
    assert response.status_code == 200 and \
        offset_json_data['results'][0]['studentId'] == json_data['results'][3]['studentId']


# 30: Student course Advise details with out of range offset parameter: "offset=#"
def test_30_student_course_advise_details_out_range_result_offset():
    offset_num = get_student_num() + 1
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students\
?offset={}'.format(offset_num)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 31: Student course predictions with a valid SIS Student Id
def test_31_student_course_predictions():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 32: Student course predictions with an invalid SIS Student Id
def test_32_student_course_predictions_invalid_id():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions'.format('102315231')
    response = integ_oauth.get(url)

    assert response.status_code == 404


"""
# These are blocked out until the course availability data is good

# 33: Student course predictions with course availability parameter: "availability=CLOSED"
# and student has closed courses
@pytest.mark.xfail
def test_33_student_course_predictions_closed_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=CLOSED'.format(dev_student_id)
    response = dev_oauth.get(url)

    assert response.status_code == 200


# 33.1: Student course predictions with course availability parameter: "availability=CLOSED"
# and student has NO closed courses
@pytest.mark.xfail
def test_33_1_student_course_predictions_no_closed_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=CLOSED'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 404



# 34: Student course predictions with course availability parameter: "availability=RECENT"
# and student has recent courses
def test_34_student_course_predictions_recent_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=RECENT'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    assert response.status_code == 200



# 34.1: Student course predictions with course availability parameter: "availability=RECENT"
# and student has NO recent courses
def test_34_1_student_course_predictions_no_recent_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=RECENT'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 404


# 35: Student course predictions with course availability parameter: "availability=CURRENT"
# and student has current courses
def test_35_student_course_predictions_current_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=CURRENT'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 35.1: Student course predictions with course availability parameter: "availability=CURRENT"
# and student has NO current courses
def test_33_1_student_course_predictions_no_current_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=CURRENT'.format(dev_student_id)
    response = dev_oauth.get(url)

    assert response.status_code == 404



# 36: Student course predictions with course availability parameter: "availability=FUTURE"
# and student has future courses
def test_36_student_course_predictions_future_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=FUTURE'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    assert response.status_code == 200



# 36.1: Student course predictions with course availability parameter: "availability=FUTURE"
# and student has NO future courses
@pytest.mark.xfail
def test_36_1_student_course_predictions_no_future_courses():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=FUTURE'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 404
"""


# 37: Student course predictions with invalid course availability parameter value: "availability=INVALID"
def test_37_student_course_predictions_invalid_avail_param_value():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?availability=INVALID'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 404


# 38: Student course predictions with no limit specified returns up to 50 by default
def test_38_student_course_predictions_default_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 50


# 39: Student course predictions with in range limit parameter: "limit=#"
def test_39_student_course_predictions_in_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?limit=5'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()

    num_results = len(json_data['results'])

    assert response.status_code == 200 and num_results <= 5


# 40: Student course predictions with out of range limit parameter: "limit=#"
def test_40_student_course_predictions_out_range_result_limit():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?limit=1001'.format(test_student_id)
    response = integ_oauth.get(url)

    assert response.status_code == 400


# 41: Student course predictions with in range offset parameter: "offset=#"
# Pre-requisites: The student must have at least 1 resulting course
def test_41_student_course_predictions_in_range_result_offset():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions'.format(test_student_id)
    response = integ_oauth.get(url)
    json_data = response.json()
    offset_url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?offset=1'.format(test_student_id)
    offset_response = integ_oauth.get(offset_url)
    offset_json_data = offset_response.json()

    # compare unique course Ids of third dataset and the first dataset where offset=1
    assert response.status_code == 200 and \
        offset_json_data['results'][0]['courseId'] == json_data['results'][1]['courseId']


# 42: Student course predictions with out of range offset parameter: "offset=#"
def test_42_student_course_predictions_out_range_result_offset():
    offset_num = get_student_course_num() + 1
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{student}/predictions\
?offset={offset}'.format(student=test_student_id, offset=offset_num)
    response = integ_oauth.get(url)

    assert response.status_code == 200


# 43: Student course predictions with an unsupported parameter
def test_43_student_course_predictions_unsupported_parameter():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?hello=3'.format(test_student_id)
    response = integ_oauth.get(url)

    # the hello parameter is ignored
    assert response.status_code == 200


# 44: Bad oAuth credentials for course predictions
def test_44_bad_oauth_credentials_course_predictions():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/courses/{}/predictions'.format(course_id)
    response = bad_oauth.get(url)

    assert response.status_code == 403


# 45: Bad oAuth credentials for students
def test_45_bad_oauth_credentials_students():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students'
    response = bad_oauth.get(url)

    assert response.status_code == 403


# 46: Bad oAuth credentials for student predictions
def test_46_bad_oauth_credentials_student_predictions():
    url = 'https://api-beta.cloud.bb/advise/api/public/v1/students/{}/predictions\
?hello=3'.format(test_student_id)
    response = bad_oauth.get(url)

    assert response.status_code == 403


integ_client_key = '#'
integ_client_secret = '#'
dev_client_key = '#'
dev_client_secret = '#'
bad_key = 'badkey'
bad_secret = 'badsecret'
# since the tests will be all get requests, in theory, we will do this all in one session
integ_oauth = OAuth1Session(client_key=integ_client_key, client_secret=integ_client_secret)
dev_oauth = OAuth1Session(client_key=dev_client_key, client_secret=dev_client_secret)
bad_oauth = OAuth1Session(client_key=bad_key, client_secret=bad_secret)

# Toggles
# the number of entries shown for manual testing in sorts
sort_range = 10
# the valid course Id to test upon
course_id = 'CMSC-205'
# set=True to ignore manual tests
manual_test_off = True
test_student_id = get_integ_student_id()
dev_student_id = get_dev_student_id()
