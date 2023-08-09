from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
from class_struct import Course, Session
from web_scraping import getCourseInfo_WebDriver, getCourseInfo_Requests
from text_formating import format_course_info, courses


# courses = []






# # Format the course info and save to a txt file
# def format_course_info(course_num):
#     csv_file = "docs/course_info/" + str(course_num) + ".csv"
#     formatted_info = []

#     with open(csv_file, newline='') as file:
#         reader = csv.reader(file)
#         header = next(reader)  # Skip the header row

#         # Extract Course Name and Title
#         curr_course = None
#         course_name = None
#         course_title = None
#         for row in reader:
#             if len(row) >= 4:
#                 subject, catalog, _, title = row[0:4]
#                 if subject and catalog and title:
#                     course_name = f"{subject}{catalog}"
#                     course_title = title
#                     curr_course = Course(course_name, course_num, course_title, [])
#                     courses.append(curr_course)
#                     break

#         if course_name and course_title:
#             course_info = f"Course Name: {course_name}\t ({course_title})"
#             # debugger
#             #print(course_info)
#             formatted_info.append(course_info)

#         # Extract Class Sessions
#         for row in reader:
#             if len(row) < 12 or not row[0].isdigit():
#                 continue
#             class_session_info = (
#                 f"[{row[0]}]".ljust(10)
#                 + f"{row[1]}".ljust(10)
#                 + f"({row[2]})".ljust(20)
#                 + f"Enrolment Capacity: {row[6]}".ljust(30)
#                 + f"Enrolment Total: {row[7]}".ljust(30)
#                 + f"Waitinglist Capacity: {row[8]}".ljust(30)
#                 + f"Waitinglist Total: {row[9]}".ljust(30)
#                 + f"Schedule: {row[10]}".ljust(45)
#                 + f"Room: {row[11]}".ljust(35)
#             )
#             if len(row) >= 13:
#                 class_session_info += f"Instructor: {row[12]}".ljust(35)
#                 curr_session = Session(row[0], row[1], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
#             else:
#                 curr_session = Session(row[0], row[1], row[6], row[7], row[8], row[9], row[10], row[11], "")
            
#             curr_course.add_session(curr_session)
            
#             formatted_info.append(class_session_info)

#     # write to str(course_num) + ".txt" file
#     with open("docs/course_info/" + str(course_num) + ".txt", "w") as f:
#         f.write("\n".join(formatted_info))
#         # debugger
#         print(f"Formatted course info written to docs/course_info/{course_num}.txt.")




import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("API_KEY")


def gpt_generate_schedule(messages=[]):
    with open("docs/commands/startup_command.txt", "r") as f:
        command_text = f.read()

    with open("docs/course_info/all_courses_info.txt", "r") as f:
        all_courses_info = f.read()

    # Replace the string in the messages list
    messages += [
        {"role": "user", "content": command_text + "\n" + all_courses_info}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stop=None,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print(response['choices'][0]['message']['content'] + "\n")
    
    with open("docs/generated/generated_schedule.txt", "w") as f:
        f.write(response['choices'][0]['message']['content'])
    
    return messages



def gpt_convert_to_calendar_format():
    with open("docs/commands/convert_to_calendar_format_command.txt", "r") as f:
        convert_to_calendar_format_command = f.read()

    with open("docs/generated/generated_schedule.txt", "r") as f:
        generated_schedule = f.read()

    # Replace the string in the messages list
    messages = [
        {"role": "user", "content": convert_to_calendar_format_command + "\n" + generated_schedule}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stop=None,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print(response['choices'][0]['message']['content'] + "\n")
    
    with open("docs/generated/generated_schedule_calendar_format.txt", "w") as f:
        f.write(response['choices'][0]['message']['content'])
    
    return messages



def chat_with_gpt(messages=[]):
    print("Welcome to ChatGPT 3.5 turbo! Type 'exit' to quit.")

    messages += [{"role": "system", "content": "You are a helpful course selection assistant at University of Waterloo."}]

    while True:
        user_input = input(">>> ")
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stop=None,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        print(response['choices'][0]['message']['content'] + "\n")

        if user_input.lower() == "exit":
            break   




# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
#term = 1239 # enter the term code
term = 1235
#course_list = ['CS341', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes
course_list = ['CS240', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
#===================================================================================================

# For each course, get the course info and save to a csv file, then format the info and save to a txt file
for course in course_list:
    course_code = re.findall('[A-Z]+', course)
    course_number = re.findall('[0-9]+', course)
    getCourseInfo_Requests(term, course_code[0], course_number[0])
    format_course_info(course)


for course in courses:
    print(course)
    print("\n")


# Combine all the course info into one txt file
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

