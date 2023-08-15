DEBUG_MODE = False

from public import * # libraries and functions that are used in multiple files
import global_variables # global variables that are used in multiple files

from class_struct import Course, Session, Schedule, print_calendar_schedule, print_calendar_schedule_simplified, print_calendar_schedule_simplified_to_file, convert_session_list_to_schedule
from web_scraping import get_course_info_Requests
from text_formating import format_course_info
from chatgpt import chat_with_gpt, gpt_generate_schedule, gpt_convert_to_calendar_format
from matching import add_courses_to_schedule, get_schedule_convert_instructions
from client_requests import get_session_info, extract_client_schedule
from calendar_display import create_calendar, add_event



# List of courses user wish to enrol in
#===================================================================================================
# HERE ARE THE INFORMATION YOU MAY NEED TO CHANGE
global_variables.term = 1239 # enter the term code
global_variables.course_list = ['CS348', 'CS346', 'CS350', 'STAT231', 'ECON371'] # enter the course codes (make sure to enter the full name, no space, case sensitive (e.g., EMLS101R not EMLS101r or EMLS 101R)))
#global_variables.course_list = ['CS136', 'CS247', 'MATH239', 'CS348', 'CO250', 'ECE192']
#===================================================================================================
# The sessions that user currently enrolled in (Beta version: mannual input required)

# client_schedule_path = 'docs/client/client_current_schedule.txt' # default path for client schedule
client_schedule_path = 'docs/client/david.txt'
global_variables.client_schedule = extract_client_schedule(client_schedule_path)

# global_variables.client_schedule = {'CS341' : [6021, 6888, 6893],
#                                     'CS346' : [6905, 6907],
#                                     'CS350' : [6958, 6359],
#                                     'ECON371' : [4127],
#                                     'STAT231' : [6433, 6879, 6885]}

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

rprint("Term & Course List are unchanged: " + str(INPUT_IDENTITY[0]))
rprint("Client Schedule is unchanged: " + str(INPUT_IDENTITY[1]) + "\n")

# DEBUG MODE: MANUAL OVERRIDE, FORCE TO RECALCULATE
if DEBUG_MODE:
    INPUT_IDENTITY = [False, False]


#=================================================================================================================================
# STEP 1: For each course, get the course info and save to a csv file, then format the info and save to a txt file

#If either term or course_list is changed since last time, then calculate courses again
if not INPUT_IDENTITY[0] or not os.path.exists('data/courses.pickle'):
    global_variables.courses = []
    new_course_list = global_variables.course_list.copy() # Just in case client's initial input is incorrect
    passed = False
    pause_point = 0

    while not passed:
        request_succeeded = None

        for i in track(range(pause_point, len(new_course_list)), description="Getting courses info: ", console=None):  # show progress bar
            passed = True
            new_course = new_course_list[i]
            course_code = re.findall('[A-Z]+', new_course)[0]
            course_number = new_course[len(course_code):]

            request_succeeded = get_course_info_Requests(global_variables.term, course_code, course_number)

            if request_succeeded:
                rprint(f"[green][italic]{course_code}{course_number}[/green][/italic] info saved to [green][italic][underline]docs/course_info/{course_code}{course_number}.csv[/green][/italic][/underline]")
                global_variables.courses += format_course_info(new_course)
                rprint(f"Formatted course info written to [green][italic][underline]docs/course_info/{new_course}.txt[/green][/italic][/underline].")

            else:
                passed = False
                pause_point = i
                break
        
        if not request_succeeded:
            rprint("Error: Couldn't find course " + new_course_list[pause_point] + " in term " + str(global_variables.term))
            rprint("# Here are some course codes examples: ")
            rprint("# Correct: EMLS101R")
            rprint("# Incorrect: EMLS101r/emls101r (case sensitive), EMLS 101R (no additional space), EMLS101 (incomplete)")
            rprint("# Please enter the correct full course code (e.g., CS135)")
            rprint("# Enter \'term\' to change term.")

            option = input('>>> ')
            if option == 'term':
                rprint("Please enter the term code: (e.g, 1239 (Fall 2023)))")
                new_term = input()
                while not new_term.isdigit():
                    rprint("INVAID TERM CODE! Please enter a valid term code: (e.g, 1239 (Fall 2023)))")
                    new_term = input()
                global_variables.term = new_term
            else:
                new_course_list[pause_point] = option
       

    global_variables.course_list = new_course_list # Update the course_list after checking validity

    # Save courses to a a local file
    console.log("Saving [green]courses[/green] to [green][italic][underline]data/courses.pickle[/green][/italic][/underline] ...")
    with open('data/courses.pickle', 'wb') as f:
        pickle.dump(global_variables.courses, f)

