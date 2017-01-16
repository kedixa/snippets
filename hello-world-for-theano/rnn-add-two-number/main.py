#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import theano
import theano.tensor as T
from RNN import RNN

"""
Training a net that can compute a + b.
"""

MAX_LEN = 8

def get_int(x):
    """
    Get an random integer in [0, x)
    """
    return np.random.randint(0, x)

def int2bin(x):
    """
    Convert a integer to binary.
    """
    k = list(bin(x)[2:])
    k = ['0'] * (MAX_LEN - len(k)) + k
    return [float(i) for i in k][::-1]

def get_data():
    """
    Get a random train data.
    """
    mmax = 2**(MAX_LEN - 2) - 1
    a, b = get_int(mmax), get_int(mmax)
    x = [[x1, x2] for x1,x2 in zip(int2bin(a), int2bin(b))]
    y = [[y1] for y1 in int2bin(a+b)]
    return (a, b), (x, y)

def train_and_test():
    train_times = 20000
    test_times = 10000
    n_in, n_hid, n_out = 2, 4, 1
    rnn = RNN(n_in, n_hid, n_out, learn_rate = 0.2)
    print "training ... "

    for i in range(train_times):
        (a,b),(x,y)=get_data()
        rnn.train(np.zeros(n_hid), x, y)
        pass
    print "done."
    print "compute..."

    right = 0
    for i in range(test_times):
        (a, b), (x, y) = get_data()
        z = [0 if k < 0.5 else 1 for k in rnn.predict(np.zeros(n_hid), x)]
        c = 0
        for k in z[::-1]:
            c = c * 2
            c = c + k
        right = right + (a+b==c)
        pass
    print right, '/', test_times

    return True

if __name__ == '__main__':
    train_and_test()
    pass
