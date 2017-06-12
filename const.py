# Has constant variables and methods useful for multiple classes
'''
In an ideal world, I would have one really big parent class for projectiles
and enemies where the methods would be contained in there but lol
'''

import pyglet

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
BOTTOM_BORDER = 60

DANGER_RADIUS = 10000
COLLISION_ENTRY = 10

WEAPON_VERT = 60
CHARACTER_VERT = 50

DIMENSIONS = {"atk0":(15, 15)} # obsolete-ifies BOMB_WIDTH, etc..


BOMB_IMAGE = pyglet.resource.image("w1.png")
BOMB_WIDTH = 15
BOMB_HEIGHT = 15

'''
THESE CHANGE IF SCREEN DIMENSIONS CHANGE
'''
BOMB_X = WINDOW_WIDTH/2-BOMB_WIDTH/2-26
BOMB_Y = 97

'''
how the fuck does this math work
'''
def in_safe_space(x, y, object_width):
    HALF_WIDTH = WINDOW_WIDTH/2 - object_width/2
    return (y - BOTTOM_BORDER)**2 + (x - HALF_WIDTH)**2 <= DANGER_RADIUS
