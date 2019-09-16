def relative(us, them):
    if us[0] < them[0]:
        x = 1
    elif us[0] > them[0]:
        x = -1
    else:
        x = 0

    if us[1] < them[1]:
        y = 1
    elif us[1] > them[1]:
        y = -1
    else:
        y = 0

    return x, y


def move(current_pos):
    x, y = current_pos
    dx, dy = game.direction
    tile, contents = game.radar(x + dx, y + dy)
    if tile in game.SAFE_TILES:
        game.forward()


game = None
def think(g):
    global game
    game = g
    current_pos = game.position
    other_tank = game.tank_positions[0]

    # where they are relative to us
    rx, ry = relative(current_pos, other_tank)

    # are we facing in that direction
    if ry == 1:
        if game.facing != game.DOWN:
            game.face(game.DOWN)
            move(current_pos)
    if ry == -1:
        if game.facing != game.UP:
            game.face(game.UP)
            move(current_pos)
    if rx == 1:
        if game.facing != game.RIGHT:
            game.face(game.RIGHT)
            move(current_pos)
    if rx == -1:
        if game.facing != game.LEFT:
            game.face(game.LEFT)
            move(current_pos)

    if rx == 0 or ry == 0:
        game.shoot()
