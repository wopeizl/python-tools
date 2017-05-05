

#codng=utf8

import httplib, urllib
import requests
import thread,time
import os
import json
import base64
import traceback
import sys

class wrapper:

    def __init__(self):
        pass

    def getData(self, filename):
        fo = open(filename, 'rb')
        content = fo.read()
        output = base64.b64encode(content)
        fo.close()
        return output

    def process(self, filename) :
        httpClient = None
        try:
            # body = urllib.urlencode({'method': 'flip', 'data': self.getData(filename) })
            body = json.dumps({'method': 'flip', 'data': self.getData(filename) })
            headers = {"Content-type": "application/x-www-form-urlencoded"
                , "Accept": "text/plain"}

            httpClient = httplib.HTTPConnection("127.0.0.1", 12345, timeout=30)
            url = "http://127.0.0.1:12345/"
            httpClient.request("POST", url, body, headers)

            response = httpClient.getresponse()
            #      print response.status
      #      print response.reason
      #       print response.read()
      #      print response.getheaders()
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

    def processbyrequest(self, filename) :
        url = 'http://127.0.0.1:12345/'
        body = json.dumps({'method': 'flip', 'data': self.getData(filename)})
        r = requests.post(url, None, {'method': 'flip', 'data': self.getData(filename)})
        print(r.json())

def threadproc(path):
    w = wrapper()
    while 1:
       # w.process(path)
        w.processbyrequest(path)

if __name__ =="__main__":
    path = sys.argv[1:]
    if len(path) == 0:
        path = 'C:\Users\Public\Pictures\Sample Pictures'
    else:
        path = path[0]

    try:
        # for k in range(1):
        #     thread.start_new_thread(threadproc(path), None)
        w = wrapper()
        for filename in os.listdir(path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # w.processbyrequest(path + os.sep + filename)
                w.process(path + os.sep + filename)
                continue
            else:
                continue
    except:
        print(traceback.format_exc())


