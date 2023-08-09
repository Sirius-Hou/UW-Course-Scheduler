import re

def convert_time(start_time, end_time, return_24h_format=True):
    # Convert start time to 24-hour format
    start_hour = int(start_time.split(":")[0])
    if start_hour < 8:
        start_hour += 12
    start_time_24h = "{:02d}:{}".format(start_hour, start_time.split(":")[1])

    # Convert end time to 24-hour format
    end_hour = int(end_time.split(":")[0])
    if end_hour < 8:
        end_hour += 12
    end_time_24h = "{:02d}:{}".format(end_hour, end_time.split(":")[1])

    # Adjust end time if it is earlier than start time
    if end_hour < start_hour:
        end_hour += 12
        end_time_24h = "{:02d}:{}".format(end_hour, end_time.split(":")[1])

    # Convert start and end times to AM/PM format
    start_time_ampm = "AM" if start_hour < 12 else "PM"
    end_time_ampm = "AM" if end_hour < 12 else "PM"

    # Return the converted times as a list of lists
    if return_24h_format:
        return [[start_time_24h, start_time_ampm], [end_time_24h, end_time_ampm]]
    else:
        return [[start_time, start_time_ampm], [end_time, end_time_ampm]]


def parse_day_time(day_time):
    if day_time == "":
        return [["", ""] , ["", ""], [], "", ""]

    # Extract start time and end time
    start_time = day_time.split("-")[0]
    end_time = re.findall("^[^A-Za-z]+", day_time.split("-")[1])[0]
    start_time, end_time = convert_time(start_time, end_time)
    
    # Extract days
    days_str = re.findall("[A-Za-z]+", day_time)[0]
    days = []
    i = 0
    while i < len(days_str):
        if days_str[i] == "M" or days_str[i] == "W" or days_str[i] == "F":
            days.append(days_str[i])
            i += 1
        elif days_str[i] == "T":
            if i < len(days_str) - 1 and days_str[i + 1] == "h":
                days.append("Th")
                i += 2
            else:
                days.append("T")
                i += 1
        else:
            # DEBUGGER
            # Invalid day
            print("Invalid day")
            print(days_str[i])

    # Extract start date and end date
    start_date = ""
    end_date = ""
    period = re.findall("[0-9]{2}/[0-9]{2}-[0-9]{2}/[0-9]{2}", day_time)
    if len(period) != 0:
        start_date = period[0].split("-")[0]
        end_date = period[0].split("-")[1]
    
    #print(start_time, end_time, days, period, start_date, end_date)
    return [start_time, end_time, days, start_date, end_date]


class Course:
    def __init__(self, course_code, course_number, course_title, class_sessions):
        self.course_code = course_code
        self.course_number = course_number
        self.course_name = course_code + course_number
        self.course_title = course_title
        self.class_sessions = class_sessions
    
    def add_session(self, class_session):
        self.class_sessions.append(class_session)

    # def print_course(self):
    #     print(f"Course Code: {self.course_code}")
    #     print(f"Course Number: {self.course_number}")
    #     print(f"Course Title: {self.course_title}")
    #     print(f"Class Sessions: {self.class_sessions}")
    
    def __str__(self):
        session_str = "\n".join(str(session) for session in self.class_sessions)
        return f"Course Code: {self.course_code}\t Course Number: {self.course_number}\t Course Title: {self.course_title}\nClass Sessions:\n{session_str}"


class Session:
    def __init__(self, course_name, class_code, section, capacity, current, waitcap, waittotal, time_day, room, instructor):
        self.course_name = course_name
        self.class_code = class_code
        self.section = section
        self.category = section[0:3]
        self.capacity = capacity
        self.current = current
        self.waitcap = waitcap
        self.waittotal = waittotal
        parse_result = parse_day_time(time_day)
        self.start_time = parse_result[0]
        self.end_time = parse_result[1]
        self.days = parse_result[2]
        self.start_date = parse_result[3]
        self.end_date = parse_result[4]
        self.room = room
        self.instructor = instructor
    
    # def print_session(self):
    #     print(f"Class Code: {self.class_code}")
    #     print(f"Section: {self.section}")
    #     print(f"Enrolment Capacity: {self.capacity}")
    #     print(f"Enrolment Total: {self.current}")
    #     print(f"Waitlist Capacity: {self.waitcap}")
    #     print(f"Waitlist Total: {self.waittotal}")
    #     if (self.start_date != ""):
    #         print(f"Time Days: ({self.start_time[0]}{self.start_time[1]}-{self.end_time[0]}{self.end_time[1]}) {self.days} {self.start_date}-{self.end_date}")
    #     else:
    #         print(f"Time Days: ({self.start_time[0]}{self.start_time[1]}-{self.end_time[0]}{self.end_time[1]}) {self.days}")

    #     print(f"Room: {self.room}")
    #     print(f"Instructor: {self.instructor}")

    def __str__(self):
        print_str = f"Course Name: {self.course_name}\t Class Code: {self.class_code}\t Section: {self.section}\t Category: {self.category}\t Enrolment Capacity: {self.capacity}\t Enrolment Total: {self.current}\t Waitlist Capacity: {self.waitcap}\t Waitlist Total: {self.waittotal}\t "
        if (self.start_date != ""):
            print_str += f"Time Days: ({self.start_time[0]}{self.start_time[1]}-{self.end_time[0]}{self.end_time[1]}) {self.days} {self.start_date}-{self.end_date}\t "
        else:
            print_str += f"Time Days: ({self.start_time[0]}{self.start_time[1]}-{self.end_time[0]}{self.end_time[1]}) {self.days}\t "
        print_str += f"Room: {self.room}\t Instructor: {self.instructor}"
        return print_str