# If term and course_list are unchanged since last time, then skip this step
else:
    # Load courses from local file
    console.log("Loading [yellow]courses[/yellow] from [yellow][italic][underline]data/courses.pickle[/yellow][/italic][/underline] ...")
    with open('data/courses.pickle', 'rb') as f:
        global_variables.courses = pickle.load(f)



# DEBUGGER
# for course in courses:
#     print(course)
#     print("\n")



#=================================================================================================================================
# STEP 2: Combine all the course info into one txt file
if not INPUT_IDENTITY[0]:
    console.log("Combining all the course info into one txt file ...")
    with open('docs/course_info/all_courses_info.txt', 'w') as outfile:
        for course in global_variables.course_list:
            with open("docs/course_info/" + course + '.txt') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n')



#=================================================================================================================================
# Step 3: Categorize sessions for each course
# courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}

# if not INPUT_IDENTITY[0]:
#     # Create a dictionary of courses, separated by course names and session categories
#     for course in global_variables.courses:
#             global_variables.courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
#             for session in course.class_sessions:
#                 global_variables.courses_dict[course.course_name][session.category].append(session)

#     # Save courses_dict to a local file
#     print("Saving [green]courses_dict[/green] to [green][italic][underline]data/courses_dict.pickle[/green][/italic][/underline] ...")
#     with open('data/courses_dict.pickle', 'wb') as f:
#         pickle.dump(global_variables.courses_dict, f)
# else:
#     # Load courses_dict from local file
#     print("Loading [yellow]courses_dict[/yellow] from [yellow][italic][underline]data/courses_dict.pickle[/yellow][/italic][/underline] ...")
#     with open('data/courses_dict.pickle', 'rb') as f:
#         global_variables.courses_dict = pickle.load(f)


if not INPUT_IDENTITY[0] or not os.path.exists('data/courses_dict.pickle'):
    # Create a dictionary of courses, separated by course names and session categories
    for course in track(global_variables.courses, description="Processing courses: "):  # show progress bar
        global_variables.courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': []}
        for session in course.class_sessions:
            global_variables.courses_dict[course.course_name][session.category].append(session)

    # Save courses_dict to a local file
    console.log("Saving [green]courses_dict[/green] to [green][italic][underline]data/courses_dict.pickle[/green][/italic][/underline] ...")
    with open('data/courses_dict.pickle', 'wb') as f:
        pickle.dump(global_variables.courses_dict, f)
else:
    # Load courses_dict from local file
    console.log("Loading [yellow]courses_dict[/yellow] from [yellow][italic][underline]data/courses_dict.pickle[/yellow][/italic][/underline] ...")
    with open('data/courses_dict.pickle', 'rb') as f:
        global_variables.courses_dict = pickle.load(f)



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
if not INPUT_IDENTITY[0] or not os.path.exists('data/all_generated_schedules.pickle'):
    global_variables.all_generated_schedules = add_courses_to_schedule([[]], global_variables.course_list.copy())

    # Save all_generated_schedules to a local file
    console.log("Saving [green]all_generated_schedules[/green] to [green][italic][underline]data/all_generated_schedules.pickle[/green][/italic][/underline] ...")
    with open('data/all_generated_schedules.pickle', 'wb') as f:
        pickle.dump(global_variables.all_generated_schedules, f)

else:
    # Load all_generated_schedules from local file
    console.log("Loading [yellow]all_generated_schedules[/yellow] from [yellow][italic][underline]data/all_generated_schedules.pickle[/yellow][/italic][/underline] ...")
    with open('data/all_generated_schedules.pickle', 'rb') as f:
        global_variables.all_generated_schedules = pickle.load(f)



#=================================================================================================================================
# Step 5: Convert all generated schedules into calendar format  (write to local file)

