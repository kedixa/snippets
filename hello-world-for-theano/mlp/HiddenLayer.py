#!/usr/bin/python

import numpy as np
import theano
import theano.tensor as T
class HiddenLayer(object):
    def __init__(self, rng, input, n_in, n_out):
        self.input = input
        w = np.asarray(
                rng.uniform(low=-0.2,high=0.2,size=(n_in,n_out)),
                dtype=theano.config.floatX)
        self.W = theano.shared(w)
        self.b = theano.shared(np.zeros((n_out,)))
        self.output = T.nnet.sigmoid(T.dot(input,self.W)+self.b)
        self.params = [self.W, self.b]
