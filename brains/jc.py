def relative(us, them):
    return us[0] - them[0], us[1] - them[1]


def move(current_pos):
    x, y = current_pos
    dx, dy = game.direction
    tile, contents = game.radar(x + dx, y + dy)
    if tile in game.SAFE_TILES and contents is None:
        game.forward()
    else:
        game.backward()


game = None
def think(g):
    print('JC:', g.color)
    global game
    game = g
    current_pos = game.position
    other_tank = game.tank_positions[0]

    # where they are relative to us
    rx, ry = relative(current_pos, other_tank)

    # are we facing in that direction
    if ry < 0:
        if game.facing != game.DOWN:
            game.face(game.DOWN)
    elif ry > 0:
        if game.facing != game.UP:
            game.face(game.UP)

    if rx < 0:
        if game.facing != game.RIGHT:
            game.face(game.RIGHT)
    elif rx > 0:
        if game.facing != game.LEFT:
            game.face(game.LEFT)

    move(current_pos)
    if abs(rx) < 2 or abs(ry) < 2:
        game.shoot()
