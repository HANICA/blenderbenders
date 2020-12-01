import bpy
import sys
from easybpy import *
import random

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/01_12")
from main import *
import material
from keyframe import *
from healthbar import *
from math import *

current_locations = defaultdict(list)

class Person(object):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.z = 0
        self.name = name
        self.material = material.Material("person")
        self.age = random.randint(0, 100)
        self.state = ""
        self.swap_position = False
        self.current_location = []
        self.next_location = []
        self.previous_direction = ""
        self.scale = .5
        self.stepsize = 2
        self.health_score = 100
        self.stubborness = False
        self.symptoms = False
        self.infected_score = 35
        self.healthbar = Healthbar(self.name + "_healthbar")

    def create(self, keyframe):
        cube = create_cube()
        rename_object(cube, self.name)

        self.add_modifier("subsurf modifier", 'SUBSURF')
        bpy.data.objects[self.name].modifiers["subsurf modifier"].levels = 2

        self.material.add_to_object(self.name)
        self.shade_smooth()
        self.set_scale()
        self.set_location()
        keyframe.add_loc_person(self, self.healthbar, self.x, self.y, self.z) # starting frame location person

        percentage = random.randint(1, 100)
        if percentage <= 10:
            self.state = "infected"
            self.health_score = self.infected_score
            self.shows_symptoms()
        else:
            self.state = "healthy"

        self.healthbar.create(self.x, self.y, self.z, self.scale, self.health_score, keyframe)

    def add_modifier(self, name, type):
        obj = get_object(self.name)
        add_modifier(obj, name, type)

    def shade_smooth(self):
        bpy.ops.object.shade_smooth()

    def set_location(self):
        location(self.name, [self.x, self.y, self.z + (self.scale / 2)])

    def set_scale(self):
        for i in range(3):
            bpy.data.objects[self.name].scale[i] = self.scale

    def determine_start_location(self, current_locations, grid_x, grid_y):
            i = len(current_locations)
            x = get_random(0, grid_x / 2) * 2
            y = get_random(0, grid_y / 2) * 2
            loc = tuple((x, y))
            if current_locations[loc]:
                self.determine_start_location(current_locations, grid_x, grid_y)

            current_locations[loc].append(i)
            self.x = loc[0]
            self.y = loc[1]

    def get_next_direction(self, next_locations, wall_locations):
        left = tuple((self.x - self.stepsize, self.y))
        right = tuple((self.x + self.stepsize, self.y))
        up = tuple((self.x, self.y + self.stepsize))
        down = tuple((self.x, self.y - self.stepsize))
        dir_array = []
        pos_loc = []

        for i in range(len(dir_array)):
            if next_locations[dir_array[i]] or wall_locations[dir_array[i]]:
                pass
            else:
                pos_loc.append(dir_array[i])

        if len(pos_loc) != 0:

            if pos_loc[ran_num] == left:
                self.previous_direction = left
            elif pos_loc[ran_num] == right:
                self.previous_direction = right
            elif pos_loc[ran_num] == up:
                self.previous_direction = up
            elif pos_loc[ran_num] == down:
                self.previous_direction = down

            return direction

    # def determine_array_order(self, left, right, up, down):
    #     if self.previous_direction == left:
    #         dir_array = [left, up, down, right]
    #     elif self.previous_direction == right:
    #         dir_array_order = [right, up, down, left]
    #     elif self.previous_direction == up:
    #         dir_array_order = [up, left, right, down]
    #     elif self.previous_direction == down:
    #         dir_array_order = [down, left, right, up]
    #
    #     return dir_array_order


    def check_infection_radius(self, persons):
        social_distance = 1.5 + self.scale
        if self.state == "infected":
            for person in persons:
                if self.state != person.state:
                    distance = sqrt(((self.x - person.x) ** 2) + ((self.y - person.y) ** 2))
                    if social_distance >= distance:
                        self.infect_other(person)

    def infect_other(self, person):
        percentage = random.randint(1, 100)
        if percentage <= 100:
            person.state = "infected"
            person.health_score = person.infected_score
            self.shows_symptoms()
            Material(self.name + "_healthbar").infected_color()

    def shows_symptoms(self):
        ran_num = random.randint(0, self.age)
        if ran_num >= 18 or self.age >= 70:
            self.symptoms = True

    def regen_health_score(self, keyframe):
        if self.health_score != 100:
            self.health_score += 5 - (self.age * 0.04)
            self.healthbar.determine_size(self.health_score, keyframe)
            if self.health_score >= 100:
                self.health_score = 100
                self.state = "healthy"

        color = (self.health_score - self.infected_score) * (255 / (100 - self.infected_score))
        Material(self.name + "_healthbar").regen_color(color)
