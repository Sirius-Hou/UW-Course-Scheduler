import csv
from class_struct import Course, Session

# courses = []    # List of courses

# Format the course info and save to a txt file
def format_course_info(course_code):
    result = None
    csv_file = "docs/course_info/" + str(course_code) + ".csv"
    formatted_info = []

    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Extract Course Name and Title
        curr_course = None
        course_name = None
        course_title = None
        for row in reader:
            if len(row) >= 4:
                subject, catalog, _, title = row[0:4]
                if subject and catalog and title:
                    course_name = f"{subject}{catalog}"
                    course_title = title
                    curr_course = Course(subject, catalog, course_title, [])
                    result = curr_course
                    break

        if course_name and course_title:
            course_info = f"Course Name: {course_name}\t ({course_title})"
            # DEBUGGER
            #print(course_info)
            formatted_info.append(course_info)

        # Extract Class Sessions
        for row in reader:
            if len(row) < 12 or not row[0].isdigit():
                continue
            class_session_info = (
                f"[{course_name}]".ljust(10)
                + f"[{row[0]}]".ljust(10)
                + f"{row[1]}".ljust(10)
                + f"({row[2]})".ljust(20)
                + f"Enrolment Capacity: {row[6]}".ljust(30)
                + f"Enrolment Total: {row[7]}".ljust(30)
                + f"Waitinglist Capacity: {row[8]}".ljust(30)
                + f"Waitinglist Total: {row[9]}".ljust(30)
                + f"Schedule: {row[10]}".ljust(45)
                + f"Room: {row[11]}".ljust(35)
            )
            if len(row) >= 13:
                class_session_info += f"Instructor: {row[12]}".ljust(35)
                curr_session = Session(course_name, row[0], row[1], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            else:
                curr_session = Session(course_name, row[0], row[1], row[6], row[7], row[8], row[9], row[10], row[11], "")
            
            curr_course.add_session(curr_session)
            
            formatted_info.append(class_session_info)

    # write to str(course_code) + ".txt" file
    with open("docs/course_info/" + str(course_code) + ".txt", "w") as f:
        f.write("\n".join(formatted_info))
        # DEBUGGER
        print(f"Formatted course info written to docs/course_info/{course_code}.txt.")
    
    return result
