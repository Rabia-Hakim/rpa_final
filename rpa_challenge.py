# Import libraries:
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

import time
import pandas as pd
import os

# Browser setting and mode setting:
parser = argparse.ArgumentParser(description='Choose browser and mode')
parser.add_argument('browser', choices=['chrome', 'firefox', 'edge'], help="Choose the browser: chrome, firefox, or edge")
parser.add_argument('mode', choices=['normal', 'headless'], help="Choose the mode: normal or headless")
args = parser.parse_args()

browser = args.browser
mode = args.mode

# Configuring the download location:
current_location = os.path.dirname(os.path.abspath(__file__))
download_location = os.path.join(current_location, "data")
if not os.path.exists(download_location):
    os.makedirs(download_location)

# drivers location
drivers_folder = os.path.join(current_location, "drivers")
chromedriver_location = os.path.join(drivers_folder, "chromedriver.exe")
firefoxdriver_location = os.path.join(drivers_folder, "geckodriver.exe")


#setting of download
download_preferences = {
    "download.default_directory": download_location,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}

# setting browser options:
if  browser == "chrome":
    options = ChromeOptions()
    if mode == "headless":
       options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs", download_preferences)
    options.page_load_strategy = 'normal'
    
    if os.path.exists(chromedriver_location):
        service = ChromeService(executable_path=chromedriver_location)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

elif browser == "firefox":
    options = FirefoxOptions()
    if mode == "headless":
       options.add_argument("--headless")
    options.set_preference("browser.download.dir", download_location)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.page_load_strategy = 'normal'

    if os.path.exists(firefoxdriver_location):
        service = FirefoxService(firefoxdriver_location)
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

# Open the Web Application:
try:
    driver.get("https://rpachallenge.com")
    time.sleep(4)
except WebDriverException as error:
    print(f"Error with opening the web application : {error}")
    driver.quit()
    exit(1)

# Download the Data File:
try:
    download_button = driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/a")
    download_button.click()
    time.sleep(5)
except NoSuchElementException as error:
    print("The download button was not found")
    driver.quit()
    exit(1)

# Start the Task: 
try:
    start_button = driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button")
    start_button.click()
    time.sleep(3)
except NoSuchElementException as error:
    print("The start button was not found.")
    driver.quit()
    exit(1)

# read the file:
challenge_file = os.path.join(download_location, "challenge.xlsx")
try:
    df = pd.read_excel(challenge_file)
    df.columns = df.columns.str.strip()  
except FileNotFoundError as error:
    print("excel file not found")
    driver.quit()
    exit(1)

# Complete the form for each line
field_elements = {
    "First Name": '[ng-reflect-name="labelFirstName"]',
    "Last Name": '[ng-reflect-name="labelLastName"]',
    "Company Name": '[ng-reflect-name="labelCompanyName"]',
    "Role in Company": '[ng-reflect-name="labelRole"]',
    "Address": '[ng-reflect-name="labelAddress"]',
    "Email": '[ng-reflect-name="labelEmail"]',
    "Phone Number": '[ng-reflect-name="labelPhone"]'
}

for index, row in df.iterrows():
    try:
        
        for column_name, selector in field_elements.items():
            try:
                field_element = driver.find_element(By.CSS_SELECTOR, selector)
                field_element.clear()
                field_element.send_keys(str(row[column_name])) 
            except NoSuchElementException:
                print(f"The field '{column_name}' not found !")
                driver.quit()
                exit(1)

        # submit the form:
        submit_button = driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input")
        submit_button.click()
        time.sleep(4)  
    except WebDriverException as error:
        print(f" Error in row submission process {index}: {error}")
        driver.quit()
        exit(1) 

# save in txt file the result:
message_element = driver.find_element(By.CLASS_NAME, "message2")
message_text = message_element.text
with open("result.txt", "w", encoding="utf-8") as file:
    file.write(message_text)


# close the browser:
driver.quit()
