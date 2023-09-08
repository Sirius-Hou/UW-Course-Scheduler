DEBUG_MODE = True

from public import * # libraries and functions that are used in multiple files
import global_variables # global variables that are used in multiple files

from class_struct import Course, Session, Schedule, print_calendar_schedule, print_calendar_schedule_simplified, print_calendar_schedule_simplified_to_file, convert_session_list_to_schedule
from web_scraping import get_course_info_Requests, get_term_codes
from text_formating import format_course_info
from chatgpt import chat_with_gpt, gpt_generate_schedule, gpt_convert_to_calendar_format
from matching import add_courses_to_schedule, get_schedule_convert_instructions
from client_requests import get_session_info, extract_client_schedule
from calendar_display import create_calendar, add_event, add_annotations



# Check if user input is unchanged since the last execution (term, course_list, and client_schedule)
INPUT_IDENTITY = [False, False]

if not DEBUG_MODE: # DEBUG MODE: MANUAL OVERRIDE, FORCE TO RECALCULATE
    if os.path.exists('data/prev.pickle'):
        # load the previous data from the file
        with open('data/prev.pickle', 'rb') as f:
            prev_data = pickle.load(f)

        # check if the current data is identical to the previous data
        INPUT_IDENTITY = [prev_data['term'] == global_variables.term and prev_data['course_list'] == global_variables.course_list,
                            prev_data['client_schedule'] == global_variables.client_schedule]

    if False in INPUT_IDENTITY:
        with open('data/prev.pickle', 'wb') as f:
            data = {
                'term': global_variables.term,
                'course_list': global_variables.course_list,
                'client_schedule': global_variables.client_schedule
            }
            pickle.dump(data, f)

    # DEBUGGER
    rprint("Term & Course List are unchanged: " + str(INPUT_IDENTITY[0]))
    rprint("Client Schedule is unchanged: " + str(INPUT_IDENTITY[1]) + "\n")



# # Print client schedule in calendar display
# def get_schedule_calendar_display(session_list, title_name='Client Schedule'):
#     root = create_calendar(title_name)
#     online_sessions = []


#     for cs in session_list:
#         # skip online sessions
#         if cs.room == 'Online' or cs.start_time == ['','']:
#             online_sessions.append(cs)
#             continue
#         add_event(root, [f"[{cs.class_code}] {cs.course_name} {cs.section}",
#                     [cs.start_time, cs.end_time],
#                     cs.days, cs.start_date, cs.end_date, cs.room], cs.category=='TST')

#     # add an annotation section at the bottom right corner if there are online sessions or global_variables.client_request_failed_courses is not empty
#     if len(online_sessions) > 0 or len(global_variables.client_request_failed_courses) > 0:
#         add_annotations(root, online_sessions, global_variables.client_request_failed_courses)

#     root.mainloop()

import threading
import time

# Define a flag to indicate whether the thread should continue running
should_run = True

# Print client schedule in calendar display
def get_schedule_calendar_display(session_list, title_name='Client Schedule'):
    global should_run
    root = create_calendar(title_name)
    online_sessions = []

    for cs in session_list:
        # skip online sessions
        if cs.room == 'Online' or cs.start_time == ['','']:
            online_sessions.append(cs)
            continue
        add_event(root, [f"[{cs.class_code}] {cs.course_name} {cs.section}",
                    [cs.start_time, cs.end_time],
                    cs.days, cs.start_date, cs.end_date, cs.room], cs.category=='TST')

    # add an annotation section at the bottom right corner if there are online sessions or global_variables.client_request_failed_courses is not empty
    if len(online_sessions) > 0 or len(global_variables.client_request_failed_courses) > 0:
        add_annotations(root, online_sessions, global_variables.client_request_failed_courses)

    while should_run:
        root.update()  # Update the display
        time.sleep(1)  # Sleep for 1 second to avoid busy waiting

    # root.destroy()  # Destroy the window when the thread is terminated
    return root




global CLIENT_SCHEDULE_ACQUIRED
CLIENT_SCHEDULE_ACQUIRED = False

# def acquire_client_schedule(is_get_friend_schedule=False):
#     file_path = None
    
#     if is_get_friend_schedule:
#         file_path = global_variables.client_friend_schedule_path
#         console.log("Acquiring client's friend's schedule ...")
#     else:
#         file_path = global_variables.client_schedule_path
#         console.log("Acquiring client's current schedule ...")

