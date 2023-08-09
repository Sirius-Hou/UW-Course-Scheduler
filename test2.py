import re
from class_struct import *






dayTime1 = "11:30-01:20F"
dayTime2 = "10:30-12:00MWF"
dayTime3 = "07:30-09:20TTh"
dayTime4 = "08:00-09:20M05/10-05/11"
dayTime5 = "03:30-04:20Th10/23-10/23"
dayTime6 = "09:19-10:20M05/08-05/09"

s1 = Session("12345", "L1A", "100", "50", "10", "5", dayTime4, "MC 2036", "John Doe")
s2 = Session("12345", "L1B", "100", "50", "10", "5", dayTime6, "MC 2036", "John Doe")

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



course1 = Course("ECE", "192", "Eng Economics & Society Impact", [
                Session("3374", "LEC 001", "144", "118", "0", "0", "03:30-04:20TW05/09-05/17", "E7 5343", "Calero,Ivan"),
                Session("3376", "TUT 101", "48", "36", "0", "0", "10:30-11:20M", "E7 4053", ""),
                Session("3377", "TUT 102", "48", "41", "0", "0", "10:30-11:20M", "E7 4053", ""),
                Session("3378", "TUT 103", "48", "41", "0", "0", "10:30-11:20M", "E7 4053", ""),
                Session("3375", "LEC 002", "144", "128", "0", "0", "11:30-12:20TW05/09-05/17", "E7 5343", "Calero,Ivan"),
                Session("3379", "TUT 104", "48", "42", "0", "0", "01:30-02:20M", "E7 4053", ""),
                Session("3380", "TUT 105", "48", "42", "0", "0", "01:30-02:20M", "E7 4053", ""),
                Session("3381", "TUT 106", "48", "44", "0", "0", "01:30-02:20M", "E7 4053", ""),
                Session("3579", "LEC 003", "135", "123", "0", "0", "12:30-01:20MW", "STC 0010", "Peralta Moarry,Dario"),
                Session("3580", "TUT 107", "135", "123", "0", "0", "12:30-01:20F", "", "")
                ])

course2 = Course("MATH", "239", "Intro Combinatorics", [
                Session("3881", "LEC 001", "135", "126", "0", "0", "10:30-11:20MWF", "MC 1085", "Crew,Logan"),
                Session("3882", "LEC 002", "135", "125", "0", "0", "11:30-12:20MWF", "STC 0060", "Nayak,Ashwin"),
                Session("3995", "LEC 003", "135", "117", "0", "0", "12:30-01:20MWF", "STC 0050", "Mandelshtam,Olya"),
                Session("4016", "LEC 004", "135", "135", "0", "0", "01:30-02:20MWF", "STC 0050", "Stebila,Douglas"),
                Session("4017", "TUT 104", "135", "135", "0", "0", "10:30-11:20F", "STC 0060", ""),
                Session("3887", "TUT 101", "135", "126", "0", "0", "02:30-03:20W", "STC 0060", ""),
                Session("3888", "TUT 102", "135", "125", "0", "0", "04:30-05:20M", "STC 0060", ""),
                Session("3996", "TUT 103", "135", "117", "0", "0", "09:30-10:20M", "STC 0060", ""),
                Session("3901", "TST 201", "540", "503", "0", "0", "04:30-06:20Th07/06-07/06", "", "")
                ])


course3 = Course("CS", "348", "Intro Database Management", 
                 [Session("3853", "LEC 001", "80", "32", "0", "0", "04:00-05:20TTh", "MC 2038", "Toman,David"),
                  Session("4089", "LEC 002", "80", "80", "0", "0", "01:00-02:20TTh", "MC 2035", "Maiyya,Sujaya"),
                  Session("4223", "LEC 003", "140", "131", "0", "0", "02:30-03:50TTh", "STC 0040", "Toman,David"),
                  Session("5401", "LEC 004", "80", "80", "0", "0", "10:00-11:20TTh", "MC 4059", "Maiyya,Sujaya"),
                  Session("4344", "TST 101", "380", "323", "0", "0", "07:00-08:50M06/26-06/26", "", "Davies,Sylvie Lynne")])