if not INPUT_IDENTITY[0] or not os.path.exists('docs/generated/generated_schedules_simplified.txt'):
    console.log(f"Saving [green]schedule calendars[/green] to file: [green][italic][underline]docs/generated/generated_schedules_simplified.txt[/green][/italic][/underline] ...")

    with open('docs/generated/generated_schedules_simplified.txt', 'w') as f:
        # Convert schedule to calendar format
        counter = 1

        for schedule in track(global_variables.all_generated_schedules, description="Converting schedules: "):  # show progress bar
            converted_schedule = convert_session_list_to_schedule(schedule)
            
            # DEBUGGER
            #print_calendar_schedule(converted_schedule)    # Print all generated schedules in calendar format
            
            # DEBUGGER
            #print_calendar_schedule_simplified(converted_schedule) # Print all generated schedules in calendar format (only show course name, class code, session code, time, days, room, and instructor)

            f.write("Schedule " + str(counter) + ":\n")
            counter += 1
            print_calendar_schedule_simplified_to_file(converted_schedule, f)

    # rprint(f"Total number of available schedule plans: {len(global_variables.all_generated_schedules)}")





#=================================================================================================================================
# Step 6: Get client's current schedule
console.log("Acquiring client's current schedule ...")

# First check if INPUT_IDENTITY[1] is True (client schedule is unchanged since last time) amd local file data/client_session_list.pickle exists
if INPUT_IDENTITY[1] and os.path.exists('data/client_session_list.pickle'):
    # Load client_session_list from local file
    console.log("Loading [yellow]client_session_list[/yellow] from [yellow][italic][underline]data/client_session_list.pickle[/yellow][/italic][/underline] ...")
    with open('data/client_session_list.pickle', 'rb') as f:
        global_variables.client_session_list = pickle.load(f)

else:
    for client_course_name in global_variables.client_schedule:
        # If the course has been scraped before, then get the session info from global_variables.courses
        if client_course_name in global_variables.courses_dict:
            for client_session_number in global_variables.client_schedule[client_course_name]:

                for category in global_variables.courses_dict[client_course_name]:
                    for session in global_variables.courses_dict[client_course_name][category]:
                        if session.class_code == str(client_session_number):
                            global_variables.client_session_list.append(session)

        # If the course has not been scraped before, then get the session info from the web
        else:
            # Split course code into subject and number
            subject = re.findall('[A-Z]+', client_course_name)[0]
            course_number = re.findall('[0-9]+', client_course_name)[0]

            request_succeeded = get_course_info_Requests(global_variables.term, subject, course_number)

            if not request_succeeded: # If the request failed, then skip this course
                # console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/yellow][/bold][/italic] in term [/yellow][bold][italic]{str(global_variables.term)}[/yellow][/bold][/italic], skipping this course ...[/red]")
                console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/italic][/bold] in term [bold][italic]{str(global_variables.term)}[/italic][/bold], skipping this course ...[/yellow][/red]")
                continue
            
            course = format_course_info(client_course_name)[0]
            # get the session info
            for client_session_number in global_variables.client_schedule[client_course_name]:
                for session in course.class_sessions:
                    if session.class_code == str(client_session_number):
                        global_variables.client_session_list.append(session)
    
    # Save client_session_list to a local file
    console.log("Saving [green]client_session_list[/green] to [green][italic][underline]data/client_session_list.pickle[/green][/italic][/underline] ...")
    with open('data/client_session_list.pickle', 'wb') as f:
        pickle.dump(global_variables.client_session_list, f)




console.log("Converting client's current schedule into calendar format ...")
global_variables.client_schedule = convert_session_list_to_schedule(global_variables.client_session_list)



#=================================================================================================================================
# Step 7: Sort the generated schedules by similarity to client's current schedule
console.log("Sorting the generated schedules by similarity to client's current schedule ...")

for generated_schedule in track(global_variables.all_generated_schedules, description="Processing generated schedules: "):  # show progress bar
    diff_degree, instructions = get_schedule_convert_instructions(global_variables.client_session_list, generated_schedule)
    global_variables.schedule_list_sorted.append(Schedule(generated_schedule, diff_degree, instructions))
    # print(diff_degree)

