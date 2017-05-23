import sys
import numpy as np
import lmdb
import caffe
import argparse
from matplotlib import pyplot

def showLmdb(lmdbpath):
    # lmdbpath = 'you/lmdb/file/path'
    env = lmdb.open(lmdbpath, readonly=True)
    with env.begin() as txn:
        cursor = txn.cursor()
        for key, value in cursor:
            print 'key: ', key
            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(value)
            flat_x = np.fromstring(datum.data, dtype=np.uint8)
            x = flat_x.reshape(datum.channels, datum.height, datum.width)
            y = datum.label
            fig = pyplot.figure()
            pyplot.imshow(x, cmap='gray')


def saveLmdb2Img(lmdbpath, dst):
    env = lmdb.open(lmdbpath, readonly=True)
    with env.begin() as txn:
        cursor = txn.cursor()
        for key, value in cursor:
            # print 'key: ', key

            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(value)
            label = int(datum.label)
            image = caffe.io.datum_to_array(datum)
            image = image.astype(np.uint8)

            wf = open(dst + str(label) + '.png', 'wb')
            wf.write(image)
            wf.flush()
            wf.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage : readLmdb.py lmdb_dir dest_dir!")
        sys.exit(1)

    path = sys.argv[1]
    dst = sys.argv[2]

    saveLmdb2Img(path, dst)