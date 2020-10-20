import os
import sys
import time
from urllib import request
from multiprocessing import Process, Manager


class DownloadProcess(Process):
    def __init__(self, process_name, url, file_name, ranges, progress):
        super().__init__()
        # 进程名
        self.name = process_name
        # 下载地址
        self.url = url
        # 文件名
        self.file_name = file_name
        # 下载块范围
        self.ranges = ranges
        # 下载进度
        self.progress = progress
        # 已下载大小
        self.downloaded = 0

    def run(self):
        """ 运行进程 """
        try:
            self.downloaded = os.path.getsize(self.file_name)
        except FileNotFoundError:
            self.downloaded = 0
        # 开始下载的位置，接着上次继续下载
        self.start_point = self.ranges[0] + self.downloaded
        # 判断文件是否已经下载完成
        if self.downloaded >= self.ranges[1]:
            print('%s has been downloaded over.' % self.name)
            return
        # 开始下载
        # 一次写入的大小
        self.one_time_size = 16384  # 16kb
        #
        headers = {'Range': 'bytes=%d-%d' % (self.start_point, self.ranges[1])}
        req = request.Request(self.url, headers=headers)
        urlHandler = request.urlopen(req)
        data = urlHandler.read(self.one_time_size)
        while data:
            with open(self.file_name, 'ab+') as file:
                file.write(data)
            self.downloaded += len(data)
            self.progress[self.name] = self.downloaded
            data = urlHandler.read(self.one_time_size)


def getFileInfo(url):
    """ 获取文件信息 """
    # 获取响应头
    urlHandler = request.urlopen(url)
    headers = urlHandler.headers
    # 初始化文件信息
    file_name = './Download/' + url.split('/')[-1]
    file_size = 0
    # 遍历响应头获取文件信息
    for key in headers:
        if key.find('Length') != -1:
            file_size = headers[key]
            file_size = int(file_size)
        elif key.find('name') != -1:
            file_name = headers[key]
    info = {}
    info['file_name'] = file_name
    info['file_size'] = file_size
    return info


def splitBlocks(file_size, block_num):
    """ 将文件划分多个块，计算每个块的范围 """
    block_size = file_size / block_num
    ranges = []
    for i in range(block_num):
        start = i * block_size
        end = start + block_size - 1
        if i == block_num - 1:
            end = file_size - 1
        ranges.append((start, end))
    return ranges


def isLive(processes):
    for task in processes:
        if task.is_alive():
            return True
    return False


def downloadedFile(url, file_name=None, block_num=1):
    """ 下载文件 """
    print('获取文件信息')
    # 文件信息
    info = getFileInfo(url)
    if file_name is None:
        file_name = info['file_name']
        file_size = info['file_size']
    else:
        file_size = info['file_size']
    # 文件分块
    ranges = splitBlocks(file_size, block_num)
    # 进程名称，临时文件名称
    process_name = ['process_%d' % i for i in range(block_num)]
    tmpfile_name = [file_name + '.tmp_%d' % i for i in range(block_num)]
    # 创建进程
    print('创建进程，开始下载')
    with Manager() as manager:
        # 给进程的下载进度(数据交互)
        progress = manager.dict()
        process_list = []
        for i in range(block_num):
            task = DownloadProcess(process_name[i], url, tmpfile_name[i],
                                   ranges[i], progress)
            task.start()
            process_list.append(task)
        time.sleep(2)
        while isLive(process_list):
            downloaded = 0
            for i in range(block_num):
                downloaded += progress[process_name[i]]
            downloaded = downloaded / file_size * 100
            tips = u'\rCompleted: %.2f%%' % downloaded
            sys.stdout.write(tips)
            sys.stdout.flush()
            time.sleep(0.5)
    with open(file_name, 'wb+') as file:
        for tmp_file in tmpfile_name:
            with open(tmp_file, 'rb') as f:
                file.write(f.read())
            try:
                os.remove(tmp_file)
            except OSError:
                pass
    print('\n已下载到: %s' % os.path.abspath(file_name))
