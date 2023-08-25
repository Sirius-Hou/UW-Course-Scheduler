
# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
term = 1239 # enter the term code
course_list = ['CS341', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes (make sure to enter the full name, no space, case sensitive (e.g., EMLS101R not EMLS101r or EMLS 101R)))
#course_list = ['CS136', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
course_list = ['PMATH331', 'CO250', 'STAT341', 'ACTSC372', 'CS330']
client_schedule_path = 'docs/client/client_current_schedule.txt' # default path for client schedule
client_schedule_path = 'docs/client/catherine.txt'
# ===================================================================================================


# client_schedule: dictionary: keys: course names (e.g. 'CS341'), values: list of session numbers (e.g. 6021) 
# (e.g. {'CS341' : [6021, 6888, 6893], 'CS346' : [6905, 6907]})
client_schedule = []

# Example:
# client_schedule = {'CS341' : [6021, 6888, 6893],
#                    'CS346' : [6905, 6907],
#                    'CS350' : [6958, 6359],
#                    'ECON371' : [4127],
#                    'STAT231' : [6433, 6879, 6885]}


# client_session_list: [list of sessions that the client has selected]
client_session_list = []


# client_schedule_calendar_dict: {'Monday': [list of sessions on Monday], 'Tuesday': [list of sessions on Tuesday], ...]}
client_schedule_calendar_dict = []

# courses that failed to be requested based on client's current schedule (e.g. ['COOP 1'])
# (Note: this might be caused due to incorrect term number or special courses that are not in the undergrad course database (e.g., COOP category courses))
client_request_failed_courses = []



# courses: [list of Course objects (with names listed in course_list)]
courses = []

# courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}, 'SEM': <list of sessions>}
courses_dict = {}

# all_generated_schedules: [list of generated schedules]
all_generated_schedules = []

# schedule_list_sorted: [list of schedule objects sorted by diff_degree from the client schedule]
schedule_list_sorted = []
