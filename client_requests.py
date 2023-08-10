from web_scraping import get_course_info_Requests
from text_formating import format_course_info
import re

# client_schedule = {'CS341' : [6021, 6888, 6893],
#                    'CS346' : [6905, 6907],
#                    'CS350' : [6958, 6359],
#                    'ECON371' : [4127],
#                    'STAT231' : [6433, 6879, 6885]}



def get_session_info(term, course_code, session_number): # e.g. 1239, CS, 136, 6300
    # Split course code into subject and number
    subject = re.findall('[A-Z]+', course_code)[0]
    course_number = re.findall('[0-9]+', course_code)[0]
    # get course info
    get_course_info_Requests(term, subject, course_number)
    course = format_course_info(course_code)
    # get the session info
    for session in course.class_sessions:
        if session.class_code == str(session_number):
            return session


# get course info
def get_client_courses(client_schedule):
    return None