# -*- coding: utf-8 -*-

import cv2
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
import numpy as np

http_mode = True
host = "dm-zyp-3.tb.dl.data.autohome.com.cn"
port = 80
# host = "127.0.0.1"
# port = 12345
skip_frames = 1
req_method = "caffe"
wait_time = 1 #s

class WorkManager(object):
    def __init__(self,thread_num=1, work_list=None):
        self.push_finish = False
        self.decode_finish = False
        self.work_list = work_list
        self.work_queue = Queue.Queue()
        self.return_queue = Queue.Queue()
        self.return_dict = {}
        self.frame_time = 25
        self.threads = []
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        self.threads.append(Work_decodevideo(self))
        for i in range(thread_num):
            self.threads.append(Work(self))

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#任务入队，Queue内部实现了同步机制

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

    def playvideo(self):
        win_name = "test"

        cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
        start = time.time()

        while not self.decode_finish or not self.push_finish or not self.return_queue.empty():
            try:
                if not self.return_queue.empty():
                    start = time.time()
                    frame = self.return_queue.get(block=False)
                    cv2.imshow(win_name, frame)  # 显示

                end = time.time()
                leave_time = self.frame_time - (end * 1000 - start * 1000)
                if leave_time < 0:
                    leave_time = 1
                c = cv2.waitKey(int(leave_time))  # 延迟
                if c == 27:
                    self.push_finish = True
                    self.decode_finish = True
                    while not self.work_queue.empty():
                        self.work_queue.get(block=False)
                    while not self.return_queue.empty():
                        self.return_queue.get(block=False)
                    break
            except:
                print(traceback.format_exc())

        cv2.destroyWindow(win_name)

    def playvideo_dict(self):
        win_name = "test"

        cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
        start = time.time()
        frame_index = 0
        try_count = 0
        try_thres = 5

        while True:
            try:
                if self.return_dict.has_key(frame_index):
                    start = time.time()
                    frame = self.return_dict.get(frame_index)
                    cv2.imshow(win_name, frame)  # 显示
                    self.return_dict[frame_index] = None
                    frame_index += 1
                    try_count = 0

                end = time.time()
                leave_time = self.frame_time - (end * 1000 - start * 1000)
                if leave_time <= 0.0:
                    leave_time = 1
                # print(leave_time)
                c = cv2.waitKey(int(leave_time))  # 延迟
                if c == 27:
                    self.push_finish = True
                    self.decode_finish = True
                    while not self.work_queue.empty():
                        self.work_queue.get(block=False)
                    while not self.return_queue.empty():
                        self.return_queue.get(block=False)
                    break
            except:
                try_count += 1
                print(traceback.format_exc())
                if try_count >= try_thres:
                    try_count = 0
                    frame_index += 1 # skip this frame
                    print("one frame is lost, skip it!")

        cv2.destroyWindow(win_name)

    def deep_http_convert(self, paras):
        httpClient = None
        frame = paras[0]
        callback = paras[1]
        # print( int(callback) + 100000)
        try:
            # body = urllib.urlencode({'method': 'flip', 'data': self.getData(filename) })
            # data = base64.b64encode(frame)
            isok, i_data = cv2.imencode('.PNG', frame)
            data = base64.b64encode(i_data)
            body = json.dumps({'method': req_method, 'data': data, 'callback': callback})
            headers = {"Content-type": "application/x-www-form-urlencoded"
                , "Accept": "text/plain", 'Connection':'close'}

            httpClient = httplib.HTTPConnection(host, port, timeout=30)
            url = "http://" + host + ":" + str(port)
            httpClient.request("POST", url, body, headers)

            response = httpClient.getresponse()

            resjson = json.loads(response.read())
            if type(resjson) == dict:
                if resjson['status'] == 200:
                    resFrame = base64.b64decode(resjson['data'])
                    npImage = np.fromstring(resFrame, np.uint8)
                    frame = cv2.imdecode(npImage, 1)
                    return frame, resjson['callback']

        except:
            print(traceback.format_exc())
        finally:
            if httpClient:
                httpClient.close()

    def deep_tcp_convert(self, paras):
        frame = paras[0]
        index = paras[1]
        try:
            import deep_pb2
            im = deep_pb2.input_m()
            im.callback = str(index)
            isok, i_data = cv2.imencode('.PNG', frame)
            if isok:
                npImage = np.fromstring(i_data, np.uint8)
                im.imgdata = npImage.tobytes()
                im.dataT = deep_pb2.PNG
            else:
                im.imgdata = frame.tobytes()
                im.dataT = deep_pb2.CV_IMAGE
            if req_method == "yolo":
                im.method = deep_pb2.input_m.YOLO
            elif req_method == "caffe":
                im.method = deep_pb2.input_m.CAFFE
            else:
                im.method = deep_pb2.input_m.CV_FLIP

            im.res_dataT = deep_pb2.CV_POST_PNG

            address = (host, port)
            lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lsock.connect(address)
            lsock.setblocking(1)

            sd = im.SerializeToString()
            # sd = socket.htonl(len(sd))
            lsock.send(struct.pack('>I', len(sd)))
            lsock.send(sd)

            r_size = lsock.recv(4)
            r_len = struct.unpack('<I', r_size)[0]
            r_len = socket.ntohl(r_len)
            buffer = ""
            while True:
                # r_msg = lsock.recv(r_len)
                buffer += lsock.recv(1024)
                if not buffer:
                    break
                if len(buffer) >= r_len:
                    break
            om = deep_pb2.output_m()
            om.ParseFromString(buffer[0:r_len])

            npImage = np.fromstring(om.imgdata, np.uint8)
            frame = cv2.imdecode(npImage, 1)
            return frame, om.callback

        except:
            print(traceback.format_exc())
        finally:
            # lsock.close()
            pass

