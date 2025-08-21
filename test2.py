from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import getpass
import time

import pyautogui
import requests

# get carleton credential 
username = input("Enter username: ") 
password = getpass.getpass("Enter your password: ")

print("Setting up Chrome driver...")
driver = webdriver.Chrome()
driver.get("https://www.carleton.edu/directory")
driver.set_window_position(0, 0)
driver.set_window_size(512,512)

sign_in_button = driver\
        .find_element(By.CLASS_NAME, "campus-directory__login-link")
sign_in_button.click();

wait = WebDriverWait(driver, 1000)
wait.until(EC.visibility_of_element_located((By.ID, "idp_55012701_button")))
login_link = driver.find_element(By.ID, "idp_55012701_button")
login_link.click()

# login using carleton credentials
print("Logging in using Carleton credentials...")
wait.until(EC.visibility_of_element_located((By.ID, "username")))
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")
username_field.send_keys(username)
password_field.send_keys(password)

ActionChains(driver)\
        .key_down(Keys.ENTER)\
        .key_up(Keys.ENTER)\
        .perform()

time.sleep(1)

try: 
    error_p = driver.find_element(By.CLASS_NAME, "form-element")
    print("Wrong Credentials!")
    driver.quit()
    exit(1)
except NoSuchElementException:
    pass

print("Waiting for DUO Authentication...")
# stupid DUO; this step is not required if using campus computers 
# connected via ethernet; check ip to check if this step is necessary
wait.until(EC.visibility_of_element_located((By.ID, "trust-browser-button")))
trust_browser = driver.find_element(By.ID, "trust-browser-button")
trust_browser.click();
# from this point on, it can be repeated for different people 
# search for people on the directory
name = "Changwoo Yu" 
print(f"Searching for {name} in the directory...")
first_name = name.split(" ")[0]
last_name = name.split(" ")[1]
wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
firstName_field = driver.find_element(By.ID, "firstName")
lastName_field = driver.find_element(By.ID, "lastName")
campus_directory_submit = driver.find_element(By.ID, "campus-directory__submit")
firstName_field.send_keys(first_name)
lastName_field.send_keys(last_name) 
campus_directory_submit.click();

wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "campus-directory__person-image")))
image_div = driver.find_element(By.CLASS_NAME, "campus-directory__person-image")
image = image_div.find_element(By.TAG_NAME, "img")
image_src = image.get_attribute("src").replace("/?gql=refresh", ".png")

cookies = driver.get_cookies();
for cookie in cookies:
    print(cookie)

s = requests.Session() 
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])

response = s.get(image_src)

if response.status_code == 200: 
    local_filename = "testing.png" # Choose a name for the local file
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    print(f"File downloaded successfully to {local_filename}")
else:
    print(f"Failed to download file. Status code: {response.status_code}")

print("Terminating...")
driver.quit()

