#use sphinx to document
#copy alex k's template
import time
import sys
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse

class Enemy:
    #image_file is a pyglet.resource.image()
    def __init__(self, x, y, image_file, velocity):
        self.x = x
        self.y = y
        self.image_file = image_file
        '''
        make sure to trim the images so collisions make sense
        '''
        self.height = self.image_file.height
        self.width = self.image_file.width
        # make self.velocity a tuple?
        self.velocity = velocity


class Level:
    #bg is a pyglet.resource.image()
    def __init__(self, level_number, enemies_list, bg_image):
        self.level = level_number
        self.enemies = enemies_list
        self.bg = bg_image

game_mode = "fight0"

'''
make just one test level at first, then export them to a text file
'''
levels = [

]
enemies_remaining = 0

event_loop = pyglet.app.EventLoop()

def get_time():
    return int(round(time.time() * 1000))
framenum = 0

clock.set_fps_limit(60)

window = pyglet.window.Window()
pyglet.gl.glClearColor(1.0,1.0,1.0,1)
batch = pyglet.graphics.Batch()

music = pyglet.resource.media('01 - Kirameki.mp3')
music.play()

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

@window.event
def on_draw():
    global framenum
    window.clear()
    label.draw()
    batch.draw()
    for place in test_places_clicked:
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
            place[0],
            place[1]
        )
    framenum += 1
    #print(framenum)
'''
@event_loop.event
def on_window_close(window):
    print("CLOSE THE DAMN WINDOW!")
    event_loop.exit()
    sys.exit()
    return pyglet.event.EVENT_HANDLED
'''
#sus
#clock.schedule_interval(on_draw, 0.1)

#event_loop.run()
pyglet.app.run()
