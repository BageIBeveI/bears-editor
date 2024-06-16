# heavily based off of Coding With Russ' videos, so figured i should give credit here

import pygame
import button
import csv
import re
import glob
from PIL import Image
import os

#pygame initializer
pygame.init()

#window maker
screenHeight = 720
screenWidth = 1280
SCREEN = pygame.display.set_mode((screenWidth, screenHeight))

#icon
ICON = pygame.image.load("tile_editor_pictures/raftin.png")
pygame.display.set_icon(ICON)

#various mode 0 variables
CONST_SPORTS = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
SPORTS = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
DIFFICULTIES = ["Beginner", "Intermediate", "Expert"]
MAX_SPORT_HEIGHTS = [[0x21A, 0x2A1, 0x31E], [0x21A, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF]] #some courses (experts) have some blank space at the ends which can be used. technically the long experts have 0x3FFB tiles at the ready, but gotta be a mult of 0x10 to have a complete row so may as well not
sportHeights = [[0x21A, 0x2A1, 0x31E], [0x21A, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x31E]]
BEARS_LEVEL_DATA_OFFSET_RANGES = [[0x28004, 0x2C004, 0x30004], [0x34004, 0x38004, 0x3C004], [0x40004, 0x44004, 0x48004], [0x4C004, 0x50004, 0x54004], [0x58004, 0x5C004, 0x60004], [0x64004, 0x68004, 0x6C004]]
sportType = 0
sportDifficulty = 0
scrollUp = False
scrollDown = False
scroll = 0
scroll2 = 0
scrollSpeed = 1
VERTICAL_LINE_COUNT = 16
NUMBER_OF_TILES = 256
chosenTile = 0
gridTileWidth = 32
allLevelTileCSVs = []
inventoryIndex = 0
effectsOn = 0
programMode = 0
clock = pygame.time.Clock()
checkerenate = False
BEARS_COURSE_HEIGHT_OFFSETS = [0x4B53, 0x8B6B, 0xCAEF, 0x10B28, 0x14C15, 0x18C2E]
bearsCourseHorizontalSpawns = [[0xB8, 0x98, 0x58], [0xB8, 0x98, 0x98], [0xB8, 0x98, 0x98], [0xB8, 0x68, 0x68], [0xB8, 0x68, 0x68], [0x78, 0x78, 0x78]]
selectOrigCoords = []
stampArr = [[0]]
drawMode = 0
bearsCourseCameras = [[0x60, 0x46, 0x14], [0x60, 0x50, 0x50], [0x60, 0x60, 0x46], [0x60, 0x20, 0x18], [0x60, 0x28, 0x28], [0x1E, 0x1E, 0x1E]]

#various mode 1 or both
hexCodes = [[100,0,0]]*0x20
bigtilePalettes = [0]*0x400
subtileGraphics = ["00000000"]*0x1EA0
bigtileSubtiles = [0]*0x400
bigtileCollisions = [0]*0x400
subtileSelected = 0
colourSelected = 0
paletteSelected = 0
subtileMode = True
colours = [[255, 219, 182], [102, 102, 102], [129, 212, 26], [180, 199, 220], [255, 166, 166], [107, 94, 155], [129, 172, 166], [129, 55, 9], [52, 101, 164], [255, 128, 0], [120, 3, 115], [21, 132, 102], [241, 13, 12], [34, 75, 18], [172, 178, 12]]
collisionColourMapper = {0x00 : 0,
           0x02 : 1,
           0x03 : 2,
           0x08 : 3,
           0x0C : 4,
           0x11 : 5,
           0x21 : 6,
           0x31 : 7,
           0x32 : 8,
           0x33 : 9,
           0x42 : 10,
           0x73 : 11,
           0x82 : 12,
           0xB3 : 13,
           0xC0 : 14}
collisionSelected = 0
bigtileSelected = 0
bigtileQuadrantSelected = 0
subtileyPalleteyThingies = [False]*4 # priority, vt_flip, hz_flip, bank
ox400IndexThingForHere = 0
displayBigtileSubtiles = True
displayBigtileCollision = True
alpher = True
scrollLeft = False
scrollRight = False
waiter = True
infoMode = False
undoStack = []
redoStack = []
currentSubtileStackInfo = []
quadrantMapper = {0:"TL", 1:"TR", 2:"BL", 3:"BR"}
maxSubtiles = []

#non tile images
TOBOGGAN_IMAGE = pygame.image.load(f'tile_editor_pictures/tobogganButton.png').convert_alpha()
SLED_IMAGE = pygame.image.load(f'tile_editor_pictures/sledButton.png').convert_alpha()
RAFT_IMAGE = pygame.image.load(f'tile_editor_pictures/raftButton.png').convert_alpha()
KAYAK_IMAGE = pygame.image.load(f'tile_editor_pictures/kayakButton.png').convert_alpha()
BIKE_IMAGE = pygame.image.load(f'tile_editor_pictures/bikeButton.png').convert_alpha()
DIRTBOARD_IMAGE = pygame.image.load(f'tile_editor_pictures/dirtboardButton.png').convert_alpha()
BEGINNER_IMAGE = pygame.image.load(f'tile_editor_pictures/beginnerButton.png').convert_alpha()
INTERMEDIATE_IMAGE = pygame.image.load(f'tile_editor_pictures/intermediateButton.png').convert_alpha()
EXPERT_IMAGE = pygame.image.load(f'tile_editor_pictures/expertButton.png').convert_alpha()
GRID_IMAGE = pygame.image.load(f'tile_editor_pictures/gridButton.png').convert_alpha()
SAVE_IMAGE = pygame.image.load(f'tile_editor_pictures/saveButton.png').convert_alpha()
LOAD_IMAGE = pygame.image.load(f'tile_editor_pictures/loadButton.png').convert_alpha()
EFFECTS_IMAGE = pygame.image.load(f'tile_editor_pictures/effectsButton.png')
COURSE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/courseEditorButton.png')
TILE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/tileEditorButton.png')
SUBTILE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/subtileEditorButton.png')
BIGTILE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/bigtileEditorButton.png')
TOGGLE_SUBTILES_IMAGE = pygame.image.load(f'tile_editor_pictures/toggleSubtilesButton.png')
TOGGLE_COLLISIONS_IMAGE = pygame.image.load(f'tile_editor_pictures/toggleCollisionsButton.png')
PRINT_IMAGE = pygame.image.load(f'tile_editor_pictures/printButton.png')
LOAD_FROM_GAME_IMAGE = pygame.image.load(f'tile_editor_pictures/loadFromGameButton.png')
LOAD_FULL_GAME_IMAGE = pygame.image.load(f'tile_editor_pictures/loadFullGameButton.png')
LOAD_LEVEL_TILES_IMAGE = pygame.image.load(f'tile_editor_pictures/loadLevelTilesButton.png')
INFO_IMAGE = pygame.image.load(f'tile_editor_pictures/infoButton.png')
INFO_IMAGES = [pygame.image.load(f'tile_editor_pictures/infoCourseEditor.png'), pygame.image.load(f'tile_editor_pictures/infoTileEditor.png')]
SUBTILE_USAGE_IMAGE = pygame.image.load(f'tile_editor_pictures/checkSubtileUsage.png')
HEIGHT_CHANGE_IMAGE = pygame.image.load(f'tile_editor_pictures/levelHeightChangeButton.png')
HORIZONTAL_SPAWN_IMAGE = pygame.image.load(f'tile_editor_pictures/horizontalSpawnButton.png')
PENCIL_IMAGE = pygame.image.load(f'tile_editor_pictures/pencil.png')
BUCKET_IMAGE = pygame.image.load(f'tile_editor_pictures/bucket.png')
STAMP_IMAGE = pygame.image.load(f'tile_editor_pictures/stamp.png')
SPAWN_CAM_IMAGE = pygame.image.load(f'tile_editor_pictures/spawnCamButton.png')

#button instances
sportTypeButtons = []
sportDifficultyButtons = []
tileInvButtons = []

def sportTypeButtonMover(mode):
    global sportTypeButtons
    sportTypeButtons = []
    sportTypeButtons.append(button.Button(560 - (80*mode), 45, TOBOGGAN_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 - (80*mode), 45, SLED_IMAGE, 2))
    sportTypeButtons.append(button.Button(560 - (80*mode), 90, RAFT_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 - (80*mode), 90, KAYAK_IMAGE, 2))
    sportTypeButtons.append(button.Button(560 - (80*mode), 135, BIKE_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 - (80*mode), 135, DIRTBOARD_IMAGE, 2))
