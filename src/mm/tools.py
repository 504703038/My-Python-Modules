# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import requests
from bs4 import BeautifulSoup
# from . import downloader

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (\
                KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
}


def getFiles(path):
    """ 获取文件夹中的文件名称列表 """
    pic_names = os.listdir(path)
    return pic_names


def tree(path, deep=1, trans=False):
    """ 打印目录树 """
    path.replace('\\', '/')
    if deep == 1:
        print('|--' + path.split('/')[-1])
    for item in os.listdir(path):
        newPath = path + '/' + item
        # print(' |    ' * deep + ' - ' + item)
        if trans:
            item.replace('_', '\\_')
        print('|  ' * deep + '|--' + item)
        if os.path.isdir(newPath):
            tree(newPath, deep=deep + 1)


# def downloadFile(url, file_name=None, block_num=10):
#     """ 下载文件 """
#     if file_name is None:
#         mkdir('./Download')
#     downloader.downloaded_file(url, file_name, block_num)


def downloadFile(url, fileName, path, logs=False):
    """ 下载文件 """
    if logs:
        print('Start download "%s".' % fileName)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        res = requests.get(url, headers=headers)
        with open(path + '/' + fileName, 'wb') as file:
            file.write(res.content)
        if logs:
            print('"%s" is downloaded.' % fileName)
    except Exception as e:
        print('"%s" download filed.' % fileName)
        if logs:
            print(e)


def getHtml(url, encoding=None):
    """ 获取网页源码 """
    while (True):
        try:
            res = requests.get(url, timeout=3)
            if encoding is not None:
                res.encoding = encoding
            html = res.text
        except Exception:
            print('请求超时，重新连接')
            continue
        break
    return html


def getBeautifulSoup(url, encoding=None):
    """ 生成BeautifulSoup对象 """
    html = getHtml(url, encoding)
    soup = BeautifulSoup(html, 'html.parser')
    return soup
