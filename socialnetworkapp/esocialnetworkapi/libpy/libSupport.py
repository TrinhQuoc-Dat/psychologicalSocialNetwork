
import json
import os
import platform
import time
import random
import string

# duy thêm import request để dùng code từ app98 vào clsHandsupchat
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess

# import cv2
# from qreader import QReader
import sys
import re

def remove_parentheses(text: str) -> str:
    text = re.sub(r"\s*\([^)]*\)", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def autoTab(goo_browser, numTab=1):
    actions = ActionChains(goo_browser.browser)
    actions.send_keys(Keys.TAB * numTab)
    actions.perform()


def autoEnter(goo_browser):
    actions = ActionChains(goo_browser.browser)
    actions.send_keys(Keys.ENTER)
    actions.perform()


def getFile(path_file_name):
    if os.path.isfile(path_file_name):
        try:
            with open(path_file_name, 'rb') as f:
                return f.read()
        except IOError:
            print("getFile Lỗi =>"+path_file_name)
    return None


def sendException(telegram_user, content_, time_):
    # 17/06/2024
    # mở chức năng báo cáo telegram
    if telegram_user == "":
        telegram_user_cf = getFile(getFolderResources_data() + "/telegram.json")
        if telegram_user_cf is not None:
            telegram_user_cf = json_load(telegram_user_cf)
            if "telegram_user" in telegram_user_cf:
                telegram_user = telegram_user_cf["telegram_user"]


def getFolderResources():
    # build=> /Users/leminhthanh/Documents/GOOINTECH-GIT/GooAuto/GooPy/dist/GooInTech.app/Contents/MacOS/lib
    # code => /Users/leminhthanh/Documents/GOOINTECH-GIT/GooAuto/GooPy/lib
    # hàm này giúp lấy đường dẫn thư mục góc, vì bản build sẽ có thư mục code
    folder_py_path = os.path.dirname(os.path.realpath(__file__))
    if "/GooInTech.app/Contents/MacOS/lib" in folder_py_path:
        folder_py_path = folder_py_path.replace("/GooInTech.app/Contents/MacOS/lib", "")
    elif "/lib" in folder_py_path:  # luôn là trường hợp cuối cùng
        folder_py_path = folder_py_path.replace("/lib", "")
    elif "\\lib" in folder_py_path:  # luôn là trường hợp cuối cùng Window
        folder_py_path = folder_py_path.replace("\\lib", "")
    # /Users/leminhthanh/Documents/GOOINTECH-GIT/GooAuto/GooPy/dist
    return folder_py_path


def getFolderResources_imgAuto():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/img_auto"


def getFolderResources_imgQuotations():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/img_quotations"


def getFolderResources_imgTmp():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/img_tmp"


def getFolderResources_data():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/data"


def getFolderDriver():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/drivers"


def createFolderSystemRequest():
    folder_py_path = getFolderResources()
    # tạo tất cả thư mục hệ thống cần
    # khi build thì resources luôn được tạo, nếu chưa có
    if not os.path.exists(folder_py_path+"/resources"):
        os.mkdir(folder_py_path+"/resources")

    if not os.path.exists(folder_py_path+"/resources/img_auto"):
        os.mkdir(folder_py_path+"/resources/img_auto")

    if not os.path.exists(folder_py_path+"/resources/img_tmp"):
        os.mkdir(folder_py_path+"/resources/img_tmp")

    if not os.path.exists(folder_py_path+"/resources/data"):
        os.mkdir(folder_py_path+"/resources/data")

    if not os.path.exists(folder_py_path+"/resources/img_quotations"):
        os.mkdir(folder_py_path+"/resources/img_quotations")


def checkOS(os_name):
    # kiểm tra hệ điều hành, trả về là thông tin cố định để tránh các hàm lấy thông OS đổi giá trị
    if platform.system() == "Darwin" and os_name == "mac":
        return True
    elif platform.system() == "Windows" and os_name == "window":
        return True
    elif platform.system() == "Linux" and os_name == "linux":
        return True

    return False


def el_getXPath(goo_browser, xpath_):
    try:
        # //span[text()='Không có bài viết mới']
        return goo_browser.browser.find_element(
            By.XPATH, xpath_)
    except Exception as inst:
        pass
    return None


def el_getXPath_From(el_from, xpath_):
    try:
        # //span[text()='Không có bài viết mới']
        return el_from.find_element(
            By.XPATH, xpath_)
    except Exception as inst:
        pass
    return None


def el_getXPaths(goo_browser, xpath_):
    try:
        # //span[text()='Không có bài viết mới']
        return goo_browser.browser.find_elements(
            By.XPATH, xpath_)
    except Exception as inst:
        pass
    return None


def el_getXPaths_From(el_from, xpath_):
    try:
        # //span[text()='Không có bài viết mới']
        return el_from.find_elements(
            By.XPATH, xpath_)
    except Exception as inst:
        pass
    return None


def writeFile(path_folder, file_name, content):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    try:
        with open(path_folder + "/" + file_name, 'w', encoding='utf-8') as a_writer:
            if isinstance(content, (dict, list)):
                a_writer.write(json.dumps(content, ensure_ascii=False, indent=2))
            else:
                a_writer.write(str(content))
        return True
    except IOError:
        print("writeFile Lỗi =>"+path_folder+"/"+file_name)
    return False


def getFolderResources_data():
    folder_py_path = getFolderResources()
    return folder_py_path+"/resources/data"


def elToStringOut(goo_browser, toEL):
    return goo_browser.browser.execute_script("return arguments[0].outerHTML", toEL)


def json_load(str):
    try:
        # đọc JSON trừ chuổi
        return json.loads(str)
    except:
        return None


def json_to_string(json_):
    try:
        return json.dumps(json_, ensure_ascii=False).encode('utf8').decode()
    except:
        return ""


def input_add(goo_browser, by: By, value: str, text: str):
    field = goo_browser.browser.find_element(by=by, value=value)
    field.send_keys(text)
    time.sleep(1)


def json_clone(json_):
    try:
        return json.loads(json.dumps(json_, ensure_ascii=False).encode('utf8').decode())
    except:
        return None


def button_click(goo_browser, by: By, value: str):
    button = goo_browser.browser.find_element(by=by, value=value)
    button.click()
    time.sleep(1)


def autoScrollToEl(goo_browser, toEL):
    goo_browser.browser.execute_script("arguments[0].scrollIntoView();", toEL)

def getParentNode(goo_browser, toEL, loop_=1):
    str_ = ""
    for l_ in range(0, loop_):
        if str_ == "":
            str_ = str_ + "parentNode"
        else:
            str_ = str_ + ".parentNode"

    return goo_browser.browser.execute_script("return arguments[0]."+str_, toEL)
