from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


import pyautogui

import getpass
import time
import os
import subprocess
import argparse
import re

# get carleton credential 
def run(name_list, output_directory, DUO_CHECK):  
    username = input("Enter username: ") 
    password = getpass.getpass("Enter your password: ")

    print("Setting up Chrome driver...")
    driver = webdriver.Chrome()
    driver.get("https://www.carleton.edu/directory")
    driver.set_window_position(0, 0)
    driver.set_window_size(1024,1024)

    sign_in_button = driver\
            .find_element(By.CLASS_NAME, "campus-directory__login-link")
    sign_in_button.click();

    wait = WebDriverWait(driver, 1000)
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

    with open(name_list, "r") as file: 
        for line in file:
            name = line.strip()
            print(f"Searching for {name} in the directory...")
            first_name = name.split(" ")[0]
            last_name = name.split(" ")[1]
            wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
            firstName_field = driver.find_element(By.ID, "firstName")
            lastName_field = driver.find_element(By.ID, "lastName")
            campus_directory_submit = driver\
                    .find_element(By.ID, "campus-directory__submit")
            firstName_field.clear()
            lastName_field.clear()
            firstName_field.send_keys(first_name)
            lastName_field.send_keys(last_name) 
            campus_directory_submit.click();

            print(f"Opening {first_name}'s image in a new window...")
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "campus-directory__person-image")))
            image_div = driver\
                    .find_element(By.CLASS_NAME, "campus-directory__person-image")
            image = image_div.find_element(By.TAG_NAME, "img")
            image_src = image.get_attribute("src").replace("/?gql=refresh", ".png")
            driver.get(image_src)
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "img")))
            image = driver.find_element(By.TAG_NAME, "img")

            print("Saving image graphically...")
            window_location = driver.get_window_position()
            window_size = driver.get_window_size()
            x = window_size['width'] / 2 + 10
            y = window_size['height'] / 2 + 123 + 10
            ActionChains(driver)\
                    .context_click(image)\
                    .perform() 
            pyautogui.moveTo(x,y)
            pyautogui.click()
            time.sleep(1)
            pyautogui.write("/")
            time.sleep(1)
            pyautogui.write(f"{output_directory[1:]}/{name.replace(' ', '_')}.jpg")
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)

            print("Navigating back to the directory...")
            driver.back()

    print("Terminating...")
    driver.quit()

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input_file", required=True, type=str)
    parser.add_argument("-o", "--output_dir", required=True, type=str)
    args = parser.parse_args()

    name_list = args.input_file
    output_directory = args.output_dir

    if not os.path.exists(name_list): 
        print(f"Error: {name_list} is not a valid path")
        exit(2)

    try:
        os.makedirs(output_directory, exist_ok=True)
        output_directory = os.path.abspath(output_directory)
        print(f"Directory '{output_directory}' created or already exists.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        exit(3)

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

    run(name_list, output_directory, DUO_CHECK)

if __name__ == "__main__": 
    main()