course4 = Course("CO", "250", "Intro Optimization", 
                 [Session("3840", "LEC 001", "120", "113", "0", "0", "11:30-12:50MW05/08-08/01", "MC 4020", "Pashkovich,Kanstantsin"),
                  Session("3841", "LEC 002", "120", "107", "0", "0", "11:30-12:50TTh", "MC 4059", "van der Pol,Jorn"),
                  Session("4311", "LEC 003", "120", "96", "0", "0", "01:00-02:20MW", "MC 4061", "Bhattiprolu,Vijay"),
                  Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin"),
                  Session("4239", "LEC 081", "130", "112", "0", "0", "", "Online", "Pei,Martin")])


courses = [course1, course2, course3, course4]
session_choices = []    # List of selected sessions
courses_dict = {}   # {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}


for course in courses:
        courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
        for session in course.class_sessions:
            if session.category == "TST":
                session_choices.append(session) # REQUIRE: if there is a TST session, it must be selected
            courses_dict[course.course_code + course.course_number][session.category].append(session)


# DEBUGGER
def print_schedule(schedule):
    print("CURRENT SCHEDULE:")
    #print("===================================================================================================")
    for session in schedule:
        print(session)
    print("===================================================================================================")
    print("\n")
    








# def add_sessions_to_schedule(curr_schedule, curr_course, session_types, new_schedule_list):
#     # base case: all sessions have been scheduled
#     if len(session_types) == 0:
#         new_schedule_list.append(curr_schedule.copy())
#         return None

#     # recursive case: add a session to the schedule
#     curr_session_type = session_types[0]
#     session_types = session_types[1:]

#     for session in courses_dict[curr_course][curr_session_type]:
#         # Check if session overlaps with any of the sessions in the current schedule
#         overlapping = False
#         for scheduled_session in curr_schedule:
#             if is_overlapping(session, scheduled_session):
#                 overlapping = True
#                 break

#         # If session does not overlap with any of the sessions in the current schedule, add it to the schedule
#         if not overlapping:
#             curr_schedule.append(session)
#             add_sessions_to_schedule(curr_schedule, curr_course, session_types, new_schedule_list)
#             curr_schedule.remove(session)

#     #restore session_types to original state (insert curr_session_type back to the front of session_types)
#     session_types.insert(0, curr_session_type)
#     return None





# def add_courses_to_schedule(schedule, to_be_scheduled_course_names):
#     new_schedule_list = []
#     for course in to_be_scheduled_course_names:
#         for curr_schedule in schedule:
#             add_sessions_to_schedule(curr_schedule, course, ["TST", "LEC", "LAB", "TUT"], new_schedule_list)
#         schedule = new_schedule_list.copy()
#         new_schedule_list.clear()
#     return schedule


def print_schedule_list(schedule_list):
    for schedule in schedule_list:
        print_schedule(schedule)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END OF SCHEDULE LIST <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")
    return None




