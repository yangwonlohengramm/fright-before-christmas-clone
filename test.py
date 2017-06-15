#use sphinx to document
#copy alex k's template
#Reminder than Pyglet CAN handle decimal (float) speeds/coordinates.
#540 641 164

# Currently I have manually drawn a safe space on each level background.

#make get wole more expensive

'''
Make sure the game states (win, lose, store, battle 0->n) don't conflict with
each other!
'''

import time
import sys
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse
import math
import move # my own file!
import const
import gen

# images (some are in const.py)
# These are for before the enemies come into contact with forcefield
enemy_pics = [
    pyglet.resource.image("e0.png"),
    pyglet.resource.image("e1.png"),
    pyglet.resource.image("e2.png"),
    pyglet.resource.image("e3.png"),
    pyglet.resource.image("e4.png"),
    pyglet.resource.image("e5.png")
]



no_batch = pyglet.graphics.Batch()
''' ENEMY_DAMAGE used to be 0.1 but now it's 0 for testing the projectiles '''
'''




'''
#all enemies do same dps for now/ever?
ENEMY_DAMAGE = 0.2

class Level:
    #bg is a pyglet.resource.image()
    def __init__(self, level_number, enemies_list, bg_image):
        self.level = level_number
        self.enemies = enemies_list
        #self.bg and bg_image are strings
        self.bg = bg_image
        self.enemies_batch = pyglet.graphics.Batch()
        self.projectile_batch = pyglet.graphics.Batch()
        self.projectiles = []
        for enemy in self.enemies:
            enemy.sprite.batch = self.enemies_batch

'''
If an enemy is destroyed change the batch of the sprite to something else.
'''

class Enemy:
    #image_file is a pyglet.resource.image()
    def __init__(self, x, y, image_name, my_id):
        self.x = x
        self.y = y
        self.image_name = image_name
        '''
        make sure to trim the images so collisions make sense
        '''
        # make self.velocity a tuple?
        # or have vx, vy
        self.vel_x = 0
        self.vel_y = 0
        self.id = my_id
        self.freeze_time = 0
        '''
        Eventually I could have a health instead of just alive or dead
        '''
        self.alive = True
        self.sprite = pyglet.sprite.Sprite(enemy_pics[0], x=self.x, y=self.y) # temp, changed in subclass
        #eventually vel_x and vel_y will not need to be instantiated by
        # the constructor as they will be part of a basic enemy AI.
        # velocity not yet implemented
        self.ice_sprite = pyglet.sprite.Sprite(pyglet.resource.image("ice.png"), x=self.x-20, y=self.y-80, batch=no_batch)
        '''sketch ^^^'''

    def __eq__(self, other):
        return self.id == other.id

    def change_colour(self):
        name, extension = self.image_name.split(".")
        #print(name, extension)
        if name[-1] == "i":
            new_name = name[:len(name)-1]+"."+extension
            self.sprite.image = pyglet.resource.image(new_name)
            self.image_name = new_name
        else:
            new_name = name+"i."+extension
            self.sprite.image = pyglet.resource.image(new_name)
            self.image_name = new_name

