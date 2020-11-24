import bpy
import sys
from easybpy import *
import random
import numpy as np
from collections import defaultdict

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blender/Save_files/24_11")
from person import *
from material import *

persons = []
locations = defaultdict(list)

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

def determine_locations_persons():
    i = 0
    while i < len(persons):
        x = random.randint(0, 10) * 2
        y = random.randint(0, 10) * 2
        loc = tuple((x, y))
        if locations[loc]:
            continue

        locations[loc].append(i)
        persons[i].x = loc[0]
        persons[i].y = loc[1]
        i += 1

def draw_persons():
    for pers in persons:
        pers.create()

def animate_persons(steps):
    for x in range(steps):
        for person in persons:
            person.animate_step(persons)


if __name__ == '__main__':
    main()
