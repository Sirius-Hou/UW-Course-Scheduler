import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib

class classStruct:
	def __init__(self, classCode,section, capacity, current, waitcap, waittotal, timeDay, room, instructor):
		self.classCode = classCode
		self.section = section
		self.capacity = capacity
		self.current = current
		self.waitcap = waitcap
		self.waittotal = waittotal
		self.timeDay = timeDay
		self.room = room	
		self.instructor = instructor

def send_email(subject, msg):
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(config.EMAIL_ADDRESS, config.PASSWORD)
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
		server.quit()
		print("Email sent!")
	except:
		print("Email failed to send")

def getClass(classCode, arr):
	for match in arr:
		if(int(match.classCode) == int(classCode)):
			return match

def getRequest(payload):
	r = requests.get(url, params=payload).text
	soup = BeautifulSoup(r, 'html.parser')

	file = soup.find_all('tr')
	classes = []
	classStructList = []

	for match in file:
		if(re.search(' LEC ', match.text) != None and re.search('Class', match.text) == None and re.search('Notes', match.text) == None):
			classes.append(match)


	for match in classes:
		classCode = match.find_all('td')[0].text
		section = match.find_all('td')[1].text
		capacity = match.find_all('td')[6].text
		current = match.find_all('td')[7].text
		waitcap = match.find_all('td')[8].text
		waittotal = match.find_all('td')[9].text
		timeDay = match.find_all('td')[10].text
		room = match.find_all('td')[11].text.replace(" ", "")
		instructor = match.find_all('td')[12].text
		classStructList.append(classStruct(classCode, section, capacity, current, waitcap, waittotal, timeDay, room, instructor));

	return classStructList


url = "https://info.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"

term = input("What is the term code? (eg. Fall2018 = 1189): ")
subject = input("What is the subject code? (eg. MATH, CS, AFM): ")
coursenumber = input("What is the course code? (eg. 137, 101): ")

payload = {'sess':int(term), 'level': 'under', 'subject':subject , 'cournum':int(coursenumber) }
classStructList = getRequest(payload)

print("========================================================================================================================================================")
print("|Class Code|\t|Section|\t|Capacity|\t|Current|\t|Wait Cap|\t|Waittotal|\t|TimeDay|\t|Room|\t\t|Instructor|")
print("========================================================================================================================================================")

for match in classStructList:
	print("   " + match.classCode + "\t " + match.section + "\t    " + match.capacity + "\t   " + match.current + "\t\t     " + match.waitcap + "\t     " + match.waittotal
		  + "     " + match.timeDay + "\t" + match.room + "\t       " + match.instructor)


watchcode = input("Which course code would you like to watch?: ")
if(getClass(watchcode, classStructList) == None):
	while(1):
		watch = input("Invalid course code, please try again: ")
		if(getClass(watch, classStructList) != None):
			watchcode = watch
			break


while 1:
	structList = getRequest(payload)
	targetClass = getClass(watchcode, structList)
	if(int(targetClass.current) < int(targetClass.capacity)):
		print("Open Space! :)")
		send_email("Space in class: " + targetClass.classCode, "Please login on quest to enroll");
		break;
	time.sleep(30)