import pyperclip 
import re
from lib import libSupport
import subprocess
import markdown

class sysMarkdown:

    def copyUbuntu(self, text):
        # Sử dụng xclip để sao chép văn bản vào clipboard
        command = f'echo "{text}" | xclip -selection clipboard'
        subprocess.run(command, shell=True)

    def public_copyMarkdown(self, text, is_group = True):
        print("vo public_coypy",text)
        if is_group: 
            text = markdown.markdown(text)  
            # phải copy cả định dạng luôn vào clipboard (kiểu html)
            process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'text/html'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        else:
            a = self.convert_markdown_to_facebook(text)
            print("a===>", a)
            self.copyUbuntu(a)
            subprocess.run(
                ['xclip', '-selection', 'clipboard', '-o'],
                check=True
            )

    def bold(self, text):
        #đọc file chuyển đổi chữ đậm bold
        a_f = libSupport.getFile(libSupport.getFolderResources()+"/sys_markdownBold.txt")
        data_char = {}
        if a_f is not None:
            array_a_f = a_f.decode().split()
            for i in array_a_f:
                if ":" in i:
                    i_ar = i.split(":")
                    if len(i_ar)==2:
                        if i_ar[0] not in data_char:
                            data_char[i_ar[0]]=i_ar[1]
                        else:
                            pass
        result = ""
        if data_char is not None:
            for i in text:
                if i in data_char:
                    result += data_char[i]
                else:
                    result += i
        return result

    def italic(self, text):
        #Đọc file chuyển đổi chữ italic
        a_f = libSupport.getFile(libSupport.getFolderResources()+"/sys_markdownItalic.txt")

        data_char = {}
        if a_f is not None:
            array_a_f = a_f.decode().split()
            for i in array_a_f:
                if ":" in i:
                    i_ar = i.split(":")
                    if len(i_ar)==2:
                        if i_ar[0] not in data_char:
                            data_char[i_ar[0]]=i_ar[1]
                        else:
                            pass
        result = ""
        if data_char is not None:
            for i in text:
                if i in data_char:
                    result += data_char[i]
                else:
                    result += i
        return result


    def convert_markdown_to_facebook(self, md):
        # **bold**
        md = re.sub(r"\*\*(.*?)\*\*", lambda m: self.bold(m.group(1)), md)
        # *italic*
        md = re.sub(r"\*(.*?)\*", lambda m: self.italic(m.group(1)), md)
        return md