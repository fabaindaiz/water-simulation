# coding=utf-8
"""
Fabian Diaz, CC3501, 2020-1
Aqui se renderiza todo
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg
import lighting_shaders as ls

class renderTask:

    def __init__(self, controller):
        self.controller = controller

        # Initialize glfw
        if not glfw.init():
            sys.exit()

        width = controller.width
        height = controller.height

        self.window = glfw.create_window(width, height, "Sea Simulator", None, None)

        if not self.window:
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(self.window)

        # Connecting the callback function 'on_key' to handle keyboard events
        glfw.set_key_callback(self.window, self.controller.on_key)

        # Assembling the shader program
        self.modelPipeline = ls.SimplePhongShaderProgram()
        self.mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

        # Telling OpenGL to use our shader program
        glUseProgram(self.modelPipeline.shaderProgram)

        # Setting up the clear screen color
        glClearColor(0.85, 0.85, 0.85, 1.0)

        # As we work in 3D, we need to check which part is in front,
        # and which one is at the back
        glEnable(GL_DEPTH_TEST)
    
    def main(self):

        # Creating shapes on GPU memory
        gpuAxis = es.toGPUShape(bs.createAxis(7))

        t0 = glfw.get_time()
        camera_theta = np.pi/4

        height = 6
        radius = 15

        while not glfw.window_should_close(self.window):
            # Using GLFW to check for input events
            glfw.poll_events()

            # Getting the time difference from the previous iteration
            t1 = glfw.get_time()
            dt = t1 - t0
            t0 = t1

            if (glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS):
                camera_theta -= 2 * dt

            elif (glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS):
                camera_theta += 2* dt
            
            if (glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS):
                if self.controller.camSwitch and height < 30:
                    height += 12* dt
                elif not self.controller.camSwitch and radius > 1:
                    radius -= 12* dt
            
            elif (glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS):
                if self.controller.camSwitch and height > -5:
                    height -= 12* dt
                elif not self.controller.camSwitch and radius < 30:
                    radius += 12* dt


            # Setting up the view transform

            camX = radius * np.sin(camera_theta)
            camY = radius * np.cos(camera_theta)

            # TODO Movimiento de la camara
            viewPos = np.array([camX, camY, height])

            view = tr.lookAt(
               viewPos,
                np.array([0,0,0]),
                np.array([0,0,1])
            )

            # Setting up the projection transform
            projection = self.controller.projection

            # Clearing the screen in both, color and depth
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Filling or not the shapes depending on the controller state
            if (self.controller.fillPolygon):
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            # Drawing shapes
            glUseProgram(self.modelPipeline.shaderProgram)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "La"), 0.6, 0.6, 0.6)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "Ld"), 0.7, 0.7, 0.7)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "Ls"), 0.6, 0.6, 0.6)

            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "Ka"), 0.6, 0.6, 0.6)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)

            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "lightPosition"), 0, 0, 10)
            glUniform3f(glGetUniformLocation(self.modelPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
            glUniform1ui(glGetUniformLocation(self.modelPipeline.shaderProgram, "shininess"), 60)

            glUniform1f(glGetUniformLocation(self.modelPipeline.shaderProgram, "constantAttenuation"), 0.01)
            glUniform1f(glGetUniformLocation(self.modelPipeline.shaderProgram, "linearAttenuation"), 0.1)
            glUniform1f(glGetUniformLocation(self.modelPipeline.shaderProgram, "quadraticAttenuation"), 0.01)


            # Drawing shapes with different model transformations
            drawNodes = self.controller.drawNodes

            # glUniformMatrix4fv(glGetUniformLocation(modelPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(0.5))
            # modelPipeline.drawShape(gpuSurface)
            for i in range(len(drawNodes)):
                glUniformMatrix4fv(glGetUniformLocation(self.modelPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
                glUniformMatrix4fv(glGetUniformLocation(self.modelPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
                glUniformMatrix4fv(glGetUniformLocation(self.modelPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
                sg.drawSceneGraphNode(drawNodes[i], self.modelPipeline, "model")
            
            if self.controller.axisSwitch:
                glUseProgram(self.mvpPipeline.shaderProgram)
                glUniformMatrix4fv(glGetUniformLocation(self.mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
                glUniformMatrix4fv(glGetUniformLocation(self.mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
                glUniformMatrix4fv(glGetUniformLocation(self.mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
                self.mvpPipeline.drawShape(gpuAxis, GL_LINES)

            # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
            glfw.swap_buffers(self.window)

            self.controller.updateModel(dt)

        glfw.terminate()

