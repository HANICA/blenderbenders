import bpy
import sys
from easybpy import *
import random

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/27_11")
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
        self.age = random.randint(0, 100)
        self.state = ""
        self.swap_position = False
        self.current_location = []
        self.next_location = []
        self.scale = .5
        self.frame_index = 1
        self.last_keyframe = 250
        self.stepsize = 2
        self.animation_speed = 20
        self.health_score = 100
        self.wisdom = ""
        self.symptoms = False
        self.infected_score = 35

    def create(self):
        cube = create_cube()
        rename_object(cube, self.name)

        self.add_modifier("subsurf modifier", 'SUBSURF')
        bpy.data.objects[self.name].modifiers["subsurf modifier"].levels = 2

        percentage = random.randint(1, 100)
        if percentage <= 10:
            self.state = "infected"
            self.health_score = self.infected_score
            self.shows_symptoms()
        else:
            self.state = "healthy"

        self.create_material()

        self.shade_smooth()
        self.set_scale()
        self.set_location()
        self.add_loc_keyframe()  # starting frame location
        # print("name: " + self.name + " age: " + str(self.age) + " state: " + self.state)

    def create_material(self):
        new_mat = material.Material(self.name)
        new_mat.create()
        if self.state == "infected":
            self.change_material(0)
        else:
            self.change_material(255)
        self.add_material(self.name)
        self.add_mat_keyframe()  # starting frame material

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
        self.regen_health_score()
        self.add_loc_keyframe()  # add keyframe for location object
        self.add_mat_keyframe()  # add keyframe for material

        bpy.context.scene.frame_end = self.frame_index  # last frame == end frame

    def add_loc_keyframe(self):
        if self.swap_position == True:
            self.add_swap_keyframe()

        select_object(self.name)
        obj = bpy.context.active_object
        obj.location = (self.x, self.y, self.z)
        obj.keyframe_insert(data_path="location", frame=self.frame_index)

    def add_swap_keyframe(self):
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
        obj.keyframe_insert(data_path="location", frame=(self.frame_index - (self.animation_speed / 2)))
        self.swap_position = False

    def add_mat_keyframe(self):
        ob = bpy.context.object
        mats = ob.data.materials

        ob.active_material = bpy.data.materials[self.name]

        for mat in mats:
            mat.keyframe_insert(data_path="diffuse_color", frame=self.frame_index)

    def add_material(self, material):
        if len(bpy.data.objects[self.name].material_slots) < 1:
            # if there is no slot then we append to create the slot and assign
            bpy.data.objects[self.name].data.materials.append(bpy.data.materials[material])
        else:
            # we always want the material in slot[0]
            bpy.data.objects[self.name].material_slots[0].material = bpy.data.materials[material]

    def change_material(self, intensity_color):
        mat = material.Material(self.name)
        if self.symptoms == True:
            mat.change_color(intensity_color, 255, intensity_color)
        else:
            mat.change_color(intensity_color, intensity_color, 255)

    def check_infection_radius(self, persons):
        social_distance = 1.5 + self.scale
        for pers in persons:
            if self.state != pers.state:
                distance = sqrt(((self.x - pers.x) ** 2) + ((self.y - pers.y) ** 2))
                if social_distance >= distance:
                    self.infect_other(pers)

    def infect_other(self, pers):
        percentage = random.randint(1, 100)
        if percentage <= 100:
            pers.state = "infected"
            pers.health_score = pers.infected_score
            self.shows_symptoms()
            pers.change_material(0)

    def shows_symptoms(self):
        ran_num = random.randint(0, self.age)
        if ran_num >= 18 or self.age >= 70:
            self.symptoms = True

    def regen_health_score(self):
        if self.health_score != 100:
            self.health_score += 5

            if self.health_score >= 100:
                self.health_score = 100
                self.state = "healthy"

        intensity = (self.health_score - self.infected_score) * (255 / (100 - self.infected_score))
        self.change_material(intensity)
