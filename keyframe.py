import random
from easybpy import *
import bpy

class Keyframe(object):
    def __init__(self):
        self.frame_index = 1
        self.animation_speed = 20

    def animate_step(self, person, persons, keyframe):
        if person.state == "infected":
            person.check_infection_radius(persons)
        person.regen_health_score(keyframe)
        self.add_loc_person(person, person.healthbar, person.x, person.y, person.z, self.frame_index)  # add keyframe for location person
        self.add_loc_healthbar(person.healthbar, person.x, person.y, person.z + person.scale + 1, self.frame_index)  # add keyframe for location healthbar

        self.add_mat(person.name + "_healthbar")  # add keyframe for material healthbar

        bpy.context.scene.frame_end = self.frame_index  # last frame == end frame

    def next(self):
        self.frame_index += self.animation_speed  # set next frame location/time

    def add_loc_person(self, person, healthbar, x, y, z, frame_index):
        if person.swap_position == True:
            self.add_swap(person, healthbar)

        select_object(person.name)
        obj = bpy.context.active_object
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=frame_index)

    def add_loc_healthbar(self, healthbar, x, y, z, frame_index):
        select_object(healthbar.name)
        obj = bpy.context.active_object
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=frame_index)

    def add_swap(self, person, healthbar):
        if person.current_location[0] != person.next_location[0]:
            if person.current_location[0] > person.next_location[0]:
                swap_x = person.current_location[0] - (person.stepsize / 2)
                swap_y = person.y + 0.5
            else:
                swap_x = person.current_location[0] + (person.stepsize / 2)
                swap_y = person.y - 0.5
        else:
            if person.current_location[1] > person.next_location[1]:
                swap_y = person.current_location[1] - (person.stepsize / 2)
                swap_x = person.x + 0.5
            else:
                swap_y = person.current_location[1] + (person.stepsize / 2)
                swap_x = person.x - 0.5

        person.swap_position = False

        self.add_loc_person(person, healthbar, swap_x, swap_y, person.z, self.frame_index - (self.animation_speed / 2))
        self.add_loc_healthbar(healthbar, swap_x, swap_y, person.z + person.scale + 1,  self.frame_index - (self.animation_speed / 2))

    def add_mat(self, mat_name):
        ob = bpy.context.object
        mats = ob.data.materials

        ob.active_material = bpy.data.materials[mat_name]
        for mat in mats:
            mat.keyframe_insert(data_path="diffuse_color", frame=self.frame_index)

    def add_scale_healthbar(self, healthbar):
        select_object(healthbar.name)
        obj = bpy.context.active_object
        obj.scale = (.15, healthbar.size, .15)
        obj.keyframe_insert(data_path="scale", frame=self.frame_index)
