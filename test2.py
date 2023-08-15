import global_variables
from class_struct import Course, Session, Schedule
from web_scraping import get_course_info_Requests
from text_formating import format_course_info
from chatgpt import chat_with_gpt, gpt_generate_schedule, gpt_convert_to_calendar_format
from matching import add_courses_to_schedule, convert_session_list_to_schedule, print_calendar_schedule, print_calendar_schedule_simplified, print_calendar_schedule_simplified_to_file, get_schedule_convert_instructions
from client_requests import get_session_info
import re
import pickle
import os


#DEBUGGER
# compare each session's class_code, section, start_time, end_time, days
def compare_sessions_and_print(session1, session2):
    result = True
    if session1.class_code != session1.class_code:
        print("Class code different: ")
        print("session1.class_code: ")
        print(session1.class_code)
        print("session2.class_code: ")
        print(session2.class_code)
        result = False
    if session1.section != session2.section:
        print("Section different: ")
        print("session1.section: ")
        print(session1.section)
        print("session2.section: ")
        print(session2.section)
        result = False
    if session1.start_time != session2.start_time:
        print("Start time different: ")
        print("session1.start_time: ")
        print(session1.start_time)
        print("session2.start_time: ")
        print(session2.start_time)
        result = False
    if session1.end_time != session2.end_time:
        print("End time different: ")
        print("session1.end_time: ")
        print(session1.end_time)
        print("session2.end_time: ")
        print(session2.end_time)
        result = False
    if session1.days != session2.days:
        print("Days different: ")
        print("session1.days: ")
        print(session1.days)
        print("session2.days: ")
        print(session2.days)
        result = False
    
    return result




# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
#term = 1239 # enter the term code
global_variables.term = 1239
global_variables.course_list = ['CS341', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes (make sure to enter the full name, no space, case sensitive (e.g., EMLS101R not EMLS101r or EMLS 101R)))
#course_list = ['CS240', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
#===================================================================================================
# The sessions that user currently enrolled in (Beta version: mannual input required)
global_variables.client_schedule = {'CS341' : [6021, 6888, 6893],
                                    'CS346' : [6905, 6907],
                                    'CS350' : [6958, 6359],
                                    'ECON371' : [4127],
                                    'STAT231' : [6433, 6879, 6885]}

#=================================================================================================================================
# Step 0: Check whether term, course_list, and client_schedule are unchanged since last time
# INPUT_IDENTITY: if user input is unchanged since the last execution (term, course_list, and client_schedule)
INPUT_IDENTITY = [False, False]

if os.path.exists('data/prev.pickle'):
    # load the previous data from the file
    with open('data/prev.pickle', 'rb') as f:
        prev_data = pickle.load(f)

    # check if the current data is identical to the previous data
    INPUT_IDENTITY = [prev_data['term'] == global_variables.term and prev_data['course_list'] == global_variables.course_list,
                      prev_data['client_schedule'] == global_variables.client_schedule]

with open('data/prev.pickle', 'wb') as f:
    data = {
        'term': global_variables.term,
        'course_list': global_variables.course_list,
        'client_schedule': global_variables.client_schedule
    }
    pickle.dump(data, f)

print("Term & Course List are unchanged: " + str(INPUT_IDENTITY[0]))
print("Client Schedule is unchanged: " + str(INPUT_IDENTITY[1]))

# DEBUG MODE: MANUAL OVERRIDE, FORCE TO RECALCULATE
#INPUT_IDENTITY = [False, False]


#=================================================================================================================================
# STEP 1: For each course, get the course info and save to a csv file, then format the info and save to a txt file
# If either term or course_list is changed since last time, then calculate courses again

global_variables.courses = []
for course in global_variables.course_list:
    course_code = re.findall('[A-Z]+', course)[0]
    course_number = course[len(course_code):]
    get_course_info_Requests(global_variables.term, course_code, course_number)
    global_variables.courses += format_course_info(course)


# If term and course_list are unchanged since last time, then skip this step

# Load courses from local file
print("Loading courses from data/courses.pickle ...")
with open('data/courses.pickle', 'rb') as f:
    pickle_courses = pickle.load(f)


