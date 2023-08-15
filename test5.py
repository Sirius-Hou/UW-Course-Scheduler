import re


def extract_info(content):
		course_dict = {}
		# Find all occurrences of the pattern '([A-Z]+ \d+)' followed by 'Status'
		course_occurrences = [m.start() for m in re.finditer(r'([A-Z]+ \d+).*?Status', content)]
		
		for i in range(len(course_occurrences)):
				# Extract the start and end indices for each course section
				start_index = course_occurrences[i]
				end_index = course_occurrences[i + 1] if i < len(course_occurrences) - 1 else len(content)
				
				# Extract the course section using start and end indices
				course_section = content[start_index:end_index]
				
				# Extract the course name using regex from the course section
				course_name_match = re.search(r'([A-Z]+ \d+)', course_section)
				course_name = course_name_match.group(1).replace(" ", "") if course_name_match else None
				
				# Find all session codes by looking for 4-digit numbers followed by "TST", "LAB", "LEC", or "TUT"
				session_codes = re.findall(r'(\d{4})\s+(TST|LAB|LEC|TUT)', course_section)
				session_codes = [int(code[0]) for code in session_codes]  # Extract the numeric part
				
				if course_name:
						course_dict[course_name] = session_codes

		return course_dict


content1 = ""
with open("docs/client/client_current_schedule.txt", "r") as f:
		content1 = f.read()


content2 = ""
with open("docs/client/emily.txt", "r") as f:
		content2 = f.read()
		
content3 = ""
with open("docs/client/david.txt", "r") as f:
		content3 = f.read()
		



content = content3




def extract_client_schedule(file_path):
	content = ""
	with open(file_path, "r") as f:
		content = f.read()

	course_list = []
	status_match_results1 = re.findall(r'.*?\bStatus\b', content, re.DOTALL)
	for status_match in status_match_results1:
		course_name_matches = re.findall(r'[A-Z]+ \d+', status_match)

		course_name = course_name_matches[-1].replace(" ", "") if course_name_matches else None

		course_list.append(course_name)


	session_list = []
	status_match_results2 = re.split(r'(?=\bStatus\b)', content)

	if len(status_match_results2) > 0:
		status_match_results2.pop(0)

	for status_match in status_match_results2:
		matches = re.findall(r'\b\d{4}\s+\d{3}\b', status_match)
		sessions = []
		for match in matches:
			sessions.append(int(match.split("\n")[0]))
		
		session_list.append(sessions)
		
	result = {}
	for i in range(len(course_list)):
		result[course_list[i]] = session_list[i]
	
	return result
	





result1 = extract_client_schedule("docs/client/emily.txt")
result2 = extract_client_schedule("docs/client/david.txt")
result3 = extract_client_schedule("docs/client/client_current_schedule.txt")


for i in result1:
	print(i, result1[i])

print("\n")

for i in result2:
	print(i, result2[i])

print("\n")

for i in result3:
	print(i, result3[i])








# course_list = []

# status_match_results1 = re.findall(r'.*?\bStatus\b', content, re.DOTALL)

# for status_match in status_match_results1:
# 		course_name_matches = re.findall(r'[A-Z]+ \d+', status_match)

# 		course_name = course_name_matches[-1].replace(" ", "") if course_name_matches else None

# 		course_list.append(course_name)

# 		# print(course_name)



# status_match_results2 = re.split(r'(?=\bStatus\b)', content)

# if len(status_match_results2) > 0:
# 		status_match_results2.pop(0)


# session_list = []

# for status_match in status_match_results2:
# 		matches = re.findall(r'\b\d{4}\s+\d{3}\b', status_match)
# 		sessions = []
# 		for match in matches:
# 				sessions.append(int(match.split("\n")[0]))
		
# 		session_list.append(sessions)
		
# result = {}
# for i in range(len(course_list)):
# 	result[course_list[i]] = session_list[i]


# for i in result:
# 		print(i, result[i])






