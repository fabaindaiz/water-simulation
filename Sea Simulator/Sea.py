# coding=utf-8
"""
Fabian Diaz, CC3501, 2020-1
Archivo principal del generador de bosques
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

import transformations as tr
import scene_graph as sg

from renderTask import renderTask
import generatorTerrain as gterr

# A class to store the application control
class Sea:
    def __init__(self):
        self.fillPolygon = True
        self.camSwitch = True
        self.axisSwitch = False

        self.gterr = gterr.generatorTerrain()
        self.width = 800
        self.height = 800

        self.time = 0

        self.projection = tr.perspective(60, float(self.width)/float(self.height), 0.1, 100)

        self.modelNode = sg.SceneGraphNode("modelNode")
        self.drawNodes = [self.modelNode]
    
    def on_key(self, window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return

        elif key == glfw.KEY_SPACE:
            self.camSwitch = not self.camSwitch

        elif key == glfw.KEY_BACKSPACE:
            self.axisSwitch = not self.axisSwitch
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            sys.exit()
    
    def updateModel(self, dt):
        self.time += 2 * dt
        self.modelNode.childs = [self.gterr.seaMesh(self, self.time)]

# We will use the global controller as communication with the callback function

sea = Sea()

if __name__ == "__main__":

    # Preparando el renderizado
    renderTask = renderTask(sea)

    sea.modelNode.childs = [sea.gterr.seaMesh(sea, 1)]

    # Ejecuta el renderizado
    renderTask.main()