# curr_schedule: list of selected sessions
# to_be_scheduled_catagories: catagories of sessions to be scheduled (e.g., ['TST', 'LEC', 'LAB', 'TUT'] => still need to schedule a TST, LEC, LAB, and TUT session)
def add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions):
    # base case: all sessions have been scheduled
    if len(to_be_scheduled_sessions) == 0:
        #print_schedule(curr_schedule)
        # print("ADDED A NEW COURSE SCHEDULE: ")
        # print(curr_course)
        new_schedule_list.append(curr_schedule.copy())
        # print("PRINTING curr_schedule:")
        # print_schedule(curr_schedule)
        # print("PRINTING new_schedule_list:")
        # print_schedule(new_schedule_list)
        return None

    # recursive case: add a session to the schedule
    curr_session = to_be_scheduled_sessions[0]
    to_be_scheduled_sessions = to_be_scheduled_sessions[1:]

    # if this course does not have a session of the current category, skip it
    if len(courses_dict[curr_course][curr_session]) == 0:
        add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions)
        return None

    for session in courses_dict[curr_course][curr_session]:
        # Check if session overlaps with any of the sessions in the current schedule
        overlapping = False
        for scheduled_session_tutple in curr_schedule:
            scheduled_session = scheduled_session_tutple[1]
            if is_overlapping(session, scheduled_session):
                # print("SESSION OVERLAPS: " + session.classCode + " " + session.section + " " + session.category)
                # print("WITH: " + scheduled_session.classCode + " " + scheduled_session.section + " " + scheduled_session.category)
                overlapping = True
                break

        # If session does not overlap with any of the sessions in the current schedule, add it to the schedule
        if not overlapping:
            curr_schedule.append((curr_course, session))
            add_sessions_to_schedule(curr_schedule, new_schedule_list, curr_course, to_be_scheduled_sessions)
            curr_schedule.remove(session)

    return None



# use backtracking to generate all possible schedules
# schedule_list: list of schedules (Format: [list of [list of (course_name, session)]])
# to_be_scheduled_course_names: list of course names to be scheduled
def add_courses_to_schedule(schedule_list, to_be_scheduled_course_names):
    for course in to_be_scheduled_course_names:
        new_schedule_list = []
        for curr_schedule in schedule_list:
            # print("ADDING A NEW COURSE SCHEDULE: ")
            # print(course)

            # print("CURRENT OLD SCHEDULE TO BE ADDED ON:")
            # print_schedule(curr_schedule)

            add_sessions_to_schedule(curr_schedule, new_schedule_list, course, ["TST", "LEC", "LAB", "TUT"])
            # print("AFTER ADDING SESSIONS: (printing new_schedule_list))")
            # print_schedule_list(new_schedule_list)

        schedule_list = new_schedule_list.copy()
        # print(f"FINISHED ADDING COURSE {course}, CURRENT SCHEDULES: ")
        # print("SCHEDULE_LIST:")
        # print_schedule_list(schedule_list)
        # print("NEW_SCHEDULE_LIST:")
        # print_schedule_list(new_schedule_list)      

        
    return schedule_list



schedule_list1 = [[Session("0301", "TST 201", "100", "100", "0", "0", "08:30-10:20M05/11-05/11", "BA 1130", "Paul Gries"),
                  Session("0103", "LEC 003", "100", "100", "0", "0", "11:00-12:00MWF", "BA 1130", "Paul Gries"),
                  Session("0202", "TUT 102", "100", "100", "0", "0", "1:00-2:00F", "BA 1130", "Paul Gries")],

                  [Session("0301", "TST 201", "100", "100", "0", "0", "08:30-10:20M05/11-05/11", "BA 1130", "Paul Gries"),
                  Session("0103", "LEC 003", "100", "100", "0", "0", "11:00-12:00MWF", "BA 1130", "Paul Gries"),
                  Session("0203", "TUT 103", "100", "100", "0", "0", "2:00-3:00F", "BA 1130", "Paul Gries")]]

