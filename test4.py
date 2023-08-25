# import tkinter as tk
# import calendar

# root = tk.Tk()

# def create_blank_schedule():
#     #root = tk.Tk()
#     root.title("Weekly Schedule")

#     # Create header for days
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     for i, day in enumerate(days):
#         tk.Label(root, text=day, width=30, height=4, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=0, column=i+1)

#     # Create time slots
#     for i in range(16, 46):
#         if i % 2 == 0:
#             hour = i//2
#             if hour < 12:
#                 time_label = f"{hour:02d}:00 AM"
#             else:
#                 time_label = f"{hour:02d}:00 PM"
#             tk.Label(root, text=time_label, width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-8)*2, column=0, rowspan=2)
#         for day in range(7):
#             tk.Label(root, text="", bg="white", width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-8)*2+1, column=day+1)

#     root.mainloop()
#     return root


# def add_event(event):
#     if root.winfo_exists():
#         print("Adding event...")
#         subject = event[0]
#         start_time = event[1][0]
#         end_time = event[1][1]
#         event_days = event[2][0]

#         days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'S']


#         # Round start and end times to nearest :00 or :30 minutes
#         start_minute = int(start_time[0].split(":")[1])
#         if start_minute < 10:
#             start_minute = 0
#         elif start_minute < 40:
#             start_minute = 30
#         else:
#             start_minute = 0
#             start_time[0] = f"{int(start_time[0].split(':')[0])+1:02d}:00"

#         end_minute = int(end_time[0].split(":")[1])
#         if end_minute < 10:
#             end_minute = 0
#         elif end_minute < 40:
#             end_minute = 30
#         else:
#             end_minute = 0
#             end_time[0] = f"{int(end_time[0].split(':')[0])+1:02d}:00"

#         # Convert start and end times to 24-hour format
#         start_hour = int(start_time[0].split(":")[0])
#         start_time_24h = f"{start_hour:02d}:{start_minute:02d}"
#         end_hour = int(end_time[0].split(":")[0])
#         end_time_24h = f"{end_hour:02d}:{end_minute:02d}"

#         for d in event_days:
#             # Map day to column index
#             day_index = days.index(d)

#             # Create event label
#             event_label = tk.Label(root, text=subject, bg="blue", fg="white", width=30, height=2, borderwidth=1, relief="solid")
#             event_label.grid(row=(start_hour-8)*2+start_minute//30+1, column=day_index+1, rowspan=(end_hour-start_hour)*2+(end_minute-start_minute)//30+1, sticky="n")


# create_blank_schedule()
# add_event(["CS346 [6907] LAB 102", [["14:30", "PM"], ["16:20", "PM"]], ["F"]])
#==================================================================================================================================================================



import threading
import tkinter as tk
from class_struct import *

root = tk.Tk()

def create_blank_schedule():
    root.title("Weekly Schedule")

    # Create header for days
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i, day in enumerate(days):
        tk.Label(root, text=day, width=30, height=4, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=0, column=i+1)

    # Create time slots
    for i in range(16, 46):
        if i % 2 == 0:
            hour = i//2
            if hour < 12:
                time_label = f"{hour:02d}:00 AM"
            else:
                time_label = f"{hour:02d}:00 PM"
            tk.Label(root, text=time_label, width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-8)*2, column=0, rowspan=2)
            # time period header rows: 16, 20, 24, 28, 32, 36, 40, 44
            #tk.Label(root, text=time_label, width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-16)//2 + 1, column=0, rowspan=2)
        for day in range(7):
            tk.Label(root, text="", bg="white", width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-8)*2+1, column=day+1)
            # time period rows: 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43
            #tk.Label(root, text="", bg="white", width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-16)+1, column=day+1)

