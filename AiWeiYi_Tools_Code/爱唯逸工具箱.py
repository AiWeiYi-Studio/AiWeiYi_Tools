# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 23:20
# @Author : 爱唯逸网络科技
# @Email : support@857xx.cn
# @File : 爱唯逸工具箱.py
# @Project: 爱唯逸工具箱

# 引入库
import webbrowser  # 引用浏览器打开网页
import urllib.parse  # 加密传输账号密码
import urllib.request  # 爬取网页资源与信息
import json  # 解析或加密Json信息
import validators  # 检测Url地址
import requests  # 获取当前文件路径
import os
import sys
import subprocess as sp

# 获取云端数据
def check_info():
    site = 'https://web.857xx.cn/api/app/aiweiyi.php'
    act = '?act=check_info'
    api = site + act
    get = urllib.request.urlopen(api)
    result = json.loads(get.read())
    return result


# 用户登录操作
def check_login(username, password):
    username = urllib.parse.quote(username)
    password = urllib.parse.quote(password)
    site = 'https://web.857xx.cn/api/app/aiweiyi.php'
    act = '?act=user_login&username=' + username + '&password=' + password
    api = site + act
    get = urllib.request.urlopen(api)
    result = json.loads(get.read())
    return result


# 获取用户信息
def user_info(username, password):
    username = urllib.parse.quote(username)
    password = urllib.parse.quote(password)
    site = 'https://web.857xx.cn/api/app/aiweiyi.php'
    act = '?act=user_info&username=' + username + '&password=' + password
    api = site + act
    get = urllib.request.urlopen(api)
    result = json.loads(get.read())
    return result


# 定义函数爱唯逸邮件发件
def send_mail(token, mail, title, text):
    site = 'https://web.857xx.cn'
    mode = '/api/api/mail.php'
    token = urllib.parse.quote(token)
    mail = urllib.parse.quote(mail)
    title = urllib.parse.quote(title)
    text = urllib.parse.quote(text)
    post = '?token=' + token + '&mail=' + mail + '&title=' + title + '&text=' + text
    api = site + mode + post
    get = urllib.request.urlopen(api)
    result = json.loads(get.read())
    return result['msg']


# 获取程序所在路径，file为程序所在目录到文件，path为所在目录
def path(type):
    if type == 'file':
        path = sys.argv[0]
    elif type == 'path':
        path = os.path.dirname(sys.argv[0])
    else:
        path = '参数错误'
    return path


# 下载图片并储存
def download_img(img_url, file_name):
    print (img_url)
    r = requests.get(img_url)
    # print(r.status_code) # 返回状态码
    if r.status_code == 200:
        if not os.path.exists(path('path') + '\\img\\'):
            os.makedirs(path('path') + '\\img\\')
        open(path('path') + '\\img\\' + file_name, 'wb').write(r.content)
        print("下载完成，已放在" + path('path') + "\\img\\" +file_name)
    del r


def imgurl_api():
    url = 'https://api.btstu.cn/sjbz/api.php?lx=suiji&format=json'
    get = urllib.request.urlopen(url)
    result = json.loads(get.read())
    return result

# 程序本地信息配置
version = "1001"  # 定义本地程序版本号

# 检测系统更新，判断本地程序版本号与云端版本号，不一致则提示更新与更新内容
if version != check_info()['version']:
    print("更新内容：")
    print(check_info()['log'])  # 输出云端更新内容
    input("程序有更新请先更新，回车跳转更新")
    os.startfile(os.getcwd() + "\\Update For 爱唯逸工具箱.exe")

# 检测云端程序开放情况，如果云端返回的状态码不为open则程序提示未开放无法运行
elif check_info()['active'] == '1':
    # 系统自检
    if check_info()['code'] == '1':
        print("系统自检进行中...")
        print("本地版本号%s，云端版本号%s，版本号匹配" % (version, check_info()['version']))
        print("\n")
        while True:
            username = input("请输入在爱唯逸官网的账号:")
            password = input("请输入在爱唯逸官网的密码：")
            username = username.strip()
            password = password.strip()
            if username and password:
                if check_login(username, password)['code'] == 1:
                    info = user_info(username, password)
                    name = info['name']
                    money = info['money']
                    print("\n")
                    print(f"亲爱的{name}，恭喜您登录成功，您当前可用余额为：{money}元")
                    while True:
                        info = user_info(username, password)
                        token = info['token']
                        print("\n")
                        print("功能列表：")
                        print("1：调用云端发邮件")
                        print("2：爬取必应壁纸")
                        print("3：打开爱唯逸网络科技官网")
                        mode = input("请选择功能：")
                        if mode == '1':
                            while True:
                                print("\n")
                                mail = input("请输入收件人邮箱：")
                                title = input("请输入邮件标题：")
                                text = input("请输入邮件内容：")
                                if mail and title and text:
                                    if validators.email(mail):
                                        print(send_mail(token, mail, title, text))
                                        break
                                    else:
                                        print("收件人格式错误")
                                else:
                                    print("请确保信息填写完整")
                        elif mode == '2':
                            number = int(input("请输入需要下载的图片数量（可能会出现相同图片）："))
                            while number > 0:
                                imgurl = imgurl_api()['imgurl']
                                file_name = imgurl[-36:]
                                print(f"{number}：")
                                download_img(imgurl, file_name)
                                number = number - 1
                            print("\n")
                        elif mode == '3':
                            webbrowser.open('https://web.857xx.cn')
                            print("\n")
                        elif mode == '4':
                            url = 'web.857xx.cn'
                            status, result = sp.getstatusoutput("ping " + url + " -w 2000")
                            print(status)
                            print(result)
                            if "请求超时" in result:
                                print('hah')
                            print("\n")
                        else:
                            print("模式选择错误")
                elif check_login(username, password)['code'] == 0:
                    print(check_login(username, password)['msg'])
                else:
                    print("登录错误")
            else:
                print("账号或密码为空")
    else:
        print("云端返回数据错误")
else:
    print("当前程序未开放使用，请耐心等待开放")