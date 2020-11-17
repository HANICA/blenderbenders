import sys
import bpy
from easybpy import *
import random
sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/blenderbenders")
from personv1 import *
from material import *

def main():
    create_materials()

    # creating 5 persons and let them animate 20 times
    for number in range(5):
        name = "person_" + str(number)
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        man = person(x, y, 0, .5, name)
        man.create()
        man.animate_step(20)

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

