#!/usr/bin/env python

# --------------------------------------------------------
# extract the specified layer into a binary file
# --------------------------------------------------------


import caffe
import argparse
import numpy as np
import os, sys

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='extract caffe full connect layer data')
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the uncompressed network',
                        default=None, type=str)
    parser.add_argument('--net', dest='caffemodel',
                        help='weights',
                        default=None, type=str)
    parser.add_argument('--layer', dest='layer',
                        help='layer name',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # prototxt = 'models/VGG16/test.prototxt'
    # caffemodel = 'snapshots/vgg16_fast_rcnn_iter_40000.caffemodel'
    net = caffe.Net(args.prototxt, args.caffemodel, caffe.TEST)

    print('Uncompressed network {} : {}'.format(args.prototxt, args.caffemodel))

    out = os.path.splitext(os.path.basename(args.caffemodel))[0] + '_layer_' + args.layer + '.txt'
    # out_dir = os.path.dirname(args.caffemodel)
    out_dir = './'

    # Compress fc6
    if net.params.has_key(args.layer):

        # uncompressed weights and biases
        W_fc6 = net.params[args.layer][0].data
        B_fc6 = net.params[args.layer][1].data

        flat_x = np.fromstring(W_fc6, dtype=np.float)

        print(flat_x)

        filename = '{}/{}'.format(out_dir, out)
        wf = open(filename, 'wb')
        wf.write(flat_x)
        wf.flush()
        wf.close()

        # rf = open(filename,'rb')
        # read_x = np.fromstring(rf.read(), dtype=np.float)
        # print(read_x)
        # rf.close()

        print 'Wrote layer to: {:s}'.format(filename)

if __name__ == '__main__':
    main()
