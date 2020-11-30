import bpy
import sys
from easybpy import *
import random
from collections import defaultdict

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/30_11")
from person import *
from material import *
from buildings import *

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

    create_material("person")

    create_collection("persons")
    set_active_collection("persons")
    create_persons(80)

    animate_persons(40)


def create_persons(amount):
    for i in range(amount):
        name = "person_" + str(len(persons))
        person = Person(name)
        persons.append(person)
    determine_start_locations_persons()
    draw_persons()

def create_material(material_name):
    new_mat = Material(material_name)
    new_mat.create()

def draw_persons():
    for pers in persons:
        pers.create()


def animate_persons(steps):
    for x in range(steps):
        current_locations_persons()
        next_locations_persons()
        for person in persons:
            person.animate_step(persons)
        current_locations.clear()
        next_locations.clear()
        # print(str(x))

def create_borders():
    create_wall("horizontal", grid_x / 2, grid_y)
    create_wall("horizontal", grid_x / 2, 0)
    create_wall("vertical", grid_x, grid_y / 2)
    create_wall("vertical", 0, grid_y / 2)
    wall_placement()
    # print(wall_locations)

def create_wall(rotation, x, y):
    name = "wall_" + str(len(walls))
    wall = Wall(name, x, y, 2)
    wall.create(grid_x, grid_y, rotation)
    walls.append(wall)

def wall_placement():
    i = 0
    for wall in walls:
        if wall.rotation == "horizontal":
            for x_cor in range(grid_x + 1):
                loc = tuple((x_cor, wall.y))
                wall_locations[loc].append(i)  # index
                i += 1
        else:
            for y_cor in range(grid_y + 1):
                loc = tuple((wall.x, y_cor))
                wall_locations[loc].append(i)  # index
                i += 1

def current_locations_persons():
    i = 0
    for pers in persons:
        loc = tuple((pers.x, pers.y))
        pers.current_location = loc
        current_locations[loc].append(i)  # index
        i += 1


def next_locations_persons():
    i = 0
    for pers in persons:
        loc = get_next_direction(pers)
        next_locations[loc].append(i)
        pers.x = loc[0]
        pers.y = loc[1]
        pers.next_location = loc
        # print("old: " + str(pers.current_location) + " new: " + str(pers.next_location))
        i += 1
    check_possible_collision()


def check_possible_collision():
    for pers_a in persons:
        for pers_b in persons:
            if pers_a.current_location == pers_b.next_location and pers_b.current_location == pers_a.next_location:
                pers_a.swap_position = True
                # print(str(pers_a.name) + " and " + str(pers_b.name) + " walking towards each other")


def get_next_direction(pers):
    left = tuple((pers.x - pers.stepsize, pers.y))
    right = tuple((pers.x + pers.stepsize, pers.y))
    up = tuple((pers.x, pers.y + pers.stepsize))
    down = tuple((pers.x, pers.y - pers.stepsize))
    dir_array = [left, up, right, down]
    pos_loc = []

    for i in range(len(dir_array)):
        if next_locations[dir_array[i]] or wall_locations[dir_array[i]]:
            pass
        else:
            pos_loc.append(dir_array[i])

    if len(pos_loc) != 0:
        ran_num = get_random(0, len(pos_loc) - 1)

        return pos_loc[ran_num]


def determine_start_locations_persons():
    i = 0
    while i < len(persons):
        x = get_random(0, grid_x / 2) * 2
        y = get_random(0, grid_y / 2) * 2
        loc = tuple((x, y))
        if current_locations[loc]:
            continue

        current_locations[loc].append(i)
        persons[i].x = loc[0]
        persons[i].y = loc[1]
        i += 1


def get_random(a, b):
    return random.randint(a, b)


if __name__ == '__main__':
    main()
