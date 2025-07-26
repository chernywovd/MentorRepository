async def search_direction(direction, string):
    '''Функция для поиска определенного направления в строке'''
    if direction.lower() in string.lower():
        direction_True = direction
    else: direction_True = False

    return direction_True

