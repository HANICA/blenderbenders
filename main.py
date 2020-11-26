import bpy
import sys
from easybpy import *
import random
from collections import defaultdict

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/26_11")
from person import *
from material import *

persons = []
start_locations = defaultdict(list)
current_locations = defaultdict(list)
new_locations = defaultdict(list)


def main():
    create_collection("persons")
    set_active_collection("persons")

    create_persons(20)
    animate_persons(20)


def create_persons(amount):
    for i in range(amount):
        name = "person_" + str(i)
        person = Person(name)
        persons.append(person)
    determine_locations_persons()
    draw_persons()


def current_locations_persons():
    i = 0
    for pers in persons:
        loc = tuple((pers.x, pers.y))
        pers.current_location = loc
        current_locations[loc].append(i)
        i += 1


def new_locations_persons():
    new_locations.clear()
    i = 0
    for pers in persons:
        loc = get_next_direction(pers)
        new_locations[loc].append(i)
        pers.x = loc[0]
        pers.y = loc[1]
        pers.next_location = loc
        # print("old: " + str(pers.current_location) + " new: " + str(pers.new_location))
        i += 1
    walk_towards_each_other()


def walk_towards_each_other():
    for pers_a in persons:
        for pers_b in persons:
            if pers_a.current_location == pers_b.next_location and pers_b.current_location == pers_a.next_location:
                pers_a.swap = True
                # print(str(pers_a.name) + " and " + str(pers_b.name) + " walking towards each other")


def get_next_direction(pers):
    left = tuple((pers.x - pers.stepsize, pers.y))
    up = tuple((pers.x, pers.y + pers.stepsize))
    right = tuple((pers.x + pers.stepsize, pers.y))
    down = tuple((pers.x, pers.y - pers.stepsize))
    dir_array = [left, up, right, down]
    pos_loc = []
    for i in range(len(dir_array)):
        if new_locations[dir_array[i]]:
            pass
        else:
            pos_loc.append(dir_array[i])
    if len(pos_loc) != 0:
        ran_num = random.randint(0, len(pos_loc) - 1)
        if pos_loc[ran_num] == left:
            pers.next_direction = "left"
        elif pos_loc[ran_num] == right:
            pers.next_direction = "right"
        elif pos_loc[ran_num] == down:
            pers.next_direction = "down"
        elif pos_loc[ran_num] == up:
            pers.next_direction = "up"

        return pos_loc[ran_num]


def determine_locations_persons():
    i = 0
    while i < len(persons):
        x = random.randint(0, 10) * 2
        y = random.randint(0, 10) * 2
        loc = tuple((x, y))
        if start_locations[loc]:
            continue

        start_locations[loc].append(i)
        persons[i].x = loc[0]
        persons[i].y = loc[1]
        i += 1


def draw_persons():
    for pers in persons:
        pers.create()


def animate_persons(steps):
    for x in range(steps):
        current_locations_persons()
        new_locations_persons()
        for person in persons:
            person.animate_step(persons)
        current_locations.clear()
        print(str(x))


if __name__ == '__main__':
    main()
