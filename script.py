DEBUG_MODE = False

from public import * # libraries and functions that are used in multiple files
import global_variables # global variables that are used in multiple files

from class_struct import Course, Session, Schedule, print_calendar_schedule, print_calendar_schedule_simplified, print_calendar_schedule_simplified_to_file, convert_session_list_to_schedule
from web_scraping import get_course_info_Requests
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






# Print client schedule in calendar display
def get_schedult_calendar_display(session_list):
    root = create_calendar()
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
    add_annotations(root, online_sessions, global_variables.client_request_failed_courses)

    root.mainloop()



global CLIENT_SCHEDULE_ACQUIRED
CLIENT_SCHEDULE_ACQUIRED = False

def acquire_client_schedule():
    console.log("Acquiring client's current schedule ...")

    global_variables.client_schedule = extract_client_schedule(global_variables.client_schedule_path)

    # INPUT_IDENTITY = check_input_identity()
    
    # First check if INPUT_IDENTITY[1] is True (client schedule is unchanged since last time) and local file data/client_session_list.pickle exists
    if INPUT_IDENTITY[1] and os.path.exists('data/client_session_list.pickle'):
        # Load client_session_list from local file
        console.log("Loading [yellow]client_session_list[/yellow] from [yellow][italic][underline]data/client_session_list.pickle[/yellow][/italic][/underline] ...")
        with open('data/client_session_list.pickle', 'rb') as f:
            global_variables.client_session_list = pickle.load(f)

    else:
        # Reset global_variables.client_session_list
        global_variables.client_session_list = []

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
                    global_variables.client_request_failed_courses.append(client_course_name)
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
            global_variables.courses_dict[course.course_name] = {'LEC': [], 'TST': [], 'LAB': [], 'TUT': [], 'SEM': []}
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
  - ***Chat with AI to adjust your schedule:*** Enter [0]
  - ***Exit the program:*** Enter [quit]
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
            rprint("Thank you for using [yellow][italic]UW Course Scheduler[/yellow][/italic]! See you next time!")
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
        thread = threading.Thread(target=get_schedult_calendar_display, args=(global_variables.client_session_list,))
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
                    thread = threading.Thread(target=get_schedult_calendar_display, args=(global_variables.schedule_list_sorted[int(schedule_number)-1].sessions,))
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




