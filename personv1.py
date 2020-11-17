import bpy
from easybpy import *
import random

class person(object):
    def __init__(self, x, y, z, scale, name):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.scale = scale
        self.frame_index = 1
        self.last_keyframe = 250
        self.stepsize = 2
        self.animation_speed = 10

    def create(self):
        cube = create_cube()
        self.add_keyframe() #starting frame
        rename_object(cube, self.name)

        add_modifier(cube, "subsurf modifier", 'SUBSURF')
        cube.modifiers["subsurf modifier"].levels = 2
        bpy.ops.object.shade_smooth()

        self.set_scale()
        self.set_location()

        # determine state when created
        ran_num = random.randint(1,10)
        bpy.ops.object.material_slot_add()
        if ran_num == 5:
            self.add_material("infected")
        else:
            self.add_material("healthy")

    def set_location(self):
        location(self.name, [self.x, self.y, self.z])

    def set_scale(self):
        for i in range(3):
            bpy.data.objects[self.name].scale[i] = self.scale

    def animate_step(self, steps):
        direction = ["left", "right", "up", "down"]

        for i in range(steps):
            index = random.randint(0, 3) # random from 0 to 3
            self.step_direction(direction[index]) # move one step
            self.set_location()
            self.frame_index += self.animation_speed # set next frame location/time
            self.add_keyframe() # add keyframe

        bpy.context.scene.frame_end = self.frame_index # last frame == end frame

    def step_direction(self, direction):
        if direction == "left":
            self.x -= self.stepsize
        elif direction == "right":
            self.x += self.stepsize
        elif direction == "down":
            self.y -= self.stepsize
        elif direction == "up":
            self.y += self.stepsize

    def add_keyframe(self):
        obj = bpy.context.object
        obj.location = (self.x, self.y, self.z)
        obj.keyframe_insert(data_path = "location", frame = self.frame_index)

    def add_material(self, material):
        D = bpy.data

        if len(D.objects[self.name].material_slots) < 1:
            # if there is no slot then we append to create the slot and assign
            D.objects[self.name].data.materials.append(D.materials[material])
        else:
            # we always want the material in slot[0]
            D.objects[self.name].material_slots[0].material = D.materials[material]