sportTypeButtonMover(0)

sportDifficultyButtons.append(button.Button(550, 190, BEGINNER_IMAGE, 2))
sportDifficultyButtons.append(button.Button(640, 190, INTERMEDIATE_IMAGE, 2))
sportDifficultyButtons.append(button.Button(730, 190, EXPERT_IMAGE, 2))

GRID_BUTTON = button.Button(710, 10, GRID_IMAGE, 1)
SAVE_BUTTON = button.Button(750, 10, SAVE_IMAGE, 1)
LOAD_BUTTON = button.Button(790, 10, LOAD_IMAGE, 1)
EFFECTS_BUTTON = button.Button(658, 10, EFFECTS_IMAGE, 2)
COURSE_EDITOR_BUTTON = button.Button(1000,400, COURSE_EDITOR_IMAGE, 1)
TILE_EDITOR_BUTTON = button.Button(1150,400, TILE_EDITOR_IMAGE, 1)
SUBTILE_EDITOR_BUTTON = button.Button(1000,550, SUBTILE_EDITOR_IMAGE, 1)
BIGTILE_EDITOR_BUTTON = button.Button(1150,550, BIGTILE_EDITOR_IMAGE, 1)
TOGGLE_SUBTILES_BUTTON = button.Button(300,500, TOGGLE_SUBTILES_IMAGE, 1)
TOGGLE_COLLISIONS_BUTTON = button.Button(400,500, TOGGLE_COLLISIONS_IMAGE, 1)
PRINT_BUTTON = button.Button(830, 10, PRINT_IMAGE, 1)
LOAD_FROM_GAME_BUTTON = button.Button(830, 10, LOAD_FROM_GAME_IMAGE, 1)
LOAD_FULL_GAME_BUTTON = button.Button(870, 10, LOAD_FULL_GAME_IMAGE, 1)
LOAD_LEVEL_TILES_BUTTON = button.Button(910, 10, LOAD_LEVEL_TILES_IMAGE, 1)
INFO_BUTTON = button.Button(1240, 10, INFO_IMAGE, 1)
SUBTILE_USAGE_BUTTON = button.Button(870, 10, SUBTILE_USAGE_IMAGE, 1)
HEIGHT_CHANGE_BUTTON = button.Button(950, 10, HEIGHT_CHANGE_IMAGE, 1)
HORIZONTAL_SPAWN_BUTTON = button.Button(990, 10, HORIZONTAL_SPAWN_IMAGE, 1)
PENCIL_BUTTON = button.Button(870, 50, PENCIL_IMAGE, 1)
BUCKET_BUTTON = button.Button(910, 50, BUCKET_IMAGE, 1)
STAMP_BUTTON = button.Button(950, 50, STAMP_IMAGE, 1)
SPAWN_CAM_BUTTON = button.Button(1030, 10, SPAWN_CAM_IMAGE, 1)

#makes bottom right buttons (the bigtile map)
def gridButtonMaker():
    currentColumn = 0
    currentRow = 0

    for byte in allLevelTileCSVs[sportType][sportDifficulty]:
        temp = currentRow * gridTileWidth + scroll
        if temp >= -32 and temp <= screenHeight: # don't need to draw things off screen
            SCREEN.blit(imageList[sportType][0][byte], (0 + currentColumn * gridTileWidth, 0 + currentRow * gridTileWidth + scroll))
            if effectsOn:
                SCREEN.blit(imageList[sportType][1][byte], (0 + currentColumn * gridTileWidth, 0 + currentRow * gridTileWidth + scroll))
        currentColumn += 1
        if currentColumn == 16:
            currentColumn = 0
            currentRow += 1

def checkerer():
    temp = (scroll%32)-32
    layer = 0
    thetangle = pygame.Surface((32, 32))
    thetangle.set_alpha(100)
    thetangle.fill((0,0,0))
    while temp < screenHeight:
        for i in range(16):
            if (i + layer)%2 == 0:
                SCREEN.blit(thetangle, (i*32, temp))
        layer += 1
        temp += 32


#tilemap data storage (lists in lists, where list[sport][diff] = the correct data)
for sport in range(6):
    tempCSVPair = []
    for difficulty in range(3):
        tempCSVRead = re.split(",|\n", open(f"levels/{SPORTS[sport]}{DIFFICULTIES[difficulty]}.csv", "r").read())
        #sportHeights[sport][difficulty] = int(tempCSVRead[0])
        #bearsCourseHorizontalSpawns[sport][difficulty] = int(tempCSVRead[1])
        #bearsCourseCameras[sport][difficulty] = int(tempCSVRead[2]) already loaded in, but i'll keep it
        tempCSV = [int(byte) for byte in tempCSVRead[16:-1]]
        tempCSV += ([0xFF] * ((MAX_SPORT_HEIGHTS[sport][difficulty] * 0x10) - len(tempCSV)))
        tempCSVPair.append(tempCSV)
    allLevelTileCSVs.append(tempCSVPair)

#tile images (they change depending on the sport type)
def tileImageStorer(sport):
    sportTileLists = []

    tileList = []
    for i in range(NUMBER_OF_TILES):
        tile = pygame.image.load(f'tiles/{sport}/tile{i}.png').convert_alpha() #you can replace i with ((hex(i)[2:]).zfill(2)).upper() if you want, just remember to generate tile names w/ hex as well
        tile = pygame.transform.scale(tile, (32, 32))
        tileList.append(tile)
    sportTileLists.append(tileList)
    tileList = []
    for i in range(NUMBER_OF_TILES):
        tile = pygame.image.load(
            f'tiles/{sport}_effects/tile{i}.png').convert_alpha()  # you can replace i with ((hex(i)[2:]).zfill(2)).upper() if you want, just remember to generate tile names w/ hex as well
        tile = pygame.transform.scale(tile, (32, 32))
        tile.set_alpha(215) #transparency for effect tiles
        tileList.append(tile)
    sportTileLists.append(tileList)
    return sportTileLists

imageList = []
for sport in SPORTS:
    tempImages = tileImageStorer(sport)
    imageList.append(tempImages)

#clickable tile buttons (bottom right) for one sport
def buttonMaker(sportIndex):
    singleSportButtonList = []
    currentColumn = 0
    currentRow = 0
    for i in range(NUMBER_OF_TILES):
        singleSportButtonList.append(button.Button(529 + currentColumn * 18, 304 + currentRow * 18, imageList[sportIndex][0][i], 0.5))
        currentColumn += 1
        if currentColumn == 16:
            currentColumn = 0
            currentRow += 1

    return singleSportButtonList

#makes a list of the clickable bigtiles in the bottom right
clicky_tiles = []
for i in range(6):
    tempButtons = buttonMaker(i)
    clicky_tiles.append(tempButtons)

#setting up tiles in inventory
tileInvPictures = [0] * 10

##course editor funcs
#load a new course
def loadLevel(name, sportType, sportDifficulty):
    global allLevelTileCSVs
    global sportHeights
    global bearsCourseHorizontalSpawns
    global bearsCourseCameras
    with open(f"levels/modified_levels/{name}.gbc", "rb") as file:
        tempAllData = file.read()
        levelOffset = BEARS_LEVEL_DATA_OFFSET_RANGES[sportType][sportDifficulty]
        length = sportHeights[sportType][sportDifficulty] * 0x10
        data = tempAllData[levelOffset:levelOffset + length]
        chunkStart = (0xA + sportType*3 + sportDifficulty) * 0x4000
        sportHeights[sportType][sportDifficulty] = int.from_bytes(tempAllData[chunkStart+2:chunkStart+4], "little")
        bearsCourseHorizontalSpawns[sportType][sportDifficulty] = tempAllData[BEARS_COURSE_HEIGHT_OFFSETS[sportType]+sportDifficulty]
        bearsCourseCameras[sportType][sportDifficulty] = tempAllData[BEARS_COURSE_HEIGHT_OFFSETS[sportType]+sportDifficulty+3]
        liszt = []
        for byte in data:
            liszt.append(byte)
        allLevelTileCSVs[sportType][sportDifficulty] = liszt
        liszt += ([0xFF] * ((MAX_SPORT_HEIGHTS[sportType][sportDifficulty] * 0x10) - len(liszt)))

