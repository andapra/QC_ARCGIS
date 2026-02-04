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

def check_web_access(driver, url_page, wa_portal, uname, pwd, file_csv, sheet_name, folder):
    
    wait = WebDriverWait(driver, 25)
    driver.maximize_window()

    print('UAT Scenario for Portal')
    driver.get('{}/{}/home'.format(url_page, wa_portal))
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_1.png'))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div/div[2]/div[12]/div/button')))
    driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[2]/div[12]/div/button').click()
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_2.png'))

    print('Portal landing page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginTitle"]')))
    driver.find_element(By.XPATH, '//*[@id="loginTitle"]').click()
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_username"]')))
    driver.find_element(By.XPATH, '//*[@id="user_username"]').send_keys(uname)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]')))
    driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(pwd)
    
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_3.png'))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signIn"]')))
    driver.find_element(By.XPATH, '//*[@id="signIn"]').click()

    print('Sign in page Response : 200')
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]')))
    driver.find_element(By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]').click()
    
    print('Content page Response : 200')
    time.sleep(10)
    driver.save_screenshot(os.path.join(folder['portal'], 'portal_4.png'))

    df = pd.read_excel(io=file_csv, sheet_name=sheet_name)
    for index, row in df.iterrows():
        if row["type"] == "Dashboard":
            driver.get('{}/{}/apps/opsdashboard/index.html#/{}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'dashboard_{}.png'.format(row["id"])))
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Web Map":
            driver.get('{}/{}/home/webmap/viewer.html?webmap={}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'webmap_{}.png'.format(row["id"])))
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Map Service":
            driver.get('{}/{}/home/webmap/viewer.html?useExisting=1&layers={}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'ms_{}.png'.format(row["id"])))
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Feature Service":
            driver.get('{}/{}/home/webmap/viewer.html?useExisting=1&layers={}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'fs_{}.png'.format(row["id"])))
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Web Mapping Application":
            # driver.get('{}/{}/apps/webappviewer/index.html?id={}'.format(url_page, wa_portal, row["id"]))
            driver.get(row["url"])
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'webapp_{}.png'.format(row["id"])))
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Image Service":
            driver.get('{}/{}/home/webmap/viewer.html?useExisting=1&layers={}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'is_{}.png'.format(row["id"]))) 
            print("completed {} with {}".format(row["type"], row["id"]))
        elif row["type"] == "Web Scene":
            driver.get('{}/{}/webscene/viewer.html?webscene={}'.format(url_page, wa_portal, row["id"]))
            time.sleep(25)
            driver.save_screenshot(os.path.join(folder['portal'], 'webscene_{}.png'.format(row["id"])))            
            print("completed {} with {}".format(row["type"], row["id"]))
    print('All Checking is Completed')

if __name__ == "__main__":
    url = input('Please input portal url example (https://machine.domain.com): ')
    uname = input('Please input administrator username : ')
    pwd = input('Please input administrator password: ')

    web_adaptor_portal = input('Please input web adaptor portal: ')

    input_driver = input('Please input your browser that will be used for automation [edge/chrome/firefox]: ')
    file_csv = input('Please input file excel: ')
    sheet_name = input('Please input sheet_name: ')

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

        check_web_access(get_driver, url, web_adaptor_portal, uname, pwd, file_csv, sheet_name, json_folder)
    except Exception as e:
        raise(e)