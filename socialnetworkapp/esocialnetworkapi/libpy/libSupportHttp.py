
import os
import platform 
import json

def getFile(path_file_name):
    if os.path.isfile(path_file_name):
        try:
            with open(path_file_name, 'rb') as f:
                return f.read()
        except IOError:
            print("getFile Lỗi =>"+path_file_name)
    return None

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
 

def writeFile(path_folder, file_name, content):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    try:
        with open(path_folder + "/" + file_name, 'w', encoding='utf-8') as a_writer:
            a_writer.write(content)
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


def json_clone(json_):
    try:
        return json.loads(json.dumps(json_, ensure_ascii=False).encode('utf8').decode())
    except:
        return None