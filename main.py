import bpy
import sys
from easybpy import *
import random
import numpy as np
from collections import defaultdict

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/25_11")
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
        current_locations[loc].append(i)
        i += 1
    print(current_locations)

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
        for person in persons:
            person.animate_step(persons)
        current_locations.clear()

if __name__ == '__main__':
    main()