class Work_decodevideo(threading.Thread):
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.manager = manager
        self.start()

    def run(self):
        # 获得视频的格式
        capture = cv2.VideoCapture(self.manager.work_list)
        # 获得码率及尺寸
        self.fps = capture.get(cv2.CAP_PROP_FPS)
        self.size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        success, frame = capture.read()
        self.manager.frame_time = 1000 / int(self.fps)
        index = 0

        while success:
            try:
                start = time.time()
                if http_mode:
                    self.manager.add_job(self.manager.deep_http_convert, frame, index)
                else:
                    self.manager.add_job(self.manager.deep_tcp_convert, frame, index)
                index += 1
                end = time.time()
                success, frame = capture.read()  # 获取下一帧
            except:
                print(traceback.format_exc())
                self.manager.push_finish = True

        self.manager.push_finish = True

class Work(threading.Thread):
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.manager = manager
        self.start()

    def run(self):
        skip_count = 0

        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                callback = '0'
                if not self.manager.work_queue.empty():
                    do, args = self.manager.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                    if skip_count >= skip_frames:
                        frame,callback = do(args)
                        skip_count = 0
                    else:
                        frame,callback = args[0], args[1]
                    skip_count += 1
                    # self.manager.return_queue.put(frame)  # 任务入队，Queue内部实现了同步机制
                    self.manager.return_dict[int(callback)] = frame
                    # self.manager.work_queue.task_done()#通知系统任务完成

                if self.manager.push_finish and self.manager.work_queue.empty() :
                    self.manager.decode_finish = True
                    break
            except:
                # print(traceback.format_exc())
                # self.manager.decode_finish = True
                # break
                pass

if __name__ == '__main__':
    # avi2mp4("C:/Users/Administrator/Videos/2.avi",
    #         "C:/Users/Administrator/Videos/test.mpg")
    if len(sys.argv) < 1:
        print("usage : cvCapture.py movie_file!")
        sys.exit(1)

    path = sys.argv[1]

    start = time.time()
    work_manager =  WorkManager(5, path)
    #cv2.waitKey(1000 * wait_time)  # 延迟
    work_manager.playvideo_dict()
    work_manager.wait_allcomplete()
    end = time.time()

    print "cost all time: %s" % (end-start)

