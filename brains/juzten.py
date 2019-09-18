#!/usr/bin/python
# -*- coding: utf-8 -*-


def think(game):
    print('JUSTIN:', game.color)

    x, y = game.position
    dx, dy = game.direction

    tile, item = game.radar(x + dx, y + dy)
    print("Tank: ", game.color, " Tile: ", tile, " Item: ", item)

    if tile is None or tile is game.WATER or item is not None:
        if game.facing is game.UP:
            game.face(game.LEFT)
            game.forward()
            game.shoot()
        elif game.facing is game.DOWN:
            game.face(game.RIGHT)
            game.forward()
            game.shoot()
        elif game.facing is game.RIGHT:
            game.face(game.UP)
            game.forward()
            game.shoot()
        elif game.facing is game.LEFT:
            game.face(game.DOWN)
            game.forward()
            game.shoot()
    else:
        game.forward()
        game.shoot()
