from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import requests

import getpass
import time
import os
import subprocess
import argparse
import re

# get carleton credential 
def run(name_list, output_directory, DUO_CHECK, USE_EMAIL):  
    username = input("Enter username: ") 
    password = getpass.getpass("Enter your password: ")

    print("Setting up Chrome driver...")
    driver = webdriver.Chrome()
    driver.get("https://www.carleton.edu/directory")

    sign_in_button = driver\
            .find_element(By.CLASS_NAME, "campus-directory__login-link")
    sign_in_button.click();

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "idp_55012701_button")))
    login_link = driver.find_element(By.ID, "idp_55012701_button")
    login_link.click()

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

    if DUO_CHECK: 
        print("Waiting for DUO Authentication...")
        wait.until(EC.visibility_of_element_located((By.ID, "trust-browser-button")))
        trust_browser = driver.find_element(By.ID, "trust-browser-button")
        trust_browser.click();

    # wait until verified
    wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
    cookies = driver.get_cookies();

    s = requests.Session() 
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    with open(name_list, "r") as file: 
        for line in file:
            if (USE_EMAIL):
                # search by email
                email = line.strip()
                wait.until(EC.visibility_of_element_located((By.ID, "email")))
                email_field = driver.find_element(By.ID, "email")
                email_field.clear()
                email_field.send_keys(email)
            else:
                # search by name
                name = line.strip()
                first_name = ""
                name_array = name.split(" ")
                if len(name_array) == 2: 
                    first_name = name_array[0] 
                last_name = name_array[-1]

                wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
                firstName_field = driver.find_element(By.ID, "firstName")
                lastName_field = driver.find_element(By.ID, "lastName")

                firstName_field.clear()
                lastName_field.clear()

                firstName_field.send_keys(first_name)
                lastName_field.send_keys(last_name) 

            # submit query
            campus_directory_submit = driver.find_element(By.ID, "campus-directory__submit")
            campus_directory_submit.click();
            
            # grab person's name
            try: 
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "campus-directory__person-name")))
                name = driver.find_element(By.CLASS_NAME, "campus-directory__person-name").text
                image_name = f"{output_directory}/{name.replace(' ', '_')}.jpg"
                if os.path.exists(image_name): 
                    print(f"File {image_name} exists")
                    continue

                # download headshot
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "campus-directory__person-image")))
                image_div = driver.find_element(By.CLASS_NAME, "campus-directory__person-image")
                image = image_div.find_element(By.TAG_NAME, "img")
                image_src = image.get_attribute("src").replace("/?gql=refresh", ".png")

                response = s.get(image_src)

                print(f"Grabbing headshot of {name}...")
                if response.status_code == 200: 
                    with open(image_name, 'wb') as f:
                        f.write(response.content)
                    print(f"File downloaded successfully to {image_name}")
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
            except TimeoutException: 
                print(f"{line.strip()} does not exist on directory, skipping...")
                pass

            driver.back()

    print("Terminating...")
    driver.quit()

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input_file", required=True, type=str)
    parser.add_argument("-o", "--output_dir", required=True, type=str)
    parser.add_argument("-e", "--email", action='store_true') 
    args = parser.parse_args()

    input_list = args.input_file
    output_directory = args.output_dir
    USE_EMAIL = args.email

    if not os.path.exists(input_list): 
        print(f"Error: {input_list} is not a valid path")
        exit(2)

    try:
        os.makedirs(output_directory, exist_ok=True)
        output_directory = os.path.abspath(output_directory)
        print(f"Directory '{output_directory}' created or already exists.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        exit(3)

    # check if duo will ask user to trust device
    DUO_CHECK = True
    try:  
        result = subprocess.run(
                ["ifconfig", "en0"], 
                capture_output=True, 
                text=True, 
                check=True)
        output = result.stdout.split('\n')
        ip4_line = [line.strip() for line in output if "broadcast" in line][0]
        ip4 = re.findall(r"137.22.\d+\.\d+", ip4_line)
        if len(ip4) > 0:
            DUO_CHECK = False
    except subprocess.CalledProcessError as e: 
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error Output: {e.stderr}")

    run(input_list, output_directory, DUO_CHECK, USE_EMAIL)

if __name__ == "__main__": 
    main()
