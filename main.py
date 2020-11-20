import bpy
import sys
from easybpy import *
import random

sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blenderbenders")
from personv1 import *
from material import *


def main():
    create_collection("persons")
    create_materials()

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
        globals()[name].create()


def animate_persons(steps):
    select_all_objects("persons")
    for i in range(steps):
        for i in range(len(selected_objects())):
            name = 'person_' + str(i)
            if bpy.data.objects[globals()[name].name].active_material_index == bpy.data.materials["infected"]:
                check_radius(globals()[name])
            globals()[name].animate_step()


def check_radius(infected_person):
    select_all_objects("persons")
    for i in range(len(selected_objects())):
        name = 'person_' + str(i)
        print(name)
        if infected_person.name != globals()[name].name:
            if (infected_person.x + infected_person.distance) > globals()[name].x and (infected_person.x - infected_person.distance) < globals()[name].x:
                if (infected_person.y + infected_person.distance) > globals()[name].y and (infected_person.y - infected_person.distance) < globals()[name].y:
                    infect_other(name)


def infect_other(name):
    ran_num = random.randint(1, 10)
    if ran_num <= 10:
        globals()[name].add_material("infected")


def create_materials():
    # creating materials
    infected_mat = material("infected")
    infected_mat.create()
    infected_mat.change_color(0, 255, 0)

    healthy_mat = material("healthy")
    healthy_mat.create()
    healthy_mat.change_color(255, 255, 255)

    danger_mat = material("infection radius")
    danger_mat.create()
    danger_mat.change_color(255, 0, 0)


if __name__ == '__main__':
    main()
