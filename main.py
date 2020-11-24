import bpy
import sys
from easybpy import *
import random

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blenderbenders")
from personv1 import *
from material import *


def main():
    create_collection("persons")
    set_active_collection("persons")
    create_persons(20)
    animate_persons(20)


def create_instance(class_name, instance_name):
    count = 0
    while True:
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        z = 0
        scale = 0.5
        name = instance_name + str(count)
        globals()[name] = class_name(x, y, z, scale, name)
        count += 1
        yield True


def create_persons(amount):
    generator_instance = create_instance(person, 'person_')

    # create amount of instances of class person
    for i in range(amount):
        next(generator_instance)

    # create amount of persons in blender
    for i in range(amount):
        name = 'person_' + str(i)
        create_material(globals()[name].name)
        globals()[name].create()


def animate_persons(steps):
    select_all_objects("persons")
    for i in range(steps):
        for i in range(len(selected_objects())):
            name = 'person_' + str(i)
            if globals()[name].state == "infected":
                check_radius(globals()[name])
            globals()[name].animate_step()


def check_radius(infected_person):
    select_all_objects("persons")
    for i in range(len(selected_objects())):
        name = 'person_' + str(i)
        if globals()[name].state != "infected":
            if (infected_person.x + infected_person.distance) > globals()[name].x and (infected_person.x - infected_person.distance) < globals()[name].x:
                if (infected_person.y + infected_person.distance) > globals()[name].y and (infected_person.y - infected_person.distance) < globals()[name].y:
                    infect_other(name)


def infect_other(name):
    pass


def create_material(mat_name):
    person_mat = material(mat_name)
    person_mat.create()
    person_mat.change_color(255, 255, 255)


if __name__ == '__main__':
    main()
