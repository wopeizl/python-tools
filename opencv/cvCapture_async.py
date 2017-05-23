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
import deep_pb2

http_mode = True
save_mpg = False
http_host = "dm-zyp-3.tb.dl.data.autohome.com.cn"
http_port = 80
tcp_host = "10.22.245.0"
tcp_port = 30005
# http_host = "127.0.0.1"
# http_port = 12345
skip_frames = 1
wait_time = 1 #s
req_method = "caffe"
req_dataT = deep_pb2.PNG
# need_res_dataT = deep_pb2.CV_POST_PNG
need_res_dataT = deep_pb2.FRCNN_RESULT

class WorkManager(object):
    def __init__(self,thread_num=1, work_list=None):
        self.push_finish = False
        self.decode_finish = False
        self.frame_index = 0
        self.alive = True
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

        while self.alive:
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
        try_count = 0
        try_thres = 5
        if save_mpg:
            videoWriter = cv2.VideoWriter("./output.mpg", cv2.VideoWriter_fourcc('m','p','4','v'), self.fps, self.size)

        while self.alive:
            try:
                if self.return_dict.has_key(self.frame_index):
                    start = time.time()
                    frame = self.return_dict.get(self.frame_index)
                    cv2.imshow(win_name, frame)  # 显示
                    self.return_dict[self.frame_index] = None
                    self.frame_index += 1
                    try_count = 0
                    if save_mpg:
                        videoWriter.write(frame)  # 写视频帧

                end = time.time()
                leave_time = self.frame_time - (end * 1000 - start * 1000)
                if leave_time <= 0.0:
                    leave_time = 1
                # print(leave_time)
                c = cv2.waitKey(int(leave_time))  # 延迟
                if c == 27:
                    self.push_finish = True
                    self.decode_finish = True
                    self.alive = False
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
                    self.frame_index += 1 # skip this frame
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
            body = json.dumps({'method': req_method, 'data': data, 'callback': callback, 'res_dataT' : need_res_dataT})
            headers = {"Content-type": "application/x-www-form-urlencoded"
                , "Accept": "text/plain", 'Connection':'close'}

            httpClient = httplib.HTTPConnection(http_host, http_port, timeout=30)
            url = "http://" + http_host + ":" + str(http_port)

            start = time.time()
            httpClient.request("POST", url, body, headers)
            response = httpClient.getresponse()
            end = time.time()
            # print "server response cost time: %s" % (end - start)

            resjson = json.loads(response.read())
            if type(resjson) == dict:
                if resjson['status'] == 200:
                    print("process " + req_method
                          + " width : " + str(resjson["width"])
                          + ", height : " + str(resjson["height"])
                          + ", channel : " + str(resjson["channel"])
                          + ", whole time : " + str(resjson["whole_time"])
                          + ", predict time : " + str(resjson["predict_time"])
                          + ", prepare time : " + str(resjson["prepare_time"])
                          + ", preprocess time : " + str(resjson["preprocess_time"])
                          + ", postprocess time : " + str(resjson["postprocess_time"])
                          )
                    resFrame = None

                    res_dataT = resjson["dataT"]

                    if res_dataT == deep_pb2.CV_POST_PNG:
                        resFrame = base64.b64decode(resjson['data'])
                        npImage = np.fromstring(resFrame, np.uint8)
                        resFrame = cv2.imdecode(npImage, 1)
                    elif res_dataT == deep_pb2.CV_POST_IMAGE:
                        resFrame = resjson['data'].tobytes()
                    elif res_dataT == deep_pb2.FRCNN_RESULT:
                        caffe_result = resjson["caffe_result"]
                        for i in range(len(caffe_result)):
                            cc = caffe_result[i]
                            text = str(cc["score"])
                            x = int(cc["x"])
                            y = int(cc["y"])
                            w = int(cc["w"])
                            h = int(cc["h"])
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            resFrame = cv2.putText(frame, text, (x,y), font, 0.6,(255,0,0), 1,cv2.LINE_AA)
                            resFrame = cv2.rectangle(resFrame, (x, y), (w,h), (0, 0, 255), 2)
                    elif res_dataT == deep_pb2.YOLO_RESULT:
                        resFrame = frame
                    return resFrame, resjson['callback']

        except:
            print(traceback.format_exc())
        finally:
            if httpClient:
                httpClient.close()

    def deep_tcp_convert(self, paras):
        frame = paras[0]
        index = paras[1]
        try:
            im = deep_pb2.input_m()
            im.callback = str(index)
            im.dataT = req_dataT
            if req_dataT == deep_pb2.PNG:
                isok, i_data = cv2.imencode('.PNG', frame)
                if isok:
                    npImage = np.fromstring(i_data, np.uint8)
                    im.imgdata = npImage.tobytes()
                else:
                    im.imgdata = frame.tobytes()
                    im.dataT = deep_pb2.CV_IMAGE

            if req_method == "yolo":
                im.method = deep_pb2.input_m.YOLO
            elif req_method == "caffe":
                im.method = deep_pb2.input_m.CAFFE
            else:
                im.method = deep_pb2.input_m.CV_FLIP

            im.res_dataT = need_res_dataT

            address = (tcp_host, tcp_port)
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

            res_dataT = om.dataT

            resFrame = None
            if res_dataT == deep_pb2.CV_POST_PNG:
                npImage = np.fromstring(om.imgdata, np.uint8)
                resFrame = cv2.imdecode(npImage, 1)
            elif res_dataT == deep_pb2.CV_POST_IMG:
                resFrame = np.fromstring(om.imgdata, np.uint8)
            elif res_dataT == deep_pb2.FRCNN_RESULT:
                resFrame = frame
            elif res_dataT == deep_pb2.YOLO_RESULT:
                resFrame = frame

            return resFrame, om.callback

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
        self.manager.fps = capture.get(cv2.CAP_PROP_FPS)
        self.manager.size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        success, frame = capture.read()
        self.manager.frame_time = 1000 / int(self.manager.fps)
        index = 0

        while success and self.manager.alive:
            try:
                start = time.time()
                if http_mode:
                    self.manager.add_job(self.manager.deep_http_convert, frame, index)
                else:
                    self.manager.add_job(self.manager.deep_tcp_convert, frame, index)
                index += 1

                while index - self.manager.frame_index >= 100 and self.manager.alive:
                    # too much frames in stack, wait for a while
                    time.sleep(0.05)

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
        while self.manager.alive:
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

                    while int(callback) - self.manager.frame_index >= 100 and self.manager.alive:
                        #too much frames in stack, wait for a while
                        time.sleep(0.05)

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
        print("usage : cvCapture_async.py movie_file!")
        sys.exit(1)

    path = sys.argv[1]

    start = time.time()
    work_manager =  WorkManager(5, path)
    #cv2.waitKey(1000 * wait_time)  # 延迟
    work_manager.playvideo_dict()
    work_manager.wait_allcomplete()
    end = time.time()

    print "cost all time: %s" % (end-start)

