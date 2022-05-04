# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/2 20:30
# @Author : 爱唯逸网络科技
# @Email : support@857xx.cn
# @File : Update For 爱唯逸工具箱.py
# @Project: 爱唯逸工具箱.py

import urllib.request  # 爬取网页资源与信息
import json  # 解析或加密Json信息
import requests  # 获取当前文件路径
import os
import os.path as op
from sys import stdout

def downloadfile(url, filename):
    filename = filename  + op.splitext(url)[-1]
    file_to_save = op.join(os.getcwd(), filename)  #获取当前路径
    print(file_to_save)

    response = requests.get(url, stream=True)
    with open(file_to_save, "wb") as f:
        f.write(response.content)
        filesize = response.headers["Content-Length"]
        chunk_size = 128
        times = int(filesize) // chunk_size
        show = 1 / times
        show2 = 1 / times
        start = 1

        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
            if start <= times:
                stdout.write(f"下载进度: {show:.2%}\n")
                start += 1
                show += show2
            else:
                stdout.write("下载进度: 100%")
        print("\n结束下载")


if __name__ == "__main__":
    site = 'https://web.857xx.cn/api/app/aiweiyi.php'
    act = '?act=check_info'
    api = site + act
    get = urllib.request.urlopen(api)
    result = json.loads(get.read())
    download = result['download']
    print(download)
    downloadfile(download, "爱唯逸工具箱")

input("回车退出")
os.startfile(os.getcwd() + "\\爱唯逸工具箱.exe")
