#use sphinx to document
#copy alex k's template
#Reminder than Pyglet CAN handle decimal (float) speeds/coordinates.

import time
import sys
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse
import math


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

enemies_remaining = 0

'''
GAME STATE
'''

level_number = 0
is_shop = False

class Level:
    #bg is a pyglet.resource.image()
    def __init__(self, level_number, enemies_list, bg_image):
        self.level = level_number
        self.enemies = enemies_list
        self.bg = bg_image
        self.enemies_batch = pyglet.graphics.Batch()
        for enemy in self.enemies:
            enemy.sprite.batch = self.enemies_batch

class Enemy:
    #image_file is a pyglet.resource.image()
    def __init__(self, x, y, image_file, vel_x, vel_y, idx):
        self.x = x
        self.y = y
        self.image_name = image_file
        self.image = pyglet.resource.image(image_file)
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        '''
        make sure to trim the images so collisions make sense
        '''
        self.height = self.image.height
        self.width = self.image.width
        # make self.velocity a tuple?
        # or have vx, vy
        self.vel_x = vel_x
        self.vel_y = vel_y
        # add an if block for each enemy for max_speed?
        self.max_speed = 0.5
        self.index = idx
        #eventually vel_x and vel_y will not need to be instantiated by
        # the constructor as they will be part of a basic enemy AI.
        # velocity not yet implemented
'''
make just one test level at first, then export them to a text file
'''

levels = []

level_data_file = open("level_data.txt")
level_data = level_data_file.readlines()
level_data_file.close()
line_num = 0
number_of_levels = 0

level_data[line_num] = level_data[line_num].rstrip()
# We are on the first line
unpacked = level_data[line_num].split()
number_of_levels = int(unpacked[1])
print("There are", number_of_levels, "levels")
line_num += 1

# Build the levels
for number_of_level_being_built in range(number_of_levels):
    # We are now on the "-" formatting separator line_num
    line_num += 1
    # We are now on the level number header line
    line_num += 1
    # We are now on the background image specifier line
    unpacked = level_data[line_num].split()
    bg_res = unpacked[1]
    print("This is where the bg image is at:", bg_res)
    line_num += 1
    # We are now on the number of enemies line
    unpacked = level_data[line_num].split()
    number_of_enemies = int(unpacked[1])
    print("There are", number_of_enemies, "enemies")
    line_num += 1
    # We are now on the first enemy specification line
    level_enemies = []
    for i in range(number_of_enemies):
        x, y, image_file, vel_x, vel_y = level_data[line_num].split()
        level_enemies.append(Enemy(float(x), float(y), image_file, float(vel_x), float(vel_y), i))
        print(unpacked)
        line_num += 1
    levels.append(Level(number_of_level_being_built, level_enemies, bg_res))

event_loop = pyglet.app.EventLoop()

def get_time():
    return int(round(time.time() * 1000))

clock.set_fps_limit(60)

window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)
pyglet.gl.glClearColor(1.0,1.0,1.0,1)
batch = pyglet.graphics.Batch()
################################
# ENEMIES BATCH                #
################################

image = pyglet.resource.image('vac0.png')

test_places_clicked = []


my_x = window.width/2-image.width/2
sprite = pyglet.sprite.Sprite(image, x=my_x, y=0, batch=batch)

#As per PEP8, variable names are lowercase, word-separated by underscores
#options are from 0-4 currently, with none being operation and only 0 drawn
char_options = {
        "vac":[True, False, False, False, False],
        "atk":[True, False, False, False, False],
        "def":[True, False, False, False, False]
        }
cur_char = "vac0"
# find a way to specify the weapon later

def check_state(dt):
    return True
clock.schedule(check_state)

def timed_erase_dots(dt):
    cur_time = get_time()
    idx = 0
    while idx < len(test_places_clicked):
        diff_time = cur_time-test_places_clicked[idx][2]
        if diff_time > 1000:
            test_places_clicked.pop(idx)
        else:
            idx += 1
clock.schedule(timed_erase_dots)

def move_enemy(enemy):
    enemy.x += enemy.vel_x # technically kinda pointless
    enemy.y += enemy.vel_y # this too
    enemy.sprite.x += enemy.vel_x
    enemy.sprite.y += enemy.vel_y

