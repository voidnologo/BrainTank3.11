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

import sys, traceback
from copy import deepcopy
from utils import DebugWriter
from symbols import Tile, Item, Facing, TankState, Command, FACING_TO_VEC
from imp import load_source
import config


class Brain:
    '''The Brain is your primary interface to write a custom tank AI.'''

    def __init__(self, tank):
        self.tank = tank
        self.tank.brain = self

        self.memory = []

    def detach(self):
        '''Detach brain in preparation for attaching a new one.'''
        self.tank.brain = None
        self.tank = None

    def forget(self):
        '''Forget (clear) saved command queue'''
        self.memory = []

    def pop(self):
        '''Return and remove the first command in the queue.'''
        if len(self.memory):
            return self.memory.pop(0)
        else:
            return None

    def face(self, facing):
        '''Queue the command to change to a certain facing.'''
        if facing in Facing.values:
            self.memory.append(facing)
        else:
            raise Exception('brain malfunction', facing)

    def forward(self):
        '''Queue the command to move the tank forward.
        The direction depends on the tank's current facing.'''
        self.memory.append(Command.FORWARD)

    def backward(self):
        '''Queue the command to move the tank backward.
        The direction depends on the tank's current facing.'''
        self.memory.append(Command.BACKWARD)

    def shoot(self):
        '''Queue a shoot command.
        The direction depends on the tank's current facing.'''
        self.memory.append(Command.SHOOT)

    def position(self):
        '''Return the (x,y) coordinate of the tank.'''
        return self.tank.get_position()

    def facing(self):
        '''Return the facing of the tank.
        It returns Facing.UP, Facing.DOWN, etc.'''
        return self.tank.get_facing()

    def direction(self):
        '''Return the facing of the tank.
        It returns (dx,dy) pointing in the direction the tank is.'''
        return self.tank.get_facing_vector()

    def radar(self, x, y):
        '''Return the tile information for a given coordinate.
        Returns (terrain, item). If no terrain or item, it uses None.
        See the World docs for some terrain types.'''
        return self.tank.world.get_tile_enum(x, y)

    def kill(self):
        '''Destroys the tank.'''
        self.tank.kill()


def thinker_import(name, filename=None):
    '''Import a new thinker or reload it if it exists already'''

    if filename:
        if config.DEBUG:
            print(f'importing {name} from {filename}')
        load_source(name, filename)
    elif name in sys.modules:
        if config.DEBUG:
            print('reloading %s')
        reload(sys.modules[name])
    else:
        if config.DEBUG:
            print('importing %s')
        __import__(name)

    return sys.modules[name]


def thinker_think(tank, thinker):
    '''Set up globals for thinking module and run think()'''
    brain = tank.brain
    world = tank.world

    game = {}

    # vars
    game['color'] = tank.color
    game['position'] = brain.position()
    game['facing'] = brain.facing()
    game['direction'] = brain.direction()
    game['shots_fired'] = tank.shots
    game['state'] = tank.state

    other_tanks = [x for x in world.tanks if x is not tank]
    game['tanks'] = [world.ITEM_TO_ENUM[x] for x in other_tanks]
    game['tank_positions'] = [x.get_position() for x in other_tanks]
    game['tank_states'] = [x.state for x in other_tanks]

    game['memory'] = deepcopy(brain.memory)

    # symbols
    game['UP'] = Facing.UP
    game['DOWN'] = Facing.DOWN
    game['LEFT'] = Facing.LEFT
    game['RIGHT'] = Facing.RIGHT
    game['SHOOT'] = Command.SHOOT
    game['FORWARD'] = Command.FORWARD
    game['BACKWARD'] = Command.BACKWARD

    game['IDLE'] = TankState.IDLE
    game['MOVING'] = TankState.MOVING
    game['SHOOTING'] = TankState.SHOOTING
    game['TURNING'] = TankState.TURNING
    game['DEAD'] = TankState.DEAD

    game['GRASS'] = Tile.GRASS
    game['DIRT'] = Tile.DIRT
    game['PLAIN'] = Tile.PLAIN
    game['WATER'] = Tile.WATER

    game['SAFE_TILES'] = [world.TILE_TO_ENUM[x] for x in world.safe]
    game['UNSAFE_TILES'] = [world.TILE_TO_ENUM[x] for x in world.unsafe]

    game['ROCK'] = Item.ROCK
    game['TREE'] = Item.TREE

    # lookup tables
    game['FACING_TO_VEC'] = {x: FACING_TO_VEC[x] for x in Facing.values}

    # functions
    game['forget'] = brain.forget
    game['face'] = brain.face
    game['forward'] = brain.forward
    game['backward'] = brain.backward
    game['shoot'] = brain.shoot
    game['radar'] = brain.radar
    game['kill'] = brain.kill

    sys.stdout = DebugWriter(tank.color)

    GameState = type('GameState', (), game)

    # start a think cycle
    try:
        thinker.think(GameState())
    except Exception:
        print('Fatal brain error:')
        sys.stdout = sys.__stdout__
        traceback.print_exc()
        tank.kill()

    sys.stdout = sys.__stdout__
