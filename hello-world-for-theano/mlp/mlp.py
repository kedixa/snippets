#!/usr/bin/python

from HiddenLayer import *
from OutputLayer import *

class MLP(object):
    def __init__(self, rng, input, n_in, n_hid, n_out):
        self.hid = HiddenLayer(rng, input, n_in, n_hid)
        self.out = OutputLayer(rng, self.hid.output, n_hid, n_out)
        self.output = self.out.output
        self.params = self.hid.params + self.out.params
        self.cost = self.out.cost
        pass
    def errors(self, y):
        y = T.argmax(y, axis = 1)
        return T.mean(T.neq(self.out.y_pred, y))
