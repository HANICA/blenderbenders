import random
from easybpy import *
import bpy
import sys

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/01_12")
from material import *
from keyframe import *

class Healthbar(object):
    def __init__(self, name):
        self.name = name
        self.material = Material(self.name)
        self.size = 0.8

    def create(self, x, y, z, scale, person_health, keyframe):
        cube = create_cube()
        rename_object(cube, self.name)

        self.determine_size(person_health, keyframe)
        self.material.create()

        location(self.name, [x, y, z + scale + 1])

        keyframe.add_loc_healthbar(self, x, y, z + scale + 1)

    def determine_size(self, person_health, keyframe):
        self.size = 0.8 * (person_health / 100)
        bpy.data.objects[self.name].scale[0] = 0.15
        bpy.data.objects[self.name].scale[1] = self.size
        bpy.data.objects[self.name].scale[2] = 0.15
        keyframe.add_scale_healthbar(self)
