# coding=utf-8
"""
Fabian Diaz, CC3501, 2020-1
Genera una malla de acuerdo a los parametros
"""

import numpy as np

import basic_shapes as bs
import easy_shaders as es

class meshGenerator:
    def __init__(self, name):
        return

def calculateNormal(nx, ny):
    n = [nx[1]*ny[2] - nx[2]*ny[1], nx[2]*ny[0] - nx[0]*ny[2], nx[0]*ny[1] - nx[1]*ny[0]]
    norm = np.sqrt(n[0]**2 + n[1]**2 + n[2]**2)

    return [n[0]/norm, n[1]/norm, n[2]/norm]

def generateTerrainMesh(xs, ys, function, t, color):
    vertices = []
    indices = []

    # We generate a vertex for each sample x,y,z
    for i in range(1, len(xs)):
        for j in range(1, len(ys)):
            x = xs[i]
            y = ys[j]
            z = function(x, y, t)

            dx = x - xs[i-1]
            dy = y - xs[i-1]

            dzx = function(x, y, t) - function(x -dx, y, t)
            dzy = function(x, y, t) - function(x, y -dy, t)

            nx = [-1, -1+dy, dzy]
            ny = [-1+dx, -1, dzx]

            n = calculateNormal(nx, ny)

            vertColor = [color[0], color[1], color[2]]
            #vertColor = [color[0] +random.randint(-5,5)/255, color[1] +random.randint(-5,5)/255, color[2] +random.randint(-5,5)/255]
            
            vertices += [x, y, z] + vertColor + n

    # The previous loops generates full columns j-y and then move to
    # the next i-x. Hence, the index for each vertex i,j can be computed as
    index = lambda i, j: i*(len(xs)-1) + j
    
    # We generate quads for each cell connecting 4 neighbor vertices
    for i in range(len(xs)-2):
        for j in range(len(ys)-2):

            # Getting indices for all vertices in this quad
            isw = index(i,j)
            ise = index(i+1,j)
            ine = index(i+1,j+1)
            inw = index(i,j+1)

            # adding this cell's quad as 2 triangles
            indices += [
                isw, ise, ine,
                ine, inw, isw
            ]

    return bs.Shape(vertices, indices)