def paint(X, Y, tile, startTile):
    global sportType
    global sportDifficulty
    global allLevelTileCSVs
    global sportHeights
    tileQueue = [[X, Y]]
    allLevelTileCSVs[sportType][sportDifficulty][X + Y * 16] = tile
    while tileQueue != []:
        x = tileQueue[0][0]
        y = tileQueue[0][1]
        tileQueue = tileQueue[1:]
        if x > 0 and allLevelTileCSVs[sportType][sportDifficulty][x-1+y*16] == startTile:
            #paint(x-1, y, tile, startTile)
            allLevelTileCSVs[sportType][sportDifficulty][x-1 + y * 16] = tile
            tileQueue.append([x-1, y])
        if x < 15 and allLevelTileCSVs[sportType][sportDifficulty][x+1+y*16] == startTile:
            #paint(x+1, y, tile, startTile)
            tileQueue.append([x+1, y])
            allLevelTileCSVs[sportType][sportDifficulty][x+1 + y * 16] = tile
        if y > 0 and allLevelTileCSVs[sportType][sportDifficulty][x+(y-1)*16] == startTile:
            #paint(x, y-1, tile, startTile)
            tileQueue.append([x, y-1])
            allLevelTileCSVs[sportType][sportDifficulty][x + (y-1) * 16] = tile
        if y < sportHeights[sportType][sportDifficulty] - 1 and allLevelTileCSVs[sportType][sportDifficulty][x+(y+1)*16] == startTile:
            #paint(x, y+1, tile, startTile)
            tileQueue.append([x, y+1])
            allLevelTileCSVs[sportType][sportDifficulty][x + (y+1) * 16] = tile
    return

def stamp(X, Y, stamp):
    global sportType
    global sportDifficulty
    global allLevelTileCSVs
    global sportHeights
    height = min(sportHeights[sportType][sportDifficulty] - Y, len(stamp))
    length = min(16 - X, len(stamp[0]))
    for i in range(height):
        for j in range(length):
            allLevelTileCSVs[sportType][sportDifficulty][X+j+(Y+i)*16] = stamp[i][j]
    return

