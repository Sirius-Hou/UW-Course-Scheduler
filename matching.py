import global_variables
import re

ONLY_ADD_UNFILLED_SESSIONS = False



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
    print("CURRENT SCHEDULE:")
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
    if len(courses_dict[curr_course][curr_session]) == 0:
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


def convert_session_list_to_schedule(session_list):
    schedule = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    for session in session_list:
        for day in session.days:
            if day == 'M':
                schedule['Monday'].append(session)
            elif day == 'T':
                schedule['Tuesday'].append(session)
            elif day == 'W':
                schedule['Wednesday'].append(session)
            elif day == 'Th':
                schedule['Thursday'].append(session)
            elif day == 'F':
                schedule['Friday'].append(session)

    for day in schedule:
        schedule[day].sort(key=lambda x: x.start_time)

    return schedule


def print_calendar_schedule(schedule):
    print("\033[33m===============================================================================================================================\033[0m")
    for day in schedule:
        print("\033[33m{}\033[0m".format(day))
        for session in schedule[day]:
            print(session)
        print()
    print("\033[33m===============================================================================================================================\033[0m")


def print_calendar_schedule_simplified(schedule):
    print("\033[33m===============================================================================================================================\033[0m")
    for day in schedule:
        print("\033[33m{}\033[0m".format(day))
        for session in schedule[day]:
            s = "\033[0m" + (session.course_name).ljust(10) \
            + ("[" + session.class_code + "]").ljust(8) \
            + (session.section).ljust(10) \
            + (str(session.start_time[0]) + " " + str(session.start_time[1]) \
            + " - " \
            + str(session.end_time[0]) + " " + str(session.end_time[1])).ljust(22) \
            + (str(session.days)).ljust(20)

            if session.start_date != "" and session.end_date != "":
                s += (str(session.start_date) + " - " + str(session.end_date)).ljust(18)
            else:
                s += "".ljust(15)


            s += (session.room).ljust(10) + session.instructor


            print(s)
        print()
    print("\033[33m===============================================================================================================================\033[0m")



def print_calendar_schedule_simplified_to_file(schedule, file):
    file.write("===============================================================================================================================\n")
    for day in schedule:
        file.write("{}\n".format(day))
        for session in schedule[day]:
            s = (session.course_name).ljust(10) \
            + ("[" + session.class_code + "]").ljust(8) \
            + (session.section).ljust(10) \
            + (str(session.start_time[0]) + " " + str(session.start_time[1]) \
            + " - " \
            + str(session.end_time[0]) + " " + str(session.end_time[1])).ljust(22) \
            + (str(session.days)).ljust(20)

            if session.start_date != "" and session.end_date != "":
                s += (str(session.start_date) + " - " + str(session.end_date)).ljust(18)
            else:
                s += "".ljust(15)


            s += (session.room).ljust(10) + session.instructor

            file.write(s + "\n\n")
    file.write("===============================================================================================================================\n\n")



def print_dict(schedule_dict_categorized):
    for course in schedule_dict_categorized:
        for category in schedule_dict_categorized[course]:
            print(course, category, schedule_dict_categorized[course][category])
    print("\n\n")



def get_schedule_convert_instructions(current_schedule, target_schedule):
    """
    Gets the instructions required to convert from a current schedule to a target schedule.

    Parameters:
        current_schedule (Schedule): The current schedule.
        target_schedule (Schedule): The target schedule.
        schedule_diff_set (Set): The set of sessions that need to be added or removed from the current schedule to get to the target schedule.

    Returns:
        A list of instructions to convert from the current schedule to the target schedule.
    """
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
            instructions.append("DROP Course" + course)
            del current_schedule_dict[course]
            diff_degree += 1
    
    # If a course is in the target schedule but not in the current schedule, add all sessions of that course to the current schedule.
    # This action is called "Adding a course" (counted as 1 step).
    for course in target_schedule_dict.copy():
        if course not in current_schedule_dict:
            instructions.append("ADD Course: " + course)
            del target_schedule_dict[course]
            diff_degree += 1



    # print("Printing current schedule dict AFTER DELETION:")
    # for course in current_schedule_dict:
    #     print("Course: " + course)
    #     for session in current_schedule_dict[course]:
    #         print(session)
    
    # print("\n")

    # print("Printing target schedule dict AFTER DELETION:")
    # for course in target_schedule_dict:
    #     print("Course: " + course)
    #     for session in target_schedule_dict[course]:
    #         print(session)

    # print("\n")
    


    
    # If a course is in both schedules, compare the sessions.
    # Compare each of the TST, LEC, TUT, LAB sessions.

    # Remove sessions that are in both schedules
    for course in current_schedule_dict:
        for session in current_schedule_dict[course].copy():
            if session in target_schedule_dict[course]:
                current_schedule_dict[course].remove(session)
                target_schedule_dict[course].remove(session)

    
    # print("Printing current schedule dict AFTER removing same sessions:")
    # for course in current_schedule_dict:
    #     print("Course: " + course)
    #     for session in current_schedule_dict[course]:
    #         print(session)
    #     print()
    
    # print("\n")
    # print("Printing target schedule dict AFTER removing same sessions:")
    # for course in target_schedule_dict:
    #     print("Course: " + course)
    #     for session in target_schedule_dict[course]:
    #         print(session)
    #     print()


    
    for course in current_schedule_dict:
        for session in current_schedule_dict[course]:
            # search target_schedule_dict[course] for the session with the same category
            for target_session in target_schedule_dict[course]:
                if target_session.category == session.category:
                    # if the session has the same category, swap the session
                    instructions.append("Swap session:\nCourse Name: " + course + "\nCategory:" + session.category + "\nFROM:\n" + str(session) + "\nTO:\n" + str(target_session) + "\n")
                    diff_degree += 1
                    break





    # Categorize the remaining sessions based on their type
    # current_schedule_dict_categorized = {}
    # target_schedule_dict_categorized = {}
    # for course in current_schedule_dict:
    #     for session in current_schedule_dict[course]:
    #         if session.category not in current_schedule_dict_categorized[course]:
    #             current_schedule_dict_categorized[course] = {session.category : None}
    #         current_schedule_dict_categorized[course][session.category] = session
            

    # for course in target_schedule_dict:
    #     for session in target_schedule_dict[course]:
    #         if session.category not in target_schedule_dict_categorized[course]:
    #             target_schedule_dict_categorized[course] = {session.category : None}
    #         target_schedule_dict_categorized[course][session.category] = session


    # print("Printing current_schedule_dict_categorized:")
    # print_dict(current_schedule_dict_categorized)
    # print("\n")
    # print("Printing target_schedule_dict_categorized:")
    # print_dict(target_schedule_dict_categorized)
    # print("\n")


    # # Generate instructions for each category
    # for course in current_schedule_dict_categorized:
    #     for category in current_schedule_dict_categorized[course]:
    #         instructions.append("Swap course session:\nCourse Name: " + course + "\nCategory:\n" + category + "\nFROM:\n" + str(current_schedule_dict_categorized[course][category]) + "\nTO:\n" + str(target_schedule_dict_categorized[course][category]) + "\n")
    #         diff_degree += 1
    

    return diff_degree, instructions








