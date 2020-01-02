# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import poplib
import email
import datetime
import time
import os
import xlrd
import xlwt
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


n = [0]
poplib._MAXLINE=20480



def decode_str(s):  # 字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def check_filename_available(filename):
    if filename not in n:
        n.append(filename)
        return filename
    else:
        filename_new = str(len(n))+filename
        n.append(filename_new)
        return filename_new

def get_att(msg,dirs):
    import email
    attachment_files = []
    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称类型
        contType = part.get_content_type()
        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)  # 对附件名称进行解码
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                print(filename)
                # filename = filename.encode("utf-8")
            data = part.get_payload(decode=True)
            # 下载附件
            if str(filename).endswith(".pdf"):
                createDir = dirs+"\\" + check_filename_available(filename)
                att_file = open(createDir, 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                attachment_files.append(filename)
                att_file.write(data)  # 保存附件
                att_file.close()
            return attachment_files

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

# 连接到POP3服务器,有些邮箱服务器需要ssl加密，对于不需要加密的服务器可以使用poplib.POP3()
def get_server(email,password,pop3_server,dirs):
    server = poplib.POP3_SSL(pop3_server)
    server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # 返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)
    index = len(mails)

    for i in range(index, 0, -1):
    # 倒序遍历邮件
        resp, lines, octets = server.retr(i)
    # lines存储了邮件的原始文本的每一行,
    # 邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
    # 解析邮件:
        msg = Parser().parsestr(msg_content)
    # 获取邮件时间
        # date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
        # date2 = time.strftime("%Y%m%d", date1)  # 邮件时间格式转换
        # if (date2 < '20191230'):
        #     continue

        f_list = get_att(msg,dirs)  # 获取附件
        # print_info(msg)

    server.quit()

