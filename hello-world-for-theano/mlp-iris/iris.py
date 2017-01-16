#!/usr/bin/python

import theano
from theano import tensor as T
import numpy as np
import load

def floatX(X):
    return np.asarray(X, dtype = theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 1))

def sgd(cost, params, lr=0.2):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p,g in zip(params, grads):
        updates.append([p, p-g*lr])
        pass
    return updates

def model(X, w_h, w_o, b_h, b_o):
    h = T.nnet.sigmoid(T.dot(X, w_h)+b_h)
    pyx = T.nnet.sigmoid(T.dot(h, w_o)+b_o)
    return pyx

trX, trY, teX, teY = load.iris()

X = T.fmatrix()
Y = T.fmatrix()
b_h = init_weights((30,))
b_o = init_weights((3,))
w_h = init_weights((4, 30))
w_o = init_weights((30,3))
py_x = model(X, w_h, w_o, b_h, b_o)
y_x = T.argmax(py_x, axis=1)
cost = T.mean(T.nnet.binary_crossentropy(py_x, Y))

params = [w_h, w_o,b_h,b_o]
updates = sgd(cost, params)

train = theano.function([X, Y], cost, updates = updates, allow_input_downcast=True)
predict = theano.function([X], y_x, allow_input_downcast=True)

for i in range(100):
    train(trX, trY)
    pass

print predict(teX)
