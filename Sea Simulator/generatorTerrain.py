# coding=utf-8
"""
Fabian Diaz, CC3501, 2020-1
GEnera un terreno de acuerdo a los parametros
"""
import math

import numpy as np

import easy_shaders as es

import generatorMesh as gm 

class generatorTerrain:
    def __init__(self):
        self.xs = np.ogrid[-20:20:40j]
        self.ys = np.ogrid[-20:20:40j]

        self.centre = [[200, -200], [200, -100], [200, 0], [200, 100], [200, 200]]
        self.a = [0.075, 0.08, 0.085, 0.09, 0.095]
        self.w = [0.25, 0.3, 0.35, 0.4, 0.45]

        self.simple = lambda x, y, t: seaTerrain(x, y, t, self.centre, self.a, self.w)

    def seaMesh(self, controller, t):

        cpuSurface = gm.generateTerrainMesh(self.xs, self.ys, self.simple, t, [10/255, 105/255, 160/255])

        return es.toGPUShape(cpuSurface)

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 -x1)**2 + (y2 -y1)**2)

def seaTerrain(x, y, t, centre, a, w):    
    res = 0
    for c, a, w in zip(centre, a, w):
        dis = distance(x, y, c[0], c[1])
        res += a * math.sin(w * t + dis)

    return res