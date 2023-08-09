import re
from class_struct import *



# schedule_list1 = [[Session("0301", "TST 201", "100", "100", "0", "0", "08:30-10:20M05/11-05/11", "BA 1130", "Paul Gries"),
#                   Session("0103", "LEC 003", "100", "100", "0", "0", "11:00-12:00MWF", "BA 1130", "Paul Gries"),
#                   Session("0202", "TUT 102", "100", "100", "0", "0", "1:00-2:00F", "BA 1130", "Paul Gries")],

#                   [Session("0301", "TST 201", "100", "100", "0", "0", "08:30-10:20M05/11-05/11", "BA 1130", "Paul Gries"),
#                   Session("0103", "LEC 003", "100", "100", "0", "0", "11:00-12:00MWF", "BA 1130", "Paul Gries"),
#                   Session("0203", "TUT 103", "100", "100", "0", "0", "2:00-3:00F", "BA 1130", "Paul Gries")]]

# schedule_list2 = [[Session("3840", "LEC 001", "120", "113", "0", "0", "11:30-12:50MW05/08-08/01", "MC 4020", "Pashkovich,Kanstantsin"),
#                    Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                   
#                    [Session("3841", "LEC 002", "120", "107", "0", "0", "11:30-12:50TTh", "MC 4059", "van der Pol,Jorn"),
#                     Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                    
#                     [Session("4311", "LEC 003", "120", "96", "0", "0", "01:00-02:20MW", "MC 4061", "Bhattiprolu,Vijay"),
#                      Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")],
                    
#                     [Session("4239", "LEC 081", "130", "112", "0", "0", "", "Online", "Pei,Martin"),
#                      Session("4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin")]]



sessions = [
    Session("CS240", "3895", "TST 201", "405", "394", "0", "0", "04:30-06:20T06/27-06/27", "STC 1012", "Anderson,Karen"),
    Session("CS240", "4263", "LEC 004", "90", "90", "0", "0", "11:30-12:50TTh", "MC 4061", "Schost,Eric"),
    Session("CS240", "4215", "TUT 105", "70", "68", "0", "0", "02:30-03:20M", "MC 4040", ""),
    Session("CS247", "4055", "TST 201", "150", "126", "0", "0", "04:30-06:20Th06/29-06/29", "", "King,Scott"),
    Session("CS247", "4053", "LEC 001", "150", "126", "0", "0", "10:00-11:20TTh", "STC 0050", "Evans,Ross"),
    Session("CS247", "4054", "TUT 101", "150", "126", "0", "0", "10:30-11:20W", "STC 0010", ""),
    Session("MATH239", "3901", "TST 201", "540", "503", "0", "0", "04:30-06:20Th07/06-07/06", "", ""),
    Session("MATH239", "4016", "LEC 004", "135", "135", "0", "0", "01:30-02:20MWF", "STC 0050", "Stebila,Douglas"),
    Session("MATH239", "3996", "TUT 103", "135", "117", "0", "0", "09:30-10:20M", "STC 0060", ""),
    Session("CS348", "4344", "TST 101", "380", "323", "0", "0", "07:00-08:50M06/26-06/26", "", "Davies,Sylvie Lynne"),
    Session("CS348", "4223", "LEC 003", "140", "131", "0", "0", "02:30-03:50TTh", "STC 0040", "Toman,David"),
    Session("CO250", "4239", "LEC 081", "130", "112", "0", "0", "", "Online", "Pei,Martin"),
    Session("CO250", "4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin"),
    Session("ECE192", "3579", "LEC 003", "135", "123", "0", "0", "12:30-01:20MW", "STC 0010", "Peralta Moarry,Dario"),
    Session("ECE192", "3378", "TUT 103", "48", "41", "0", "0", "10:30-11:20M", "E7 4053", "")
]

sessions = [
    
    
    
    
    
    
    
    
    
    
    
    
    Session("CO250", "4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin"),
    
    
]

sessions2 = [
    # M
    Session("MATH239", "3996", "TUT 103", "135", "117", "0", "0", "09:30-10:20M", "STC 0060", ""),
    Session("ECE192", "3378", "TUT 103", "48", "41", "0", "0", "10:30-11:20M", "E7 4053", ""),
    Session("ECE192", "3579", "LEC 003", "135", "123", "0", "0", "12:30-01:20MW", "STC 0010", "Peralta Moarry,Dario"),
    Session("MATH239", "4016", "LEC 004", "135", "135", "0", "0", "01:30-02:20MWF", "STC 0050", "Stebila,Douglas"),
    Session("CS240", "4215", "TUT 105", "70", "68", "0", "0", "02:30-03:20M", "MC 4040", ""),
    Session("CS348", "4344", "TST 101", "380", "323", "0", "0", "07:00-08:50M06/26-06/26", "", "Davies,Sylvie Lynne"),

    # T
    Session("CS247", "4053", "LEC 001", "150", "126", "0", "0", "10:00-11:20TTh", "STC 0050", "Evans,Ross"),
    Session("CS240", "4263", "LEC 004", "90", "90", "0", "0", "11:30-12:50TTh", "MC 4061", "Schost,Eric"),
    Session("CS348", "4223", "LEC 003", "140", "131", "0", "0", "02:30-03:50TTh", "STC 0040", "Toman,David"),
    Session("CS240", "3895", "TST 201", "405", "394", "0", "0", "04:30-06:20T06/27-06/27", "STC 1012", "Anderson,Karen"),

    # W
    Session("CS247", "4054", "TUT 101", "150", "126", "0", "0", "10:30-11:20W", "STC 0010", ""),
    Session("ECE192", "3579", "LEC 003", "135", "123", "0", "0", "12:30-01:20MW", "STC 0010", "Peralta Moarry,Dario"),
    Session("MATH239", "4016", "LEC 004", "135", "135", "0", "0", "01:30-02:20MWF", "STC 0050", "Stebila,Douglas"),

    # Th
    Session("CS247", "4053", "LEC 001", "150", "126", "0", "0", "10:00-11:20TTh", "STC 0050", "Evans,Ross"),
    Session("CS240", "4263", "LEC 004", "90", "90", "0", "0", "11:30-12:50TTh", "MC 4061", "Schost,Eric"),
    Session("CS348", "4223", "LEC 003", "140", "131", "0", "0", "02:30-03:50TTh", "STC 0040", "Toman,David"),
    Session("CS247", "4055", "TST 201", "150", "126", "0", "0", "04:30-06:20Th06/29-06/29", "", "King,Scott"),
    Session("MATH239", "3901", "TST 201", "540", "503", "0", "0", "04:30-06:20Th07/06-07/06", "", ""),

    # F
    Session("CO250", "4312", "TUT 101", "360", "316", "0", "0", "12:30-01:20F", "STC 1012", "Pei,Martin"),
    Session("MATH239", "4016", "LEC 004", "135", "135", "0", "0", "01:30-02:20MWF", "STC 0050", "Stebila,Douglas")
    
]



def convert_session_list_to_schedule(session_list):
    schedule = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    for session in session_list:
        for day in session.days:
            if day == 'M':
                schedule['Monday'].append(session)
            elif day == 'T':
                schedule['Tuesday'].append(session)
            elif day == 'W':
                schedule['Wednesday'].append(session)
            elif day == 'Th':
                schedule['Thursday'].append(session)
            elif day == 'F':
                schedule['Friday'].append(session)

    for day in schedule:
        schedule[day].sort(key=lambda x: x.start_time)

    return schedule

result = convert_session_list_to_schedule(sessions)

for day in result:
    print("DAY: " + day)
    for session in result[day]:
        print(session)
    print()
