
import cv2
import xml.etree.ElementTree as ET
import numpy as np

def test():
    # e = cv2.load(filename)
    # print(e)
    fs = cv2.FileStorage(filename,cv2.FileStorage_FORMAT_XML)
    # print(fs.root(1).value)
    # print(fs.root(0)["data"])
    # mapping = cv2.construct_mapping(fs.root(0), deep=True)
    print(fs.root(0).name)
    # for elem in fs.root(0):
    print(fs.root(0))
    # print(fs.root(0).isMap())
    fs.release()


if __name__ == '__main__':
    filename = r'c:\Opencv-3.1.0\opencv\sources\samples\data\data01.xml'
    tree = ET.ElementTree(file=filename)
    data_data = []
    for elem in tree.iter(tag='datamat'):
        data_rows = int(elem[0].text)
        data_cols = int(elem[1].text)
        data_dt = elem[2].text
        ll = elem[3].text.split('\n')
        for i in ll:
            list.append(data_data, i.split(' '))
        print(data_data)
        # data_data = np.array(elem[3].text)
        break
    for elem in tree.iter(tag='labelsmat'):
        label_rows = int(elem[0].text)
        label_cols = int(elem[1].text)
        label_dt = elem[2].text
        label_data = np.array(elem[3].text)
        # data.reshape(rows,cols)
        break
    # print(len(label_data.tolist()))
    # data_data.reshape(len(label_data.tolist()),data_rows,data_cols)
    # print(data_data)
    # print(label_data.tolist())
    # print(label_data.arange.reshape((3, 2)))
    # help(label_data)
    # print(type(label_data).shape)
    lr = cv2.ml.LogisticRegression_create()
    lr.train(data_data, 0, label_data)

