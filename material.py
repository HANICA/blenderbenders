import random
from easybpy import *
import bpy

class Material(object):
    def __init__(self, name):
        self.name = name

    def create(self):
        create_material(self.name)

    def change_color(self, r, g, b):
        bpy.data.materials[self.name].diffuse_color[0] = r / 255
        bpy.data.materials[self.name].diffuse_color[1] = g / 255
        bpy.data.materials[self.name].diffuse_color[2] = b / 255



