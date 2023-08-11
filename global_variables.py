term = None
# course_list: [list of course names (strings)] (e.g. ['CS135', 'CS136', 'MATH135', 'MATH136'])
course_list = []

# client_schedule: dictionary: keys: course names (e.g. 'CS341'), values: list of session numbers (e.g. 6021) 
# (e.g. {'CS341' : [6021, 6888, 6893], 'CS346' : [6905, 6907]})
client_schedule = []

# courses: [list of Course objects (with names listed in course_list)]
courses = []

# courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}
courses_dict = {}

# all_generated_schedules: [list of generated schedules]
all_generated_schedules = []

# client_session_list: [list of sessions that the client has selected]
client_session_list = []
