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

    def add_to_object(self, object_name):
        if len(bpy.data.objects[object_name].material_slots) < 1:
            # if there is no slot then we append to create the slot and assign
            bpy.data.objects[object_name].data.materials.append(bpy.data.materials[self.name])
        else:
            # we always want the material in slot[0]
            bpy.data.objects[object_name].material_slots[0].material = bpy.data.materials[self.name]

    def regen_color(self, intensity_color):
        self.change_color(255 - intensity_color, intensity_color, 0) # intensity 255 == green    intensity 0 == red

    def healthy_color(self):
        self.change_color(0, 255, 0)

    def infected_color(self):
        self.change_color(255, 0, 0)



