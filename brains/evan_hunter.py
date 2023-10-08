from dataclasses import dataclass

'''
Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Variables available to brains:
    color - string, tank color
    position - tuple (x,y), current tank grid position
    facing - symbol UP, DOWN, LEFT, RIGHT, current tank facing
    direction - tuple (x,y), unit vector representing tank facing
    shots - how many shots have been fired
    tanks - list of other tanks in map
    tank_positions - [(x,y)] other tank positions
    tank_states - list of other tank states (see Tank States)
'''

'''
1. Find out where the other tank is
    - Above us, to the right, left, below
2. If in the same row or column as us, face them and fire
3. If they are more than one rows/cols away, figure out which direction is closest and move that way
4. if they are within one rows/cols, face them and fire (bullets take time to get there)
'''

'''
Edge cases:
   - dont drive into water
   - what if we cannot move close to them?
'''


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Tile:
    terrain: str
    object: str


def think(game):
    chase(game)


def chase(game):
    print('memory (before):', game.memory)
    relative_position = get_relative_position(game)

    dodging = getattr(game.self, 'dodging', False)
    if not dodging:
        i_should_face = which_way_should_i_face(relative_position, game)
        if i_should_face is not None:
            game.face(i_should_face)
            return
    i_turn = can_i_move_forward(game)
    if i_turn is not None:
        game.self.dodging = True
        game.face(i_turn)
        return
    else:
        game.self.dodging = False
        game.forward()
        return


def get_relative_position(game):
    other_tank_position = Position(*game.tank_positions[0])
    our_tank_position = Position(*game.position)

    print('other tank', other_tank_position)
    print('our tank', our_tank_position)

    # how far left <-> right they are to us
    relative_x = other_tank_position.x - our_tank_position.x

    # how far up <-> down they are to us
    relative_y = other_tank_position.y - our_tank_position.y

    return Position(relative_x, relative_y)


def human_readable_relative(position, game):
    if position.x > 0:
        horizontal = game.RIGHT
    else:
        horizontal = game.LEFT

    if position.y > 0:
        vertical = game.DOWN
    else:
        vertical = game.UP

    return Position(horizontal, vertical)


def tile_is_safe(tile, game):
    bad_tiles = [game.WATER]

    if tile.terrain in bad_tiles or tile.object is not None:
        return False
    return True


def can_i_move_forward(game):
    our_tank_position = Position(*game.position)
    relative_position = get_relative_position(game)
    hrrel_pos = human_readable_relative(relative_position, game)

    # if I am facing ___ and cannot go forward, which way should I turn?
    match game.facing:
        case game.UP:
            tile = Tile(*game.radar(our_tank_position.x, our_tank_position.y - 1))
            if not tile_is_safe(tile, game):
                return hrrel_pos.x
        case game.DOWN:
            tile = Tile(*game.radar(our_tank_position.x, our_tank_position.y + 1))
            if not tile_is_safe(tile, game):
                return hrrel_pos.x
        case game.LEFT:
            tile = Tile(*game.radar(our_tank_position.x - 1, our_tank_position.y))
            if not tile_is_safe(tile, game):
                return hrrel_pos.y
        case game.RIGHT:
            tile = Tile(*game.radar(our_tank_position.x + 1, our_tank_position.y))
            if not tile_is_safe(tile, game):
                return hrrel_pos.y


def which_way_should_i_face(relative_position, game):
    # which way should we face
    new_facing = None
    if abs(relative_position.x) > abs(relative_position.y):
        # move up/down
        if relative_position.y > 0:
            new_facing = game.DOWN
        elif relative_position.y < 0:
            new_facing = game.UP
        elif relative_position.y == 0:
            if relative_position.x > 0:
                new_facing = game.RIGHT
            if relative_position.x < 0:
                new_facing = game.LEFT
    else:
        # move right/left
        if relative_position.x > 0:
            new_facing = game.RIGHT
        elif relative_position.x < 0:
            new_facing = game.LEFT
        elif relative_position.x == 0:
            if relative_position.y > 0:
                new_facing = game.DOWN
            if relative_position.y < 0:
                new_facing = game.UP

    if new_facing != game.facing:
        return new_facing
