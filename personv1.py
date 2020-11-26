import bpy
import sys
from easybpy import *
import random

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/26_11")
from main import *
import material
from math import *

current_locations = defaultdict(list)

class Person(object):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.z = 0
        self.name = name
        self.state = ""
        self.swap = False
        self.current_location = []
        self.next_location = []
        self.scale = .5
        self.frame_index = 1
        self.last_keyframe = 250
        self.stepsize = 2
        self.animation_speed = 10

    def create(self):
        cube = create_cube()
        rename_object(cube, self.name)

        self.add_modifier("subsurf modifier", 'SUBSURF')
        bpy.data.objects[self.name].modifiers["subsurf modifier"].levels = 2

        percentage = random.randint(1, 100)
        if percentage <= 10:
            self.state = "infected"
        else:
            self.state = "healthy"

        self.create_material()

        self.shade_smooth()
        self.set_scale()
        self.set_location()
        self.add_loc_keyframe()  # starting frame location

    def create_material(self):
        new_mat = material.Material(self.name)
        new_mat.create()
        if self.state == "infected":
            new_mat.change_color(0, 255, 0)
        else:
            new_mat.change_color(255, 255, 255)
        self.add_material(self.name)
        self.add_mat_keyframe() # starting frame material

    def add_modifier(self, name, type):
        obj = get_object(self.name)
        add_modifier(obj, name, type)

    def shade_smooth(self):
        bpy.ops.object.shade_smooth()

    def shade_flat(self):
        bpy.ops.object.shade_flat()

    def set_location(self):
        location(self.name, [self.x, self.y, self.z])

    def set_scale(self):
        for i in range(3):
            bpy.data.objects[self.name].scale[i] = self.scale

    def animate_step(self, persons):
        self.set_location()
        self.frame_index += self.animation_speed  # set next frame location/time
        if self.state == "infected":
            self.check_infection_radius(persons)
        self.add_loc_keyframe()  # add keyframe for location object
        self.add_mat_keyframe()  # add keyframe for material

        bpy.context.scene.frame_end = self.frame_index  # last frame == end frame

    def add_loc_keyframe(self):
        if self.swap == True:
            if self.current_location[0] != self.next_location[0]:
                if self.current_location[0] > self.next_location[0]:
                    swap_x = self.current_location[0] - (self.stepsize / 2)
                    swap_y = self.y + 0.5
                else:
                    swap_x = self.current_location[0] + (self.stepsize / 2)
                    swap_y = self.y - 0.5
            else:
                if self.current_location[1] > self.next_location[1]:
                    swap_y = self.current_location[1] - (self.stepsize / 2)
                    swap_x = self.x + 0.5
                else:
                    swap_y = self.current_location[1] + (self.stepsize / 2)
                    swap_x = self.x - 0.5
            select_object(self.name)
            obj = bpy.context.active_object
            obj.location = (swap_x, swap_y, self.z)
            obj.keyframe_insert(data_path="location", frame=(self.frame_index - (self.animation_speed / 2) ) )
            self.swap = False

        select_object(self.name)
        obj = bpy.context.active_object
        obj.location = (self.x, self.y, self.z)
        obj.keyframe_insert(data_path="location", frame=self.frame_index)

    def add_mat_keyframe(self):
        ob = bpy.context.object
        mats = ob.data.materials

        ob.active_material = bpy.data.materials[self.name]

        for mat in mats:
            mat.keyframe_insert(data_path="diffuse_color", frame=self.frame_index)

    def add_material(self, material):
        D = bpy.data

        if len(D.objects[self.name].material_slots) < 1:
            # if there is no slot then we append to create the slot and assign
            D.objects[self.name].data.materials.append(D.materials[material])
        else:
            # we always want the material in slot[0]
            D.objects[self.name].material_slots[0].material = D.materials[material]

    def change_material(self, r, g, b):
        select_object(self.name)
        obj = bpy.context.active_object
        obj.active_material.diffuse_color[0] = r / 255
        obj.active_material.diffuse_color[1] = g / 255
        obj.active_material.diffuse_color[2] = b / 255

    def check_infection_radius(self, persons):
        social_distance = 1.5 + self.scale
        for pers in persons:
            if self.state != pers.state:
                distance = sqrt(((self.x - pers.x) ** 2) + ((self.y - pers.y) ** 2))
                if social_distance >= distance:
                    self.infect_other(pers)

    def infect_other(self, pers):
        percentage = random.randint(1, 100)
        if percentage <= 20:
            pers.state = "infected"
            pers.change_material(0, 255, 0)


