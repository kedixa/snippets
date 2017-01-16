#!/usr/bin/python

import numpy as np
import theano
import theano.tensor as T

class OutputLayer(object):
    def __init__(self, rng, input, n_in, n_out):
        self.input = input
        w = np.asarray(
                rng.uniform(low=-0.2,high=0.2,size=(n_in,n_out)))
        self.W = theano.shared(w)
        self.b = theano.shared(np.zeros((n_out,)))
        self.output = T.nnet.sigmoid(T.dot(input, self.W)+self.b)
        self.y_pred = T.argmax(self.output, axis = 1)
        self.params = [self.W, self.b]
        pass
    def cost(self, y):
        return T.mean(T.nnet.binary_crossentropy(self.output, y))
