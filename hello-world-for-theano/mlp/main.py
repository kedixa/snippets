#!/usr/bin/python

import numpy as np
import theano
import theano.tensor as T
from mlp import *
import load

def test_mlp():
    learning_rate = 0.07
    trX, teX, trY, teY = load.mnist()
    x = T.fmatrix('x')
    y = T.fmatrix('y')
    rng = np.random.RandomState(12345)

    classifier = MLP(rng = rng, input = x, n_in = 28*28,
            n_hid = 60, n_out = 10)
    cost = classifier.cost(y)
    gparams = [T.grad(cost, param) for param in classifier.params]
    updates = [(param, param - learning_rate * gparam)
            for param, gparam in zip(classifier.params, gparams)]
    train_model = theano.function(
            inputs = [x,y], outputs = cost, updates = updates,
            allow_input_downcast=True)
    test_model = theano.function(inputs = [x,y], outputs = classifier.errors(y),
            allow_input_downcast=True)

    m_size = 25
    for i in range(100):
        for i in range(0,len(trX)-m_size,m_size):
            train_model(trX[i:i+m_size],trY[i:i+m_size])
            pass
        print test_model(teX,teY)
        pass
    pass

if __name__ == '__main__':
    test_mlp()
    pass
