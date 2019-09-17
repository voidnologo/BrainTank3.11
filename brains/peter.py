
def choices(game):
    x, y = game.position
    choice_list = []
    print(game.radar(x - 1, y))
    if game.radar(x - 1, y)[0] is not None:
        choice_list.append(game.LEFT)
    if game.radar(x + 1, y)[0] is not None:
        choice_list.append(game.RIGHT)
    if game.radar(x, y - 1)[0] is not None:
        choice_list.append(game.UP)
    if game.radar(x, y + 1)[0] is not None:
        choice_list.append(game.DOWN)
    return choice_list


counter = 0

def think(game):
    print('PETER:', game.color)
    ch = choices(game)

    game.shoot()

    for c in ch:
        if c != game.facing:
            game.face(c)



