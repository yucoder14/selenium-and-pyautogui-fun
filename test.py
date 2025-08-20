from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
import getpass
import time

import pyautogui

# get carleton credential 
username = input("Enter username: ") 
password = getpass.getpass("Enter your password: ")


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
wait.until(EC.visibility_of_element_located((By.ID, "username")))
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")
username_field.send_keys(username)
password_field.send_keys(password)

ActionChains(driver)\
        .key_down(Keys.ENTER)\
        .key_up(Keys.ENTER)\
        .perform()

# stupid DUO; this step is not required if using campus computers 
# connected via ethernet
wait.until(EC.visibility_of_element_located((By.ID, "trust-browser-button")))
trust_browser = driver.find_element(By.ID, "trust-browser-button")
trust_browser.click();

# search for people on the directory
wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
firstName_field = driver.find_element(By.ID, "firstName")
lastName_field = driver.find_element(By.ID, "lastName")
campus_directory_submit = driver.find_element(By.ID, "campus-directory__submit")
firstName_field.send_keys("Changwoo")
lastName_field.send_keys("Yu") 
campus_directory_submit.click();

# go to the image
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "campus-directory__person-image")))
image_div = driver.find_element(By.CLASS_NAME, "campus-directory__person-image")
image = image_div.find_element(By.TAG_NAME, "img")
image_src = image.get_attribute("src").replace("/?gql=refresh", ".png")
driver.get(image_src)
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "img")))
image = driver.find_element(By.TAG_NAME, "img")

# right click on the image and save image
window_location = driver.get_window_position()
window_size = driver.get_window_size()
x = window_size['width'] / 2 + 10
y = window_size['height'] / 2 + 123 + 10
ActionChains(driver)\
        .context_click(image)\
        .perform() 
pyautogui.moveTo(x,y)
pyautogui.click()
time.sleep(2)
pyautogui.write("test.jpg")
pyautogui.press('enter')

driver.back()

driver.quit()