# TESTING
courses_same = True
for i in range(len(global_variables.courses)):
    # find the course in pickle_courses that has the same course_code and course_number as the current course
    for j in range(len(pickle_courses)):
        if global_variables.courses[i].course_code == pickle_courses[j].course_code and global_variables.courses[i].course_number == pickle_courses[j].course_number:
            # compare each session's class_code, section, start_time, end_time, days in the two courses
            for k in range(len(global_variables.courses[i].class_sessions)):
                courses_same = compare_sessions_and_print(global_variables.courses[i].class_sessions[k], pickle_courses[j].class_sessions[k])
                

print(f">>>>>> COMPARISON RESULT: global_variables.courses == pickle_courses: {str(courses_same)}\n")



# DEBUGGER
# for course in courses:
#     print(course)
#     print("\n")



#=================================================================================================================================
# STEP 2: Combine all the course info into one txt file
if not INPUT_IDENTITY[0]:
    print("Combining all the course info into one txt file ...")
    with open('docs/course_info/all_courses_info.txt', 'w') as outfile:
        for course in global_variables.course_list:
            with open("docs/course_info/" + course + '.txt') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n')



# Generate schedule
# messages = []
# messages = gpt_generate_schedule(messages)
# messages = gpt_convert_to_calendar_format()


# Chat with GPT to adjust the schedule
# chat_with_gpt(messages)



#=================================================================================================================================
# Step 3: Categorize sessions for each course
# courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}

# Create a dictionary of courses, separated by course names and session categories
for course in global_variables.courses:
        global_variables.courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
        for session in course.class_sessions:
            global_variables.courses_dict[course.course_name][session.category].append(session)



# Load courses_dict from local file
print("Loading courses_dict from data/courses_dict.pickle ...")
with open('data/courses_dict.pickle', 'rb') as f:
    pickle_courses_dict = pickle.load(f)

# TESTING
courses_dict_same = True
for course in global_variables.courses_dict:
    for category in global_variables.courses_dict[course]:
        for i in range(len(global_variables.courses_dict[course][category])):
            # compare each session's class_code, section, start_time, end_time, days in the two courses
            courses_dict_same = compare_sessions_and_print(global_variables.courses_dict[course][category][i], pickle_courses_dict[course][category][i])
            
print(f">>>>>> COMPARISON RESULT: global_variables.courses_dict == pickle_courses_dict: {str(courses_dict_same)}\n")


#global_variables.courses_dict = pickle_courses_dict



# # DEBUGGER
# def print_courses_dict():
#     print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PRINTING COURSES_DICT: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     for course in courses_dict:
#         print(f"Course: {course}")
#         for category in courses_dict[course]:
#             print(f"Category: {category}")
#             for session in courses_dict[course][category]:
#                 print(session)
#         print("\n\n")

# # DEBUGGER
# print_courses_dict()



#=================================================================================================================================
# Step 4: Generate all possible schedules
global_variables.all_generated_schedules = add_courses_to_schedule([[]], global_variables.course_list.copy())


# Load all_generated_schedules from local file
print("Loading all_generated_schedules from data/all_generated_schedules.pickle ...")
with open('data/all_generated_schedules.pickle', 'rb') as f:
    picle_all_generated_schedules = pickle.load(f)


# TESTING
all_generated_schedules_same = True
for i in range(len(global_variables.all_generated_schedules)):
    # compare each session's class_code, section, start_time, end_time, days in the two courses
    for j in range(len(global_variables.all_generated_schedules[i])):
        all_generated_schedules_same = compare_sessions_and_print(global_variables.all_generated_schedules[i][j], picle_all_generated_schedules[i][j])

print(f">>>>>> COMPARISON RESULT: global_variables.all_generated_schedules == picle_all_generated_schedules: {str(all_generated_schedules_same)}\n")


global_variables.all_generated_schedules = picle_all_generated_schedules.copy()


from matching import print_schedule