#     global_variables.client_schedule = extract_client_schedule(file_path)

#     # INPUT_IDENTITY = check_input_identity()
    
#     # First check if INPUT_IDENTITY[1] is True (client schedule is unchanged since last time) and local file data/client_session_list.pickle exists
#     if not is_get_friend_schedule and INPUT_IDENTITY[1] and os.path.exists('data/client_session_list.pickle'):
#         # Load client_session_list from local file
#         console.log("Loading [yellow]client_session_list[/yellow] from [yellow][italic][underline]data/client_session_list.pickle[/yellow][/italic][/underline] ...")
#         with open('data/client_session_list.pickle', 'rb') as f:
#             global_variables.client_session_list = pickle.load(f)

#     else:
#         # Reset global_variables.client_session_list
#         global_variables.client_session_list = []

#         for client_course_name in global_variables.client_schedule:

#             # If the course has been scraped before, then get the session info from global_variables.courses
#             if client_course_name in global_variables.courses_dict:
#                 for client_session_number in global_variables.client_schedule[client_course_name]:

#                     for category in global_variables.courses_dict[client_course_name]:
#                         for session in global_variables.courses_dict[client_course_name][category]:
#                             if session.class_code == str(client_session_number):
#                                 global_variables.client_session_list.append(session)

#             # If the course has not been scraped before, then get the session info from the web
#             else:
#                 # Split course code into subject and number
#                 subject = re.findall('[A-Z]+', client_course_name)[0]
#                 course_number = re.findall('[0-9]+', client_course_name)[0]

#                 request_succeeded = get_course_info_Requests(global_variables.term, subject, course_number)

#                 if not request_succeeded: # If the request failed, then skip this course
#                     # console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/yellow][/bold][/italic] in term [/yellow][bold][italic]{str(global_variables.term)}[/yellow][/bold][/italic], skipping this course ...[/red]")
#                     console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/italic][/bold] in term [bold][italic]{str(global_variables.term)}[/italic][/bold], skipping this course ...[/yellow][/red]")
#                     global_variables.client_request_failed_courses.append(client_course_name)
#                     continue
                
#                 course = format_course_info(client_course_name)[0]
#                 # get the session info
#                 for client_session_number in global_variables.client_schedule[client_course_name]:
#                     for session in course.class_sessions:
#                         if session.class_code == str(client_session_number):
#                             global_variables.client_session_list.append(session)
        
#         # Save client_session_list to a local file
#         console.log("Saving [green]client_session_list[/green] to [green][italic][underline]data/client_session_list.pickle[/green][/italic][/underline] ...")
#         with open('data/client_session_list.pickle', 'wb') as f:
#             pickle.dump(global_variables.client_session_list, f)
    
#     global CLIENT_SCHEDULE_ACQUIRED
#     CLIENT_SCHEDULE_ACQUIRED = True

