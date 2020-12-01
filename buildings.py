from easybpy import *
import bpy
import math


class Wall(object):
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.width = 1
        self.length = 0
        self.rotation = ""

    def create(self, grid_x, grid_y, rotation):
        cube = create_cube()
        rename_object(cube, self.name)

        self.set_rotation(rotation)
        if self.rotation == "horizontal":
            self.length = (grid_x / 2) + (1 * self.width)
        else:
            self.length = (grid_y / 2) + (3 * self.width)
        self.set_scale()
        self.set_location()

    def set_scale(self):
        bpy.data.objects[self.name].scale[0] = self.width
        bpy.data.objects[self.name].scale[1] = self.length
        bpy.data.objects[self.name].scale[2] = self.z
        bpy.data.objects[self.name].location[2] = self.z

    def set_location(self):
        if self.rotation == "horizontal":
            bpy.data.objects[self.name].location[0] = self.x
            if self.y == 0:
                self.y -= (2 * self.width)
                bpy.data.objects[self.name].location[1] = self.y
            else:
                self.y += (2 * self.width)
                bpy.data.objects[self.name].location[1] = self.y
        else:
            bpy.data.objects[self.name].location[1] = self.y
            if self.x == 0:
                self.x -= (2 * self.width)
                bpy.data.objects[self.name].location[0] = self.x
            else:
                self.x += (2 * self.width)
                bpy.data.objects[self.name].location[0] = self.x

        bpy.data.objects[self.name].location[2] = self.z

    def set_rotation(self, rotation):
        if rotation == "horizontal":
            bpy.data.objects[self.name].rotation_euler[2] = math.radians(90)
            self.rotation = "horizontal"
        else:
            bpy.data.objects[self.name].rotation_euler[2] = math.radians(0)
            self.rotation = "vertical"

    def get_coordinates(self, wall_locations, grid_x, grid_y):
        i = len(wall_locations)
        if self.rotation == "horizontal":
            for x_cor in range(grid_x + 1):
                loc = tuple((x_cor, self.y))
                wall_locations[loc].append(i)  # index
                i += 1
        else:
            for y_cor in range(grid_y + 1):
                loc = tuple((self.x, y_cor))
                wall_locations[loc].append(i)  # index
                i += 1





