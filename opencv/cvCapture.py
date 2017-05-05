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
import numpy as np

http_mode = True
host = "dm-zyp-3.tb.dl.data.autohome.com.cn"
port = 80
req_method = "caffe"

def avi2mp4(input, output):

    # 获得视频的格式
    videoCapture = cv2.VideoCapture(input)

    # 获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 指定写视频的格式, I420-avi, MJPG-mp4
    videoWriter = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('m','p','4','v'), fps, size)
    # videoWriter = cv2.VideoWriter(output, -1, fps, size)

        # 读帧
    success, frame = videoCapture.read()

    while success:
        # cv2.imshow("Oto Video", frame)  # 显示
        cv2.waitKey(1000 / int(fps))  # 延迟
        videoWriter.write(frame)  # 写视频帧
        success, frame = videoCapture.read()  # 获取下一帧


def image2video(inputs, output):
    cv2.merge(inputs, output)

    fps = 24
    size = (100,100)
    # videoWriter = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    videoWriter = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    videoWriter.write(output)  # 写视频帧

def playvideo(input, callback):
    win_name = "test"

    # 获得视频的格式
    capture = cv2.VideoCapture(input)
    # 获得码率及尺寸
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)

    success, frame = capture.read()
    frame_time = 1000 / int(fps)

    while success:
        try:
            start = time.time()
            if callback != None :
                rawImage = callback(frame)
                npImage = np.fromstring(rawImage, np.uint8)
                frame = cv2.imdecode(npImage, 1)
            cv2.imshow(win_name, frame)  # 显示
            end = time.time()
            leave_time = frame_time - (end * 1000 - start * 1000)
            if leave_time < 0 :
                leave_time = 1
            # cv2.ShowImage(win_name, frame)
            c = cv2.waitKey(leave_time)  # 延迟
            # c = cv2.waitKey(33)
            if c == 27:
                break
            success, frame = capture.read()  # 获取下一帧
        except Exception, e:
            print(traceback.format_exc())
            sys.exit(1)

    cv2.destroyWindow(win_name)

def deep_http_convert(frame):
    httpClient = None
    try:
        # body = urllib.urlencode({'method': 'flip', 'data': self.getData(filename) })
        # data = base64.b64encode(frame)
        isok, i_data = cv2.imencode('.PNG', frame)
        data = base64.b64encode(i_data)
        body = json.dumps({'method': req_method, 'data': data})
        headers = {"Content-type": "application/x-www-form-urlencoded"
            , "Accept": "text/plain"}

        httpClient = httplib.HTTPConnection(host, port, timeout=30)
        url = "http://" + host + ":" + str(port)
        httpClient.request("POST", url, body, headers)

        response = httpClient.getresponse()

        resjson = json.loads(response.read())
        if type(resjson) == dict:
            if resjson['status'] == 200:
                resFrame = base64.b64decode(resjson['data'])
                return resFrame

    except Exception, e:
        print(traceback.format_exc())
    finally:
        if httpClient:
            httpClient.close()

def deep_tcp_convert(frame):
    httpClient = None
    try:
        # body = urllib.urlencode({'method': 'flip', 'data': self.getData(filename) })
        data = output = base64.b64encode(frame)
        body = json.dumps({'method': 'caffe', 'data': data})
        headers = {"Content-type": "application/x-www-form-urlencoded"
            , "Accept": "text/plain"}

        httpClient = httplib.HTTPConnection("127.0.0.1", 12345, timeout=30)
        url = "http://127.0.0.1:12345/"
        httpClient.request("POST", url, body, headers)

        response = httpClient.getresponse()

        resjson = json.loads(response.read())
        if type(resjson) == dict:
            if resjson['status'] == 200:
                resFrame = base64.b64decode(resjson['data'])
                return resFrame

    except Exception, e:
        print(traceback.format_exc())
    finally:
        if httpClient:
            httpClient.close()

if __name__ == '__main__':
    # avi2mp4("C:/Users/Administrator/Videos/2.avi",
    #         "C:/Users/Administrator/Videos/test.mpg")
    if len(sys.argv) < 1:
        print("usage : cvCapture.py movie_file!")
        sys.exit(1)

    path = sys.argv[1]

    playvideo(path, deep_http_convert)
