
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
import matplotlib.pyplot as plt
import matplotlib as mpl

http_mode = True
http_host = "dm-zyp-3.tb.dl.data.autohome.com.cn"
http_port = 80
tcp_host = "dm-zyp-3.service.dl.data.autohome.com.cn"
tcp_port = 80
# http_host = "127.0.0.1"
# http_port = 12345
skip_frames = 1
wait_time = 1 #s
req_method = "caffe"
req_dataT = deep_pb2.PNG
# need_res_dataT = deep_pb2.CV_POST_PNG
need_res_dataT = deep_pb2.FRCNN_RESULT

class WorkManager(object):
    def __init__(self,thread_num=2, work_list=None):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_list)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    def __init_work_queue(self, jobs_list):
        for j in jobs_list:
            self.add_job(deep_http_convert, j)

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                self.work_queue.task_done()
            except:
                break

def deep_http_convert(paras, frame_count):
    capture = cv2.VideoCapture(paras)

    success, frame = capture.read()
    count = 0
    all_whole_time = 0
    all_prepare_time = 0
    all_preprocess_time = 0
    all_predict_time = 0
    all_postprocess_time = 0
    all_jsonparse_time = 0
    all_decode_time = 0
    all_cvreadimage_time = 0
    all_writeresult_time = 0

    while success and count < frame_count:
        try:
            start = time.time()
            isok, i_data = cv2.imencode('.PNG', frame)
            data = base64.b64encode(i_data)
            body = json.dumps({'method': req_method, 'data': data, 'callback': 0, 'res_dataT': need_res_dataT})
            headers = {"Content-type": "application/x-www-form-urlencoded"
                , "Accept": "text/plain", 'Connection': 'close'}

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
                          + " whole time : " + str(resjson["whole_time"])
                          + ", predict time : " + str(resjson["predict_time"])
                          + ", prepare time : " + str(resjson["prepare_time"])
                          + ", preprocess time : " + str(resjson["preprocess_time"])
                          + ", postprocess time : " + str(resjson["postprocess_time"])
                          )
                    all_whole_time += resjson["whole_time"]
                    all_prepare_time += resjson["prepare_time"]
                    all_preprocess_time += resjson["preprocess_time"]
                    all_predict_time += resjson["predict_time"]
                    all_postprocess_time += resjson["postprocess_time"]
                    all_jsonparse_time += resjson["jsonparse_time"]
                    all_decode_time += resjson["decode_time"]
                    all_cvreadimage_time += resjson["cvreadimage_time"]
                    all_writeresult_time += resjson["writeresult_time"]
                    count += 1

            end = time.time()
            success, frame = capture.read()
        except:
            print(traceback.format_exc())

    return count, all_whole_time, all_prepare_time, all_preprocess_time, all_predict_time, all_postprocess_time ,all_jsonparse_time, all_decode_time, all_cvreadimage_time, all_writeresult_time

def draw_bar(labels,quants):
    width = 1.4
    ind = np.linspace(0.5,9.5,len(quants))
    # make a square figure
    fig = plt.figure(num=None, figsize=(8, 6), dpi=110, facecolor='w', edgecolor='k')
    ax  = fig.add_subplot(111)
    # Bar Plot
    ax.bar(ind,quants,width,color='green')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    # labels
    ax.set_xlabel('pipeline stage')
    ax.set_ylabel('Cost time (ms)')

    n = len(quants)
    X = np.arange(n)

    for x, y in zip(X, quants):
        plt.text(ind[x] , y + 0.05, '%.2f' % y, ha='center', va='bottom')

    # for i in range(len(quants)):
    #     plt.annotate(str(quants[i]), xy=(100 * i, int(quants[i])), xycoords='data', xytext=(100 * i, int(quants[i])),
    #                  arrowprops=dict(facecolor='black', shrink=0.05),
    #                  )
    # title
    ax.set_title('deep_server statistics for ' + req_method, bbox={'facecolor':'0.9', 'pad':5})
    plt.grid(True)
    plt.savefig(req_method + '.png')

def draw_bar2(labels,quants):
    plt.figure(figsize=(9, 6))
    n = len(quants)
    X = np.arange(n)

    Y1 = np.random.uniform(0.5, 1.0, n)
    # Y2 = np.random.uniform(0.5, 1.0, n)
    plt.bar(X, Y1, width=0.35, facecolor='lightskyblue', edgecolor='white')

    # plt.bar(X + 0.35, Y2, width=0.35, facecolor='yellowgreen', edgecolor='white')
    fig = plt.figure(1)
    ax  = fig.add_subplot(111)
    ax.set_xticklabels(labels)
    ax.set_xlabel('pipeline stage')
    ax.set_ylabel('Cost time (ms)')
    ax.set_title('deep_server statistics for ' + req_method, bbox={'facecolor':'0.8', 'pad':5})

    for x, y in zip(X, Y1):
        plt.text(x , y + 0.05, '%.2f' % y, ha='center', va='bottom')

    # for x, y in zip(X, Y2):
    #     plt.text(x + 0.6, y + 0.05, '%.2f' % y, ha='center', va='bottom')
    plt.ylim(0, +1.25)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : cvCapture.py movie_file frame_count!")
        sys.exit(1)

    path = sys.argv[1]
    frame_count = sys.argv[2]

    labels = ['whole_time', 'jsonparse_time', 'cvreadimage_time', 'predict_time', 'writeresult_time']
    count, all_whole_time, all_prepare_time, all_preprocess_time, all_predict_time, all_postprocess_time \
        , all_jsonparse_time, all_decode_time, all_cvreadimage_time, all_writeresult_time \
        = deep_http_convert(path, int(frame_count))
    quants = [all_whole_time / count,all_jsonparse_time / count,all_cvreadimage_time / count,all_predict_time / count,all_writeresult_time / count ]

    draw_bar(labels, quants)
    plt.show()
