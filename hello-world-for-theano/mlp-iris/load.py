#!/usr/bin/python

import os
def iris():
    iris_dir = "iris.data"
    if not os.path.exists(iris_dir):
        raise Exception("iris.data not exists.")

    f = open(iris_dir)
    datas = [[float(i) for i in line.split(' ')] for line in f]
    f.close()
    trX, trY, teX, teY = [], [], [], []
    for data in datas:
        trX.append(data[1:])
        tmp = [0., 0., 0.]
        tmp[int(data[0]-1)] = 1.
        trY.append(tmp)
        pass
    teX = trX[40:50]+trX[90:100]+trX[140:150]
    trX = trX[:40]+trX[50:90]+trX[100:140]
    teY = trY[40:50]+trY[90:100]+trY[140:150]
    trY = trY[:40]+trY[50:90]+trY[100:140]
    return trX, trY, teX, teY
