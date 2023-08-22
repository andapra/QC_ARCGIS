import os, shutil
import requests
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_web_access(url_page, wa_portal, wa_server, uname, pwd):

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    driver.get('{}/{}/home'.format(url_page, wa_portal))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button')))
    driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button').click()

    print('Portal landing page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginTitle"]')))
    driver.find_element(By.XPATH, '//*[@id="loginTitle"]').click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_username"]')))
    driver.find_element(By.XPATH, '//*[@id="user_username"]').send_keys(uname)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]')))
    driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(pwd)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signIn"]')))
    driver.find_element(By.XPATH, '//*[@id="signIn"]').click()

    print('Sign in page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]')))
    driver.find_element(By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]').click()
    

    print('Content page Response : 200')

    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-dropdown"]')))
    # driver.find_element(By.XPATH, '//*[@id="create-dropdown"]').click()

    driver.get('{}/{}/home'.format(url_page, wa_server))

if __name__ == "__main__":
    url = input('Please input portal url example (https://machine.domain.com): ')
    uname = input('Please input administrator username : ')
    pwd = input('Please input administrator password: ')

    web_adaptor_portal = input('Please input web adaptor portal: ')
    web_adaptor_server = input('Please input web adaptor server: ')

    check_web_access(url, web_adaptor_portal, web_adaptor_server, uname, pwd)