##tile editor funcs
#loading in subtiles as images, for subtile mode
def loadSubtileData(sport):
    global hexCodes
    global subtileGraphics
    global bigtilePalettes
    global bigtileCollisions
    global bigtileSubtiles
    bigtileCollisionOffsets = [0x4D6C, 0x8DCD, 0xCCE1, 0x10DAA, 0x14EF1, 0x19031]
    #bigtileGraphicsOffsets = above plys 0x40A
    #bigtilePaletteOffsets = above plus 0x80A
    subtileGraphicsOffsets = [0x5976, 0x99D7, 0xD8EB, 0x119B4, 0x15AFB, 0x19C3B]
    subtileGraphicsLengths = [0x1EA0, 0x1DC0, 0x1FA0, 0x1FD0, 0x1F70, 0x1900]
    #subtileColoursOffsets = above two added, plus 0xA
    name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (. to abort): ")
    while name == "E":
        if input("are you sure? (E again if yes): ") == "E":
            hexCodes = [[0, 0, 0]] * 0x20
            bigtilePalettes = [0] * 0x400
            subtileGraphics = ["00000000"] * subtileGraphicsLengths[sport]
            return
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as file:
                byteLand = file.read()
                check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} palette? (if no, don't enter anything): ")
                if check != "":
                    extraOffsets = [[0x4A98, 0, 0, 0x4AA5],[0x8AB0, 0, 0, 0x8ABD],[0, 0, 0xCA3C, 0xCA45],[0, 0, 0x10A75, 0x10A7E],[0, 0, 0x14B62, 0x14B6B],[0, 0, 0x18B7B, 0x18B84]]
                    hexCodes = []
                    paletteOffset = subtileGraphicsOffsets[sport] + subtileGraphicsLengths[sport] + 0xA
                    paletteData = b''
                    for i in range(4):
                        if extraOffsets[sport][i] == 0:
                            paletteData += byteLand[paletteOffset+(i*2):paletteOffset+(i*2)+2]
                        else:
                            paletteData += byteLand[(extraOffsets[sport][i]):(extraOffsets[sport][i])+2]
                    paletteData += byteLand[paletteOffset+0x08:paletteOffset+0x40] #0x40 bytes in a 7 colour palette
                    for i in range(0, 0x40, 2):
                        hexCodes.append([int((paletteData[i] & 0x1F) << 3), int(((paletteData[i] >> 5) + ((paletteData[i+1] & 0x3) << 3)) << 3), int(((paletteData[i+1] & 0x7C) >> 2) << 3)]) #GGGRRRRR XBBBBBGG into hex (R, G, B). normal conversion to a val btwn 0 and 1f, then left shift three times cuz hex takes 0 to 255 (so we approx)
                        # possibly bad to do this in a global way but whatevs
                        # hmmmmm the colour conversion doesn't work perfectly, maybe there's something im missing, but it works well enough

                check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} subtile graphics? (if no, don't enter anything): ")
                if check != "":
                    subtileGraphics = []
                    subtileyOffset = subtileGraphicsOffsets[sportType]
                    lengthe = subtileGraphicsLengths[sportType]
                    subtileData = byteLand[subtileyOffset:subtileyOffset+lengthe]
                    for i in range(0, lengthe, 2):
                        subtileGraphics.append(str(int(bin(subtileData[i])[2:]) + int(bin(subtileData[i+1])[2:]) * 2).zfill(8))
                        #either mult i by 2 or i+1 by 2 (with binary as integers)

                check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} bigtile subtile graphic configurations and collisions? (if no, don't enter anything): ")
                if check != "":
                    for i in range(0x400):
                        bigtileCollisions[i] = byteLand[bigtileCollisionOffsets[sport] + i]
                        bigtileSubtiles[i] = byteLand[bigtileCollisionOffsets[sport]+0x40A+i]
                        bigtilePalettes[i] = byteLand[bigtileCollisionOffsets[sport]+0x80A+i]
            print("Changes have been made. (unless you didn't do any of the three i guess)")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return

#saves tile editor data to a game
def saveThineData(sport):
    global hexCodes
    global subtileGraphics
    global bigtilePalettes
    global bigtileCollisions
    global bigtileSubtiles
    bigtileCollisionOffsets = [0x4D6C, 0x8DCD, 0xCCE1, 0x10DAA, 0x14EF1, 0x19031]
    # bigtileGraphicsOffsets = above plus 0x40A
    # bigtilePaletteOffsets = above plus 0x80A
    subtileGraphicsOffsets = [0x5976, 0x99D7, 0xD8EB, 0x119B4, 0x15AFB, 0x19C3B]
    subtileGraphicsLengths = [0x1EA0, 0x1DC0, 0x1FA0, 0x1FD0, 0x1F70, 0x1900]
    # subtileColoursOffsets = above two added, plus 0xA
    name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as file:
                check = input("Do you want to save your palette to the file? (if no, don't enter anything): ")
                if check != "":
                    extraOffsets = [[0x4A98, 0, 0, 0x4AA5], [0x8AB0, 0, 0, 0x8ABD], [0, 0, 0xCA3C, 0xCA45],
                                    [0, 0, 0x10A75, 0x10A7E], [0, 0, 0x14B62, 0x14B6B], [0, 0, 0x18B7B, 0x18B84]]
                    paletteOffset = subtileGraphicsOffsets[sport] + subtileGraphicsLengths[sport] + 0xA
                    for i in range(4):
                        RGB = hexCodes[i]
                        G = bin(RGB[1] >> 3)[2:].zfill(5)
                        temp = G[2:].zfill(3) + bin(RGB[0] >> 3)[2:].zfill(5) + "0" + bin(RGB[2] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                        bitey = int(temp, 2).to_bytes(2, "big")
                        if extraOffsets[sport][i] == 0:
                            file.seek(paletteOffset + i*2, 0)
                            file.write(bitey)
                        else:
                            file.seek(extraOffsets[sport][i], 0)
                            file.write(bitey)
                    file.seek(paletteOffset + 8, 0)
                    for i in range(4, 0x20):
                        RGB = hexCodes[i]
                        G = bin(RGB[1] >> 3)[2:].zfill(5)
                        temp = G[2:].zfill(3) + bin(RGB[0] >> 3)[2:].zfill(5) + "0" + bin(RGB[2] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                        bitey = int(temp, 2).to_bytes(2, "big")
                        file.write(bitey)
                check = input("Do you want to save your subtile graphics to the file? (if no, don't enter anything): ")
                if check != "":
                    pass
                    subtileyOffset = subtileGraphicsOffsets[sport]
                    file.seek(subtileyOffset)
                    for i in range(subtileGraphicsLengths[sport]//2):
                        quaternary = subtileGraphics[i]
                        left = ""
                        right = ""
                        #prolly a bad way of doing this but can't think of a better one rn
                        for num in quaternary:
                            if num == "0":
                                left += "0"
                                right += "0"
                            elif num == "1":
                                left += "1"
                                right += "0"
                            elif num == "2":
                                left += "0"
                                right += "1"
                            elif num == "3":
                                left += "1"
                                right += "1"
                        file.write(int(left, 2).to_bytes())
                        file.write(int(right, 2).to_bytes())

                check = input("Do you want to save your bigtile subtile graphic configurations and collisions to the file? (if no, don't enter anything): ")
                if check != "":
                    file.seek(bigtileCollisionOffsets[sport], 0)
                    for bytten in bigtileCollisions:
                        file.write(bytten.to_bytes())
                    file.seek(bigtileCollisionOffsets[sport] + 0x40A, 0)
                    for bytten in bigtileSubtiles:
                        file.write(bytten.to_bytes())
                    file.seek(bigtileCollisionOffsets[sport] + 0x80A, 0)
                    for bytten in bigtilePalettes:
                        file.write(bytten.to_bytes())
            print("Changes have been made. (unless you didn't do any of the three i guess)")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return

#makes printed tiles from bmp into png
def pngify(name):
    if not os.path.exists(f"tiles/{name}"):
        os.makedirs(f"tiles/{name}")
    count = 0
    for bitmap in glob.glob(f"tiles/temptiles/*.bmp"):
        Image.open(bitmap).save(f"tiles/{name}/tile{count}.png")
        count += 1

    if not os.path.exists(f"tiles/{name}_effects"):
        os.makedirs(f"tiles/{name}_effects")
    count = 0
    for bitmap in glob.glob(f"tiles/efftemptiles/*.bmp"):
        Image.open(bitmap).save(f"tiles/{name}_effects/tile{count}.png")
        count += 1

#draws all the tiny top right subtiles in tile mode
def wowowo():
    # testing drawing selectable subtiles
    for k in range(32):
        for l in range(16):
            for i in range(8):
                for j in range(8):

                    X = (750 + (j * 4) + (l * 32))
                    Y = (50 + (i * 4) + (k * 32)) + scroll2
                    if Y < 50 or Y >= 370:
                        continue
                    rectangle = pygame.Rect = (X, Y, 4, 4)
                    try:
                        colourSelected = int(subtileGraphics[((k * 16) + l) * 8 + i][j])
                    except Exception:
                        return
                    pygame.draw.rect(SCREEN, hexCodes[colourSelected + paletteSelected * 4], rectangle)  # gotta use paletteSelected for this because subtiles aren't connected to one palette, rather a palette is assigned upon bigtile construction

#todo probably use this method more often? everything is so janky and spaghettish
#kind of a general tile editor updater
def infoUpdater():
    global subtileSelected
    global paletteSelected
    global colourSelected
    global bigtileSelected
    global collisionSelected
    global bigtileQuadrantSelected
    global ox400IndexThingForHere
    global undoStack
    global redoStack
    global currentSubtileStackInfo
    ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
    P = bigtilePalettes[ox400IndexThingForHere]
    collisionSelected = collisionColourMapper[bigtileCollisions[bigtileSelected * 4 + bigtileQuadrantSelected % 4]]
    subtileSelected = bigtileSubtiles[ox400IndexThingForHere]
    paletteSelected = P & 7
    subtileyPalleteyThingies[0] = P & 0x80 != 0  # priority
    subtileyPalleteyThingies[1] = P & 0x40 != 0  # vt_flip
    subtileyPalleteyThingies[2] = P & 0x20 != 0  # hz_flip
    if P & 0x8 != 0:  # bank
        subtileyPalleteyThingies[3] = True
    else:
        subtileyPalleteyThingies[3] = False
    undoStack = []
    redoStack = []
    currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]
    return

#making the font
pygame.font.init()
thefont = pygame.font.SysFont("Times New Roman", 32)

#game loop
running = True
while running:

    #fps (and title)
    clock.tick()
    pygame.display.set_caption(f"bears tile editor: {clock.get_fps()} fps")

    #bg colour (blue!)
    SCREEN.fill((36, 45, 104))

    #mouse pos tracker
    mousePos = pygame.mouse.get_pos()
    mouseX = (mousePos[0])
    mouseY = (mousePos[1])

    #mode changing buttons
    if COURSE_EDITOR_BUTTON.draw(SCREEN):
        programMode = 0
        sportTypeButtonMover(programMode)
    if TILE_EDITOR_BUTTON.draw(SCREEN):
        programMode = 1
        sportTypeButtonMover(programMode)

    # info mode, stops other modes to make things a bit quicker
    if infoMode:
        pygame.event.get()
        SCREEN.blit(INFO_IMAGES[programMode], (0, 0))
        pygame.display.update()
        pygame.display.set_caption(f"bears tile editor: paused fps")
        while not INFO_BUTTON.draw(SCREEN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
        infoMode = not infoMode
        pygame.time.wait(200)

    #
    # COURSE EDITOR MODE (for editing course layout)
    #
    elif programMode == 0:

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

              # keystrokes
            if event.type == pygame.KEYDOWN:
                # grid scrolling
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scrollUp = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scrollDown = True
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollSpeed = 2

                # inventory slot chooser
                if event.key == pygame.K_1:
                    inventoryIndex = 0
                    chosenTile = tileInvPictures[0]
                elif event.key == pygame.K_2:
                    inventoryIndex = 1
                    chosenTile = tileInvPictures[1]
                elif event.key == pygame.K_3:
                    inventoryIndex = 2
                    chosenTile = tileInvPictures[2]
                elif event.key == pygame.K_4:
                    inventoryIndex = 3
                    chosenTile = tileInvPictures[3]
                elif event.key == pygame.K_5:
                    inventoryIndex = 4
                    chosenTile = tileInvPictures[4]
                elif event.key == pygame.K_6:
                    inventoryIndex = 5
                    chosenTile = tileInvPictures[5]
                elif event.key == pygame.K_7:
                    inventoryIndex = 6
                    chosenTile = tileInvPictures[6]
                elif event.key == pygame.K_8:
                    inventoryIndex = 7
                    chosenTile = tileInvPictures[7]
                elif event.key == pygame.K_9:
                    inventoryIndex = 8
                    chosenTile = tileInvPictures[8]
                elif event.key == pygame.K_0:
                    inventoryIndex = 9
                    chosenTile = tileInvPictures[9]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scrollUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scrollDown = False
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollSpeed = 1

            #scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll += 256 * scrollSpeed
                elif event.y == -1:
                    scroll -= 256 * scrollSpeed

        # scolling (up/down, or W/D)
        if scrollUp == True:
            scroll += 32 * scrollSpeed
        if scrollDown == True:
            scroll -= 32 * scrollSpeed

        if scroll > 0:
            scroll = 0

        #limit on the scroll
        if scroll < -(sportHeights[sportType][sportDifficulty]) * (gridTileWidth) + 600: #this is prob very inefficient, should change the value every time diff/grid is changed and store it somrwhere future me pleeeeease :)
            scroll = -(sportHeights[sportType][sportDifficulty]) * (gridTileWidth) + 600

        #draw sport buttons, sport button memory, & actions
        sportCount = 0
        for sportCount, typeButton in enumerate(sportTypeButtons):
            if typeButton.draw(SCREEN):
                sportType = sportCount

        #draw diff buttons, difficulty button memory, & actions
        difficultyCount = 0
        for difficultyCount, difficultyButton in enumerate(sportDifficultyButtons):
            if difficultyButton.draw(SCREEN):
                sportDifficulty = difficultyCount
                imageList[sportType] = tileImageStorer(SPORTS[sportType])

        #draw clickable tiles, clicky tile memory, also changes inventory
        tileCount = 0
        for tileCount, i in enumerate(clicky_tiles[sportType]):
            if i.draw(SCREEN):
                chosenTile = tileCount
                tileInvPictures[inventoryIndex] = tileCount

        #highlighting (sport, diff, tile)
        pygame.draw.rect(SCREEN, (255, 0, 0), sportTypeButtons[sportType], 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), sportDifficultyButtons[sportDifficulty], 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), clicky_tiles[sportType][chosenTile], 1)

        invRect = pygame.Rect = (582 + inventoryIndex * 18, 274, 18, 18) #maybe also bad? idk, im goin ta sleep
        pygame.draw.rect(SCREEN, (255, 0, 0), invRect)

        #draws grid tile images to screen
        gridButtonMaker()

        #drawing the height line
        lineHeight = sportHeights[sportType][sportDifficulty]*32 + scroll*1 + 2
        if lineHeight > 0 and lineHeight < 720:
            pygame.draw.line(SCREEN, (255, 0, 0), (0, lineHeight), (511, lineHeight), 5)

        #and the spawn rectangle
        spawnRect = pygame.rect = (bearsCourseHorizontalSpawns[sportType][sportDifficulty] * 2 - 16, sportHeights[sportType][sportDifficulty]*32 + scroll*1 - 64, 32, 32)
        pygame.draw.rect(SCREEN, (255, 0, 0), spawnRect, 2)

        #camera test
        cameraX = bearsCourseCameras[sportType][sportDifficulty]*2
        cameraRect = pygame.rect = (cameraX, lineHeight - 0x122, 0x140, 0x120)
        pygame.draw.rect(SCREEN, (255, 200, 200), cameraRect, 2)

        # toggles the grid spacings (and draws grid button)
        if GRID_BUTTON.slowDraw(SCREEN):
            checkerenate = not checkerenate
            pygame.time.wait(200)
            """#nuked in lieu of a checkerboard
            if gridTileWidth == 32:
                gridTileWidth = 33
            else:
                gridTileWidth = 32"""
        if checkerenate:
            checkerer()

        # saving features (and draw save)
        if SAVE_BUTTON.draw(SCREEN):
            CSVList = allLevelTileCSVs[sportType][sportDifficulty][0:0x10*sportHeights[sportType][sportDifficulty]]

            filename = input("Name your file (leave blank to skip): ") #CSV maker
            if filename != "":
                proceed = True
                if not os.path.exists(f"levels/modified_levels"):
                    os.makedirs(f"levels/modified_levels")
                if os.path.exists(f"levels/modified_levels/{filename}.csv"):
                    if not input('File exists. Do you want to overwrite? ("Y" for yes): ').upper() == "Y":
                        proceed = False
                if proceed:
                    with open(f"levels/modified_levels/{filename}.csv", "w", newline="") as file:
                        writenator = csv.writer(file, delimiter=",")
                        writenator.writerow([sportHeights[sportType][sportDifficulty], bearsCourseHorizontalSpawns[sportType][sportDifficulty]])
                        for i in range(0, len(CSVList), 16):
                            writenator.writerow(CSVList[i:i + 16])
                        print("File saved.")

            bearsname = input("enter the name of the bears file (in levels/modified_levels/) to which the data should be saved here (.gbc file format assumed, so don't type it)? (leave blank to skip): ") #GBC editor
            if bearsname != "":
                try:
                    with open(f"levels/modified_levels/{bearsname}.gbc", "r+b") as file:
                        file.seek(BEARS_LEVEL_DATA_OFFSET_RANGES[sportType][sportDifficulty])
                        CSVByteArray = b''
                        for num in CSVList:
                            CSVByteArray += num.to_bytes(1, "little")
                        file.write(CSVByteArray)
                        #new height
                        file.seek((0xA + sportType*3 + sportDifficulty)*0x4000+2)
                        file.write(min(sportHeights[sportType][sportDifficulty].to_bytes(2, "little", signed=False), MAX_SPORT_HEIGHTS[sportType][sportDifficulty].to_bytes(2, "little", signed=False)))
                        #new spawn
                        file.seek(BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty)
                        file.write(bearsCourseHorizontalSpawns[sportType][sportDifficulty].to_bytes())
                        #new cam
                        file.seek(BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty + 3)
                        file.write(bearsCourseCameras[sportType][sportDifficulty].to_bytes())
                        file.close()
                        print("Data saved.")
                except FileNotFoundError:
                    print("GBC file not found. No edits have been made.")

        # loading features
        if LOAD_BUTTON.draw(SCREEN):
            filename = input("enter the name of the CSV file (in levels/modified_levels/) here (.csv file format assumed, so don't type it) (leave blank to abort): ")
            if filename != "":
                fileFound = True
                try:
                    file = open(f"levels/modified_levels/{filename}.csv", "r")
                except FileNotFoundError:
                    try:
                        file = open(f"levels/{filename}.csv", "r")
                    except FileNotFoundError:
                        fileFound = False
                if fileFound:
                    try:
                        tempArrrgh = re.split(",|\n", file.read())
                        header = tempArrrgh[0:3]
                        liszt = [int(byte) for byte in tempArrrgh[16:-1]] #the -1 takes off the last \n of a csv file, and the 16 is to remove the empty header junk
                        courseSize = len(liszt)
                        if courseSize < sportHeights[sportType][sportDifficulty]*0x10:
                            liszt += ([0xFF] * ((MAX_SPORT_HEIGHTS[sportType][sportDifficulty] * 0x10) - courseSize)) #if the height isn't the max, this fills the rest with sawdust (0xFF tiles cuz why not)
                        allLevelTileCSVs[sportType][sportDifficulty] = liszt
                        sportHeights[sportType][sportDifficulty] = int(header[0])
                        if MAX_SPORT_HEIGHTS[sportType][sportDifficulty] < int(header[0]): #heights can't go past the orig cap yet sadly
                            print("the level height stored in this CSV is too long for this level and has been automatically shortened.")
                            sportHeights[sportType][sportDifficulty] = sportHeights[sportType][sportDifficulty]
                        bearsCourseHorizontalSpawns[sportType][sportDifficulty] = int(header[1])
                        bearsCourseCameras[sportType][sportDifficulty] = int(header[2])

                        file.close()
                    except ValueError:
                        print("bad sport or diff :(")
                    except IndexError:
                        print("sport/diff num out of bounds :(")
                else:
                    print("File not found.")

        # effect vision toggle
        if EFFECTS_BUTTON.draw(SCREEN):
            if effectsOn:
                effectsOn = 0
            else:
                effectsOn = 1

            imageList[sportType] = tileImageStorer(SPORTS[sportType])

            pygame.time.wait(200)

        if LOAD_FROM_GAME_BUTTON.draw(SCREEN):
            name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
            if name != "":
                try:
                    loadLevel(name, sportType, sportDifficulty)
                except IOError:
                    print("bad file .. ;( i will now cry")

        if LOAD_FULL_GAME_BUTTON.draw(SCREEN):
            name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
            if name != "":
                try:
                    for i in range(6):
                        for j in range(3):
                            loadLevel(name, i, j)
                except IOError:
                    print("bad file .. ;( i will now cry")

        if LOAD_LEVEL_TILES_BUTTON.draw(SCREEN):
            name = input("enter the name of the folder (in tiles/) containing the new tile graphics and effects here (e.g. if in the levels folder you have toboggan and toboggan_effects, type toboggan. to fill these folders, use the tile editor mode) (leave blank to abort): ")
            if name != "":
                if os.path.exists(f"tiles/{name}") and os.path.exists(f"tiles/{name}_effects"):
                    temp = SPORTS[sportType]
                    SPORTS[sportType] = name
                    print(f"{temp} has been replaced by {name}.")
                    imageList[sportType] = tileImageStorer(SPORTS[sportType])
                    clicky_tiles[sportType] = buttonMaker(sportType)
                else:
                    print(f"couldn't find one of the two folders ({name} or {name}_effects) in the tiles folder")

        if HEIGHT_CHANGE_BUTTON.draw(SCREEN):
            try:
                    tempHeight = int(input(f"Input the new height you want (the old one was {sportHeights[sportType][sportDifficulty]}, and the max height is {MAX_SPORT_HEIGHTS[sportType][sportDifficulty]}): "))
                    if tempHeight < 9 or tempHeight > MAX_SPORT_HEIGHTS[sportType][sportDifficulty]:
                        print("The height is either too small (under 9) or too tall (and would overwrite other code).")
                    else:
                        sportHeights[sportType][sportDifficulty] = tempHeight
                    #make var to hold, also compare to original_heights, and add that in the last input message
            except ValueError:
                print("bad input :(")

        if INFO_BUTTON.draw(SCREEN):
            infoMode = not infoMode
            pygame.time.wait(200)

        if HORIZONTAL_SPAWN_BUTTON.draw(SCREEN):
            tempHoriz = input(f'Input the new horizontal spawn location you want (the current horizontal spawn location is {bearsCourseHorizontalSpawns[sportType][sportDifficulty]}, or {hex(bearsCourseHorizontalSpawns[sportType][sportDifficulty])}): ')
            try:
                if tempHoriz[0:2].lower() == "0x":
                    tempHoriz = int(tempHoriz, 16)
                elif tempHoriz.isnumeric():
                    tempHoriz = int(tempHoriz)
                if tempHoriz >= 0x8 and tempHoriz <= 0xF8:
                    bearsCourseHorizontalSpawns[sportType][sportDifficulty] = tempHoriz
                else:
                    print("Out of bounds (keep it between 8 and 248).")
            except Exception:
                print("Invalid input.")

        if SPAWN_CAM_BUTTON.draw(SCREEN):
            tempInput = input(f"where should the camera start when entering the course (value from 0 to 96)? (current value is {bearsCourseCameras[sportType][sportDifficulty]}. to get the bear closest to the center of the screen, try {max(min(bearsCourseHorizontalSpawns[sportType][sportDifficulty] - 0x50, 0x60), 0)}): ")
            try:
                if tempInput.isnumeric():
                    tempInput = int(tempInput)
                else:
                    tempInput = int(tempInput, 16)
                if tempInput < 0 or tempInput > 96:
                    print("Out of bounds.")
                else:
                    bearsCourseCameras[sportType][sportDifficulty] = tempInput
            except Exception:
                print("Invalid input.")

        #mouse tracker (adjusted for tile grid clicking)
        mouseX = mouseX // (gridTileWidth)
        mouseY = (mouseY - scroll) // (gridTileWidth)

        if mouseX < VERTICAL_LINE_COUNT and mouseX >= 0 and mouseY < sportHeights[sportType][sportDifficulty]:
            if pygame.mouse.get_pressed()[0] == 1:
                if drawMode == 0 and allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] != chosenTile:
                    allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] = chosenTile
                elif drawMode == 1 and allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] != chosenTile:
                    paint(mouseX, mouseY, chosenTile, allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16])
                elif drawMode == 2:
                    stamp(mouseX, mouseY, stampArr)
            elif pygame.mouse.get_pressed()[1] == 1 and allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] != chosenTile:
                chosenTile = allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16]
                tileInvPictures[inventoryIndex] = chosenTile
            elif pygame.mouse.get_pressed()[2] == 1:
                if selectOrigCoords == []:
                    selectOrigCoords = [mouseX, mouseY]
                selectNewCoords = [mouseX, mouseY]
                selectangle = pygame.rect = (min(selectOrigCoords[0], selectNewCoords[0]) * 32, min(selectOrigCoords[1], selectNewCoords[1]) * 32 + scroll, abs(selectOrigCoords[0] - selectNewCoords[0]) * 32 + 32, abs(selectOrigCoords[1] - selectNewCoords[1]) * 32 + 32)
                pygame.draw.rect(SCREEN, (100, 255, 100), selectangle, 2)
            elif pygame.mouse.get_pressed()[2] == 0:
                if selectOrigCoords != []:
                    stampArr = []
                    horizLen = abs(selectOrigCoords[0] - selectNewCoords[0]) + 1
                    topLeft = [min(selectOrigCoords[0], selectNewCoords[0]), min(selectOrigCoords[1], selectNewCoords[1])]
                    for i in range(abs(selectOrigCoords[1] - selectNewCoords[1]) + 1):
                        stampArr.append(allLevelTileCSVs[sportType][sportDifficulty][topLeft[0]+(topLeft[1]+i)*16:topLeft[0]+horizLen+(topLeft[1]+i)*16])
                selectOrigCoords = []

        #buttons for drawing mode
        if PENCIL_BUTTON.draw(SCREEN):
            drawMode = 0
        if BUCKET_BUTTON.draw(SCREEN):
            drawMode = 1
        if STAMP_BUTTON.draw(SCREEN):
            drawMode = 2
        #and highlight selected
        modangle = pygame.rect = (870 + drawMode*40, 50, 32, 32)
        pygame.draw.rect(SCREEN, (255, 0, 0), modangle, 1)

        for i in range(10): #draws inv items to the screen
            tempPic = pygame.transform.scale(imageList[sportType][0][tileInvPictures[i]], (16, 16)) #this seems bad, maybe use 2 lists, one which stores numbers and another which stores pictures?
            SCREEN.blit(tempPic, (583 + (i * 18), 275))
            if effectsOn:
                tempPic = pygame.transform.scale(imageList[sportType][1][tileInvPictures[i]], (16, 16))  # this seems bad, maybe use 2 lists, one which stores numbers and another which stores pictures?
                tempPic.set_alpha(215)
                SCREEN.blit(tempPic, (583 + (i * 18), 275))


    #
    # SUBTILE PAINT MODE AND BIGTILE CONSTRUCTOR MODE
    #
    elif programMode == 1:

        if SUBTILE_EDITOR_BUTTON.draw(SCREEN):
            subtileMode = True
            currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]

        if BIGTILE_EDITOR_BUTTON.draw(SCREEN):
            subtileMode = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keystrokes
            if event.type == pygame.KEYDOWN:
                # grid scrolling
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scrollUp = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scrollDown = True
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollSpeed = 2
                #changing bigtile:
                if not subtileMode:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        scrollLeft = True
                        if waiter:
                            pygame.time.wait(100)
                        waiter = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        scrollRight = True
                        if waiter:
                            pygame.time.wait(100)
                        waiter = False
                else:
                    if event.key == pygame.K_z:
                        if undoStack != []:
                            latest = undoStack.pop()
                            undoneSubtileSelected = latest[0]
                            redoStack.append([undoneSubtileSelected,subtileGraphics[undoneSubtileSelected*8:undoneSubtileSelected*8+8]])
                            if len(redoStack) > 150:
                                redoStack = redoStack[50:]
                            subtileGraphics[undoneSubtileSelected*8:undoneSubtileSelected*8+8] = latest[1]
                            currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]
                    elif event.key == pygame.K_y:
                        if redoStack != []:
                            latest = redoStack.pop()
                            undoneSubtileSelected = latest[0]
                            undoStack.append([undoneSubtileSelected,subtileGraphics[undoneSubtileSelected*8:undoneSubtileSelected*8+8]])
                            if len(undoStack) > 150:
                                undoStack = undoStack[50:]
                            subtileGraphics[undoneSubtileSelected*8:undoneSubtileSelected*8+8] = latest[1]
                            currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scrollUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scrollDown = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    scrollLeft = False
                    waiter = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    scrollRight = False
                    waiter = True
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollSpeed = 1

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #lmb up, check if undo stack should be updated
                if subtileGraphics[subtileSelected*8:subtileSelected*8+8] != currentSubtileStackInfo:
                    undoStack.append([subtileSelected, currentSubtileStackInfo])
                    if len(undoStack) > 150:
                        undoStack = undoStack[50:]
                    redoStack = []
                currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll2 += 32 * scrollSpeed
                elif event.y == -1:
                    scroll2 -= 32 * scrollSpeed

        # scolling (up/down, or W/D)
        if scrollUp == True:
            scroll2 += 16 * scrollSpeed
        if scrollDown == True:
            scroll2 -= 16 * scrollSpeed
        if scrollLeft or scrollRight:
            if scrollLeft == True:
                bigtileSelected -= 1 * scrollSpeed
            if scrollRight == True:
                bigtileSelected += 1 * scrollSpeed
            pygame.time.wait(20)
            if bigtileSelected < 0 or bigtileSelected > 255:
                bigtileSelected = bigtileSelected & 255
            infoUpdater()

        if scroll2 < -704:
            scroll2 = -704

        if scroll2 > 0:
            scroll2 = 0

        adder = 0 #helps with updating subtileSelected, but in the future should maybe be gone since having this option is kinda dumb and just an artifact from them needing to signify selecting another bank
        if subtileyPalleteyThingies[3]:
            adder = 0x100

        #clicks
        if pygame.mouse.get_pressed()[0] == 1:
            #clicking a palette and colour (choose them and change cur quadrant)
            if mouseX > 0 and mouseX < 80 and mouseY > 0 and mouseY < 160:
                colourSelected = (mouseX // 20)
                paletteSelected = mouseY // 20
                if not subtileMode:
                    ox400IndexThingForHere = bigtileSelected*2 + bigtileQuadrantSelected%2 + (bigtileQuadrantSelected//2)*0x20 + (bigtileSelected//0x10)*0x20
                    bigtilePalettes[ox400IndexThingForHere] = (bigtilePalettes[ox400IndexThingForHere] & 0b11111000) | paletteSelected

            #clicking a big subtile thingy to change it
            elif mouseX > 100 and mouseX < 420 and mouseY > 50 and mouseY < 370:
                if subtileMode:
                    colnum = ((mouseX - 100) // 40)
                    rownum = ((mouseY - 50) // 40)
                    index = subtileSelected * 8 + rownum
                    if index < len(subtileGraphics):
                        subtileGraphics[index] = subtileGraphics[index][0:colnum] + str(colourSelected) + subtileGraphics[index][colnum+1:]
                else:
                #clicking a big bigtile quadrant
                    bigtileQuadrantSelected = ((mouseX-100)//160) + ((mouseY-50)//160)*2
                    ox400IndexThingForHere = bigtileSelected*2 + bigtileQuadrantSelected%2 + (bigtileQuadrantSelected//2)*0x20 + (bigtileSelected//0x10)*0x20
                    P = bigtilePalettes[ox400IndexThingForHere]
                    collisionSelected = collisionColourMapper[bigtileCollisions[bigtileSelected*4 + bigtileQuadrantSelected%4]]
                    subtileSelected = bigtileSubtiles[ox400IndexThingForHere]
                    paletteSelected = P&7
                    subtileyPalleteyThingies[0] = P&0x80 != 0 #priority
                    subtileyPalleteyThingies[1] = P&0x40 != 0 #vt_flip
                    subtileyPalleteyThingies[2] = P&0x20 != 0 #hz_flip
                    if P&0x8!= 0:#bank
                        subtileyPalleteyThingies[3] = True
                    else:
                        subtileyPalleteyThingies[3] = False

            #clicking a small subtile
            elif mouseX > 750 and mouseX < 1262 and mouseY > 50 and mouseY < 370:
                if subtileGraphics[subtileSelected*8:subtileSelected*8+8] != currentSubtileStackInfo:
                    undoStack.append([subtileSelected, currentSubtileStackInfo])
                    if len(undoStack) > 150:
                        undoStack = undoStack[50:]
                    redoStack = []
                ###print("C")
                subtileSelected = int(((mouseY - scroll2 - 50) // 32) * 16 + ((mouseX - 750) // 32))
                if subtileSelected > len(subtileGraphics)//8 - 1:
                    subtileSelected = len(subtileGraphics)//8 - 1
                if not subtileMode:
                    if subtileSelected < 0x100:
                        if subtileyPalleteyThingies[3] == True:
                            bigtilePalettes[ox400IndexThingForHere] ^= 0x8
                            subtileyPalleteyThingies[3] = False
                    else:
                        if subtileyPalleteyThingies[3] == False:
                            bigtilePalettes[ox400IndexThingForHere] ^= 0x8
                            subtileyPalleteyThingies[3] = True
                    subtileSelected %= 0x100  # bytes above 255 still hafta go back
                    ox400IndexThingForHere = bigtileSelected*2 + bigtileQuadrantSelected%2 + (bigtileQuadrantSelected//2)*0x20 + (bigtileSelected//0x10)*0x20
                    bigtileSubtiles[ox400IndexThingForHere] = subtileSelected
                else:
                    currentSubtileStackInfo = subtileGraphics[subtileSelected*8:subtileSelected*8+8]
                    subtileyPalleteyThingies[3] = False

            #clicking a collision colour (and change cur quadrant)
            elif mouseX > 0 and mouseX < 120 and mouseY > 400 and mouseY < 600 and not subtileMode:
                ###print("D")
                collisionSelected = ((mouseY-400)//40)*3+(mouseX//40)
                for key in collisionColourMapper:
                    if collisionColourMapper[key] == collisionSelected:
                        bigtileCollisions[bigtileSelected * 4 + bigtileQuadrantSelected % 4] = key
                        break

            #clicking a subtileythingy
            elif mouseX > 500 and mouseX < 700 and mouseY > 300 and mouseY < 350 and not subtileMode:
                ###print("E")
                if mouseX < 540: #button 1 (prio)
                    subtileyPalleteyThingies[0] = not subtileyPalleteyThingies[0]
                    bigtilePalettes[ox400IndexThingForHere] ^= 0x80
                elif mouseX > 550 and mouseX < 590: #button 2 (vt flip)
                    subtileyPalleteyThingies[1] = not subtileyPalleteyThingies[1]
                    bigtilePalettes[ox400IndexThingForHere] ^= 0x40
                elif mouseX > 600 and mouseX < 640: #button 3 (hz flip)
                    subtileyPalleteyThingies[2] = not subtileyPalleteyThingies[2]
                    bigtilePalettes[ox400IndexThingForHere] ^= 0x20
                elif mouseX > 650: #button 4 (bank)
                    subtileyPalleteyThingies[3] = not subtileyPalleteyThingies[3]
                    bigtilePalettes[ox400IndexThingForHere] ^= 0x8
                pygame.time.wait(100)

        #right clicks
        elif pygame.mouse.get_pressed()[2] == 1:
            #clicking a palette colour (change it)
            if mouseX < 80 and mouseY < 160:
                gogo = False
                while not gogo:
                    newHex = input(f"input new rgb values, separated by spaces (e.g. 12 23 255) (currently {hexCodes[(mouseY//20)*4+(mouseX//20)]}) (leave blank to abort): ")
                    if newHex != "":
                        newHex = newHex.split(" ", 3)
                        if len(newHex) != 3:
                            print("Invalid input.")
                        else:
                            try:
                                for i in range(3):
                                    newHex[i] = int(newHex[i])
                                hexCodes[(mouseY//20)*4+(mouseX//20)] = newHex
                                gogo = True
                            except Exception:
                                print("Invalid input.")
                    else:
                        gogo = True

        # loading palettes, and later subtiles and bigtiles
        if LOAD_BUTTON.draw(SCREEN):
            loadSubtileData(sportType)
            infoUpdater()

        # saving palette and tile data to a game
        if SAVE_BUTTON.draw(SCREEN):
            saveThineData(sportType)

        #making pngs of bigtiles
        if PRINT_BUTTON.draw(SCREEN):
            #making folders if needed
            if not os.path.exists(f"tiles/temptiles"):
                os.makedirs(f"tiles/temptiles")
            if not os.path.exists(f"tiles/efftemptiles"):
                os.makedirs(f"tiles/efftemptiles")
            #loop for each bigtile
            for i in range(0x100):
                guaug = []
                for j in (1,0): #first j will add the bottom subtiles to guaug, second j will add the top ones (no idea why it needs to be 0 1, it just doesn't work as 1, 0 though my logic sayc it should wasawawawa)
                    ox400er = (i%0x10)*2 + (i//0x10)*0x40 + (j)*0x20 #weirdo address calculator because it's stored all messily
                    P = bigtilePalettes[ox400er:ox400er+2] #palette data at address and address + 1
                    palettes = [pal & 7 for pal in P] #and 7 to get the palette number (stored in bits 0 1 and 2)
                    palettecode = []
                    graphicsies = []
                    for k in (0,1): #first does the left subtile, next does the right subtile
                        for l in range(4): # converting hex code palette data into bitmap file palette data
                            RGB = hexCodes[palettes[k]*4 + l]
                            G = bin(RGB[1] >> 3)[2:].zfill(5) #next is a lil different as BMP uses GGGBBBBB XRRRRRGG
                            temp = G[2:].zfill(3) + bin(RGB[2] >> 3)[2:].zfill(5) + "0" + bin(RGB[0] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                            bitey = int(temp, 2).to_bytes(2, "big")
                            palettecode.append(bitey)

                        subtile = bigtileSubtiles[ox400er+k] + (P[k]&0x8)*0x20 #add 0x100, the 02 is just b/c multed with 0x8 cuz less lines, so felt like it
                        graphicsies.append(subtileGraphics[subtile*8:subtile*8+8][::-1]) #stores quaternary row graphics, so need to get the 8 starting at s*8
                    for k in (0,1):
                        if bigtilePalettes[ox400er+k] & 0x40: #vt flip
                            graphicsies[k] = graphicsies[k][::-1]
                        if bigtilePalettes[ox400er+k] & 0x20: #hz flip
                            for l in range(8):
                                graphicsies[k][l] = graphicsies[k][l][::-1]
                    for k in range(8):
                        for bit in graphicsies[0][k]:#graphicsies[0] has 8 bytes in its list (contains the left subtile's data.) ([1] has 8 bytes for the right subtile)
                            guaug.append(palettecode[int(bit)]) #would += to a b'' but that takes super long
                        for bit in graphicsies[1][k]:
                            guaug.append(palettecode[int(bit)+4])
                with open(f"tiles/temptiles/tile{str(i).zfill(3)}.bmp", "wb") as bmp:
                    bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (16).to_bytes(4, "little") + (16).
                    to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(guaug))
                ######
                ###### now collisions
                gorg = b''
                for j in (1,0): #first j will add the bottom subtiles to guaug, second j will add the top ones (no idea why it needs to be 0 1, it just doesn't work as 1, 0 though my logic sayc it should wasawawawa)
                    ox400er = i*4 + j*2 #normal this time
                    C = bigtileCollisions[ox400er:ox400er+2]
                    wwwwww = b''
                    for k in range(2):
                        for l, key in enumerate(collisionColourMapper):
                            if key == C[k]:
                                RGB = colours[l]
                                break
                        G = bin(RGB[1] >> 3)[2:].zfill(5)  # next is a lil different as BMP uses GGGBBBBB XRRRRRGG
                        temp = G[2:].zfill(3) + bin(RGB[2] >> 3)[2:].zfill(5) + "0" + bin(RGB[0] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                        wwwwww += (int(temp, 2).to_bytes(2, "big") * 8)
                    gorg += (wwwwww)*8
                with open(f"tiles/efftemptiles/tile{str(i).zfill(3)}.bmp", "wb") as bmp:
                    bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (16).to_bytes(4, "little") + (16).
                    to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + gorg)
            print("tiles saved to temp folders in levels as bmp files!")
            name = input("do you want to turn these into png files, and if so to which folder should they be saved? (makes folders called 'name' and 'name_effects' in the tiles folder, unless they exist already) (leave blank for no): ")
            if name != "":
                go_ahead = True
                if os.path.exists(f"tiles/{name}") or os.path.exists(f"tiles/{name}_effects"):
                    if input(f'a folder with this name ({name} or {name}_effects exists. Do you want to overwrite it? ("Y" for yes) ').upper() != "Y":
                        go_ahead = False
                if go_ahead:
                    print("working...")
                    pngify(name)
                    pygame.time.wait(200)
                    print("done! :)")
                else:
                    print("no changes have been made.")

        #prints where subtiles are used in bigtiles
        if SUBTILE_USAGE_BUTTON.draw(SCREEN):
            bigtilesUsing = []
            breakFlag = False
            for i in range(0x100): #for each bigtile
                if breakFlag:
                    break
                for j in range(4):
                    ox400PainIndex = (i%0x10)*2 + (i//0x10)*0x40 + (j%2) + (j//2)*0x20 #why must these be stored in such a strange order :(
                    if bigtileSubtiles[ox400PainIndex]+((bigtilePalettes[ox400PainIndex]&0x8) * 0x20) == subtileSelected + adder: #palette adds 0x100 if using the next bank
                        bigtilesUsing.append(str(i) + quadrantMapper[j])
            if bigtilesUsing == []:
                print(f"subtile {subtileSelected + adder} is never used in any bigtile.")
            else:
                print(f"subtile {subtileSelected + adder} is used in these bigtiles: {[i for i in bigtilesUsing]}")
            pygame.time.wait(200)

        adder = 0
        if subtileyPalleteyThingies[3]:
            adder = 0x100

        #testing drawing palettes
        for i in range(0x20):
            rectangle = pygame.Rect = ((i*20)%80,((i)//4)*20,20,20)
            pygame.draw.rect(SCREEN, hexCodes[i], rectangle)
        # and highlight the selected one
        highlightangle = (20 * colourSelected, 20 * paletteSelected, 20, 20)
        pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

        #testing drawing changeable subtiles
        if subtileMode:
            for i in range(8):
                for j in range(8):
                    rectangle = pygame.Rect = ((100 + j * 40), (50 + i * 40), 40, 40)
                    try:
                        wower = (subtileGraphics[(subtileSelected + adder) * 8 + i][j])
                        pygame.draw.rect(SCREEN, hexCodes[paletteSelected*4+(int(wower))], rectangle)
                    except Exception:
                        break
        #and drawing changeable bigtiles:
        else:
            #drawing collision colours
            for i in range(5):
                for j in range(3):
                    rectangle = pygame.Rect = ((j * 40), (400 + i * 40), 40, 40)
                    pygame.draw.rect(SCREEN, colours[i*3+j], rectangle)
            #and highlight the selected one
            highlightangle = (40 * (collisionSelected % 3) + 0, 40 * (collisionSelected // 3) + 400, 40, 40)
            pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

            if displayBigtileSubtiles:
                #drawing subtiles on big bigtile:
                for i in range(2):
                    for j in range(2):
                        go_long = 0
                        hz_range = range(8)
                        vt_range = range(8)
                        ox400LengthStartIndex = bigtileSelected*2 + j + (i * 0x20) + (bigtileSelected // 16) * 0x20
                        palalala = (bigtilePalettes[ox400LengthStartIndex])
                        if palalala & 0x8 == 0x8:
                            go_long = 1
                        if palalala & 0x20 == 0x20:
                            hz_range = hz_range[::-1]
                        if palalala & 0x40 == 0x40: # vt flip
                            vt_range = vt_range[::-1]
                        for k, K in enumerate(vt_range):
                            for l, L in enumerate(hz_range):
                                rectangle = pygame.Rect = ((100 + l*20 + j*160), (50 + k*20 + i*160), 20, 20)
                                try:
                                    pygame.draw.rect(SCREEN, hexCodes[(palalala&7)*4+int(subtileGraphics[bigtileSubtiles[ox400LengthStartIndex]*8+K+go_long*0x800][L])], rectangle)
                                except Exception:
                                    continue

            if displayBigtileCollision:
                #drawing collison on big bigtile
                for i in range(2):
                    for j in range(2):
                        s = pygame.Surface((160, 160))
                        if alpher:
                            s.set_alpha(150)
                        s.fill(colours[collisionColourMapper[bigtileCollisions[bigtileSelected * 4 + j + i*2]]])
                        SCREEN.blit(s, (100 + j * 160, 50 + i * 160))

        # highlight the selected quadrant
        if not subtileMode:
            highlightangle = (100 + (bigtileQuadrantSelected % 2) * 160, 50 + (bigtileQuadrantSelected // 2) * 160, 160, 160)
            pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

        # drawing the subtile menu thing in top right
        wowowo()
        # and highlight the selected one
        highlightangle = (32 * (subtileSelected % 16) + 750, 32 * (subtileSelected // 16) + 50 + scroll2 + adder * 2, 32, 32)
        pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

        # draw sport buttons, sport button memory, & actions
        sportCount = 0
        for sportCount, typeButton in enumerate(sportTypeButtons):
            if typeButton.draw(SCREEN):
                sportType = sportCount

        #highlight for sport type
        pygame.draw.rect(SCREEN, (255, 0, 0), sportTypeButtons[sportType], 1)

        if not subtileMode:
            # drawing subtile palettey extra thingies
            for i, thingy in enumerate(subtileyPalleteyThingies):
                rectangle = pygame.Rect = (500 + i*50, 300, 40, 40)
                if thingy:
                    pygame.draw.rect(SCREEN, (255, 255, 0), rectangle)
                else:
                    pygame.draw.rect(SCREEN, (75, 75, 100), rectangle)

            # and the display toggler buttons
            if TOGGLE_SUBTILES_BUTTON.draw(SCREEN):
                displayBigtileSubtiles = not displayBigtileSubtiles
                alpher = not alpher
                pygame.time.wait(200)

            if TOGGLE_COLLISIONS_BUTTON.draw(SCREEN):
                displayBigtileCollision = not displayBigtileCollision
                pygame.time.wait(200)

            SCREEN.blit(thefont.render(f"bigtile: {bigtileSelected}", False, (0, 0, 0)), (100, 8))

        SCREEN.blit(thefont.render(f"subtile: {subtileSelected + adder}", False, (0, 0, 0)), (950, 8))

        if INFO_BUTTON.draw(SCREEN):
            infoMode = not infoMode
            pygame.time.wait(200)

    pygame.display.update()