def add_event2(event):
    if root.winfo_exists():
        subject = event[0]
        start_time = event[1][0]
        end_time = event[1][1]
        event_days = event[2][0]

        days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'S']

        # Round start and end times to nearest :00 or :30 minutes
        start_minute = int(start_time[0].split(":")[1])
        if start_minute < 10:
            start_minute = 0
        elif start_minute < 40:
            start_minute = 30
        else:
            start_minute = 0
            start_time[0] = f"{int(start_time[0].split(':')[0])+1:02d}:00"

        end_minute = int(end_time[0].split(":")[1])
        if end_minute < 10:
            end_minute = 0
        elif end_minute < 40:
            end_minute = 30
        else:
            end_minute = 0
            end_time[0] = f"{int(end_time[0].split(':')[0])+1:02d}:00"

        # Convert start and end times to 24-hour format
        start_hour = int(start_time[0].split(":")[0])
        start_time_24h = f"{start_hour:02d}:{start_minute:02d}"
        end_hour = int(end_time[0].split(":")[0])
        end_time_24h = f"{end_hour:02d}:{end_minute:02d}"

        print(f"Start hour: {start_hour}; Start minute: {start_minute}; End hour: {end_hour}; End minute: {end_minute}")

        for d in event_days:
            # Map day to column index
            day_index = days.index(d)
            # rowspan = the number of 30 minute blocks the event spans
            rs = (end_hour-start_hour)*2+(end_minute-start_minute)//30
            print("rs:" + str(rs))

            print("row: " + str(16+(start_hour-8)*4+(start_minute//30)*2))

            # Create event label
            event_label = tk.Label(root, text=subject, bg="blue", fg="white", width=30, height=rs*2, borderwidth=1, relief="solid")
            event_label.grid(row=16+(start_hour-8)*4+(start_minute//30)*2, column=day_index+1, rowspan=rs*2+1, sticky="n")



def add_event3(event, one_time=False):
    subject = event[0]
    start_time = event[1][0]
    end_time = event[1][1]
    event_days = event[2][0]
    start_date = event[3]
    end_date = event[4]

    subject += "\n" + start_time[0] + start_time[1] + " - " + end_time[0] + end_time[1]

    days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'S']

    # Round start and end times to nearest :00 or :30 minutes
    start_minute = int(start_time[0].split(":")[1])
    if start_minute < 10:
        start_minute = 0
    elif start_minute < 40:
        start_minute = 30
    else:
        start_minute = 0
        start_time[0] = f"{int(start_time[0].split(':')[0])+1:02d}:00"

    end_minute = int(end_time[0].split(":")[1])
    if end_minute < 10:
        end_minute = 0
    elif end_minute < 40:
        end_minute = 30
    else:
        end_minute = 0
        end_time[0] = f"{int(end_time[0].split(':')[0])+1:02d}:00"

    # Convert start and end times to 24-hour format
    start_hour = int(start_time[0].split(":")[0])
    end_hour = int(end_time[0].split(":")[0])

    for d in event_days:
        # Map day to column index
        day_index = days.index(d)
        # rowspan = the number of 30-minute blocks the event spans
        rs = (end_hour-start_hour)*2+(end_minute-start_minute)//30

        # Calculate row and column
        row = 16+(start_hour-8)*4+(start_minute//30)*2
        col = day_index+1
        print("RS: " + str(rs) + "; Row: " + str(row) + "; Col: " + str(col))

        # Create canvas
        canvas = tk.Canvas(root, width=214, height=34*rs, borderwidth=0, highlightthickness=0)
        canvas.grid(row=row, column=col, rowspan=rs*2+1, sticky="n")

        # Draw event rectangle
        fill_color = "#efcc00" if one_time else "#b6d192"
        txt = subject if not one_time else subject + "\n(" + start_date + " - " + start_date + ")"

        canvas.create_rectangle(0, 0, 214, 34*rs, fill=fill_color, outline="black")
        canvas.create_text(107, 17*rs, text=txt, fill="black", font=("Arial", 12), justify="center")


def add_event(root, event, one_time=False):
    subject = event[0]
    start_time = event[1][0].copy()
    end_time = event[1][1].copy()
    event_days = event[2]
    start_date = event[3]
    end_date = event[4]
    room = event[5]

    subject += "\n" + start_time[0] + start_time[1] + " - " + end_time[0] + end_time[1]
    if room != "":
        subject += "\n" + room

    days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'S']

    # Round start and end times to nearest :00 or :30 minutes
    start_minute = int(start_time[0].split(":")[1])
    if start_minute < 10:
        start_minute = 0
    elif start_minute < 40:
        start_minute = 30
    else:
        start_minute = 0
        start_time[0] = f"{int(start_time[0].split(':')[0])+1:02d}:00"

    end_minute = int(end_time[0].split(":")[1])
    if end_minute < 10:
        end_minute = 0
    elif end_minute < 40:
        end_minute = 30
    else:
        end_minute = 0
        end_time[0] = f"{int(end_time[0].split(':')[0])+1:02d}:00"

    # Convert start and end times to 24-hour format
    start_hour = int(start_time[0].split(":")[0])
    end_hour = int(end_time[0].split(":")[0])

    for d in event_days:
        # Map day to column index
        day_index = days.index(d)
        # rowspan = the number of 30-minute blocks the event spans
        rs = (end_hour-start_hour)*2+(end_minute-start_minute)//30

        # Calculate row and column
        row = 16+(start_hour-8)*4+(start_minute//30)*2
        col = day_index+1

        # Create canvas
        canvas = tk.Canvas(root, width=214, height=34*rs, borderwidth=0, highlightthickness=0)
        canvas.grid(row=row, column=col, rowspan=rs*2+1, sticky="n")

        # Draw event rectangle
        fill_color = "#efcc00" if one_time else "#b6d192"
        txt = subject if not one_time else subject + "\n(" + start_date + " - " + end_date + ")"

        canvas.create_rectangle(0, 0, 214, 34*rs, fill=fill_color, outline="black")
        canvas.create_text(107, 17*rs, text=txt, fill="black", font=("Arial", 12), justify="center")



def add_annotations(root, online_sessions, request_failed_courses):
    rs = len(online_sessions) + len(request_failed_courses) + 3

    # Create canvas
    canvas = tk.Canvas(root, width=214, height=34*rs, borderwidth=0, highlightthickness=0)
    canvas.grid(row=76-2*rs, column=7, rowspan=rs*2+1, sticky="n")

    # Draw bounding rectangle
    canvas.create_rectangle(0, 0, 214, 34*rs, fill="#d3d3d3", outline="black")

    # Add online sessions
    online_text = "Online sessions:\n"
    for session in online_sessions:
        online_text += f"[{session.class_code}] {session.course_name} {session.section}\n"
    
    # # Add request failed courses
    failed_text = "Request failed courses:\n" + "\n".join(request_failed_courses)

    txt = "* Annotation:\n" + online_text + "\n" + failed_text

    # canvas.create_text(107, 17*rs, text=txt, fill="black", font=("Arial", 12), justify="left")
    canvas.create_text(90, 13*rs, text=txt, fill="black", font=("Arial", 12), justify="left")

    # Add tags to different parts of the text
    canvas.tag_bind("bold_italic", "1.0", "1.end")
    canvas.tag_bind("italic", "2.0", "2.end")
    canvas.tag_bind("online_text", "3.0", "end")
    canvas.tag_bind("failed_text", "5.0", "end")

    # Configure font styles for each tag
    canvas.tag_config("bold_italic", font=("Arial", 13, "bold", "italic"))
    canvas.tag_config("italic", font=("Arial", 13, "italic"))
    canvas.tag_config("online_text", font=("Arial", 12))
    canvas.tag_config("failed_text", font=("Arial", 12))





    # canvas.create_text(60, 30, text="* Annotation:\n", fill="black", font=("Arial", 13, "bold", "italic"), justify="left")
    # canvas.create_text(80, 50, text="*Online sessions:\n", fill="black", font=("Arial", 13, "italic"), justify="left")
    # canvas.create_text(105, 70+len(online_sessions)*20, text="*Request failed courses:\n", fill="black", font=("Arial", 13, "italic"), justify="left")
    # canvas.create_text(70, 100+len(online_sessions)*20, text="\n".join(request_failed_courses), fill="black", font=("Arial", 13), justify="left")


# def __init__(self, course_name, class_code, section, capacity, current, waitcap, waittotal, time_day, room, instructor):
#         self.course_name = course_name
#         self.class_code = class_code
#         self.section = section
#         self.category = section[0:3]
#         self.capacity = capacity
#         self.current = current
#         self.waitcap = waitcap
#         self.waittotal = waittotal
#         parse_result = parse_day_time(time_day)
#         self.start_time = parse_result[0]
#         self.end_time = parse_result[1]
#         self.days = parse_result[2]
#         self.start_date = parse_result[3]
#         self.end_date = parse_result[4]
#         self.room = room
#         self.instructor = instructor


# session1 = Session("CS341", "1234", "TUT 103", "123", "120", "0", "0", "11:30-12:50TTh", "MC 4060", "John Doe")
# session2 = Session("CS350", "1235", "LEC 001", "123", "120", "0", "0", "01:30-02:50TTh", "MC 4061", "John Doe")
# session3 = Session("CS346", "1237", "LAB 102", "123", "120", "0", "0", "12:30-01:50TTh", "MC 4062", "John Doe")
session1 = Session("CS341", "1234", "TUT 103", "123", "120", "0", "0", "", "", "John Doe")
session2 = Session("CS350", "1235", "LEC 001", "123", "120", "0", "0", "", "Online", "John Doe")
session3 = Session("CS346", "1237", "LAB 102", "123", "120", "0", "0", "", "Online", "John Doe")




# create_blank_schedule()
# add_event(root, ["CS346 [6907] LAB 102", [["14:30", "PM"], ["16:20", "PM"]], ["F"], "", "", "MC 4059"])
# add_event(root, ["CS341 [6908] TUT 103", [["9:00", "AM"], ["10:00", "AM"]], ["F"], "", "", "MC 4060"])
# add_event(root, ["CS348 [6907] LEC 001", [["10:30", "AM"], ["11:20", "AM"]], ["F"], "10/20", "10/20", "MC 4062"], True)

# online_sessions = [session1, session2, session3]
# request_failed_courses = ["CS350", "STAT231", "CS346"]
# add_annotations(root, online_sessions, request_failed_courses)

# root.mainloop()








#==================================================================================================================================================================


# import tkinter as tk

# root = tk.Tk()

# def create_blank_schedule():
#     root.title("Weekly Schedule")

#     # Create header for days
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     for i, day in enumerate(days):
#         tk.Label(root, text=day, width=30, height=2, borderwidth=1, relief="groove").grid(row=0, column=i+1)

#     # Create time slots
#     for i in range(8, 23):
#         hour = i
#         if hour < 12:
#             time_label = f"{hour:02d}:00 AM"
#         else:
#             time_label = f"{hour-12:02d}:00 PM" if hour > 12 else "12:00 PM"
#         tk.Label(root, text=time_label, width=30, height=2, borderwidth=1, relief="groove").grid(row=(i-8)*2+1, column=0, rowspan=2)

#         for day in range(7):
#             frame = tk.Frame(root, width=30, height=4, borderwidth=1, relief="groove")
#             frame.grid(row=(i-8)*2+1, column=day+1, rowspan=2)
#             frame.grid_propagate(False)
#             tk.Label(frame, text="", bg="white", width=30, height=2).pack()
#             tk.Label(frame, text="", bg="white", width=30, height=2).pack()

# def add_event(event):
#     if root.winfo_exists():
#         subject = event[0]
#         start_time = event[1][0]
#         end_time = event[1][1]
#         event_days = event[2][0]

#         days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'S']

#         # Round start and end times to nearest :00 or :30 minutes
#         start_minute = int(start_time[0].split(":")[1])
#         if start_minute < 10:
#             start_minute = 0
#         elif start_minute < 40:
#             start_minute = 30
#         else:
#             start_minute = 0
#             start_time[0] = f"{int(start_time[0].split(':')[0])+1:02d}:00"

#         end_minute = int(end_time[0].split(":")[1])
#         if end_minute < 10:
#             end_minute = 0
#         elif end_minute < 40:
#             end_minute = 30
#         else:
#             end_minute = 0
#             end_time[0] = f"{int(end_time[0].split(':')[0])+1:02d}:00"

#         # Convert start and end times to 24-hour format
#         start_hour = int(start_time[0].split(":")[0])
#         start_time_24h = f"{start_hour:02d}:{start_minute:02d}"
#         end_hour = int(end_time[0].split(":")[0])
#         end_time_24h = f"{end_hour:02d}:{end_minute:02d}"

#         print(f"Start hour: {start_hour}; Start minute: {start_minute}; End hour: {end_hour}; End minute: {end_minute}")

#         for d in event_days:
#             # Map day to column index
#             day_index = days.index(d)
#             # rowspan = the number of 30 minute blocks the event spans
#             rs = ((end_hour-start_hour)*2+(end_minute-start_minute)//30)*2
#             event_label = tk.Label(root, text=subject, bg="blue", fg="white", width=30, height=2*rs, borderwidth=1, relief="groove")
#             event_label.grid(row=16+(start_hour-8)*4+(start_minute//30)*2, column=day_index+1, rowspan=rs, sticky="n")

# create_blank_schedule()
# add_event(["CS346 [6907] LAB 102", [["14:30", "PM"], ["16:20", "PM"]], ["F"]])
# root.mainloop()



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def get_term_codes():
    # Set up the request
    url = "https://classes.uwaterloo.ca/under.html"

    r = requests.get(url).text

    # extract the line that contains the term codes
    # Find the start and end indices of the line containing the term codes
    start_index = r.find("Term (")
    end_index = r.find("):<br>", start_index)

    # Extract the line containing the term codes
    return r[start_index:end_index]


get_term_codes()