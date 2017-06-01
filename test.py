#use sphinx to document
#copy alex k's template
import time
import sys
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

enemies_remaining = 0

level_number = 0


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
    def __init__(self, x, y, image_file, vel_x, vel_y):
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
        #eventually vel_x and vel_y will not need to be instantiated by
        # the constructor as they will be part of a basic enemy AI.
        # velocity not yet implemented



game_mode = "fight0"

'''
make just one test level at first, then export them to a text file
'''

level_data_file = open("level_data.txt")
level_data = level_data_file.readlines()
level_data_file.close()
line_num = 0
while line_num < len(level_data):
    level_data[line_num] = level_data[line_num].rstrip()
    print(level_data[line_num])
    line_num += 1

levels = [
    Level(0, [
        Enemy(100, 100, "e0.png", 0, -1),
        Enemy(200, 100, "e0.png", 0, -1),
        Enemy(300, 100, "e0.png", 0, -1),
        Enemy(400, 100, "e0.png", 0, -1),
        Enemy(500, 100, "e0.png", 0, -1)
    ], "bg0.png")
]

event_loop = pyglet.app.EventLoop()

def get_time():
    return int(round(time.time() * 1000))
framenum = 0

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
print(sprite.width, sprite.height)

label = pyglet.text.Label('Tower Defense(??) START!',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                          color=(0, 0, 0, 255))

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

def move_enemies(dt):
    for enemy in levels[level_number].enemies:
        enemy.x += enemy.vel_x # technically kinda pointless
        enemy.y += enemy.vel_y # this too
        enemy.sprite.x += enemy.vel_x
        enemy.sprite.y += enemy.vel_y
clock.schedule(move_enemies)

@window.event
def on_key_press(symbol, modifiers):
    #image has batch=batch so I assume batch will be modified globally too
    global sprite, batch, image, cur_char, my_x
    print("A key was pressed")
    print(symbol, modifiers)

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

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print("Left mouse button clicked at ({}, {}).".format(x, y))
        test_places_clicked.append([('v2i', (x, y)), ('c3B', (0, 0, 0)), get_time()])

def draw_bg(level_number):
    bg_image = pyglet.resource.image('bg'+str(level_number)+'.png')
    sprite = pyglet.sprite.Sprite(bg_image)
    sprite.draw()

@window.event
def on_draw():
    global framenum
    window.clear()
    draw_bg(level_number)
    label.draw()
    batch.draw()
    levels[level_number].enemies_batch.draw()
    for place in test_places_clicked:
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
            place[0],
            place[1]
        )
    framenum += 1

pyglet.app.run()
