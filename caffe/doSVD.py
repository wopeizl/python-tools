
import argparse
import numpy as np
import os, sys

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='do the svd opertion')
    parser.add_argument('--file', dest='file',
                        help='filen name',
                        default=None, type=str)
    parser.add_argument('--dimension', dest='dimension',
                        help='dimension',
                        default=None, type=int)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    LA = np.linalg

    rf = open(args.file,'rb')
    a = np.fromstring(rf.read(), dtype=np.float)
    a = np.array(a).reshape(args.dimension,len(a)/args.dimension)
    print('original matrix is : {}', a)
    rf.close()

    U, s, Vh = LA.svd(a, full_matrices=False)
    assert np.allclose(a, np.dot(U, np.dot(np.diag(s), Vh)))

    print('U is : {}' ,U)
    print('s is : {}' ,s)
    print('V is : {}' ,Vh)

    s[2:] = 0
    new_a = np.dot(U, np.dot(np.diag(s), Vh))
    print('recalculate the matrix as : {}' ,new_a)

if __name__ == '__main__':
    main()


