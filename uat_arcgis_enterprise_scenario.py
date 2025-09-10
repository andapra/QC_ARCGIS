import os, shutil
import requests
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pynput.keyboard import Key, Controller

def choosing_driver(input_driver):

    if input_driver == 'chrome':
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)
    
    elif input_driver == 'edge':
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)

    elif input_driver == 'firefox':
        driver = webdriver.Firefox()

    return driver

def check_web_access(driver, url_page, wa_portal, uname, pwd, file_csv, folder):
    
    keyboard = Controller()
    wait = WebDriverWait(driver, 60)
    driver.maximize_window()

    print('UAT Scenario for Portal')
    driver.get('{}/{}/home'.format(url_page, wa_portal))
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_1.jpeg'))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button')))
    driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button').click()
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_2.jpeg'))

    print('Portal landing page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginTitle"]')))
    driver.find_element(By.XPATH, '//*[@id="loginTitle"]').click()
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_username"]')))
    driver.find_element(By.XPATH, '//*[@id="user_username"]').send_keys(uname)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]')))
    driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(pwd)
    
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_3.jpeg'))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signIn"]')))
    driver.find_element(By.XPATH, '//*[@id="signIn"]').click()

    print('Sign in page Response : 200')
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]')))
    driver.find_element(By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]').click()
    
    print('Content page Response : 200')
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_4.jpeg'))

    df = pd.read_excel(io=file_csv, sheet_name='list_portal')
    for index, row in df.iterrows():
        if row["type"] == "Dashboard":
            driver.get('{}/{}/apps/dashboards/{}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'dashboard_{}.jpeg'.format(row["itemid"])))
        elif row["type"] == "Web Map":
            driver.get('{}/{}/apps/mapviewer/index.html?webmap={}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'webmap_{}.jpeg'.format(row["itemid"])))
        elif row["type"] == "Map Service":
            driver.get('{}/{}/apps/mapviewer/index.html?layers={}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'ms_{}.jpeg'.format(row["itemid"])))
        elif row["type"] == "Feature Service":
            driver.get('{}/{}/apps/mapviewer/index.html?layers={}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'fs_{}.jpeg'.format(row["itemid"])))
        elif row["type"] == "Experience builder":
            driver.get('{}/{}/apps/experiencebuilder/experience/?id={}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'expb_{}.jpeg'.format(row["itemid"])))
        elif row["type"] == "Web App":
            driver.get('{}/{}/apps/webappviewer/index.html?id={}'.format(url_page, wa_portal, row["itemid"]))
            time.sleep(60)
            driver.save_screenshot(os.path.join(folder['portal'], 'webapp_{}.jpeg'.format(row["itemid"])))

    print('All Checking is Completed')

if __name__ == "__main__":
    url = input('Please input portal url example (https://machine.domain.com): ')
    uname = input('Please input administrator username : ')
    pwd = input('Please input administrator password: ')

    web_adaptor_portal = input('Please input web adaptor portal: ')
    web_adaptor_server = input('Please input web adaptor server: ')

    input_driver = input('Please input your browser that will be used for automation [edge/chrome/firefox]: ')
    file_csv = input('Please input file csv: ')


    print('Preparing the screenshot folder')
    if os.path.isdir('screenshot'):
        pass
    else:
        os.mkdir('screenshot')

    folder_portal = os.path.join(os.getcwd(), 'screenshot', 'portal')
    if os.path.isdir(folder_portal):
        pass
    else:
        os.mkdir(folder_portal)

    print('Screenshot folders have been created')
    json_folder = {
        'portal': folder_portal
    }


    try:
        print('Preparing the web driver, you have choose {}'.format(input_driver))
        get_driver = choosing_driver(input_driver)
        print('Webdriver is completed')

        check_web_access(get_driver, url, web_adaptor_portal, uname, pwd, file_csv, json_folder)
    except Exception as e:
        raise(e)