def move_enemy_0(enemy):
    HALF_WIDTH = WINDOW_WIDTH//2 - enemy.width//2
    if (enemy.y - 0)**2 + (enemy.x - HALF_WIDTH)**2 <= 10000:
        enemy.vel_x = 0
        enemy.vel_y = 0
    elif enemy.x == HALF_WIDTH:
        enemy.vel_y = -enemy.max_speed
        enemy.vel_x = 0
    elif enemy.y == 0:
        enemy.vel_y = 0
        if enemy.x < HALF_WIDTH:
            enemy.vel_x = enemy.max_speed
        elif enemy.x > HALF_WIDTH:
            enemy.vel_x = -enemy.max_speed
    else:
        #print(enemy.x, enemy.y)
        slope = (enemy.y - 0)/(enemy.x - HALF_WIDTH)
        tan_of_theta = 1/slope
        radians = math.atan(tan_of_theta)
        enemy.vel_y = -math.cos(radians)*enemy.max_speed
        enemy.vel_x = -math.sin(radians)*enemy.max_speed
        degrees = radians * 180.0 / math.pi


def move_enemies(dt):
    # If the current stage of the game is a shop stage then don't animate enemies.
    if is_shop:
        return
    if level_number == len(levels):
        return
    for enemy in levels[level_number].enemies:
        if enemy.image_name == "e0.png":
            move_enemy_0(enemy)
            #print(enemy.vel_x, enemy.vel_y)
            move_enemy(enemy)

clock.schedule(move_enemies)

@window.event
def on_key_press(symbol, modifiers):
    global is_shop
    #image has batch=batch so I assume batch will be modified globally too
    global sprite, batch, image, cur_char, my_x

    #fighting level
    if not is_shop:
        # move left
        if symbol == key.LEFT:
            my_x -= 15
            sprite.x = my_x
        # move right
        elif symbol == key.RIGHT:
            my_x += 15
            sprite.x = my_x
        # switch character
        # try to add animation later
        elif symbol == key.SPACE:
            # don't forget to add ".png" later
            if cur_char[:3] == "vac":
                cur_char = "atk"+str(char_options["atk"].index(True))
            elif cur_char[:3] == "atk":
                cur_char = "def"+str(char_options["def"].index(True))
            elif cur_char[:3] == "def":
                cur_char = "vac"+str(char_options["vac"].index(True))
            image = pyglet.resource.image(cur_char+".png")
            sprite = pyglet.sprite.Sprite(image, x=my_x, y=0, batch=batch)

        # This is a developer-only key. It lets you skip a level.
        elif symbol == key.ENTER:
            # It is currently a fighting stage.
            is_shop = True


@window.event
def on_mouse_press(x, y, button, modifiers):
    global is_shop, level_number
    # Fighting level
    if not is_shop:
        if button == mouse.LEFT:
            print("Left mouse button clicked during battle at ({}, {}).".format(x, y))
            test_places_clicked.append([('v2i', (x, y)), ('c3B', (0, 0, 0)), get_time()])
    # Shop level
    else:
        if button == mouse.LEFT: # (!!!) make sure you can't double click this or double-ENTER during fighting
            print("Left mouse button clicked at shop at ({}, {}).".format(x, y))
            if x >= 843 and y <= 120:
                is_shop = False
                level_number += 1


def draw_bg():
    if not is_shop:
        bg_image = pyglet.resource.image('bg'+str(level_number)+'.png')
        sprite = pyglet.sprite.Sprite(bg_image)
        sprite.draw()
        return
    bg_image = pyglet.resource.image('shop_temp.png')
    bg_sprite = pyglet.sprite.Sprite(bg_image)
    bg_sprite.draw()

@window.event
def on_draw():
    window.clear()

    # The game has ended and you've won (past last level)
    if is_shop and level_number == len(levels)-1:
        # FIX THIS
        label = pyglet.text.Label('You win!\nTHE END',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width//2, y=400,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  multiline=True,
                                  width=10)
        label.draw()
    # This is a battling level
    elif is_shop == False:
        draw_bg()
        batch.draw()
        levels[level_number].enemies_batch.draw()
        for place in test_places_clicked:
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                place[0],
                place[1]
            )
    # This is a shop level
    else:
        draw_bg()
        label = pyglet.text.Label('SHOP',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width//2, y=440,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255))
        label.draw()

pyglet.app.run()
