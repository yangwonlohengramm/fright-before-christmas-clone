# Documentation

## Overall File Structure

There are four python files in my project.

* ***test.py*** is the main file that is run to start the game.

* ***move.py***  contains functions to change the velocity and position of `Enemy` objects.

* ***gen.py*** handles the generation of level data, which is primarily the number and types of enemies. This is passed directly to *test.py*.

* ***const.py*** contains some constants and functions that are used in multiple contexts to reduce code clutter from *test.py*.

 * Unfortunately, this led to some redundancies in code, and some inconsistencies, as some pieces of code that could belong in *const.py* are instead in *test.py*.

## Overview of Classes

There are three main classes in *test.py*.

* **`Level`**: This contains information about a given level of the game. This does not include the shop level and win/lose states, which are other screens displayed during certain points in the game. The information stored in a `Level` object are the list of `Enemy`s in the level, the list of `Projectile`s in the level, the background image, and various other data.

* **`Enemy`**: This contains information about an enemy, including its position, velocity, time last frozen, image, and batch. The batch is a property that sprites have. Each batch, or group of sprites is drawn as its group. A sprite is an image with position information and other data.

 * There are many subclasses for the different types of enemies, including `GreenWing`, `RedWing`, `BlueWing`, etc.

* **`Projectile`**: This contains information about a projectile, which at this point can be either a `Bomb` object or a `FrostPotion` object (subclasses). The type of information stored is similar to the data stored in an `Enemy` object.

In `Enemy`, there is the `change_colour` function.

* `change_colour` changes the colour of an Enemy. Specifically, it inverts the colour (except for the black outline). This occurs when an enemy impacts the centre forcefield.

In `Projectile`, there is the `apply_movement` function.

* `apply_movement` applies the velocity of the object to change the position.

## Overview of Functions

Most of the functions are self-explanatory by their name, although they are very poorly documented by corporate and scholastic standards. Here is a brief overview of some of the main functions:

* `on_draw()` draws one of four screens: A battle screen with animations, a shop screen where you can purchase upgrades, a win screen, and a lose screen.

* `apply_damage(dt)` is scheduled to run whenever the clock ticks and it adds the amount of health that the player regenerates per tick but subtracts the amount of damage that enemies encroaching on the force field barrier deal.

* `on_mouse_press()` handles the clicking that the player does. This can either create a projectile (in the battle game state) or indicate which items you wish to buy (in the shop).

* `on_key_press()` handles the keys pressed on the keyboard. The only key that is required to play the game properly (and the only keyboard button that *should* be used in gameplay) is the spacebar.

* `move_all(dt)` is scheduled by the clock and moves all of the enemies.

* `remove_out_of_window_projectiles()` removes projectiles that have gone outside of the screen.

* `enemy_projectile_collision(dt):` is scheduled by the clock and checks for collisions between enemies and projectiles, with different results for different types of projectiles.

* Finally, `for number_of_level_being_built in range(number_of_levels):` is not a function, but it is another important block of code, as it is what grabs the data from *gen.py* and translates it into the objects recognized by *test.py*.

## Pyglet Game Engine

The Pyglet Game Engine is built off of Pygame, and is a higher-level version of Pygame.

The game begins when `pyglet.app.run()` is called, and from then, functions with a `@<event>` decorator are called only when the given `<event>` occurs. Otherwise, nothing happens in the game. The `<event>` could be a key press or a mouse click, for example.

The only other time the program runs a piece of code is when the clock, which automatically comes into play with `from pyglet import clock`, is scheduled to run certain functions with the following command: `clock.schedule(<function_name>)`. This is how the animation was handled.
