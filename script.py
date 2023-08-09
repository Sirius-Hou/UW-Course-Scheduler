from class_struct import Course, Session
from web_scraping import getCourseInfo_WebDriver, getCourseInfo_Requests
from text_formating import format_course_info, courses
from chatgpt import chat_with_gpt, gpt_generate_schedule, gpt_convert_to_calendar_format
import re


# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
#term = 1239 # enter the term code
term = 1235
#course_list = ['CS341', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes
course_list = ['CS240', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
#===================================================================================================

# STEP 1: For each course, get the course info and save to a csv file, then format the info and save to a txt file
for course in course_list:
    course_code = re.findall('[A-Z]+', course)
    course_number = re.findall('[0-9]+', course)
    getCourseInfo_Requests(term, course_code[0], course_number[0])
    format_course_info(course)

# DEBUGGER
for course in courses:
    print(course)
    print("\n")


# STEP 2: Combine all the course info into one txt file
with open('docs/course_info/all_courses_info.txt', 'w') as outfile:
    for course in course_list:
        with open("docs/course_info/" + course + '.txt') as infile:
            outfile.write(infile.read())
            outfile.write('\n\n')



# Generate schedule
# messages = []
# messages = gpt_generate_schedule(messages)
# messages = gpt_convert_to_calendar_format()


# Chat with GPT to adjust the schedule
# chat_with_gpt(messages)





















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