schedule_list2 = [[Session("3840", "LEC 001", "120", "113", "0", "0", "11:30-12:50MW05/08-08/01", "MC 4020", "Pashkovich,Kanstantsin"),
                   Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                   
                   [Session("3841", "LEC 002", "120", "107", "0", "0", "11:30-12:50TTh", "MC 4059", "van der Pol,Jorn"),
                    Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                    
                    [Session("4311", "LEC 003", "120", "96", "0", "0", "01:00-02:20MW", "MC 4061", "Bhattiprolu,Vijay"),
                     Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                    
                    [Session("4239", "LEC 081", "130", "112", "0", "0", "", "Online", "Pei,Martin"),
                     Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")]]


# new_schedule_list = []
# curr_course = "CS348"
# add_sessions_to_schedule(schedule_list2[0], new_schedule_list, curr_course, ["TST", "LEC", "LAB", "TUT"])
# print_schedule_list(new_schedule_list)


schedule_list = [[]]

result = add_courses_to_schedule(schedule_list, ["CO250", "CS348", "MATH239", "ECE192"])

print(len(schedule_list))

# for curr_schedule in schedule_list:
#     print("PRINTING SCHEDULE:")

#     print_schedule(curr_schedule)

print_schedule_list(result)
print(len(result))





# course1 = Course("CS", "108", "Intro to Computer Programming", 
#                 [Session("0101", "LEC 001", "100", "100", "0", "0", "08:00-09:00MWF", "BA 1130", "Paul Gries"),
#                  Session("0102", "LEC 002", "100", "100", "0", "0", "10:00-11:00MWF", "BA 1130", "Paul Gries"),
#                  Session("0103", "LEC 003", "100", "100", "0", "0", "11:00-12:00MWF", "BA 1130", "Paul Gries"),
#                  Session("0201", "TUT 101", "100", "100", "0", "0", "11:30-1:00F", "BA 1130", "Paul Gries"),
#                  Session("0202", "TUT 102", "100", "100", "0", "0", "1:00-2:00F", "BA 1130", "Paul Gries"),
#                  Session("0203", "TUT 103", "100", "100", "0", "0", "2:00-3:00F", "BA 1130", "Paul Gries"),
#                  Session("0301", "TST 201", "100", "100", "0", "0", "08:30-10:20M05/11-05/11", "BA 1130", "Paul Gries")])

# course2 = Course("CS", "148", "Intro to Computer Science",
#                  [Session("1101", "LEC 301", "100", "100", "0", "0", "08:00-09:00TTh", "BA 1150", "John Doe"),
#                   Session("1102", "LEC 302", "100", "100", "0", "0", "09:00-10:00TTh", "BA 1150", "John Doe"),
#                   Session("1103", "LEC 303", "100", "100", "0", "0", "10:00-11:00TTh", "BA 1150", "John Doe"),
#                   Session("1201", "LAB 401", "100", "100", "0", "0", "11:30-12:30F", "BA 1150", "John Doe"),
#                   Session("1202", "LAB 402", "100", "100", "0", "0", "12:30-1:30F", "BA 1150", "John Doe"),
#                   Session("1203", "LAB 403", "100", "100", "0", "0", "1:30-2:30F", "BA 1150", "John Doe"),
#                   Session("1301", "TST 501", "100", "100", "0", "0", "05:30-06:20M05/09-05/09", "BA 1150", "John Doe")])

# course3 = Course("CS", "348", "Intro Database Management", 
#                  [Session("3853", "LEC 001", "80", "32", "0", "0", "04:00-05:20TTh", "MC 2038", "Toman,David"),
#                   Session("4089", "LEC 002", "80", "80", "0", "0", "01:00-02:20TTh", "MC 2035", "Maiyya,Sujaya"),
#                   Session("4223", "LEC 003", "140", "131", "0", "0", "02:30-03:50TTh", "STC 0040", "Toman,David"),
#                   Session("5401", "LEC 004", "80", "80", "0", "0", "10:00-11:20TTh", "MC 4059", "Maiyya,Sujaya"),
#                   Session("4344", "TST 101", "380", "323", "0", "0", "07:00-08:50M06/26-06/26", "", "Davies,Sylvie Lynne")])

# course4 = Course("CO", "250", "Intro Optimization", 
#                  [Session("3840", "LEC 001", "120", "113", "0", "0", "11:30-12:50MW05/08-08/01", "MC 4020", "Pashkovich,Kanstantsin"),
#                   Session("3841", "LEC 002", "120", "107", "0", "0", "11:30-12:50TTh", "MC 4059", "van der Pol,Jorn"),
#                   Session("4311", "LEC 003", "120", "96", "0", "0", "01:00-02:20MW", "MC 4061", "Bhattiprolu,Vijay"),
#                   Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin"),
#                   Session("4239", "LEC 081", "130", "112", "0", "0", "", "Online", "Pei,Martin")])