# Sort the schedule list by diff_degree
global_variables.schedule_list_sorted.sort(key=lambda x: x.diff_degree)



#=================================================================================================================================
# Step 8: Interact with client

console.print(Markdown('# ***CALCULATIONS COMPLETED***'))

# rprint("===============================================================================================================================")
# rprint("[bold][green][italic]CALCULATIONS COMPLETED![/bold][/green][/italic]")
#console.print(Markdown("# {}".format(Text("CALCULATIONS COMPLETED!", style=Style(bold=True, italic=True)))))

import pyfiglet
from termcolor import colored

rprint(f"[yellow]{seperate_line}[/yellow]")

# msg = pyfiglet.figlet_format("UW COURSE SCHEDULER", font='slant', justify='center', width=120)
msg = pyfiglet.figlet_format("UW COURSE SCHEDULER", font='slant', justify='center', width=120)
colored_msg = colored(msg, color='yellow', on_color='on_grey', attrs=['bold'])
print(colored_msg)
rprint(f"[yellow]{seperate_line}[/yellow]")

# Welcome message
rprint("[yellow]Welcome to [bold][italic]UW Course Scheduler[/bold][/italic]! How may I assist you today?[/yellow] \U0001F60E\U0001F339\n") # \U0001F60E & \U0001F339: Unicode characters of cool face emoji and rose emoji

# Print summary
msg = f"""
\U0001F4CC ***_Summary:_***
  - ***Courses you wish to enroll in:*** {str(global_variables.course_list)}
  - ***Total number of available schedule plans:*** {len(global_variables.all_generated_schedules)}
"""
rprint(Panel(Markdown(msg), title="Summary", style="bold green"))

# console.print("* Courses you wish to enrol in: " + str(global_variables.course_list))
# console.print(f"* Total number of available schedule plans: {len(global_variables.all_generated_schedules)}")


# Print client schedule in calendar display
def get_schedult_calendar_display(session_list):
    root = create_calendar()
    for cs in session_list:
        # skip online sessions
        if cs.room == 'Online':
            continue
        add_event(root, [f"[{cs.class_code}] {cs.course_name} {cs.section}",
                    [cs.start_time, cs.end_time],
                    cs.days, cs.start_date, cs.end_date], cs.category=='TST')
    root.mainloop()


# Print instruction tips using print from rich (rprint) and Markdown
def print_tips():
    msg = """
\U0001F4A1 ***_TIPS:_***
  - ***Show your schedule on console:*** Enter [1]
  - ***Show your schedule in calendar display:*** Enter [2]
  - ***Chat with AI to adjust your schedule:*** Enter [0]
  - ***Exit the program:*** Enter [quit]
"""
    rprint(Panel(Markdown(msg), title="Schedule Tips", style="bold red"))



# Service Interactive Panel
print_tips()
rprint("\U0001F449 Enter [yellow][underline][bold]i[/yellow][/underline][/bold] to view the tips.")
while True:

    instr = input(">>> ")
    if not instr.isdigit():
        if instr == 'i':
            print_tips()
            continue

        elif instr == 'quit':
            rprint("Thank you for using [yellow][italic]UW Course Scheduler[/yellow][/italic]! See you next time!")
            sys.exit()  # Terminate all threads and exit the program

        else:
            rprint("Invalid input! Please enter a valid instruction code.")
            continue

    elif instr == '1': # Print client schedule on console
        console.print('* Your Current Schedule:')
        print_calendar_schedule_simplified(global_variables.client_schedule)
        console.print('\n')

    elif instr == '2': # Print client schedule in calendar display
        thread = threading.Thread(target=get_schedult_calendar_display, args=(global_variables.client_session_list,))
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()


    elif instr == '0': # Chat with GPT to adjust the schedule
        # TO-DO
        continue
    













#=================================================================================================================================
# Step 8: Filter course schedules that meets client's preferences (e.g, prefer morning/afternoon/evening classes; prefer instructors with high ratings; prefer/dislike consecutive sessions; etc.)










#=================================================================================================================================
# Step 9: Chat with GPT to adjust the schedule

# Generate schedule
# messages = []
# messages = gpt_generate_schedule(messages)
# messages = gpt_convert_to_calendar_format()


# Chat with GPT to adjust the schedule
# chat_with_gpt(messages)



























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

