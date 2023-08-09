from class_struct import *
from script import courses

def is_overlapping(session1, session2):
    # Check if sessions have overlapping dates
    if session1.startDate != "" and session1.endDate != "" and session2.startDate != "" and session2.endDate != "":
        if session1.startDate > session2.endDate or session1.endDate < session2.startDate:
            return False

    # Check if sessions are on the same day
    if not set(session1.days).intersection(set(session2.days)):
        return False

    # Check if sessions overlap in time
    start1 = session1.startTime[0] * 60 + session1.startTime[1]
    end1 = session1.endTime[0] * 60 + session1.endTime[1]
    start2 = session2.startTime[0] * 60 + session2.startTime[1]
    end2 = session2.endTime[0] * 60 + session2.endTime[1]

    if start1 <= start2 < end1 or start1 < end2 <= end1:
        return True

    return False








session_choices = []    # List of selected sessions
courses_dict = {}   # {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}


# curr_schedule: list of selected sessions
# to_be_scheduled_catagories: catagories of sessions to be scheduled (e.g., ['LEC', 'TST', 'LAB', 'TUT'] => still need to schedule a LEC, TST, LAB, and TUT session)
def add_sessions_to_schedule(curr_schedule, curr_course, to_be_scheduled_sessions):
    # base case: all sessions have been scheduled
    if len(to_be_scheduled_sessions) == 0:
        return curr_schedule
    
    # recursive case: add a session to the schedule
    curr_session = to_be_scheduled_sessions[0]
    to_be_scheduled_sessions = to_be_scheduled_sessions[1:]
    for session in courses_dict[curr_course][curr_session]:


# use backtracking to generate all possible schedules
# curr_schedule: list of selected sessions
# to_be_scheduled_course_names: list of course names to be scheduled
def add_courses_to_schedule(curr_schedule, to_be_scheduled_course_names):
    # base case: all courses have been scheduled
    if len(to_be_scheduled_course_names) == 0:
        return curr_schedule
    
    # recursive case: add a course to the schedule





def generate_combinations(courses):

    for course in courses:
        courses_dict[course.name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
        for session in course.sessions:
            if session.category == "TST":
                session_choices.append(session) # REQUIRE: if there is a TST session, it must be selected
            courses_dict[course.course_code + course.course_number][session.category].append(session)



    combinations = []   # List of combinations of selected sessions (e.g., [schedule1, schedule2, ...] => [[session1, session2, ...], [session3, session4, ...], ...])

    # Generate all possible combinations of sessions
    for course in courses:
        for lec in courses_dict[course.name]['LEC']:
            

