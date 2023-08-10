from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

### METHOD 1: Use Selenium to scrape the data ###

# Set up the Selenium WebDriver
def get_course_info_WebDriver(term=1239, subject="CS", course_number=136):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get('https://classes.uwaterloo.ca/under.html')

    # Select the term (replace '1239' with the desired term value)
    term_select = Select(driver.find_element(By.NAME, 'sess'))
    term_select.select_by_value(str(term))

    # Select the subject (replace 'CS' with the desired subject value)
    subject_select = Select(driver.find_element(By.NAME, 'subject'))
    subject_select.select_by_value(subject)

    # Enter the course number (replace '101' with the desired course number)
    course_number_input = driver.find_element(By.NAME, 'cournum')
    course_number_input.send_keys(str(course_number))

    # Find the search button using the value attribute and click it
    search_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Search"]')
    search_button.click()

    html = driver.page_source  # Your HTML content here
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', border=2)

    # Extract table data
    rows = table.find_all('tr')
    csv_data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols = [ele.text.strip() for ele in cols]
        csv_data.append(cols)

    # Write to CSV file
    with open('course_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("CSV file created successfully.")
    driver.quit()



### METHOD 2: Use Requests to scrape the data ### (PREFERED)
def get_course_info_Requests(term=1239, subject="CS", course_number="136"):
    # Set up the request
    url = "https://info.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"
    payload = {'sess': int(term), 'level': 'under', 'subject': subject, 'cournum': int(course_number)}
    r = requests.get(url, params=payload).text
    soup = BeautifulSoup(r, 'html.parser')
    main_table = soup.find('table', border=2)

    # Generate output file name
    output_file = f"docs/course_info/{subject}{course_number}.csv"

    # Open CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate through main table rows
        for row in main_table.find_all('tr'):
            # Check if row contains a sub-table
            sub_table = row.find('table')
            if sub_table:
                continue
            else:
                # If no sub-table, process main table row
                cols = row.find_all(['td', 'th'])
                if cols:  # Check if cols is not empty
                    cols = [ele.text.strip() for ele in cols]
                    writer.writerow(cols)
    # DEBUGGER
    print(f"{subject}{course_number} info saved to docs/course_info/{subject}{course_number}.csv")



