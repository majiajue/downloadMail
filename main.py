import os
from mail import get_server,GetDesktopPath





l =[0]

if __name__ == '__main__':
    with open("config.txt", "r") as f:
        for index, line in enumerate(f.readlines()):
            line = line.strip('\n')
            # 去掉列表中每一个元素的换行符
            l.insert(index, line)

    # 输入邮件地址, 口令和POP3服务器地址:

    email = l[0]
    password = l[1]
    pop3_server = l[2]
    desktop = GetDesktopPath()
    dirs = str(desktop) + "\\发票报销"

    if not os.path.exists(dirs):
        os.mkdir(dirs)
    get_server(email,password,pop3_server,dirs)