#=================================================================================================================================
# Step 5: Convert all generated schedules into calendar format  (write to local file)
with open('docs/generated/generated_schedules_simplified.txt', 'w') as f:
    f.write('') # Clear the file

    # Convert schedule to calendar format
    counter = 1
    for schedule in global_variables.all_generated_schedules:
        converted_schedule = convert_session_list_to_schedule(schedule)
        
        #DEBUGGER
        # if (counter == 99):
        #     print_schedule(schedule)
        #     print_calendar_schedule(converted_schedule)
        #     print_calendar_schedule_simplified(converted_schedule) # Print all generated schedules in calendar format (only show course name, class code, session code, time, days, room, and instructor)



        # DEBUGGER
        #print_calendar_schedule(converted_schedule)    # Print all generated schedules in calendar format
        
        # DEBUGGER
        #print_calendar_schedule_simplified(converted_schedule) # Print all generated schedules in calendar format (only show course name, class code, session code, time, days, room, and instructor)

        f.write("Schedule " + str(counter) + ":\n")
        counter += 1
        print_calendar_schedule_simplified_to_file(converted_schedule, f)
f.close()

print(f"Total number of available schedule plans: {len(global_variables.all_generated_schedules)}")





#=================================================================================================================================
# Step 6: Get client's current schedule
print("Acquiring client's current schedule ...")

for client_course_name in global_variables.client_schedule:
    for client_session_number in global_variables.client_schedule[client_course_name]:
        # get course info
        result_session = None
        if client_course_name not in global_variables.courses_dict: # if the course has not been scraped yet
            # Split course code into subject and number
            subject = re.findall('[A-Z]+', client_course_name)[0]
            course_number = re.findall('[0-9]+', client_course_name)[0]

            get_course_info_Requests(global_variables.term, subject, course_number)
            course = format_course_info(client_course_name)[0]
            # get the session info
            for s in course.class_sessions:
                if s.class_code == str(client_session_number):
                    result_session = s
        else:
            for course in global_variables.courses:
                for session in course.class_sessions:
                    if session.class_code == str(client_session_number):
                        result_session = session

        #print(result_session)
        global_variables.client_session_list.append(result_session)

global_variables.client_schedule = convert_session_list_to_schedule(global_variables.client_session_list)

# print("\033[33mYour Current Schedule:\033[0m")
# print_calendar_schedule_simplified(global_variables.client_schedule)



#=================================================================================================================================
# Step 7: Sort the generated schedules by similarity to client's current schedule
print("Sorting the generated schedules by similarity to client's current schedule ...")

from matching import print_schedule

diff_degree, instructions = get_schedule_convert_instructions(global_variables.client_session_list, global_variables.all_generated_schedules[0])


n = 1
for generated_schedule in global_variables.all_generated_schedules:
    print("####### PRINTING SCHEDULE " + str(n) + " #######")
    n += 1
    # print("CLIENT SCHEDULE: ")
    # print_schedule(global_variables.client_session_list)
    # print("\n")
    print("GENERATED SCHEDULE: ")
    print_schedule(generated_schedule)


    diff_degree, instructions = get_schedule_convert_instructions(global_variables.client_session_list, generated_schedule)
    global_variables.schedule_list_sorted.append(Schedule(generated_schedule, diff_degree, instructions))
    #print(diff_degree)

#global_variables.all_generated_schedules = sorted(global_variables.all_generated_schedules, key=lambda schedule: get_schedule_convert_instructions(schedule, global_variables.client_session_list))



global_variables.schedule_list_sorted.sort(key=lambda x: x.diff_degree)


for s in global_variables.schedule_list_sorted:
    print(s.diff_degree)

# a=global_variables.schedule_list_sorted
# a[0].print_schedule_calendar_format()




# TESTING SECTION (UNUSED)

import datetime
import icalendar

def convert_schedule_to_calendar(summary, start_time, end_time, day_of_week):
    # Create a new calendar
    cal = icalendar.Calendar()

    # Create a new event for the specified summary
    event = icalendar.Event()
    event.add('summary', summary)

    # Set the start and end times of the event
    start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
    end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)
    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    # Set the recurrence rule for the event
    rrule = {'freq': 'weekly', 'byday': 'TU'}
    event.add('rrule', rrule)

    # Add the event to the calendar
    cal.add_component(event)

    # Write the calendar to a file
    with open('calendar.ics', 'wb') as f:
        f.write(cal.to_ical())


#convert_schedule_to_calendar("TESTING FOR CALENDAR", datetime.time(13, 30), datetime.time(14, 50), "TU")

