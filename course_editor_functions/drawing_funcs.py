# iterative flood fill
def paint(X, Y, tile, startTile, currentMapTiles, currentMapHeight):
    # big queue of coordinates to check for filling
    tileQueue = [[X, Y]]
    currentMapTiles[X + Y * 16] = tile
    while tileQueue != []:
        x = tileQueue[0][0]
        y = tileQueue[0][1]
        tileQueue = tileQueue[1:]
        if x > 0 and currentMapTiles[x - 1 + y * 16] == startTile:
            currentMapTiles[x - 1 + y * 16] = tile
            tileQueue.append([x - 1, y])
        if x < 15 and currentMapTiles[x + 1 + y * 16] == startTile:
            tileQueue.append([x + 1, y])
            currentMapTiles[x + 1 + y * 16] = tile
        if y > 0 and currentMapTiles[x + (y - 1) * 16] == startTile:
            tileQueue.append([x, y - 1])
            currentMapTiles[x + (y - 1) * 16] = tile
        if y < currentMapHeight - 1 and currentMapTiles[x + (y + 1) * 16] == startTile:
            tileQueue.append([x, y + 1])
            currentMapTiles[x + (y + 1) * 16] = tile
    return

# stamp 2d tile array onto the csv
def stamp(X, Y, stamp, sportHeights, allLevelTileCSVs, sportType, sportDifficulty):
    height = min(sportHeights[sportType][sportDifficulty] - Y, len(stamp))
    length = min(16 - X, len(stamp[0]))
    for i in range(height):
        for j in range(length):
            allLevelTileCSVs[sportType][sportDifficulty][X + j + (Y + i) * 16] = stamp[i][j]
    return