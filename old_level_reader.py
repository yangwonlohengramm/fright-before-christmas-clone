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
line_num += 1

'''
I don't need vel_x vel_y input anymore, but different enemies need different things
BRUH MAKE SUBCLASSES FOR EACH ENEMY???? :O :O
'''

''' may have minor bugs since the copy+paste was kinda messed '''
for number_of_level_being_built in range(number_of_levels):
    # We are now on the "-" formatting separator line_num
    line_num += 1
    # We are now on the level number header line
    line_num += 1
    # We are now on the background image specifier line
    unpacked = level_data[line_num].split()
    bg_res = unpacked[1]
    #print("This is where the bg image is at:", bg_res)
    line_num += 1
    # We are now on the number of enemies line
    unpacked = level_data[line_num].split()
    number_of_enemies = int(unpacked[1])
    #print("There are", number_of_enemies, "enemies")
    line_num += 1
    # We are now on the first enemy specification line
    level_enemies = []
    for i in range(number_of_enemies):
        splist = level_data[line_num].split()
        x, y, image_file = splist[0], splist[1], splist[2]
        if image_file == "e0.png":
            level_enemies.append(GreenWing(float(x), float(y), image_file, cur_id))
        elif image_file == "e1.png":
            level_enemies.append(RedWing(float(x), float(y), image_file, cur_id))
        #cur_id += 1
        #print(unpacked)
        line_num += 1
    levels.append(Level(number_of_level_being_built, level_enemies, bg_res))