class GreenWing(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[0]
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 1.0
        self.value = 1

class RedWing(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[1] #preloaded
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 2.0
        self.value = 2

class BlueWing(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[2] #preloaded
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 4.0
        self.value = 3

class LeftFoot(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[3] #preloaded
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 1
        self.value = 1

class RightFoot(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[4] #preloaded
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 1
        self.value = 1

# bird that cannot walk
class PinkBird(Enemy):
    def __init__(self, x, y, image_name, my_id):
        super().__init__(x, y, image_name, my_id)
        self.image = enemy_pics[5] #preloaded
        self.height = self.image.height
        self.width = self.image.width
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                            y=self.y)
        self.max_speed = 8
        self.value = 3

class Projectile:
    last_time = 0

    def __init__(self, x, y, image, my_id): #add index parameter?
        global last_time
        '''
        Projectile differs from Enemy in that Projectile is directly passed a
        Pyglet image whereas Enemy is passed an image name.
        '''
        '''
        x and y are different from actual sprite.x and sprite.y
        '''
        self.x = x
        self.y = y
        self.image = image
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y)
        self.height = self.image.height
        self.width = self.image.width
        self.vel_x = 0
        self.vel_y = 0
        self.id = my_id

    def apply_movement(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.sprite.x += self.vel_x
        self.sprite.y += self.vel_y

    def __eq__(self, other):
        return self.id == other.id

class Bomb(Projectile):
    def __init__(self, x, y, image, my_id):
        super().__init__(x, y, image, my_id)
        self.dest_x = x
        self.dest_y = y
        self.x = const.BOMB_X
        self.y = const.BOMB_Y
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.SPEED = 20


    # should only be called once, when the bomb is created
    def update_velocity(self):
        HALF_WIDTH = const.WINDOW_WIDTH//2 - self.width//2

        if (const.BOMB_X+self.width/2) - self.dest_x == 0:
            self.vel_x = 0
            self.vel_y = self.SPEED
        elif (const.BOMB_Y+self.height/2) - self.dest_y == 0:
            if self.dest_x <= const.BOMB_X:
                ''' note the equals '''
                self.vel_x = -self.SPEED
                self.vel_y = 0
            elif self.dest_x > const.BOMB_X:
                self.vel_x = self.SPEED
                self.vel_y = 0
        else:
            '''
            ATAN2 IS FUCKING BLESSED!!!!
            '''
            '''(x+width/2, y+height/2) is the centre of the projectile image'''
            dy = self.dest_y - (const.BOMB_Y+self.height/2)
            dx = self.dest_x - (const.BOMB_X+self.width/2)
            #print(dx, dy)
            '''
            I have no idea why adding math.pi/2 would work. It's a temporary
            (read: permanent) workaround.
            '''
            radians = math.atan2(dy, dx)# + math.pi/2
            self.vel_y = math.sin(radians)*self.SPEED
            self.vel_x = math.cos(radians)*self.SPEED
            degrees = radians * 180.0 / math.pi
            #print(degrees)

class FrostPotion(Projectile):
    def __init__(self, x, y, image, my_id):
        super().__init__(x, y, image, my_id)
        self.dest_x = x
        self.dest_y = y
        self.x = const.FROST_POTION_X
        self.y = const.FROST_POTION_Y
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.SPEED = 20


    # should only be called once, when the bomb is created
    def update_velocity(self):
        HALF_WIDTH = const.WINDOW_WIDTH//2 - self.width//2

        if (const.FROST_POTION_X+self.width/2) - self.dest_x == 0:
            self.vel_x = 0
            self.vel_y = self.SPEED
        elif (const.FROST_POTION_Y+self.height/2) - self.dest_y == 0:
            if self.dest_x <= const.BOMB_X:
                ''' note the equals '''
                self.vel_x = -self.SPEED
                self.vel_y = 0
            elif self.dest_x > const.BOMB_X:
                self.vel_x = self.SPEED
                self.vel_y = 0
        else:
            '''
            ATAN2 IS FUCKING BLESSED!!!!
            '''
            '''(x+width/2, y+height/2) is the centre of the projectile image'''
            dy = self.dest_y - (const.FROST_POTION_Y+self.height/2)
            dx = self.dest_x - (const.FROST_POTION_X+self.width/2)
            #print(dx, dy)
            '''
            I have no idea why adding math.pi/2 would work. It's a temporary
            (read: permanent) workaround.
            '''
            radians = math.atan2(dy, dx)# + math.pi/2
            self.vel_y = math.sin(radians)*self.SPEED
            self.vel_x = math.cos(radians)*self.SPEED
            degrees = radians * 180.0 / math.pi
            #print(degrees)


levels = []

number_of_levels = len(gen.enemies)
for number_of_level_being_built in range(number_of_levels):
    bg_res = "bg"+str(number_of_level_being_built%3)+".png"
    ''' change the above soon '''
    number_of_enemies = sum(gen.enemies[number_of_level_being_built])
    level_enemies = gen.generate(number_of_level_being_built)
    for i in range(number_of_enemies):
        #print(number_of_level_being_built, i, level_enemies[i])
        if level_enemies[i][2] == "e0.png":
            level_enemies[i] = GreenWing(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
        elif level_enemies[i][2] == "e1.png":
            level_enemies[i] = RedWing(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
        elif level_enemies[i][2] == "e2.png":
            level_enemies[i] = BlueWing(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
        elif level_enemies[i][2] == "e3.png":
            level_enemies[i] = LeftFoot(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
        elif level_enemies[i][2] == "e4.png":
            level_enemies[i] = RightFoot(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
        elif level_enemies[i][2] == "e5.png":
            level_enemies[i] = PinkBird(level_enemies[i][0], level_enemies[i][1], level_enemies[i][2], level_enemies[i][3])
    levels.append(Level(number_of_level_being_built, level_enemies, bg_res))

event_loop = pyglet.app.EventLoop()

def rect_collide(x1l, x1r, y1d, y1u, x2l, x2r, y2d, y2u):
    #(x1, y1) bottom left (x2, y2) top right, for the first rectangle

    if (x1r >= x2l + const.COLLISION_ENTRY and x1l <= x2r - const.COLLISION_ENTRY
        and y1u >= y2d + const.COLLISION_ENTRY and y1d <= y2d - const.COLLISION_ENTRY):
        return True
    return False

# https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
# Currently unused
def mozilla_rect_collide(x1l, x1r, y1d, y1u, x2l, x2r, y2d, y2u):
    w1 = x1r-x1l
    h1 = y1u-y1d
    w2 = x2r-x2l
    h2 = y2u-y2d
    return x1l < x2l + w2 and x1l + w1 > x2l and y1d < y2d + h2 and h1 + y1d > y2d

def get_time():
    return int(round(time.time() * 1000))

clock.set_fps_limit(60)

window = pyglet.window.Window(width = const.WINDOW_WIDTH, height = const.WINDOW_HEIGHT)
pyglet.gl.glClearColor(1.0,1.0,1.0,1)
batch = pyglet.graphics.Batch()

ice_batch = pyglet.graphics.Batch()

image = pyglet.resource.image('atk0.png')

test_places_clicked = []

####################
# PLAYER CHARACTER #
####################
my_x = window.width/2-image.width/2
my_y = const.CHARACTER_VERT
sprite = pyglet.sprite.Sprite(image, x=my_x, y=my_y, batch=batch)

#As per PEP8, variable names are lowercase, word-separated by underscores
#options are from 0-4 currently, with none being operation and only 0 drawn
char_options = {
        "vac":[True, False, False, False, False],
        "atk":[True, False, False, False, False],
        "def":[True, False, False, False, False]
        }
vac_equip = 0
atk_equip = 0
def_equip = 0
cur_char = "atk" + str(atk_equip)

def enemy_projectile_collision(dt):
    if level_number >= len(levels):
        return

    global is_shop, punch_time, coins, is_win

    #ATTACK
    remove_enemies = []
    remove_projectiles = []

    for projectile in levels[level_number].projectiles:
        if projectile.image != const.BOMB_IMAGE:
            continue
        closest_dist = 10000000
        corresponding_enemy = -1
        if projectile in remove_projectiles:
            continue
        for enemy in levels[level_number].enemies:
            if enemy in remove_projectiles: continue
            #make sure rect_collide isn't too sketchy... it seems to
            #brush past the legs of e0.png without collision
            #fuck it i'm trying mozilla_rect_collide

            ''' If statement checks:
                    - If collision occurs
                    - If the enemy is closer to the projectile than another
                    enemy collided with the projectile
                    - If the collision happened on the screen
            '''
            if (mozilla_rect_collide(enemy.x, enemy.x+enemy.width,
                enemy.y, enemy.y+enemy.height,
                projectile.x, projectile.x+projectile.width,
                projectile.y, projectile.y+projectile.height)
                and ((enemy.y+enemy.height/2)-(projectile.y+projectile.height/2))**2+
                ((enemy.x+enemy.width)-(projectile.x+projectile.width))**2 < closest_dist
                and -enemy.width <= enemy.x <= const.WINDOW_WIDTH
                and enemy.y <= const.WINDOW_HEIGHT):
                    closest_dist = (((enemy.y+enemy.height/2)-(projectile.y+projectile.height/2))**2+
                    ((enemy.x+enemy.width)-(projectile.x+projectile.width))**2)
                    corresponding_enemy = enemy
        if isinstance(corresponding_enemy, Enemy):
            remove_projectiles.append(projectile)
            remove_enemies.append(corresponding_enemy)
            '''
            recreate a player for each time.
            '''
    if len(remove_enemies) != 0:
        player.seek(0.0)
        player.play()
        punch_time = int(round(time.time() * 1000))
    for enemy in remove_enemies:
        # quick fix for ValueError: list.remove(x): x not in list:
        ''' I thought I fixed this tho!!! '''
        if enemy not in levels[level_number].enemies:
            continue
        coins += enemy.value
        levels[level_number].enemies.remove(enemy)
    for projectile in remove_projectiles:
        levels[level_number].projectiles.remove(projectile)

    if len(levels[level_number].enemies) == 0:
        next_level_setup()

    #DEFENCE
    frozen_enemies = []
    remove_projectiles = []

    for projectile in levels[level_number].projectiles:
        if projectile.image != const.FROST_IMAGE:
            continue
        if projectile in remove_projectiles:
            continue
        for enemy in levels[level_number].enemies:
            #make sure rect_collide isn't too sketchy... it seems to
            #brush past the legs of e0.png without collision
            #fuck it i'm trying mozilla_rect_collide

            ''' If statement checks:
                    - If collision occurs
                    - If the enemy is closer to the projectile than another
                    enemy collided with the projectile
                    - If the collision happened on the screen
            '''
            if (mozilla_rect_collide(enemy.x, enemy.x+enemy.width,
                enemy.y, enemy.y+enemy.height,
                projectile.x, projectile.x+projectile.width,
                projectile.y, projectile.y+projectile.height)
                and -enemy.width <= enemy.x <= const.WINDOW_WIDTH
                and enemy.y <= const.WINDOW_HEIGHT):
                for enemy2 in levels[level_number].enemies:
                    if (((enemy2.x+enemy2.width/2) - (projectile.x+projectile.width/2))**2
                        + ((enemy2.y+enemy2.height/2) - (projectile.y+projectile.height/2))**2
                        <= 10000):
                        frozen_enemies.append(enemy2)
                        remove_projectiles.append(projectile)

    ice_time = get_time()
    if len(frozen_enemies) != 0:
        ice_player.seek(0.0)
        '''audible?^^'''
        ice_player.play()
    for enemy in frozen_enemies:
        if enemy not in levels[level_number].enemies:
            continue
        idx = levels[level_number].enemies.index(enemy)
        levels[level_number].enemies[idx].freeze_time = ice_time
    done = []
    for projectile in remove_projectiles:
        if projectile in done:
            continue
        done.append(projectile)
        levels[level_number].projectiles.remove(projectile)

clock.schedule(enemy_projectile_collision)

def timed_erase_dots(dt):
    cur_time = get_time()
    idx = 0
    while idx < len(test_places_clicked):
        diff_time = cur_time-test_places_clicked[idx][2]
        if diff_time > 1000:
            test_places_clicked.pop(idx)
        else:
            idx += 1
#####
# clock.schedule(timed_erase_dots)
#####

def remove_out_of_window_projectiles():
    # The following removes projectiles that are outside the window.
    # This should save some CPU/memory in extreme scenarios.
    remove_projectiles = []
    for projectile in levels[level_number].projectiles:
        projectile.apply_movement()
        if (projectile.x + projectile.width < 0
            or projectile.x > const.WINDOW_WIDTH
            or projectile.y > const.WINDOW_HEIGHT
            or projectile.y + projectile.height < 0):
                remove_projectiles.append(projectile)
    for projectile in remove_projectiles:
        levels[level_number].projectiles.remove(projectile)

def move_all(dt):
    if is_game_over:
        return
    if is_shop:
        return
    if level_number == len(levels):
        return
    for enemy in levels[level_number].enemies:
        if enemy.alive == False:
            continue

        # Changes the velocity of the enemy

        # line motion
        if enemy.image_name in ["e0.png", "e1.png", "e2.png"]:
            move.move_enemy_line(enemy)
        elif enemy.image_name in ["e3.png", "e4.png", "e5.png"]:
            move.move_enemy_hori(enemy)

        # Actually applies the velocity to the position
        move.move_enemy(enemy)
    remove_out_of_window_projectiles()
clock.schedule(move_all)

@window.event
def on_key_press(symbol, modifiers):
    global is_shop
    #image has batch=batch so I assume batch will be modified globally too
    global sprite, batch, image, cur_char, my_x, coins

    # cheat
    if symbol == key.BACKSPACE:
        coins += 100

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
                cur_char = "def"+str(char_options["def"].index(True))
            elif cur_char[:3] == "atk":
                cur_char = "vac"+str(char_options["vac"].index(True))
            elif cur_char[:3] == "def":
                cur_char = "atk"+str(char_options["atk"].index(True))
            image = pyglet.resource.image(cur_char+".png")
            sprite = pyglet.sprite.Sprite(image, x=my_x, y=my_y, batch=batch)

        # This is a developer-only key. It lets you skip a level.
        elif symbol == key.ENTER:
            # It is currently a fighting stage.
            next_level_setup()

def add_projectile_a0(x, y):
    #print("---- ({}, {})".format(x, y))
    levels[level_number].projectiles.append(Bomb(x-const.BOMB_WIDTH/2, y-const.BOMB_HEIGHT/2, const.BOMB_IMAGE, gen.cur_id))
    gen.cur_id += 1
    bomb = levels[level_number].projectiles[-1]
    bomb.sprite.batch = levels[level_number].projectile_batch
    bomb.update_velocity()

def add_projectile_d0(x, y):
    #print("---- ({}, {})".format(x, y))
    levels[level_number].projectiles.append(FrostPotion(x-const.FROST_POTION_WIDTH/2, y-const.FROST_POTION_HEIGHT/2, const.FROST_IMAGE, gen.cur_id))
    gen.cur_id += 1
    frost_potion = levels[level_number].projectiles[-1]
    frost_potion.sprite.batch = levels[level_number].projectile_batch
    frost_potion.update_velocity()

def can_fire():
    #cur_time = get_time()
    #print(cur_time, Projectile.last_time, cur_time-Projectile.last_time, RELOAD_TIME)
    return get_time() - Projectile.last_time >= RELOAD_TIME

def auto_character_change(dt):
    ''' AUTO-CHANGE CHARACTER SKINS '''
    if can_fire() and cur_char[:3] in ["atk", "def"]:
        if cur_char[:3] == "atk":
            ''' make it so that i don't have to create an image each frame THIS IS SO INEFFICIENT'''
            sprite.image = pyglet.resource.image(cur_char[:3]+str(atk_equip)+"i.png")
        elif cur_char[:3] == "def":
            sprite.image = pyglet.resource.image(cur_char[:3]+str(def_equip)+"i.png")
    else:
        if cur_char[:3] == "atk":
            sprite.image = pyglet.resource.image(cur_char[:3]+str(atk_equip)+".png")
        elif cur_char[:3] == "def":
            sprite.image = pyglet.resource.image(cur_char[:3]+str(def_equip)+".png")
        elif cur_char[:3] == "vac":
            sprite.image = pyglet.resource.image(cur_char[:3]+str(vac_equip)+".png")
clock.schedule(auto_character_change)

def add_projectile(x, y):
    #print("-- ({}, {})".format(x, y))
    ''' CURRENTLY THIS ONLY USES THE X-VALUE TO DETERMINE SAFE-SPACE COLLISIONS '''
    #if const.in_safe_space(x, y, const.DIMENSIONS[cur_char][0]):
    #    return
    # I want to shoot even if I'm slightly in the safe sapce
    '''change this to automate adding more weapons'''
    if cur_char[3] == "0":
        object_width = 15
    HALF_WIDTH = const.WINDOW_WIDTH/2 - object_width/2
    if (y - const.BOTTOM_BORDER)**2 + (x - HALF_WIDTH)**2 <= const.DANGER_RADIUS/4:
        return
    if not can_fire():
        return
    Projectile.last_time = get_time()
    if cur_char[:3] == "atk":
        if cur_char[3] == "0":
            add_projectile_a0(x, y)
    elif cur_char[:3] == "def":
        if cur_char[3] == "0":
            add_projectile_d0(x, y)

@window.event
def on_mouse_press(x, y, button, modifiers):
    '''
    Increments level_number.
    '''
    global is_shop, cur_char, is_win, health, max_health, coins
    # Fighting level
    if not is_shop:
        if button == mouse.LEFT:
            #print("Left mouse button clicked during battle at ({}, {}).".format(x, y))
            #test_places_clicked.append([('v2i', (x, y)), ('c3B', (0, 0, 0)), get_time()])
            if cur_char[:3] in ["atk", "def"]:
                add_projectile(x, y)


    # Shop level
    elif is_shop:
        global level_number
        '''
        potion is 160x160
        21, 700 to 150, 540 (have to translate from gimp coords to pyglet coords)
        '''
        if button == mouse.LEFT: # (!!!) make sure you can't double click this or double-ENTER during fighting
            print("Left mouse button clicked at shop at ({}, {}).".format(x, y))
            POTION_COST = 10
            SWOLE_COST = 50
            if x >= 843 and y <= 120:
                is_shop = False
                level_number += 1
            elif 11 <= x <= 171 and 27 <= y <= 186:
                if coins < POTION_COST:
                    print("You don't have enough money.")
                elif health == max_health:
                    print("Your health is already full!")
                else:
                    health = min(health+20, max_health)
                    coins -= POTION_COST
            elif 187 <= x <= 346 and 27 <= y <= 185:
                if coins < SWOLE_COST:
                    print("You don't have enough money.")
                elif max_health == MAX_MAX_HEALTH:
                    print("You are already at the maximum amount of maximum health.")
                else:
                    max_health += 50
                    coins -= SWOLE_COST

def draw_bg():
    if is_game_over:
        bg_image = pyglet.resource.image("lose.png")
    elif is_win:
        bg_image = pyglet.resource.image("win.png")
    elif not is_shop: # battle
        #automated version below assuming bg0.png to bg#.png are ready
        #bg_image = pyglet.resource.image('bg'+str(level_number)+'.png')
        bg_image = pyglet.resource.image(levels[level_number].bg)
    else:
        bg_image = pyglet.resource.image('shop_temp.png') # shop
    bg_sprite = pyglet.sprite.Sprite(bg_image)
    bg_sprite.draw()

def draw_health_bar(X_POS, Y_POS):
    # Create sprites
    black_bar_image = pyglet.resource.image("black.png")
    black_bar_image.width=max_health*BAR_WIDTH_MULTIPLIER+BLACK_PADDING*2
    black_bar_image.height=BAR_HEIGHT+BLACK_PADDING*2
    black_bar_sprite = pyglet.sprite.Sprite(black_bar_image, x=X_POS-BLACK_PADDING, y=Y_POS-BLACK_PADDING)

    red_bar_image = pyglet.resource.image("red.png")
    red_bar_image.width=max_health*BAR_WIDTH_MULTIPLIER
    red_bar_image.height=BAR_HEIGHT
    red_bar_sprite = pyglet.sprite.Sprite(red_bar_image, x=X_POS, y=Y_POS)

    green_bar_image = pyglet.resource.image("green.png")
    green_bar_image.width=health*BAR_WIDTH_MULTIPLIER
    green_bar_image.height=BAR_HEIGHT
    green_bar_sprite = pyglet.sprite.Sprite(green_bar_image, x=X_POS, y=Y_POS)

    black_bar_sprite.draw()
    red_bar_sprite.draw()
    green_bar_sprite.draw()

'''
for now I'll do damage per frame but eventually I'll record the last damage
time per enemy so I can do damage per second or a smaller, regular time period
'''

def next_level_setup():
    global cur_char, is_shop, is_win
    cur_char = "atk" + str(atk_equip)
    sprite.image = pyglet.resource.image(cur_char+".png")
    levels[level_number].projectiles = [] # save memory/CPU?

    #increment level number after clicking shop button
    if level_number+1 < len(levels):
        is_shop = True
    else:
        is_win = True

def stop_sound(dt):
    t = int(round(time.time() * 1000))
    if t > punch_time + 585:
        player.pause()
    t = int(round(time.time() * 1000))
    if t > ice_time + 510:
        ice_player.pause()
clock.schedule(stop_sound)

millis = int(round(time.time() * 1000))
def apply_damage(dt):
    global millis, health, is_game_over
    if is_shop:
        return
    if is_game_over:
        return
    if is_win:
        return
    # what are the other game states that are not battle?
    for enemy in levels[level_number].enemies:
        if get_time() - enemy.freeze_time < 2000:
            continue
        #print(int(round(time.time() * 1000)) - millis)
        if enemy.image_name in ["e0.png", "e1.png", "e2.png", "e0i.png", "e1i.png", "e2i.png"]:
            HALF_WIDTH = const.WINDOW_WIDTH//2 - enemy.width//2
            if const.in_safe_space(enemy.x, enemy.y, enemy.width):
                enemy.change_colour()
                health -= ENEMY_DAMAGE
        elif enemy.image_name in ["e3.png", "e4.png", "e5.png", "e3i.png", "e4i.png", "e5i.png"]:
            if const.HORI_LEFT <= enemy.x <= const.HORI_RIGHT:
                enemy.change_colour()
                health -= ENEMY_DAMAGE
        if health <= 0:
            is_game_over = True
        #millis = int(round(time.time() * 1000))
clock.schedule(apply_damage)

@window.event
def on_draw():
    window.clear()
    draw_bg()
    # You lost (add menu options later)
    if is_game_over:
        label = pyglet.text.Label('You lose!\nTHE END',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width//2, y=400,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  multiline=True,
                                  width=10)
        label.draw()

    # The game has ended and you've won (past last level)
    elif is_win:
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
        batch.draw()
        levels[level_number].enemies_batch.draw()
        for enemy in levels[level_number].enemies:
            enemy.ice_sprite.x = enemy.x-25
            enemy.ice_sprite.y = enemy.y-25
            if get_time() - enemy.freeze_time < 2000:
                enemy.ice_sprite.batch = ice_batch
            else:
                enemy.ice_sprite.batch = no_batch
        ice_batch.draw()
        '''
        for place in test_places_clicked:
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                place[0],
                place[1]
            )
        '''
        # health bar
        X_POS = const.WINDOW_WIDTH//2-max_health*BAR_WIDTH_MULTIPLIER//2
        Y_POS = 30
        draw_health_bar(X_POS, Y_POS)
        levels[level_number].projectile_batch.draw()

        coin_label = pyglet.text.Label('Money: {}'.format(coins),
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=700, y=14,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  bold=True)
        coin_label.draw()

        level_label = pyglet.text.Label('LEVEL {}'.format(level_number+1),
                                  font_name='Times New Roman',
                                  font_size=20,
                                  x=const.WINDOW_WIDTH/2, y=700,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  bold=True)
        level_label.draw()

    # This is a shop level
    else:
        X_POS = 82
        Y_POS = 6
        draw_health_bar(X_POS, Y_POS)

        health_label = pyglet.text.Label('Health',
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=16, y=14,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  multiline=True,
                                  width=10,
                                  bold=True)
        health_label.draw()

        coin_label = pyglet.text.Label('Money: {}'.format(coins),
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=700, y=14,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  bold=True)
        coin_label.draw()

        level_label = pyglet.text.Label('Congrats! You just beat level {}!'.format(level_number+1),
                                  font_name='Impact',
                                  font_size=40,
                                  x=const.WINDOW_WIDTH/2, y=680,
                                  anchor_x='center', anchor_y='center',
                                  color=(0, 0, 0, 255),
                                  bold=True)
        level_label.draw()





punch_sound = pyglet.resource.media('strong-punch.wav', streaming = False)
player = pyglet.media.Player()
player.queue(punch_sound)
player.eos_action = player.EOS_LOOP
punch_time = 0

ice_sound = pyglet.resource.media('ice.wav', streaming = False)
ice_player = pyglet.media.Player()
ice_player.queue(ice_sound)
ice_player.eos_action = player.EOS_LOOP
ice_time = 0

# GAME STATE
level_number = 0
coins = 0
is_shop = False
is_win = False
is_game_over = False

# HEALTH
BAR_WIDTH_MULTIPLIER=1
BAR_HEIGHT = 12
BLACK_PADDING = 2
health = 100
max_health = 100
MAX_MAX_HEALTH = 500

# bg music
fight_music = pyglet.resource.media('epic2.wav', streaming = False)
fight_player = pyglet.media.Player()
fight_player.queue(fight_music)
fight_player.eos_action = player.EOS_LOOP
fight_player.play()

RELOAD_TIME = 500



pyglet.app.run()
