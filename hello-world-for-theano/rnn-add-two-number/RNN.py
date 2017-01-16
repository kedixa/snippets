#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import theano
import theano.tensor as T

class RNN(object):
    def __init__(self, n_in, n_hid, n_out, learn_rate = 0.1):
        def floatX(shape):
            return np.asarray(np.random.uniform(low = -0.2, high = 0.2, size = shape), dtype = theano.config.floatX)

        self.x = T.fmatrix()
        self.y = T.fmatrix()
        self.h0 = T.fvector()

        self.w_h = theano.shared(floatX((n_hid, n_hid)))
        self.w_i = theano.shared(floatX((n_in, n_hid)))
        self.w_o = theano.shared(floatX((n_hid, n_out)))
        self.b_h = theano.shared(floatX((n_hid,)))
        self.b_o = theano.shared(floatX((n_out,)))

        def step(x, h_tm1, w_h, w_i, w_o, b_h, b_o):
            _h = T.nnet.sigmoid(T.dot(x, w_i)+T.dot(h_tm1, w_h)+self.b_h)
            _y = T.nnet.sigmoid(T.dot(_h, w_o)+self.b_o)
            return _h, _y

        [self.h, self.o], _ = theano.scan(step, sequences=self.x,
                outputs_info=[self.h0, None],
                non_sequences=[self.w_h, self.w_i, self.w_o, self.b_h, self.b_o])

        self.cost = T.mean(T.nnet.binary_crossentropy(self.o, self.y))

        self.params = [self.w_h, self.w_i, self.w_o, self.b_h, self.b_o]
        self.gparams = T.grad(self.cost, self.params)
        updates = [[p, p - learn_rate * gp] for p, gp in zip(self.params, self.gparams)]

        self.train_data = theano.function([self.h0, self.x, self.y],
                self.cost, updates=updates,
                allow_input_downcast=True)
        self.predict_data = theano.function([self.h0, self.x], self.o,
                allow_input_downcast=True)
        pass
    
    def train(self, h0, x, y):
        return self.train_data(h0, x, y)
    def predict(self, h0, x):
        return self.predict_data(h0, x)
