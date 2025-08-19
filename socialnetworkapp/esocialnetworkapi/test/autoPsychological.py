import sys
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.chrome.service import Service


# Thêm thư mục cha của thư mục hiện tại (chính là thư mục chứa thư mục "lib")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clsAuto.clsPsychological import clsPsychological
from lib import libSupport


def connectChrome():
    try:
        print("----------Docker-----connectChrome------")
        options = OptionsChrome()

        # Thiết lập các tham số trình duyệt
        options.set_capability('se:abc', 'test_visit_basic_auth_secured_page (ChromeTests)')
        options.add_argument("--no-sandbox")  # Bắt buộc trong môi trường Docker
        options.add_argument("--disable-dev-shm-usage")  # Sử dụng shared memory thay vì /dev/shm
        options.add_argument("--disable-infobars")
        options.add_argument("--headless=new")  # Headless chế độ mới (ổn định hơn)
        options.add_argument("--disable-extensions")  # Tắt các extension không cần thiết
        options.add_argument("--disable-background-networking")  # Giảm tải mạng
        options.add_argument("--disable-renderer-backgrounding")  # Không tạm dừng rendering
        options.add_argument("--disable-sync")  # Tắt đồng bộ hóa (không cần thiết trong test)
        options.add_argument("--disable-crash-reporter")  # Tắt crash reporting
        options.add_argument("--disable-logging")  # Tắt logging
        options.add_argument("--disable-notifications")  # Tắt thông báo
        options.add_argument("--window-size=1920,1080")  # Đặt kích thước trình duyệt
        options.add_argument("--enable-logging")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        options.add_argument("--v=1")

        # Thêm user-agent hiện đại để tránh trình duyệt cũ
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Kết nối tới Selenium Grid (Docker)
        return webdriver.Remote(
            options=options,
            keep_alive=True,
            command_executor="http://localhost:4444/wd/hub"
        )

    except Exception as inst:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        aaaa_error = """connectChrome.1
        Lỗi tại:""" + str(exc_tb.tb_lineno) + """, loại:""" + str(exc_type) + """
        Lỗi:""" + str(inst)
        print("---exp--->", aaaa_error)

    return None


def connectChromeLocal():
    try:
        print("---------connectChromeLocal------")
        chrome_options = OptionsChrome()
        service = None
        if libSupport.checkOS("mac"):
            service = Service(libSupport.getFolderDriver()+'/chromedriver_mac')
            chrome_options.binary_location = libSupport.getFolderDriver()+'/chrome-mac.app/Contents/MacOS/Google Chrome for Testing'
        elif libSupport.checkOS("window"):
            service = Service(libSupport.getFolderDriver()+'/chromedriver.exe')

            # file lớn
            chrome_options.binary_location = libSupport.getFolderDriver()+'/chrome-win64/chrome.exe'

        elif libSupport.checkOS("linux"):
            service = Service(libSupport.getFolderDriver()+'/chromedriver')

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
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', "disable-popup-blocking"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        browser = webdriver.Chrome(service=service, options=chrome_options)
        time.sleep(3)
        browser.maximize_window()

        return browser

    except Exception as inst:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        aaaa_error = """connectChrome.2
      Lỗi tại:"""+str(exc_tb.tb_lineno)+""", loại:"""+str(exc_type)+"""
      Lỗi:"""+str(inst)
        print("---exp--->", aaaa_error)

    return None


def callTest():
    time.sleep(10)
    clsPsychological__ = clsPsychological()

    # Local
    Goobrowser = connectChromeLocal()
    if Goobrowser == None:
        print("không thể kết nối với Goobrowser Local")
        return
    data_user = {
        "user": "VMSNWFcuQoyv",
        "pass": "TWcKknHLRtns",
        "2fa": "PQOCLZ6M7X2GGNLLJ7DD4LNAOM23XWVX",
        "user_work_space": "kenco__dockersele_com",
        "type": "forum",
        "status": "A",
        "docker_memory": "1",
        "docker_proxy": False,
        "proxy-list-proxy": "",
        "email": "",
        "form-code": "dockersele-add-acc",
        "master_data_key": "iGgWZR_311224134242",
        "master_data_time": 1735627554868.8691
    }
    clsPsychological__.public_start(Goobrowser, data_user, {
        "telegram_user_admin": "-4566353440",
        "telegram_user": "thanhlm22",
    })
    clsPsychological__.autoGetData_trangtamly_dataset()
    print("end")
    time.sleep(4000)


if __name__ == '__main__':
    libSupport.createFolderSystemRequest()
    callTest()
