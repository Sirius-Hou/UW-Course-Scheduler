from public import * # libraries and functions that are used in multiple files
import global_variables # global variables that are used in multiple files

import class_struct

ONLY_ADD_UNFILLED_SESSIONS = False


# compare each session's class_code, section, start_time, end_time, days
def same_session(session1, session2):
    return session1.class_code == session2.class_code and session1.section == session2.section and session1.start_time == session2.start_time and session1.end_time == session2.end_time and session1.days == session2.days


def is_overlapping(session1, session2):
    # Check if sessions have overlapping dates
    if session1.start_date != "" and session1.end_date != "" and session2.start_date != "" and session2.end_date != "":
        if session1.start_date > session2.end_date or session1.end_date < session2.start_date:
            return False

    # Check if sessions are on the same day
    if not set(session1.days).intersection(set(session2.days)):
        return False

    # Check if sessions overlap in time
    start1 = session1.start_time[0] * 60 + session1.start_time[1]
    end1 = session1.end_time[0] * 60 + session1.end_time[1]
    start2 = session2.start_time[0] * 60 + session2.start_time[1]
    end2 = session2.end_time[0] * 60 + session2.end_time[1]

    if start1 <= start2 < end1 or start1 < end2 <= end1:
        return True

    return False




# DEBUGGER
def print_schedule(schedule):
    #print("===================================================================================================")
    for session in schedule:
        print(session)
    print("===================================================================================================")
    print("\n")
    

# DEBUGGER
def print_schedule_list(schedule_list):
    for schedule in schedule_list:
        print_schedule(schedule)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END OF SCHEDULE LIST <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")
    return None




# curr_schedule: list of selected sessions
# to_be_scheduled_catagories: catagories of sessions to be scheduled (e.g., ['TST', 'LEC', 'LAB', 'TUT'] => still need to schedule a TST, LEC, LAB, and TUT session)
def add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions, courses_dict):
    # base case: all sessions have been scheduled
    if len(to_be_scheduled_sessions) == 0:
        new_schedule_list.append(curr_schedule.copy())
        return None

    # recursive case: add a session to the schedule
    curr_session = to_be_scheduled_sessions[0]
    to_be_scheduled_sessions = to_be_scheduled_sessions[1:]

    # if this course does not have a session of the current category, skip it
    if curr_course not in courses_dict or curr_session not in courses_dict[curr_course] or len(courses_dict[curr_course][curr_session]) == 0:
        add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions, courses_dict)
        return None

    for session in courses_dict[curr_course][curr_session]:
        # Check if session is full
        if ONLY_ADD_UNFILLED_SESSIONS:
            if session.capacity.isdigit() and session.current.isdigit() and session and int(session.capacity) <= int(session.current):
                continue

        # Check if session overlaps with any of the sessions in the current schedule
        overlapping = False
        for scheduled_session in curr_schedule:
            if is_overlapping(session, scheduled_session):
                overlapping = True
                break

        # If session does not overlap with any of the sessions in the current schedule, add it to the schedule
        if not overlapping:
            curr_schedule.append(session)
            add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions, courses_dict)
            curr_schedule.remove(session)

    return None



# use backtracking to generate all possible schedules
# schedule_list: list of schedules (Format: [list of [list of Session]])
# to_be_scheduled_course_names: list of course names to be scheduled
def add_courses_to_schedule(schedule_list, to_be_scheduled_course_names):
    for course in to_be_scheduled_course_names:
        new_schedule_list = []
        for curr_schedule in schedule_list:
            add_sessions_to_schedule(curr_schedule, new_schedule_list, course, ["TST", "LEC", "LAB", "TUT"], global_variables.courses_dict)
        schedule_list = new_schedule_list.copy()  
    return schedule_list


# current_schedule, target_schedule: both are lists of selected sessions
def get_schedule_convert_instructions(current_schedule, target_schedule):
    current_schedule_dict = {}
    for session in current_schedule:
        if session.course_name not in current_schedule_dict:
            current_schedule_dict[session.course_name] = []
        current_schedule_dict[session.course_name].append(session)
    
    target_schedule_dict = {}
    for session in target_schedule:
        if session.course_name not in target_schedule_dict:
            target_schedule_dict[session.course_name] = []
        target_schedule_dict[session.course_name].append(session)

    # print("Printing current schedule dict:")
    # for course in current_schedule_dict:
    #     print("Course: " + course)
    #     for session in current_schedule_dict[course]:
    #         print(session)
    
    # print("Printing target schedule dict:")
    # for course in target_schedule_dict:
    #     print("Course: " + course)
    #     for session in target_schedule_dict[course]:
    #         print(session)
    
    instructions = []
    diff_degree = 0

    # If a course is in the current schedule but not in the target schedule, remove all sessions of that course from the current schedule.
    # This action is called "Dropping a course" (counted as 1 step).
    for course in current_schedule_dict.copy():
        if course not in target_schedule_dict:
            msg = "DROP Course: " + course + "\nSessions:\n"
            for session in current_schedule_dict[course]:
                msg += session.print_session_simplified() + "\n"
                
            instructions.append(msg)
            del current_schedule_dict[course]
            diff_degree += 1
    
    # If a course is in the target schedule but not in the current schedule, add all sessions of that course to the current schedule.
    # This action is called "Adding a course" (counted as 1 step).
    for course in target_schedule_dict.copy():
        if course not in current_schedule_dict:
            msg = "ADD Course: " + course + "\nSessions:\n"
            for session in target_schedule_dict[course]:
                msg += session.print_session_simplified() + "\n"

            instructions.append(msg)
            del target_schedule_dict[course]
            diff_degree += 1

    # If a course is in both schedules, compare the sessions.
    # Compare each of the TST, LEC, TUT, LAB sessions.

    # Remove sessions that are in both schedules
    # (Note: use same_session(session1, session2) function instead of == to compare sessions!)
    for course in current_schedule_dict:
        for session1 in current_schedule_dict[course].copy():
            for session2 in target_schedule_dict[course].copy():
                if same_session(session1, session2):
                    current_schedule_dict[course].remove(session1)
                    target_schedule_dict[course].remove(session2)

    # Swap sessions of the same category from the same course
    for course in current_schedule_dict:
        for session in current_schedule_dict[course]:
            # search target_schedule_dict[course] for the session with the same category
            for target_session in target_schedule_dict[course]:
                if target_session.category == session.category:
                    # if the session has the same category, swap the session
                    #instructions.append("Swap session:\nCourse Name: " + course + "\nCategory:" + session.category + "\nFROM:\n" + str(session) + "\nTO:\n" + str(target_session) + "\n")
                    instructions.append("Swap session:\n FROM:\n" + session.print_session_simplified() + "\n TO:\n" + target_session.print_session_simplified() + "\n")
                    

                    diff_degree += 1
                    break

    return diff_degree, instructions








