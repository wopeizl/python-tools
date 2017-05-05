# !/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
import threading
import time
import traceback
import json
import base64
import httplib
import os
import sys
import socket
import struct

http_mode = False
# host = "dm-zyp-3.tb.dl.data.autohome.com.cn"
# port = 80
host = "127.0.0.1"
port = 12345
req_method = "flip"

class WorkManager(object):
    def __init__(self,thread_num=2, work_list=None):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_list)
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        初始化工作队列
    """
    def __init_work_queue(self, jobs_list):
        for j in jobs_list:
            if http_mode:
                self.add_job(do_http_job, j)
            else:
                self.add_job(do_tcp_job, j)

    """
        添加一项工作入队
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()#通知系统任务完成
            except:
                break

def getData(filename):
    fo = open(filename, 'rb')
    content = fo.read()
    output = base64.b64encode(content)
    fo.close()
    return output

#具体要做的任务
def do_http_job(args):
    filename = args[0]
    httpClient = None
    try:
        # body = urllib.urlencode({'method': 'flip', 'data': self.getData(filename) })
        body = json.dumps({'method': req_method, 'data': getData(filename)})
        headers = {"Content-type": "application/x-www-form-urlencoded"
            , "Accept": "text/plain"}

        httpClient = httplib.HTTPConnection(host, port, timeout=30)
        url = "http://" + host + ":" + str(port)
        httpClient.request("POST", url, body, headers)

        response = httpClient.getresponse()

        resjson = json.loads(response.read())
        if type(resjson) == dict:
            if resjson['status'] == 200:
                rd = base64.b64decode(resjson['data'])
                wf = open(os.path.splitext(filename)[0] + '_result.png', 'wb')
                wf.write(rd)
                wf.flush()
                wf.close()

    except Exception, e:
        print(traceback.format_exc())
    finally:
        if httpClient:
            httpClient.close()
    print threading.current_thread(), list(args)

#具体要做的任务
def do_tcp_job(args):
    filename = args[0]
    try:
        # size = os.path.getsize(filename)

        fo = open(filename, 'rb')
        content = fo.read()
        fo.close()

        import deep_pb2
        im = deep_pb2.input_m()
        im.imgdata = content
        im.method = deep_pb2.input_m.CV_FLIP
        im.dataT = deep_pb2.PNG

        address = (host, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.setblocking(1)

        sd = im.SerializeToString()
        sock.send(struct.pack('>I',len(sd)))
        sock.send(sd)

        r_size = sock.recv(4)
        r_len = struct.unpack('<I', r_size)[0]
        r_len = socket.ntohl(r_len)
        r_msg = sock.recv(r_len)
        # r_size = sock.recv(4)
        om = deep_pb2.output_m()
        om.ParseFromString(r_msg)
        # print(om.status())

        wf = open(os.path.splitext(filename)[0] + '_result.png', 'wb')
        wf.write(om.imgdata)
        wf.flush()
        wf.close()

    except Exception, e:
        print(traceback.format_exc())
    finally:
        sock.close()

    print threading.current_thread(), list(args)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : deep_client_mt.py thread_num pics_folder!")
        sys.exit(1)

    number = int(sys.argv[1])
    path = sys.argv[2]

    files = []
    try:
        for filename in os.listdir(path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                list.append(files, path + os.sep + filename)
    except Exception, e:
        print(traceback.format_exc())
        sys.exit(1)

    start = time.time()
    work_manager =  WorkManager(number, files)
    work_manager.wait_allcomplete()
    end = time.time()

    print "cost all time: %s" % (end-start)
