import json
import os
import platform
import sys
import time

import requests
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from libpy import libSupport


class clsPsychological:
    def __init__(self):
        pass

    # khởi tạo
    goo_browser = None
    account_info = None
    data_config = None
    data_tabs = {}

    # mã tab hiện tại giúp chụp màn hình theo tab đó
    data_tab_code_current = ""

    # đường dẫn vật lý tự thay đổi khi ở trong docker container
    path_save_screenshot = libSupport.getFolderResources_data() + '/dockersele-view-img/'

    # đường dẫn vật lý tự thay đổi theo resources_data
    path_data = libSupport.getFolderResources_data()

    def public_start(self, ss_goo_browser, acc, data_config_):
        self.goo_browser = ss_goo_browser
        self.account_info = acc
        self.data_config = data_config_

        # nếu có file docker config nghĩa là đang ở docker container
        path_file_docker = os.path.dirname(os.path.realpath(__file__))
        path_file_docker = path_file_docker.replace("clsAuto", "")
        docker_config = libSupport.getFile(path_file_docker + "type_user.json")
        if docker_config is not None:
            self.path_save_screenshot = path_file_docker + "img/"
            self.path_data = path_file_docker + "resources/data/"

        if len(self.goo_browser.window_handles) < 1:
            self.data_tabs["current"] = self.goo_browser.current_window_handle
        else:
            self.data_tabs["current"] = self.goo_browser.window_handles[0]
            

    def sysCheckOk(self):
        # Kiểm tra tài hệ thống đã đủ biến cần thiết
        # sys là hàm hệ thống yêu cầu không được chỉnh sửa
        if self.goo_browser is None or self.account_info is None or self.data_config is None:
            return False

        # riêng email cần kiểm tra thêm
        if "" in self.account_info and "" in self.account_info and "" in self.account_info:
            return False
        return True
    
    def autoSelectAll(self):
        actions = ActionChains(self.goo_browser)
        if platform.system() == 'Darwin':  # Mac
            actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        else:  # Windows hoặc Linux
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.perform()

    def el_getXPath(self, xpath_):
        try:
            # //span[text()='Không có bài viết mới']
            return self.goo_browser.find_element(By.XPATH, xpath_)
        except Exception as inst:
            pass
        return None

    def el_getXPath_From(self, el_from, xpath_):
        try:
            # //span[text()='Không có bài viết mới']
            return el_from.find_element(By.XPATH, xpath_)
        except Exception as inst:
            pass
        return None
    
    def autoScrollToEl_bottom(self):
        self.goo_browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    def el_getXPaths(self, xpath_):
        try:
            # //span[text()='Không có bài viết mới']
            return self.goo_browser.find_elements(
                By.XPATH, xpath_)
        except Exception as inst:
            pass
        return None

    def el_getXPaths_From(self, el_from, xpath_):
        try:
            # //span[text()='Không có bài viết mới']
            return el_from.find_elements(
                By.XPATH, xpath_)
        except Exception as inst:
            pass
        return None

    def save_screenshot(self):
        self.goo_browser.save_screenshot(
            self.path_save_screenshot + self.account_info["user_work_space"] + '-' +
            self.account_info["type"] + '-' + self.account_info[
                "user"] + '-' + self.data_tab_code_current + '.png')

    def switch_toTab(self, tab_code):
        self.data_tab_code_current = tab_code
        self.goo_browser.switch_to.window(self.data_tabs[tab_code])
        time.sleep(5)
        self.save_screenshot()
        time.sleep(1)

    def paste_from_clipboard(self, element):
        """ Dán nội dung từ clipboard vào phần tử Selenium """
        element.click()
        time.sleep(0.5)  # Chờ một chút để trình duyệt nhận diện focus
        element.send_keys(Keys.CONTROL, 'v')  # Dán nội dung

    def autoSelectAll(self):
        actions = ActionChains(self.goo_browser)
        if platform.system() == 'Darwin':  # Mac
            actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        else:  # Windows hoặc Linux
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.perform()

    def autoClear(self):
        actions = ActionChains(self.goo_browser)
        actions.send_keys(Keys.DELETE)
        actions.perform()

    def autoScrollToEl(self, toEL):
        self.goo_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", toEL)
   
    def autoGetData_trangtamly_blog(self):
        if self.sysCheckOk() == False:
            return # stopp
        
        try:
            self.switch_toTab("current")
            time.sleep(1)
            self.goo_browser.get("https://trangtamly.blog/")
            time.sleep(15)

            # logic cần lấy hết tất cả các dữ liệu tìm kiếm thấy khi nhập tử khóa
            list_tag_a = []
            len_list_tag_a = -1

            # scrool đến khi nào load hết các bài viết
            div_container = self.el_getXPath("//div[@id='posts']")
            if div_container is not None:
                list_tag_a = self.el_getXPaths_From(div_container, ".//article[contains(@id, 'post') and contains(@class, 'post')]")
                if len(list_tag_a) > 0:
                    while True:
                        if len_list_tag_a == len(list_tag_a):
                            break
                        # ghi lại số lượng danh sách cũ
                        len_list_tag_a = len(list_tag_a)
                        # scrool element end
                        # self.autoScrollToEl_bottom()
                        self.autoScrollToEl(list_tag_a[len(list_tag_a)-1])
                        time.sleep(15)
                        # cập nhật lại danh sách
                        list_tag_a = self.el_getXPaths_From(div_container, ".//article[contains(@id, 'post') and contains(@class, 'post')]")
            print("1")
            time.sleep(3*60)
            data = []
            for blog in list_tag_a:
                link = self.el_getXPath_From(blog, "./figure/a")
                time.sleep(2)
                link_blog = link.get_attribute("href")
                data.append(link_blog)

            print(data)
            libSupport.writeFile(libSupport.getFolderResources_data() + "/tamlyhoc", "trangtamly.json", libSupport.json_to_string(data))

        except Exception as ex:
            print("=============================================")
            print("Lỗi: ", ex)

    
    def autoGetData_trangtamly_dataset(self):
        if self.sysCheckOk() == False:
            return # stopp
        
        try:

            self.switch_toTab("current")
            time.sleep(1)

            data = {}
            # đoc file
            file_dataset = libSupport.getFile(libSupport.getFolderResources_data() + '/tamlyhoc/trangtamly_dataset.json')
            if file_dataset is not None:
                data = libSupport.json_load(file_dataset)

            file_content = libSupport.getFile(libSupport.getFolderResources_data() + '/tamlyhoc/trangtamly.json')
            if file_content is not None:
                all_link = libSupport.json_load(file_content)
                if all_link is not None:
                    for link in all_link:
                        self.goo_browser.get(link)
                        time.sleep(10)

                        page = self.el_getXPath("//div[@class='post-content']")
                        if page is None:
                            continue

                        title = self.el_getXPath('//h1[@class="post-title"]')
                        if title is not None:
                            title = title.text
                            if title in data:
                                continue
                        text = ""
                        contents = self.el_getXPaths_From(page, "./p")
                        for c in contents:
                            if self.el_getXPath_From(c, "./span/em") is not None:
                                continue
                            text += c.text
                        
                        data[title] = text
                        # print(data)
                        libSupport.writeFile(libSupport.getFolderResources_data() + "/tamlyhoc", "trangtamly_dataset.json", libSupport.json_to_string(data))
                        
        except Exception as inst:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("=============================================")
            print({"content": """Lỗi tại:"""+str(exc_tb.tb_lineno)+""", loại:"""+str(exc_type)+"""
                    Lỗi:"""+str(inst) + "\nTime:"+time.strftime("%d/%m/%Y %H:%M:%S")})

