import tkinter as tk

def create_calendar():
    root = tk.Tk()
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
            # time period header rows: 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72
            #tk.Label(root, text=time_label, width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-16)//2 + 1, column=0, rowspan=2)
        for day in range(7):
            tk.Label(root, text="", bg="white", width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-8)*2+1, column=day+1)
            # time period rows: 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, ...
            #tk.Label(root, text="", bg="white", width=30, height=2, borderwidth=1, relief="groove", highlightbackground="grey").grid(row=(i-16)+1, column=day+1)
    return root




# event format: ["[6907] CS348 LEC 001", [["10:30", "AM"], ["11:20", "AM"]], ["F"], "10/20", "10/20"]
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



# def add_event2(root, event):
#     if root.winfo_exists():
#         subject = event[0]
#         start_time = event[1][0]
#         end_time = event[1][1]
#         event_days = event[2]

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
#             # rowspan = the number of 30 minute blocks the event spans
#             rs = (end_hour-start_hour)*2+(end_minute-start_minute)//30
        
#             # Create event label
#             event_label = tk.Label(root, text=subject, bg="blue", fg="white", width=30, height=rs*2, borderwidth=1, relief="solid")
#             event_label.grid(row=16+(start_hour-8)*4+(start_minute//30)*2, column=day_index+1, rowspan=rs*2+1, sticky="n")




def add_annotations(root, online_sessions, request_failed_courses):
    rs = len(online_sessions) + len(request_failed_courses) + 3

    # Create canvas
    canvas = tk.Canvas(root, width=214, height=34*rs, borderwidth=0, highlightthickness=0)
    canvas.grid(row=76-2*rs, column=7, rowspan=rs*2+1, sticky="n")

    # Draw bounding rectangle
    canvas.create_rectangle(0, 0, 214, 34*rs, fill="#e5e4e2", outline="black")

    # Add online sessions
    online_text = "Online sessions:\n"
    if len(online_sessions) == 0:
        online_text += "None"
    else:
        online_text += "\n".join([f"[{session.class_code}] {session.course_name} {session.section}" for session in online_sessions])

    # # Add request failed courses
    failed_text = "Request failed courses:\n"
    if len(request_failed_courses) == 0:
        failed_text += "None"
    else:
        failed_text += "\n".join(course_name for course_name in request_failed_courses)

    txt = "* Annotation:\n" + online_text + "\n\n" + failed_text

    canvas.create_text(100, 12*rs, text=txt, fill="black", font=("Arial", 12), justify="left")