def acquire_client_schedule(is_get_friend_schedule=False):
    file_path = None
    target_session_list = None
    target_session_list_name = None
    target_schedule = None
    request_failed_courses_list = None

    
    if is_get_friend_schedule:
        console.log("Acquiring client's friend's schedule ...")
        file_path = global_variables.client_friend_schedule_path
        target_session_list = global_variables.client_friend_session_list
        target_session_list_name = 'client_friend_session_list'
        target_schedule = global_variables.client_friend_schedule
        request_failed_courses_list = global_variables.client_friend_request_failed_courses
    else:
        console.log("Acquiring client's current schedule ...")
        file_path = global_variables.client_schedule_path
        target_session_list = global_variables.client_session_list
        target_session_list_name = 'client_session_list'
        target_schedule = global_variables.client_schedule
        request_failed_courses_list = global_variables.client_request_failed_courses
        
    # Get client schedule from the copied text from Quest
    target_schedule = extract_client_schedule(file_path)

    # INPUT_IDENTITY = check_input_identity()
    
    # First check if INPUT_IDENTITY[1] is True (client schedule is unchanged since last time) and local file data/client_session_list.pickle exists
    if not is_get_friend_schedule and INPUT_IDENTITY[1] and os.path.exists('data/client_session_list.pickle'):
        # Load client_session_list from local file
        console.log("Loading [yellow]client_session_list[/yellow] from [yellow][italic][underline]data/client_session_list.pickle[/yellow][/italic][/underline] ...")
        with open('data/client_session_list.pickle', 'rb') as f:
            global_variables.client_session_list = pickle.load(f)

    else:
        # Reset session list
        target_session_list.clear()

        for client_course_name in target_schedule:

            # If the course has been scraped before, then get the session info from global_variables.courses
            if client_course_name in global_variables.courses_dict:
                for client_session_number in target_schedule[client_course_name]:
                    for category in global_variables.courses_dict[client_course_name]:
                        for session in global_variables.courses_dict[client_course_name][category]:
                            if session.class_code == str(client_session_number):
                                target_session_list.append(session)

            # If the course has not been scraped before, then get the session info from the web
            else:
                # Split course code into subject and number
                subject = re.findall('[A-Z]+', client_course_name)[0]
                course_number = re.findall('[0-9]+', client_course_name)[0]

                request_succeeded = get_course_info_Requests(global_variables.term, subject, course_number)

                if not request_succeeded: # If the request failed, then skip this course
                    # console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/yellow][/bold][/italic] in term [/yellow][bold][italic]{str(global_variables.term)}[/yellow][/bold][/italic], skipping this course ...[/red]")
                    console.log(f"[red]Error: Couldn't find course [yellow][bold][italic]{client_course_name}[/italic][/bold] in term [bold][italic]{str(global_variables.term)}[/italic][/bold], skipping this course ...[/yellow][/red]")
                    request_failed_courses_list.append(client_course_name)
                    continue
                
                course = format_course_info(client_course_name)[0]
                # get the session info
                for client_session_number in target_schedule[client_course_name]:
                    for session in course.class_sessions:
                        if session.class_code == str(client_session_number):
                            target_session_list.append(session)
        
        # Save client_session_list to a local file
        console.log(f"Saving [green]{target_session_list_name}[/green] to [green][italic][underline]data/{target_session_list_name}.pickle[/green][/italic][/underline] ...")
        with open(f"data/{target_session_list_name}.pickle", 'wb') as f:
            pickle.dump(global_variables.client_session_list, f)
    
    if not is_get_friend_schedule:
        global CLIENT_SCHEDULE_ACQUIRED
        CLIENT_SCHEDULE_ACQUIRED = True



def get_courses():
    # INPUT_IDENTITY = check_input_identity()

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

                # Scraping course info from the web
                request_succeeded = get_course_info_Requests(global_variables.term, course_code, course_number)

                if request_succeeded:
                    rprint(f"[green][italic]{course_code}{course_number}[/green][/italic] info saved to [green][italic][underline]docs/course_info/{course_code}{course_number}.csv[/green][/italic][/underline]")
                    
                    # Format the course info and save to a txt file; Create a Course object and add to global_variables.courses
                    global_variables.courses += format_course_info(new_course)

                    rprint(f"Formatted course info written to [green][italic][underline]docs/course_info/{new_course}.txt[/green][/italic][/underline].")

                else:
                    passed = False
                    pause_point = i
                    break
            
            # Error handling
            if not request_succeeded:
                rprint("Error: Couldn't find course " + new_course_list[pause_point] + " in term " + str(global_variables.term))
                rprint("# Here are some course codes examples: ")
                rprint("# Correct: EMLS101R")
                rprint("# Incorrect: EMLS101r/emls101r (case sensitive), EMLS 101R (no additional space), EMLS101 (incomplete)")
                rprint("# Please enter the correct full course code (e.g., CS135)")
                rprint("# Enter \'term\' to change term.")

                option = input('>>> ')
                if option == 'term':
                    rprint(f"Please enter the term code: (e.g, {get_term_codes()})")
                    new_term = input()
                    while not new_term.isdigit():
                        rprint(f"INVAID TERM CODE! Please enter a valid term code: (e.g, {get_term_codes()})")
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


