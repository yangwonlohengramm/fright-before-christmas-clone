# hopefully the random is random enough.
from random import randrange

cur_id = 0

'''change it so enemies have to appear off screen and move in?'''

def gen0(level_number):
    if sum(enemies[level_number][:3]) <= 20:
        x = randrange(0, 1100)
        y = randrange(300, 700)
    elif sum(enemies[level_number][:3]) <= 50:
        x = randrange(-50, 1150)
        y = randrange(300, 800)
    elif sum(enemies[level_number][:3]) <= 100:
        x = randrange(-100, 1200)
        y = randrange(300, 900)
    else:
        x = randrange(-200, 1300)
        y = randrange(300, 1000)

    return (x, y, "e0.png", cur_id)

def gen1(level_number):
    if sum(enemies[level_number][:3]) <= 20:
        x = randrange(-100, 1200)
        y = randrange(300, 800)
    elif sum(enemies[level_number][:3]) <= 50:
        x = randrange(-200, 1300)
        y = randrange(300, 900)
    elif sum(enemies[level_number][:3]) <= 100:
        x = randrange(-400, 1500)
        y = randrange(300, 1100)
    else:
        x = randrange(-600, 1700)
        y = randrange(300, 1300)
    return (x, y, "e1.png", cur_id)

def gen2(level_number):
    if sum(enemies[level_number][:3]) <= 20:
        x = randrange(-200, 1300)
        y = randrange(300, 900)
    elif sum(enemies[level_number][:3]) <= 50:
        x = randrange(-600, 1700)
        y = randrange(300, 1100)
    elif sum(enemies[level_number][:3]) <= 100:
        x = randrange(-1000, 2100)
        y = randrange(300, 1400)
    else:
        x = randrange(-1400, 2500)
        y = randrange(300, 1700)
    return (x, y, "e2.png", cur_id)

def gen3(level_number):
    if enemies[level_number][3] + enemies[level_number][5]/2 <= 5:
        x = randrange(-50, 240)
    elif enemies[level_number][3] + enemies[level_number][5]/2 <= 10:
        x = randrange(-150, 240)
    else:
        x = randrange(-250, 240)
    y = 60
    return (x, y, "e3.png", cur_id)


def gen4(level_number):
    if enemies[level_number][4] + enemies[level_number][5]/2 <= 5:
        x = randrange(840, 1150)
    elif enemies[level_number][4] + enemies[level_number][5]/2 <= 10:
        x = randrange(840, 1250)
    else:
        x = randrange(840, 1350)
    y = 60
    return (x, y, "e4.png", cur_id)

def gen5(level_number):
    if sum(enemies[level_number][3:]) <= 10:
        x = randrange(0, 2)
        if x == 0:
            x = randrange(-200, 240)
        elif x == 1:
            x = randrange(840, 1300)
    elif enemies[level_number][4] + enemies[level_number][5]/2 <= 20:
        x = randrange(0, 2)
        if x == 0:
            x = randrange(-600, 240)
        elif x == 1:
            x = randrange(840, 1700)
    else:
        x = randrange(0, 2)
        if x == 0:
            x = randrange(-1000, 240)
        elif x == 1:
            x = randrange(840, 2100)
    y = 60
    return (x, y, "e5.png", cur_id)

# For other enemies make sure they are generated in particular places
# and if the whole rectangle is used make sure that you have a while in wrong
# place (near ppl) get new randrange.

def generate(level_number):
    global cur_id
    enemies_this_level = [] # Enemy list for level
    for i in range(enemies[level_number][0]):
        enemies_this_level.append(gen0(level_number))
        cur_id += 1
    for i in range(enemies[level_number][1]):
        enemies_this_level.append(gen1(level_number))
        cur_id += 1
    for i in range(enemies[level_number][2]):
        enemies_this_level.append(gen2(level_number))
        cur_id += 1
    for i in range(enemies[level_number][3]):
        enemies_this_level.append(gen3(level_number))
        cur_id += 1
    for i in range(enemies[level_number][4]):
        enemies_this_level.append(gen4(level_number))
        cur_id += 1
    for i in range(enemies[level_number][5]):
        enemies_this_level.append(gen5(level_number))
        cur_id += 1
    return enemies_this_level

#background include.

enemies = [
    (5, 0, 0, 0, 0, 0),
    (10, 5, 0, 5, 5, 0),
    (20, 10, 5, 10, 10, 0),
    (30, 20, 10, 5, 5, 0),
    (20, 20, 40, 10, 10, 0),
    (0, 0, 100, 20, 20, 0),
    (10, 10, 10, 0, 0, 5),
    (10, 10, 100, 20, 20, 10)
]
