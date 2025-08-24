from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import sys
from selenium.webdriver.chrome.options import Options
from lib import libSupport
import platform
import time


class GooBrowser:
    browser, service = None, None

    def __init__(self):
        self.folder_py_path_imgAuto = libSupport.getFolderResources_imgAuto()
        self.folder_py_path_imgTmp = libSupport.getFolderResources_imgTmp()
        chrome_options = Options()

        if libSupport.checkOS("mac"):
            self.service = Service(libSupport.getFolderDriver()+'/chromedriver_mac') 
            chrome_options.binary_location = libSupport.getFolderDriver()+'/chrome-mac.app/Contents/MacOS/Google Chrome for Testing'
        elif libSupport.checkOS("window"):
            self.service = Service(libSupport.getFolderDriver()+'/chromedriver.exe')

            #file lớn
            chrome_options.binary_location = libSupport.getFolderDriver()+'/chrome-win64/chrome.exe'
            
        elif libSupport.checkOS("linux"): 
            self.service = Service(libSupport.getFolderDriver()+'/chromedriver')

        
        chrome_options.add_argument("--disable-extensions") 
        chrome_options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2})
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")  
        # chrome_options.add_argument("--app=https://min.cafe")  
        # chrome_options.add_argument("--app=https://facebook.com")  
 
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

 
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation',"disable-popup-blocking"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
        chrome_options.add_argument("--start-maximized")
      
        self.browser = webdriver.Chrome(service=self.service, options=chrome_options)

        time.sleep(3)
        self.browser.maximize_window()

    def open_page(self, url: str):
        self.browser.get(url)

    def getImgTmp(self):
        return self.folder_py_path_imgTmp

    def getImgAuto(self):
        return self.folder_py_path_imgAuto

    def getSource(self):
        return self.browser.page_source

    def close_browser(self):
        self.browser.close()
        time.sleep(5)
        self.browser.quit()
