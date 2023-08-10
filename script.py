from class_struct import Course, Session
from web_scraping import get_course_info_Requests
from text_formating import format_course_info
from chatgpt import chat_with_gpt, gpt_generate_schedule, gpt_convert_to_calendar_format
from matching import add_courses_to_schedule, convert_session_list_to_schedule, print_calendar_schedule, print_calendar_schedule_simplified, print_calendar_schedule_simplified_to_file
from client_requests import get_session_info
import re



# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
#term = 1239 # enter the term code
term = 1239
course_list = ['CS341', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes (make sure to enter the full name, no space, case sensitive (e.g., EMLS101R not EMLS101r or EMLS 101R)))
#course_list = ['CS240', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
#===================================================================================================
# The sessions that user currently enrolled in (Beta version: mannual input required)
client_schedule = {'CS341' : [6021, 6888, 6893],
                   'CS346' : [6905, 6907],
                   'CS350' : [6958, 6359],
                   'ECON371' : [4127],
                   'STAT231' : [6433, 6879, 6885]}


#===================================================================================================

# STEP 1: For each course, get the course info and save to a csv file, then format the info and save to a txt file
courses = []
for course in course_list:
    course_code = re.findall('[A-Z]+', course)
    course_number = re.findall('[0-9]+', course)
    get_course_info_Requests(term, course_code[0], course_number[0])
    courses.append(format_course_info(course))

# DEBUGGER
# for course in courses:
#     print(course)
#     print("\n")


# STEP 2: Combine all the course info into one txt file
# with open('docs/course_info/all_courses_info.txt', 'w') as outfile:
#     for course in course_list:
#         with open("docs/course_info/" + course + '.txt') as infile:
#             outfile.write(infile.read())
#             outfile.write('\n\n')



# Generate schedule
# messages = []
# messages = gpt_generate_schedule(messages)
# messages = gpt_convert_to_calendar_format()


# Chat with GPT to adjust the schedule
# chat_with_gpt(messages)




courses_dict = {}   # {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}

# Create a dictionary of courses, separated by course names and session categories
for course in courses:
        courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
        for session in course.class_sessions:
            courses_dict[course.course_name][session.category].append(session)



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




schedule_list = [[]]

result_schedule_list = add_courses_to_schedule(schedule_list, course_list, courses_dict)

# print_schedule_list(result_schedule_list)





# Clear the file
with open('docs/generated/generated_schedules_simplified.txt', 'w') as f:
    f.write('')

    # Convert schedule to calendar format
    counter = 1
    for schedule in result_schedule_list:
        converted_schedule = convert_session_list_to_schedule(schedule)
        
        # DEBUGGER
        #print_calendar_schedule(converted_schedule)    # Print all generated schedules in calendar format
        
        # DEBUGGER
        #print_calendar_schedule_simplified(converted_schedule) # Print all generated schedules in calendar format (only show course name, class code, session code, time, days, room, and instructor)

        f.write("Schedule " + str(counter) + ":\n")
        counter += 1
        print_calendar_schedule_simplified_to_file(converted_schedule, f)
f.close()

print(f"Total number of available schedule plans: {len(result_schedule_list)}")





client_session_list = []

for client_course_name in client_schedule:
    for client_session_number in client_schedule[client_course_name]:
        # get course info
        result_session = None
        if client_course_name not in courses_dict: # if the course has not been scraped yet
            # Split course code into subject and number
            subject = re.findall('[A-Z]+', client_course_name)[0]
            course_number = re.findall('[0-9]+', client_course_name)[0]

            get_course_info_Requests(term, subject, course_number)
            course = format_course_info(client_course_name)
            # get the session info
            for s in course.class_sessions:
                if s.class_code == str(client_session_number):
                    result_session = s
        else:
            for course in courses:
                for session in course.class_sessions:
                    if session.class_code == str(client_session_number):
                        result_session = session

        #print(result_session)
        client_session_list.append(result_session)

client_schedule = convert_session_list_to_schedule(client_session_list)
print("\033[33mYour Current Schedule:\033[0m")
print_calendar_schedule_simplified(client_schedule)















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

