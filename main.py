import bpy
import sys
from easybpy import *
import random
from collections import defaultdict

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/03_12")
from person import *
from material import *
from buildings import *
from keyframe import *
from healthbar import *

persons = []
walls = []
current_locations = defaultdict(list)
next_locations = defaultdict(list)
wall_locations = defaultdict(list)
grid_x = 50
grid_y = 50


def main():
    create_collection("walls")
    set_active_collection("walls")
    create_borders()

    new_mat = Material("person")
    new_mat.create()

    keyframe = Keyframe()

    create_collection("persons")
    set_active_collection("persons")
    create_persons(80, keyframe)

    animate_persons(20, keyframe)

def create_persons(amount, keyframe):
    for i in range(amount):
        name = "person_" + str(len(persons))
        person = Person(name)
        person.determine_start_location(current_locations, grid_x, grid_y)
        persons.append(person)
        person.create(keyframe)

def animate_persons(steps, keyframe):
    for x in range(steps):
        current_locations_persons()
        next_locations_persons()
        for person in persons:
            keyframe.animate_step(person, persons, keyframe)
        keyframe.next()
        current_locations.clear()
        next_locations.clear()

def create_borders():
    create_instance_wall("horizontal", grid_x / 2, grid_y)
    create_instance_wall("horizontal", grid_x / 2, 0)
    create_instance_wall("vertical", grid_x, grid_y / 2)
    create_instance_wall("vertical", 0, grid_y / 2)
    for wall in walls:
        wall.get_coordinates(wall_locations, grid_x, grid_y)

def create_instance_wall(rotation, x, y):
    name = "wall_" + str(len(walls))
    wall = Wall(name, x, y, 2)
    wall.create(grid_x, grid_y, rotation)
    walls.append(wall)

def current_locations_persons():
    i = 0
    for person in persons:
        loc = tuple((person.x, person.y))
        person.current_location = loc
        current_locations[loc].append(i)  # index
        i += 1

def next_locations_persons():
    i = 0
    for person in persons:
        loc = person.get_next_direction(next_locations, wall_locations)
        next_locations[loc].append(i)
        person.next_location = loc
        # print("old: " + str(pers.current_location) + " new: " + str(pers.next_location))
        i += 1
    check_possible_collision()

def check_possible_collision():
    for person_a in persons:
        for person_b in persons:
            if person_a.current_location == person_b.next_location and person_b.current_location == person_a.next_location:
                person_a.swap_position = True
                # print(str(pers_a.name) + " and " + str(pers_b.name) + " walking towards each other")

def get_random(a, b):
    return random.randint(a, b)


if __name__ == '__main__':
    main()