def get_course(course):
    passed = False

    while not passed:
        request_succeeded = None
        course_code = re.findall('[A-Z]+', course)[0]
        course_number = course[len(course_code):]
        result = None

        # Scraping course info from the web
        request_succeeded = get_course_info_Requests(global_variables.term, course_code, course_number)

        if request_succeeded:
            rprint(f"[green][italic]{course_code}{course_number}[/green][/italic] info saved to [green][italic][underline]docs/course_info/{course_code}{course_number}.csv[/green][/italic][/underline]")
            
            # Format the course info and save to a txt file
            result = format_course_info(course)[0]
            
            rprint(f"Formatted course info written to [green][italic][underline]docs/course_info/{course}.txt[/green][/italic][/underline].")
            passed = True

        
        # Error handling
        if not request_succeeded:
            rprint("Error: Couldn't find course " + course + " in term " + str(global_variables.term))
            rprint("# Here are some course codes examples: ")
            rprint("# Correct: EMLS101R")
            rprint("# Incorrect: EMLS101r/emls101r (case sensitive), EMLS 101R (no additional space), EMLS101 (incomplete)")
            rprint("# Please enter the correct full course code (e.g., CS135)")
            rprint("# Enter \'term\' to change term.")

            option = input('>>> ')
            if option == 'term':
                rprint(f"Please enter the term code: (e.g, {get_term_codes()})")
                new_term = input()
                while not new_term.isdigit():
                    rprint(f"INVAID TERM CODE! Please enter a valid term code: (e.g, {get_term_codes()})")
                    new_term = input()
                global_variables.term = new_term
            else:
                course = option

    # Save courses to a a local file
    console.log("Saving [green]courses[/green] to [green][italic][underline]data/courses.pickle[/green][/italic][/underline] ...")
    with open('data/courses.pickle', 'wb') as f:
        pickle.dump(global_variables.courses, f)

    return result





# Combine all the course info into one txt file
def combine_course_text_info():
    if not INPUT_IDENTITY[0]:
        console.log("Combining all the course info into one txt file ...")
        with open('docs/course_info/all_courses_info.txt', 'w') as outfile:
            for course in global_variables.course_list:
                with open("docs/course_info/" + course + '.txt') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')




# Categorize sessions for each course
#   courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}
def categorize_sessions():
    if not INPUT_IDENTITY[0] or not os.path.exists('data/courses_dict.pickle'):
        # Create a dictionary of courses, separated by course names and session categories
        for course in track(global_variables.courses, description="Processing courses: "):  # show progress bar
            # global_variables.courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': [], 'SEM': []}
            global_variables.courses_dict[course.course_name] = {}
            for session in course.class_sessions:
                if session.category not in global_variables.courses_dict[course.course_name]:
                    global_variables.courses_dict[course.course_name][session.category] = []
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



# Generate all possible schedules
def generate_schedules():
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


# Convert all generated schedules into calendar format  (write to local file)
def save_calendar_format_schedules_to_file():
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


# Sort the generated schedules by similarity to client's current schedule
def sort_schedules():
    console.log("Sorting the generated schedules by similarity to client's current schedule ...")

    for generated_schedule in track(global_variables.all_generated_schedules, description="Processing generated schedules: "):  # show progress bar
        diff_degree, instructions = get_schedule_convert_instructions(global_variables.client_session_list, generated_schedule)
        global_variables.schedule_list_sorted.append(Schedule(generated_schedule, diff_degree, instructions))
        # print(diff_degree)

    # Sort the schedule list by diff_degree
    global_variables.schedule_list_sorted.sort(key=lambda x: x.diff_degree)


global PREPARE_AND_GENERATED_SCHEDULES_EXECUTED
PREPARE_AND_GENERATED_SCHEDULES_EXECUTED = False

# Prepares course information, generates all possible schedules, saves them in a calendar format, and sorts them by similarity to the client's current schedule.
def prepare_and_generate_schedules():
    # Update global_variables.courses
    get_courses()
    # Combine all the course info into one txt file (OPTIONAL)
    combine_course_text_info()
    # Categorize sessions for each course
    categorize_sessions()
    # Generate all possible schedules
    generate_schedules()
    # Convert all generated schedules into calendar format and write to 'docs/generated/generated_schedules_simplified.txt' (OPTIONAL)
    save_calendar_format_schedules_to_file()
    # Sort the generated schedules by similarity to client's current schedule
    sort_schedules()
    
    if not DEBUG_MODE:
        global PREPARE_AND_GENERATED_SCHEDULES_EXECUTED
        PREPARE_AND_GENERATED_SCHEDULES_EXECUTED = True



def show_sessions_in_time_range(start_time, end_time, is_online=False, is_in_person=True, msg_header="Result"):
    result = []
    for course in global_variables.courses_dict:
        for category in global_variables.courses_dict[course]:
            for session in global_variables.courses_dict[course][category]:
                if is_online and (session.room == "Online" or session.start_time == ['',''] or session.end_time == ['',''] or session.days == []):
                    result.append(session)
                elif is_in_person and start_time <= session.start_time[0] <= end_time:
                    result.append(session)
        
    msg = f"\U0001F4CC {msg_header}: (Total: {len(result)})\n" + '\n'.join([f"- [{s.class_code}] {s.course_name} {s.section}  ({s.start_time[0]}{s.start_time[1]}-{s.end_time[0]}{s.end_time[1]}) {s.days}" + ("" if s.start_date == "" else f"{s.start_date}-{s.end_date}") for s in result])
    print(msg)
    return result


