#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Python AI Battle
#
# Copyright 2011 Matthew Thompson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

'''
Wander Brain

This is a sample wandering brain. It just drives until it
hits an obstacle then chooses a new direction. It also changes
direction periodically.

Variables available to brains:
    color - string, tank color
    position - tuple (x,y), current tank grid position
    facing - symbol UP, DOWN, LEFT, RIGHT, current tank facing
    direction - tuple (x,y), unit vector representing tank facing
    shots - how many shots have been fired
    tanks - list of other tanks in map
    tank_positions - [(x,y)] other tank positions
    tank_states - list of other tank states (see Tank States)

Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Facings:
    UP, DOWN, LEFT, RIGHT,

Brain Commands:
    FORWARD, BACKWARD, SHOOT

Tank States:
    IDLE, MOVING, TURNING, SHOOTING, DEAD

Tiles:
    GRASS, DIRT, PLAIN, WATER
    SAFE_TILES = (GRASS, DIRT, PLAIN) - can be driven on safely
    UNSAFE_TILES = (WATER,) - will destroy your tank if you drive into them

Items:
    ROCK, TREE - blocking items that can be destroyed
    TANK_BLUE, TANK_RED - tanks located on a tile

Lookup Helper Dictionaries:
    FACING_TO_VEC - takes a facing symbol and returns the (x,y) unit vector

'''


def scan_map(game):
    # from itertools import product
    # game_map = []
    # for x, y in product(range(8), range(10)):
    #     tile = game.radar(x, y)
    #     game_map.append(tile)
    # print('MAP:', game_map)
    game_map = []
    for y in range(8):
        row = []
        for x in range(10):
            row.append(game.radar(x, y))
        game_map.append(row)
    print('MAP:', game_map)


done = False


def think(game):
    global done
    if done:
        return
    color = game.color
    print('COLOR:', color)
    position = game.position
    print('POSITION:', position)
    facing = game.facing
    print('FACING:', facing)
    direction = game.direction
    print('DIRECTION:', direction)
    # shots = game.shots
    # print('SHOTS:', shots)
    tanks = game.tanks
    print('TANKS:', tanks)
    tank_positions = game.tank_positions
    print('TANK POSITIONS:', tank_positions)
    tank_states = game.tank_states
    print('TANK STATES:', tank_states)

    # Functions available to brains:
    print('FACING TO VEC(LEFT):', game.FACING_TO_VEC[game.LEFT])
    print('RADAR:', game.radar(*position))  # get a tuple (tile, item) from the map's x,y coordinate
    game.face(game.LEFT)  # change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    game.forward()  # move tank forward one space
    game.backward()  # move tank backward one space
    game.shoot()  # fire tank's weapon with current facing
    print('MEMORY:', game.memory)  # returns [symbol], a read only copy of queued commands
    scan_map(game)
    done = True
    game.kill()  # self destruct tank
