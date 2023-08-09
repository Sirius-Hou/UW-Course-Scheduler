import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("API_KEY")


def gpt_generate_schedule(messages=[]):
    with open("docs/commands/startup_command.txt", "r") as f:
        command_text = f.read()

    with open("docs/course_info/all_courses_info.txt", "r") as f:
        all_courses_info = f.read()

    # Replace the string in the messages list
    messages += [
        {"role": "user", "content": command_text + "\n" + all_courses_info}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stop=None,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print(response['choices'][0]['message']['content'] + "\n")
    
    with open("docs/generated/generated_schedule.txt", "w") as f:
        f.write(response['choices'][0]['message']['content'])
    
    return messages



def gpt_convert_to_calendar_format():
    with open("docs/commands/convert_to_calendar_format_command.txt", "r") as f:
        convert_to_calendar_format_command = f.read()

    with open("docs/generated/generated_schedule.txt", "r") as f:
        generated_schedule = f.read()

    # Replace the string in the messages list
    messages = [
        {"role": "user", "content": convert_to_calendar_format_command + "\n" + generated_schedule}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stop=None,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print(response['choices'][0]['message']['content'] + "\n")
    
    with open("docs/generated/generated_schedule_calendar_format.txt", "w") as f:
        f.write(response['choices'][0]['message']['content'])
    
    return messages



def chat_with_gpt(messages=[]):
    print("Welcome to ChatGPT 3.5 turbo! Type 'exit' to quit.")

    messages += [{"role": "system", "content": "You are a helpful course selection assistant at University of Waterloo."}]

    while True:
        user_input = input(">>> ")
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stop=None,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        print(response['choices'][0]['message']['content'] + "\n")

        if user_input.lower() == "exit":
            break