def is_valid_course_code(course_code):
    return bool(re.match(r'^[A-Z]+\d+[a-zA-Z]*$', course_code))


def scrape_course_info(course_code):
    # Check if the course code is valid
    if not is_valid_course_code(course_code):
        rprint(f"{course_code} does not match the specified format.")
        return {}
    
    # Scrape course info; 
    new_course = get_course(course_code)
    # Categorize sessions for the course
    new_course_dict = {}
    for session in new_course.class_sessions:
        if session.category not in new_course_dict:
            new_course_dict[session.category] = []
        new_course_dict[session.category].append(session)
    return new_course_dict







# Print summary
# PREREQUISTE: prepare_and_generate_schedules() has been executed!
def print_summary():
    msg = f"""
\U0001F4CC ***_Summary:_***
- ***Courses you wish to enroll in:*** {str(global_variables.course_list)}
- ***Total number of available schedule plans:*** {len(global_variables.all_generated_schedules)}
"""
    rprint(Panel(Markdown(msg), title="Summary", style="bold green"))






# Print instruction tips using print from rich (rprint) and Markdown
def print_tips():
    msg = """
\U0001F4A1 ***_TIPS:_***
  - ***Show your schedule on console:*** Enter [1]
  - ***Show your schedule in calendar display:*** Enter [2]
  - ***Show the top 5 schedules that are most similar to your current schedule:*** Enter [3]
  - ***Show instructions to convert from your current schedule to your friend's schedule:*** Enter [4]
  - ***Adjust your schedule:*** Enter [5]
  - ***Chat with AI to adjust your schedule:*** Enter [0]
  - ***Exit the program:*** Enter [quit]
"""
    rprint(Panel(Markdown(msg), title="Schedule Tips", style="bold red"))



def print_adjustment_commands():
    msg = """
\U0001F4A1 ***_ADJUSTMENT COMMANDS:_***
  - ***[show all]:*** Show all the sessions.
  - ***[show course [course code]]:*** Show the sessions of the course with the given course code. (e.g.: show course CS135)
  - ***[show morning/afternoon/evening]:*** Show the sessions that start in the morning/afternoon/evening.
  - ***[show LEC/LAB/TUT/TST]:*** Show the sessions that are lectures/labs/tutorials/tests categories.
  - ***[show online/in-person]:*** Show the sessions that are online/in-person.
  - ***[show period [start time] [end time]]:*** Show the sessions that start between the given start time and end time. (e.g.: show period 10:00 12:00)
  - ***[add [course code]]:*** Add the course with the given course code to your schedule. (e.g.: add CS135)
  - ***[drop [course code]]:*** Drop the course with the given course code from your schedule. (e.g.: drop CS135)
  - ***[swap [session1 code] [session2 code]]:*** Swap the session with the given session1 code with the session with the given session2 code. (e.g.: swap 6021 6893)
  - ***Press [ENTER] to go back to the main menu.***
  - ***Press [i] to show the instructions again.***
"""
    rprint(Panel(Markdown(msg), title="Schedule Tips", style="bold red"))



############################################################################################################################################################################

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

############################################################################################################################################################################
# Interactive Service Panel
print_tips()
rprint("\U0001F449 Enter [yellow][underline][bold]i[/yellow][/underline][/bold] to view the tips.")

