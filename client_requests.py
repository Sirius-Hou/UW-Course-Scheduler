from public import * # libraries and functions that are used in multiple files
import global_variables # global variables that are used in multiple files

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


def extract_client_schedule(file_path):
	if not os.path.exists(file_path):
		console.log("ERROR: Client schedule file does not exist: " + file_path)
		return False

	content = ""
	with open(file_path, "r") as f:
		content = f.read()

	course_list = []
	status_match_results1 = re.findall(r'.*?\bStatus\b', content, re.DOTALL)
	for status_match in status_match_results1:
		course_name_matches = re.findall(r'[A-Z]+ \d+', status_match)

		course_name = course_name_matches[-1].replace(" ", "") if course_name_matches else None

		course_list.append(course_name)


	session_list = []
	status_match_results2 = re.split(r'(?=\bStatus\b)', content)

	if len(status_match_results2) > 0:
		status_match_results2.pop(0)

	for status_match in status_match_results2:
		matches = re.findall(r'\b\d{4}\s+\d{3}\b', status_match)
		sessions = []
		for match in matches:
			sessions.append(int(match.split("\n")[0]))
		
		session_list.append(sessions)
		
	result = {}
	for i in range(len(course_list)):
		result[course_list[i]] = session_list[i]
	
	return result

