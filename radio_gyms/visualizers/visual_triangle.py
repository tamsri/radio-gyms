"""
This file is currently not used, it was replaced by pywavefront to avoid the complexity.
"""
import ctypes
from typing import List
from pyglet.gl import glUseProgram, GLchar, glCreateShader,\
    GL_VERTEX_SHADER, glShaderSource, glCompileShader, GL_FRAGMENT_SHADER,\
    glCreateProgram, glAttachShader, glLinkProgram, glGenBuffers, GLuint,\
    GL_ARRAY_BUFFER, glBindBuffer, GLfloat, GL_STATIC_DRAW, glBufferData, \
    glVertexAttribPointer, GL_FLOAT, GL_FALSE, glEnableVertexAttribArray, \
    glUniform3fv, glGetUniformLocation, glUniform4fv

import numpy as np

from ..utils import VecNorm

class VisualTriangle:
    shader = None

    def __init__(self, point_a: List, point_b: List, point_c: List, color_a: List):
        normal = VecNorm(np.cross(np.array(point_b) - np.array(point_a), np.array(point_c) - np.array(point_a)))
        self.triangle = [*point_a, *normal,
                         *point_b, *normal,
                         *point_c, *normal,]
        self.color = color_a
        self.vertex_shader_binary = b"""
        #version 330
        in layout(location=0) vec3 position;
        in layout(location=1) vec3 normal;
        
        // out vec3 FragPos;
        out vec3 newNormal;
        
        //uniform mat4 model;
        //uniform mat4 view;
        //uniform mat4 projection;
        
        void main(){
            // FragPos = vec3(model*vec4(position, 1.0));
            newNormal = normal;
            
            //gl_Position = projection * view * model * Vec4(position, 1.0f);
            gl_Position = Vec4(position, 1.0f);
        }
        """

        self.vertex_shader_binary = b"""
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 color;

        out vec3 newColor;

        void main()
        {
            gl_Position = vec4(position, 1.0f);
            newColor = color;
        }
        """

        self.fragment_shader_binary = b"""
        #version 330
        out vec4 FragColor;
        
        in vec3 newNormal;
        
        // uniform vec3 lightPos;
        // uniform vec3 lightColor;
        // uniform vec3 objectColor;
        
        void main(){
            /*float ambientStrength = 0.1;
            vec3 ambient = ambientStrength * lightColor;

            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor;

            vec3 result = (ambient + diffuse) * objectColor;
            FragColor = vec4(result, 1.0);*/
            outColor = vec4(1.0f, 0.0f, 0.0f 1.0f);
        }
        """
        self.fragment_shader_binary = b"""
        #version 330
        in vec3 newColor;

        out vec4 outColor;

        void main()
        {
            outColor = vec4(newColor, 1.0f);
        }
        """

        vertex_buffer = ctypes.create_string_buffer(self.vertex_shader_binary)
        c_vertex = ctypes.cast(ctypes.pointer(ctypes.pointer(vertex_buffer)),
                               ctypes.POINTER(ctypes.POINTER(GLchar)))
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, 1, c_vertex, None)
        glCompileShader(vertex_shader)

        fragment_buffer = ctypes.create_string_buffer(self.fragment_shader_binary)
        c_fragment = ctypes.cast(ctypes.pointer(ctypes.pointer(fragment_buffer)),
                               ctypes.POINTER(ctypes.POINTER(GLchar)))
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, 1, c_fragment, None)
        glCompileShader(fragment_shader)

        self.shader = glCreateProgram()
        glAttachShader(self.shader, vertex_shader)
        glAttachShader(self.shader, fragment_shader)
        glLinkProgram(self.shader)

        glUseProgram(self.shader)

        vbo = GLuint(0)
        glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, 72, (GLfloat * len(self.triangle))(*self.triangle), GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

    def update(self, view, projection, lightPos, lightColor, objectColor):
        model = np.ones((4,4))