while True:

    instr = input(">>> ")
    if not instr.isdigit():
        if instr == 'i':
            print_tips()
            continue

        elif instr == 'quit':
            # rprint("Thank you for using [yellow][italic]UW Course Scheduler[/yellow][/italic]! See you next time!")
            console.print(Markdown('# ***Thank you for using UW Course Scheduler! See you next time!***'))
            sys.exit()  # Terminate all threads and exit the program

        else:
            rprint("Invalid input! Please enter a valid instruction code.")
            continue

    elif instr == '1': # Print client schedule on console
        if not CLIENT_SCHEDULE_ACQUIRED:
            acquire_client_schedule()
    
        console.log("Converting client's current schedule into calendar format ...")
        global_variables.client_schedule_calendar_dict = convert_session_list_to_schedule(global_variables.client_session_list)
        console.log('\n\n')

        console.print('* Your Current Schedule:')
        print_calendar_schedule_simplified(global_variables.client_schedule_calendar_dict)
        console.print('\n')

    elif instr == '2': # Print client schedule in calendar display
        if not CLIENT_SCHEDULE_ACQUIRED:
            acquire_client_schedule()
        
        console.log("Converting client's current schedule into calendar display format ...")
        thread = threading.Thread(target=get_schedule_calendar_display, args=(global_variables.client_session_list, "Client Current Schedule",))
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

    elif instr == '3': # Print top 10 schedules that are most similar to client's current schedule
        if not CLIENT_SCHEDULE_ACQUIRED:
            acquire_client_schedule()
        if not PREPARE_AND_GENERATED_SCHEDULES_EXECUTED:
            # Prepares course information, generates all possible schedules, saves them in a calendar format, 
            # and sorts them by similarity to the client's current schedule.
            prepare_and_generate_schedules()
            console.print(Markdown('# ***CALCULATIONS COMPLETED***'))

        # Print the top 10 schedules that are most similar to client's current schedule
        console.print("\U0001F449 Top 5 schedules that are most similar to your current schedule:")
        for i in range(5):
            console.print(f"Schedule {i+1}:")
            global_variables.schedule_list_sorted[i].print_schedule_calendar_format()
            console.print('\n')
        
        print_summary()
        index = 5

        while True:
            console.print("\U0001F449 Enter [yellow][underline][bold](n)[/yellow][/underline][/bold] to view the next 5 schedules.")
            console.print("\U0001F449 Enter [green][underline][bold](v)[/green][/underline][/bold] to view a specific schedule in calendar display.")
            console.print("\U0001F449 Enter [red][underline][bold](i)[/red][/underline][/bold] to view instructions to convert from your current schedule to a specific generated schedule.")
            console.print("\U0001F449 Press [underline][italic]ENTER[/underline][/italic] to go back to the main menu.")

            option = input(">>> ")
            if option == 'n':
                for i in range(5):
                    # end of the list
                    if index+i >= len(global_variables.schedule_list_sorted):
                        console.print(">>> Reached the end of the list!")
                        break
                    console.print(f"Schedule {index+i+1}:")
                    global_variables.schedule_list_sorted[index+i].print_schedule_calendar_format()
                    console.print('\n')

                index += 5

            elif option == 'v' or option == 'i':
                console.print("\U0001F449 Enter the schedule number (e.g., 1, 2, 3, ...):")
                schedule_number = input(">>> ")
                interrupt = False
                while not schedule_number.isdigit() or int(schedule_number) <= 0 or int(schedule_number) > len(global_variables.schedule_list_sorted):
                    console.print(">>> Invalid input! Please enter a valid schedule number. (Or enter ([italic]q[/italic]) to back to the previous menu.)")
                    schedule_number = input(">>> ")
                    if schedule_number == 'q':
                        interrupt = True
                        break
                if interrupt:
                    continue

                if option == 'v':
                    thread = threading.Thread(target=get_schedule_calendar_display, args=(global_variables.schedule_list_sorted[int(schedule_number)-1].sessions,))
                    thread.daemon = True  # Set the thread as a daemon thread
                    thread.start()
                else:
                    console.print(f"Instructions to convert from your current schedule to schedule {schedule_number}:")
                    selected_schedule = global_variables.schedule_list_sorted[int(schedule_number)-1]
                    for i in range(len(selected_schedule.instructions)):
                        console.print(f"{i+1}. {selected_schedule.instructions[i]}")
                    console.print('\n')

            

            
            elif option == '':
                console.print(">>> MAIN MENU:")
                print_tips()
                break
                
            else:
                console.print(">>> Invalid input! Please enter a valid option.")
                continue
    
    elif instr == '4': # Print instructions to convert from client's current schedule to client's friend's schedule
        if not CLIENT_SCHEDULE_ACQUIRED:
            acquire_client_schedule()
        acquire_client_schedule(True)
    
        console.log("Converting client friend's current schedule into calendar format ...")
        global_variables.client_friend_schedule_calendar_dict = convert_session_list_to_schedule(global_variables.client_friend_session_list)
        console.print('\n\n')

        console.print("* Your Friend's Schedule:")
        print_calendar_schedule_simplified(global_variables.client_friend_schedule_calendar_dict)
        console.print('\n')

        console.log("Converting client friend's current schedule into calendar display format ...\n\n")
        thread = threading.Thread(target=get_schedule_calendar_display, args=(global_variables.client_friend_session_list, "Client Friend's Schedule",))
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

        diff_degree, instructions = get_schedule_convert_instructions(global_variables.client_session_list, global_variables.client_friend_session_list)
        global_variables.client_friend_schedule_class = Schedule(global_variables.client_friend_session_list, diff_degree, instructions)
        console.print("* Here are the instructions to convert from your current schedule to your friend's schedule:")
        for i in range(len(instructions)):
            console.print(f"> Step {i+1}: {instructions[i]}")
    

    elif instr == '5': # Adjust client's current schedule
        # Update global_variables.courses
        get_courses()
        # Combine all the course info into one txt file (OPTIONAL)
        combine_course_text_info()
        # Categorize sessions for each course
        categorize_sessions()

        if not CLIENT_SCHEDULE_ACQUIRED:
            acquire_client_schedule()
        thread = threading.Thread(target=get_schedule_calendar_display, args=(global_variables.client_session_list, "Client Current Schedule",))
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

        # Make a copy of the current client_session_list
        temp_session_list = global_variables.client_session_list.copy()

        # Strores course codes of the courses that have been added to the client's schedule
        temp_course_list = list(global_variables.courses_dict.keys())


        temp_courses_info = dict()

        print_adjustment_commands()
        while True:
            cmd = input(">>> ").split()
            if len(cmd) == 0:
                rprint("> Returning to the main menu ...")
                break

            elif cmd[0] == 'show' and len(cmd) >= 2:
                if cmd[1] == 'all':
                    show_sessions_in_time_range('00:00', '23:59', True, True, "All Sessions")
                elif cmd[1] == 'morning':
                    show_sessions_in_time_range('08:00', '12:00', False, True, "Morning Sessions")
                elif cmd[1] == 'afternoon':
                    show_sessions_in_time_range('12:00', '18:00', False, True, "Afternoon Sessions")
                elif cmd[1] == 'evening':
                    show_sessions_in_time_range('18:00', '23:00', False, True, "Evening Sessions")
                elif cmd[1] == 'online':
                    show_sessions_in_time_range('00:00', '23:59', True, False, "Online Sessions")
                elif cmd[1] == 'in-person':
                    show_sessions_in_time_range('00:00', '23:59', False, True, "In-person Sessions")
                elif cmd[1] == 'LEC' or cmd[1] == 'TST' or cmd[1] == 'LAB' or cmd[1] == 'TUT':
                    result = []
                    for course in global_variables.courses_dict:
                        if cmd[1] in global_variables.courses_dict[course]:
                            for session in global_variables.courses_dict[course][cmd[1]]:
                                result.append(session)
                    msg = f"\U0001F4CC {cmd[1]} Sessions:\n" + '\n'.join([f"- [{s.class_code}] {s.course_name} {s.section}  ({s.start_time[0]}{s.start_time[1]}-{s.end_time[0]}{s.end_time[1]}) {s.days}" + ("" if s.start_date == "" else f"{s.start_date}-{s.end_date}") for s in result])
                    print(msg)
                elif cmd[1] == 'period' and len(cmd) >= 4:
                    start_time = cmd[2]
                    end_time = cmd[3]
                    show_sessions_in_time_range(start_time, end_time)
                elif cmd[1] == 'course' and len(cmd) >= 3:
                    course_code = cmd[2]
                    if not is_valid_course_code(course_code):
                        rprint(f"{course_code} does not match the specified format.")
                        continue

                    if course_code in temp_courses_info:
                        for category in temp_courses_info[course_code]:
                            for s in temp_courses_info[course_code][category]:
                                s.print_session_display_simplified()
                    else:
                        result = scrape_course_info(course_code)
                        for category in result:
                            for session in result[category]:
                                session.print_session_display_simplified()
                        temp_courses_info[course_code] = result

                else:
                    rprint("Invalid input! Please enter a valid command.")
            
            elif cmd[0] == 'add' and len(cmd) >= 2:
                new_course_dict = scrape_course_info(cmd[1])
                if len(new_course_dict) == 0:
                    continue

                # Backup the scaped course info in case needed later
                temp_courses_info[cmd[1]] = new_course_dict
                
                # Ask client to choose one session from each category
                session_choices = []
                for category in new_course_dict:
                    if len(new_course_dict[category]) == 1: # if there is only one session in the category, then add it automatically
                        session_choices.append(new_course_dict[category][0])
                    else:
                        # Ask user to choose
                        rprint(f"Please choose one {category} session:")
                        # Print all the sessions in the category
                        for i in range(len(new_course_dict[category])):
                            s = new_course_dict[category][i]
                            msg = f"[{i+1}] - [{s.class_code}] {s.course_name} {s.section}  ({s.start_time[0]}{s.start_time[1]}-{s.end_time[0]}{s.end_time[1]}) {s.days}" + ("" if s.start_date == "" else f"{s.start_date}-{s.end_date}")
                            rprint(msg)

                        while True:
                            option = input('>>> ')
                            if option.isdigit() and 1 <= int(option) <= len(new_course_dict[category]):
                                session_choices.append(new_course_dict[category][int(option)-1])
                                break
                            else:
                                rprint("Invalid input! Please enter a valid option.")

                # Add the chosen sessions to the client's current schedule
                temp_session_list += session_choices
                
                # Add the course code to the client's current schedule
                temp_course_list.append(cmd[1])

                # Update the client's current schedule
                # Terminate the thread
                should_run = False  # Set the flag to indicate that the thread should stop running
                thread.join()  # Wait for the thread to complete

                should_run = True
                thread = threading.Thread(target=get_schedule_calendar_display, args=(temp_session_list, "Client Current Schedule",))
                thread.daemon = True  # Set the thread as a daemon thread
                thread.start()
            
            elif cmd[0] == 'drop' and len(cmd) >= 2:
                # Check if the course code is valid
                if not is_valid_course_code(cmd[1]):
                    rprint(f"{cmd[1]} does not match the specified format.")
                    continue

                # Check if the course is in the client's current schedule
                if cmd[1] not in temp_course_list:
                    rprint(f"{cmd[1]} is not in your current schedule.")
                    continue

                # Display the sessions to be removed, ask for client's confirmation
                sessions_to_be_removed = []
                sessions_left = []
                for session in temp_session_list:
                    if session.course_name == cmd[1]:
                        sessions_to_be_removed.append(session)
                    else:
                        sessions_left.append(session)
                
                rprint(f"Are you sure you want to drop {cmd[1]}? (Y/N)")
                rprint(f"Sessions to be removed:")
                for session in sessions_to_be_removed:
                    session.print_session_display_simplified()
                
                if input(">>> ").lower() == 'y':
                    temp_session_list = sessions_left
                    temp_course_list.remove(cmd[1])
                
                    # Update the client's current schedule
                    # Terminate the thread
                    should_run = False  # Set the flag to indicate that the thread should stop running
                    thread.join()  # Wait for the thread to complete

                    should_run = True
                    thread = threading.Thread(target=get_schedule_calendar_display, args=(temp_session_list, "Client Current Schedule",))
                    thread.daemon = True  # Set the thread as a daemon thread
                    thread.start()
                
            elif cmd[0] == 'swap' and len(cmd) >= 3:
                pass

            elif cmd[0] == 'help':
                print_adjustment_commands()
            
            elif cmd[0] == 'save':
                # Save the screenshot of client's current schedule to a local file
                console.log("Saving [green]client's current schedule[/green] to [green][italic][underline]docs/generated/client_current_schedule.png[/green][/italic][/underline] ...")
                

        
            elif cmd[0] == 'i':
                print_adjustment_commands()

            else:
                rprint("Invalid input! Please enter a valid command.")

            rprint("> Press [ENTER] to go back to the main menu.")

            


                
    

    elif instr == '0': # Chat with GPT to adjust the schedule
        # TO-DO
        continue












#=================================================================================================================================
# STEP 1: For each course, get the course info and save to a csv file, then format the info and save to a txt file




#=================================================================================================================================
# STEP 2: Combine all the course info into one txt file




#=================================================================================================================================
# Step 3: Categorize sessions for each course
# courses_dict: {<course name> : {'LEC': <list of sessions>, 'TST': <list of sessions>, 'LAB': <list of sessions>, 'TUT': <list of sessions>}}




#=================================================================================================================================
# Step 4: Generate all possible schedules




#=================================================================================================================================
# Step 5: Convert all generated schedules into calendar format  (write to local file)




#=================================================================================================================================
# Step 6: Get client's current schedule


#=================================================================================================================================
# Step 7: Sort the generated schedules by similarity to client's current schedule



#=================================================================================================================================
# Step 8: Interact with client



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




