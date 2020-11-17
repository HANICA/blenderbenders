import sys
import bpy
from easybpy import *
import random
sys.path.append("C:/Users/david/OneDrive/Documenten/S4D/python_files")
from personv1 import *
from material import *

def main():
    # creating 5 persons and let them animate 20 times
    for number in range(5):
        name = "person_" + str(number)
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        man = person(x, y, 0, .5, name)
        man.create()
        print(get_materials_from_object(man))
        man.animate_step(20)

if __name__ == '__main__':
    main()

