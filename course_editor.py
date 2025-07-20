# heavily based off of Coding With Russ' videos, so figured i should give credit here

import pygame
import button
import csv
import re
import glob
from PIL import Image
import os
import tkinter
from enum import Enum

#  pygame initializer
pygame.init()

#  window maker
screenHeight = 720
screenWidth = 1280
SCREEN = pygame.display.set_mode((screenWidth, screenHeight))

# icon
ICON = pygame.image.load("tile_editor_pictures/raftin.png")
pygame.display.set_icon(ICON)

# various mode 0 variables
CONST_SPORTS = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
SPORTS = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
DIFFICULTIES = ["Beginner", "Intermediate", "Expert"]

MAX_SPORT_HEIGHTS = [[0x21A, 0x2A1, 0x31E], [0x21A, 0x2A1, 0x31E], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF], [0x21B, 0x2A1, 0x3FF]]  # some courses (experts) have some blank space at the ends which can be used. technically the long experts have 0x3FFB tiles at the ready, but gotta be a mult of 0x10 to have a complete row so may as well not
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

effectsOn = False

class programModes(Enum):
    courseEditor = 0
    subtileDrawer = 1
programMode = programModes.courseEditor

clock = pygame.time.Clock()

checkerenate = False

BEARS_COURSE_HEIGHT_OFFSETS = [0x4B53, 0x8B6B, 0xCAEF, 0x10B28, 0x14C15, 0x18C2E]
bearsCourseHorizontalSpawns = [[0xB8, 0x98, 0x58], [0xB8, 0x98, 0x98], [0xB8, 0x98, 0x98], [0xB8, 0x68, 0x68], [0xB8, 0x68, 0x68], [0x78, 0x78, 0x78]]
bearsCourseCameras = [[0x60, 0x46, 0x14], [0x60, 0x50, 0x50], [0x60, 0x60, 0x46], [0x60, 0x20, 0x18], [0x60, 0x28, 0x28], [0x1E, 0x1E, 0x1E]]

selectOrigCoords = []
stampArr = [[0]]

class drawModes(Enum):
    draw = 0
    bucket = 1
    stamp = 2
drawMode = drawModes.draw

# various mode 1 or both
hexCodes = [[100, 0, 0]] * 0x20
bigtileCollisions = [0] * 0x400
spriteSubtiles = [[0] * 0x400]
spritePalettes = [[0] * 0x400]
subtileGraphics = [["00000000"] * 0x100]  # 0x1EA0]
subtileSelected = 0
colourSelected = 0
paletteSelected = 0
subtileMode = True
colours = [[255, 219, 182], [102, 102, 102], [129, 212, 26], [180, 199, 220], [255, 166, 166], [107, 94, 155], [129, 172, 166], [129, 55, 9], [52, 101, 164], [255, 128, 0], [120, 3, 115], [21, 132, 102], [241, 13, 12], [34, 75, 18], [172, 178, 12]]
COLLISION_COLOUR_MAPPER = {0x00: 0,
                           0x02: 1,
                           0x03: 2,
                           0x08: 3,
                           0x0C: 4,
                           0x11: 5,
                           0x21: 6,
                           0x31: 7,
                           0x32: 8,
                           0x33: 9,
                           0x42: 10,
                           0x73: 11,
                           0x82: 12,
                           0xB3: 13,
                           0xC0: 14}

collisionSelected = 0
bigtileSelected = 0
bigtileQuadrantSelected = 0

subtileyPalleteyThingies = [False] * 3  # priority, vt_flip, hz_flip
ox400IndexThingForHere = 0
displayBigtileSubtiles = True
displayBigtileCollision = True
alpher = True
scrollLeft = False
scrollRight = False
waiter = True
infoMode = False

lockFileName = False
lockedFileName = ""

undoStack = []
redoStack = []
currentSubtileStackInfo = []

# copy paste variables in subtile mode
subtileClipboardNumber = 0
subtileClipboard = [["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"], ["00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"]]

QUADRANT_MAPPER = {0: "TL", 1: "TR", 2: "BL", 3: "BR"}
maxSubtiles = []
groupNum = 0
BIGTILE_COLLISION_OFFSETS = [0x4D6C, 0x8DCD, 0xCCE1, 0x10DAA, 0x14EF1, 0x19031]
SUBTILE_GRAPHICS_OFFSETS = [0x5976, 0x99D7, 0xD8EB, 0x119B4, 0x15AFB, 0x19C3B]
SUBTILE_GRAPHICS_LENGTHS = [0x1EA0, 0x1DC0, 0x1FA0, 0x1FD0, 0x1F70, 0x1900]

# spritey stuff:
BROBEAR_SPRITE_OFFSETS = [[],
[(0x20000, 0x21128), (0x9C000, 0x9C69E, 0x9CB4F), (0x9EBD5, 0x9F384, 0x9F8BE), (0x9CF56, 0x9D62B, 0x9DABE), (0xA110D, 0xA1BF6, 0xA21A0), (0x9DE3C, 0x9E52E, 0x9E7BE), (0xA0000, 0xA068C, 0xA0A5F), (0x21D65, 0x220C5), (), (0x21BF4, 0x21CD7, 0x236A3), (), (), (0x222D1, 0x22E30), (), ([0x24000, 0x2496E], [0x25034, 0x2627E]), (), ()],
[],
[(0x4E1B4, 0x4F282), (0xA2D00, 0xA3630), (0xA6536, 0xA709A), (0xA4000, 0xA493B, 0xA4DD0), (0xA8D7C, 0xA9137, 0xA936B), (0xA5769, 0xA6089), (0xA8000, 0xA8977), (), (), (0x139CE, 0x13A69, 0x13AE2), (), (), (), (0x916F6, 0x9223D), ([0x90000, 0x90976], [0x90D36, 0x91359]), ()],
[(0x8C000, 0x8CF2E), (0x99AE4, 0x99DC9, 0x99FF3), (0x98B82, 0x98FC1, 0x99246), (0x9A2C7, 0x9A594, 0x9A784), (0x994F6, 0x99734, 0x9990C), (0x98000, 0x9846E, 0x98766), (0x9A9C9, 0x9ADF3, 0x9B151), (0x2B459, 0x2B779), (), (0x26E9B, 0x26F36, 0x26FAF), (0x2704A, 0x274A5), (0x276CF, 0x27B2A, 0x1F35F), (), (), ([0x2EA14, 0x2F3F0], [0x5A1B4, 0x5AF03]), (), (0xDC000, 0xDC5DC)],
[(0xC9DFD, 0xCAE58), (0x92724, 0x92B71, 0x92E37), (0x94585, 0x94B70, 0x94F3B), (0x93185, 0x9342E, 0x935D8), (0x95969, 0x96005, 0x963D7), (0x9688E, 0x96F4F, 0x9738A), (0x9536C, 0x95615, 0x95737), (0xB7E1, 0xBB23), (0x94000, 0x94386), (0x1B585, 0x1B5F8, 0x1B638), (0x3F1E4, 0x3F537), (0x8D7AB, 0x8D9EE, 0x6664B), (), (), ([0x331E4, 0x3398C], [0x3AA14, 0x3B0A7]), (0x84000, 0x84EAA), (0x421B4, 0x427A0)]]
# moving, A, B, AUL, BUL, AUR, BUR, Lramp, Rramp, jump, mud, pud, ice, whirl, wipeout, slowing, stopped

SISBEAR_SPRITE_OFFSETS = [[],
[(0xC0000, 0xC127C), (0xD2131, 0xD27CF, 0x9CB4F), (0xD4A0A, 0xD5153, 0x9F8BE), (0xD2BE7, 0xD32BC, 0x9DABE), (0xD60FD, 0xD6BE6, 0xA21A0), (0xD4000, 0xD46F2, 0x9E7BE), (0xD565A, 0xD5CE6, 0xA0A5F), (0xCC13E, 0xCC49E), (), (0xCC000, 0xCC0C1, 0x236A3), (), (), (0xCC6CC, 0xCD1C5), (), ([0xCDA9E, 0xCE3D9], [0xD0000, 0xD129F]), (), ()],
[],
[(0xC4000, 0xC50CE), (0xD724B, 0xD7A38), (0xB5EBF, 0xB69F0, 0xA4DD0), (0xCEA4A, 0xCF352, 0xA936B), (0x8B914, 0x8BCCF), (0xB6F6B, 0xB78AD), (0x8E7AE, 0x8F125), (), (), (0xE1729, 0xE17C4, 0x13AE2), (), (), (), (0xE183D, 0xE2384), ([0xE0000, 0xE0987], [0xE0D47, 0xE136A]), (), ()],
[(0xC20DE, 0xC2F84), (0xDD1BA, 0xDD48E, 0x99FF3), (0xDE2EC, 0xDE72B, 0x99246), (0xDD6FC, 0xDD9A7, 0x9A784), (0xDF204, 0xDF464, 0x9990C), (0xDDBFD, 0xDE016, 0x98766), (0xDEA5A, 0xDEE84, 0x9B151), (0xDB105, 0xDB425), (), (0xDA74C, 0xDA7E7, 0x26FAF), (0xDA860, 0xDAD87), (0x1EE38, 0x1F556, 0x1F35F), (), (), ([0xD8000, 0xD89CB], [0xD9066, 0xD9D4F]), (), (0xDC899, 0xDCE64)],
[(0xC5C94, 0xC6CEF), (0xFC000, 0xFC44D, 0x92E37), (0x5EA14, 0x5F087, 0x94F3B), (0x6686C, 0x66AD1, 0x935D8), (0x52F22, 0x535E0, 0x963D7), (0x66C9D, 0x6736F, 0x9738A), (0x52A14, 0x52D12, 0x95737), (0x6B1E4, 0x6B56A), (0x6B7F1, 0x6BB77), (0x6AA14, 0x6AA87, 0x1B638), (0x6AAFA, 0x6AE80), (0x661B4, 0x6643B, 0x6664B), (), (), ([0x8ACD2, 0x8B425], [0x8DCDB, 0x8E32A]), (0x7630B, 0x77193), (0x42B17, 0x43103)]]

FAMILYBEAR_SPRITE_OFFSETS = [[(0x1C000, 0x1D08F, 0x1DB5B), (0xA970E, 0xAA4F8, 0xAADC5, 0xAB340), (0xAE58C, 0xAECD6, 0xAF013, 0xAF284), (0xAC000, 0xAC739, 0xACA65, 0xACD5E), (0xB186F, 0xB236D, 0xB28E8, 0xB2E1F), (0xAD541, 0xADB45, 0xADEF6, 0xAE2B8), (0xB0000, 0xB0AD7, 0xB1229, 0xB16C2), (0x1E3AC, 0x1E82D, 0x1EB5A), (), (0x1E22B, 0x1E2C2, 0x1E337, 0x1EDBB), (), (), (0x74000, 0x75104, 0x75C74), (), ([0x70000, 0x70D5A, 0x71454], [0x71AF9, 0x7270E, 0x72F9E], [0x361A4, 0x370B6, 0x378CF], [0x2A1A4, 0x2AA39, 0x2AD7E]), (), ()],
[],
[([0x80000, 0x80C78, 0x81360], [0x81B14, 0x82B1E, 0x83253], [0xC8000, 0xC8E3F, 0xC93BA]), (0xBDD31, 0xBEA18, 0xBF127), (0xBC000, 0xBCE94, 0xBD73F), (0xBA2DF, 0xBAB5B, 0xBB162, 0xBB4B0), (0xB8000, 0xB8CB8, 0xB9541, 0xB9A78), (0xB4000, 0xB4676, 0xB4AFF), (0xB4E89, 0xB56C0, 0xB5BE9), (), (), (0xF8D5, 0xF9FC, 0xFA8A, 0xFAF6), (), (), (), (0x85B45, 0x86CB0, 0x87821), ([0x88000, 0x889CE, 0x88FC2], [0x894B7, 0x89FDF, 0x8A5A6]), (), ()]]

BRO_OBJ_PALETTE_OFFSETS = [0, 0x210E8, 0, 0x4F242, 0x8CEEE, 0xCAE18]
SIS_OBJ_PALETTE_OFFSETS = [0, 0xC123C, 0, 0xC508E, 0xC2F44, 0xC6CAF]
FAMILY_OBJ_PALETTE_OFFSETS = [0x1D04F, 0, 0x80C38]

MORE_SPRITEISH_OFFSETS = [0x7A787, 0x7A7C4, 0xE52AA, 0xEA25C, 0xEA17E]

MORE_PALETTEY_OFFSETS = ['OBJ', 'OBJ', 0xE5967, 0xEA21C, 0xEA21C]

LONG_GRAPHICS_OFFSETS = [0xFA144, 0xEA344, 0xF6167, 0xE8000, 0x79073, 0x79BFD, (0xED4EA, 0xF108A, 0xF4153, 0xF8000, 0xEE7A4, 0xF1F74, 0xF516D, 0xF90CA, 0xEC000, 0xF0000), 0x46A14, (0xE59A7, 0xE6819, 0xE4000)]

LONG_PALETTE_OFFSETS = [0xFA64E, 0xEA61E, 0xF6731, (0xE86D6, 0xEA060, 0xEA0AA, 0xEA0F4, 0xEA13E), 0x791BD, 0x79D47, (0xED7C4, 0xF1364, 0xF442D, 0xF82DA, 0xEEA7E, 0xF224E, 0xF5447, 0xF93A4, 0xEC2DA, 0xF02DA), (0x4705E, 0x47F98), (0xE5E49, 0xE6CBB, 0xE42DA)]

LONG_GRAPHICS_LENGTHS = [0x1550, 0x1270, 0x10A0, 0x1940, 0xA00, 0xB60, (0xFA0, 0xBD0, 0xD00, 0xDB0, 0xF60, 0xBD0, 0xCE0, 0xD60, 0x11D0, 0xD70), 0xEF0, (0x990, 0x900, 0xF90)]

SPRITES = ["moving", "a trick", "b trick", "a up left trick", "b up left trick", "a up right trick", "b up right trick", "left side ramp", "right side ramp", "ramp jump", "mud", "puddle", "ice", "whirlpool", "wipeout", "slowing", "stopped", "HUD difficulties", "HUD sports", "medal", "5x5 selectangle", "4x3 selectangle", "course bigtile", "dev&publisher credit intro", "cool brother bear biking intro", "car intro", "various menu items", "font 1", "font 2", "course intro", "scoreboard", "podium finish"]
BEARTYPES = ["brother", "sister"]
spriteType = 22
loadedSpriteType = 22
bearType = 0
loadedBearType = 0
loadedSportType = 0
loadedMenuPagePalette = 0
layers = 1
layerChosen = 0
eyeMode = False
HIGHLIGHTY_SPRITE_RECTANGLE_POSITIONS = [(981, 631, 18, 18), (1082, 608, 18, 18), (1103, 608, 18, 18), (1082, 629, 18, 18), (1103, 629, 18, 18), (1082, 650, 18, 18), (1103, 650, 18, 18), (972, 596, 18, 18), (1014, 596, 18, 18), (993, 596, 18, 18), (1156, 596, 18, 18), (1177, 596, 18, 18), (1177, 617, 18, 18), (1156, 617, 18, 18), (1167, 638, 18, 18), (1002, 631, 18, 18), (1023, 631, 18, 18), (950, 651, 18, 18), (971, 651, 18, 18), (992, 651, 18, 18), (1013, 651, 18, 18), (1034, 651, 18, 18), (960, 631, 18, 18), (772, 608, 18, 18), (793, 608, 18, 18), (814, 608, 18, 18), (772, 629, 18, 18), (793, 629, 18, 18), (814, 629, 18, 18), (772, 650, 18, 18), (793, 650, 18, 18), (814, 650, 18, 18)]
tempRect = pygame.Rect = HIGHLIGHTY_SPRITE_RECTANGLE_POSITIONS[0]
tempRect2 = pygame.Rect = (0, 0, 0, 0)
HIGHLIGHTY_BEAR_RECTANGLE_POSITIONS = [(1230, 592, 38, 38), (1230, 633, 38, 38)]
bearRect = pygame.Rect = HIGHLIGHTY_BEAR_RECTANGLE_POSITIONS[0]
frameCount = 256
spriteHeight = [2]
spriteWidth = [2]
quadrantPixel = 15
PALETTE_PIXEL = 20
COLLISION_PIXEL = 40
SMALLTILE_PIXEL = 4
THINGY_PIXEL = 40
numOfSubtiles = len(subtileGraphics[layerChosen])//8
NUM_OF_SMALLTILES_DISPLAYED_VT = ((320 + SMALLTILE_PIXEL) // (SMALLTILE_PIXEL * 8))
NUM_OF_SMALLTILES_DISPLAYED_HZ = (64//SMALLTILE_PIXEL)
MAX_SCROLL2 = -704 #min(0, -(8 * (numOfSubtiles // (NUM_OF_SMALLTILES_DISPLAYED_HZ)) * SMALLTILE_PIXEL - 290)) ughh whatever ill just hope nobody cares
# [((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ())],


# waiting times to stop button double clicks and to slow down some scrolling
buttonWait = 0
infoWait = 0
thingyWait = 0
subtileUsageWait = 0
scrollLRWait = 0
subtileMovWait = 0
bigQuadMovWait = 0
subtileMovement = 0
bigQuadMovement = 0


# non tile images
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
# SPRITE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/spriteEditorButton.png')
SUBTILE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/subtileEditorButton.png')
BIGTILE_EDITOR_IMAGE = pygame.image.load(f'tile_editor_pictures/bigtileEditorButton.png')
TOGGLE_SUBTILES_IMAGE = pygame.image.load(f'tile_editor_pictures/toggleSubtilesButton.png')
TOGGLE_COLLISIONS_IMAGE = pygame.image.load(f'tile_editor_pictures/toggleCollisionsButton.png')
PRINT_IMAGE = pygame.image.load(f'tile_editor_pictures/printButton.png')
LOCK_FILE_NAME_IMAGE = pygame.image.load(f'tile_editor_pictures/lockFileName.png')
LOAD_FROM_GAME_IMAGE = pygame.image.load(f'tile_editor_pictures/loadFromGameButton.png')
LOAD_FULL_GAME_IMAGE = pygame.image.load(f'tile_editor_pictures/loadFullGameButton.png')
LOAD_LEVEL_TILES_IMAGE = pygame.image.load(f'tile_editor_pictures/loadLevelTilesButton.png')
INFO_IMAGE = pygame.image.load(f'tile_editor_pictures/infoButton.png')
INFO_IMAGES = [pygame.image.load(f'tile_editor_pictures/infoCourseEditor.png'),
               pygame.image.load(f'tile_editor_pictures/infoTileEditor.png'),
               pygame.image.load(f'tile_editor_pictures/infoSpriteEditor.png'),
               pygame.image.load(f'tile_editor_pictures/infoLongPicEditor.png')]
SUBTILE_USAGE_IMAGE = pygame.image.load(f'tile_editor_pictures/checkSubtileUsage.png')
HEIGHT_CHANGE_IMAGE = pygame.image.load(f'tile_editor_pictures/levelHeightChangeButton.png')
HORIZONTAL_SPAWN_IMAGE = pygame.image.load(f'tile_editor_pictures/horizontalSpawnButton.png')
PENCIL_IMAGE = pygame.image.load(f'tile_editor_pictures/pencil.png')
BUCKET_IMAGE = pygame.image.load(f'tile_editor_pictures/bucket.png')
STAMP_IMAGE = pygame.image.load(f'tile_editor_pictures/stamp.png')
SPAWN_CAM_IMAGE = pygame.image.load(f'tile_editor_pictures/spawnCamButton.png')
wawa = pygame.image.load(f'tile_editor_pictures/wawa.png')
EYE_IMAGES = [pygame.image.load(f'tile_editor_pictures/eyesEeNothing.png'),
              pygame.image.load(f'tile_editor_pictures/eyesWideOpen.png')]

# button instances
sportTypeButtons = []
sportDifficultyButtons = []
tileInvButtons = []

"""
hzSportPos = [560, 704, 560, 704, 560, 704]
hzSportPosShift = [360, 320, 360, 320, 360, 320]
vtSportPos = [45, 45, 90, 90, 135, 135]
vtSportPosShift = 360
"""
def sportTypeButtonMover(mode):
    global sportTypeButtons
    sportTypeButtons = []
    sportTypeButtons.append(button.Button(560 + (360 * mode), 45 + 360 * mode, TOBOGGAN_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 + (320 * mode), 45 + 360 * mode, SLED_IMAGE, 2))
    sportTypeButtons.append(button.Button(560 + (360 * mode), 90 + 360 * mode, RAFT_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 + (320 * mode), 90 + 360 * mode, KAYAK_IMAGE, 2))
    sportTypeButtons.append(button.Button(560 + (360 * mode), 135 + 360 * mode, BIKE_IMAGE, 2))
    sportTypeButtons.append(button.Button(704 + (320 * mode), 135 + 360 * mode, DIRTBOARD_IMAGE, 2))
    """ tbh idk which is more readable, think i prefer the old way?
    sportImages = [TOBOGGAN_IMAGE, SLED_IMAGE, RAFT_IMAGE, KAYAK_IMAGE, BIKE_IMAGE, DIRTBOARD_IMAGE]
    sportButtonScale = 2
    for i in range(6):
        sportTypeButtons.append(button.Button(
            hzSportPos[i] + (hzSportPosShift[i] * mode),
            vtSportPos[i] + (vtSportPosShift * mode),
            sportImages[i],
            sportButtonScale)
        )
    """


sportTypeButtonMover(0)

# same readability question as earlier
sportDifficultyButtons.append(button.Button(550, 190, BEGINNER_IMAGE, 2))
sportDifficultyButtons.append(button.Button(640, 190, INTERMEDIATE_IMAGE, 2))
sportDifficultyButtons.append(button.Button(730, 190, EXPERT_IMAGE, 2))

"""
hzDifficultyPos = [550, 640, 730]
vtDifficultyPos = 190
difficultyImages = [BEGINNER_IMAGE, INTERMEDIATE_IMAGE, EXPERT_IMAGE]
difficultyButtonScale = 2
for i in range(3):
    sportDifficultyButtons.append(button.Button(
        hzDifficultyPos[i],
        vtDifficultyPos,
        difficultyImages[i],
        difficultyButtonScale)
    )
"""

GRID_BUTTON = button.Button(710, 10, GRID_IMAGE, 1)
SAVE_BUTTON = button.Button(750, 10, SAVE_IMAGE, 1)
LOAD_BUTTON = button.Button(790, 10, LOAD_IMAGE, 1)
EFFECTS_BUTTON = button.Button(658, 10, EFFECTS_IMAGE, 2)
COURSE_EDITOR_BUTTON = button.Button(1125, 400, COURSE_EDITOR_IMAGE, 0.5)
TILE_EDITOR_BUTTON = button.Button(1200, 400, TILE_EDITOR_IMAGE, 0.5)
# SPRITE_EDITOR_BUTTON = button.Button(1150, 400, SPRITE_EDITOR_IMAGE, 1)
SUBTILE_EDITOR_BUTTON = button.Button(1125, 475, SUBTILE_EDITOR_IMAGE, 0.5)
BIGTILE_EDITOR_BUTTON = button.Button(1200, 475, BIGTILE_EDITOR_IMAGE, 0.5)
TOGGLE_SUBTILES_BUTTON = button.Button(300, 500, TOGGLE_SUBTILES_IMAGE, 1)
TOGGLE_COLLISIONS_BUTTON = button.Button(400, 500, TOGGLE_COLLISIONS_IMAGE, 1)
PRINT_BUTTON = button.Button(830, 10, PRINT_IMAGE, 1)
LOCK_FILE_NAME_BUTTON = button.Button(910, 10, LOCK_FILE_NAME_IMAGE, 1)
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
EYE_BUTTON = button.Button(856, 395, EYE_IMAGES[0], 1)


# makes bottom right buttons (the bigtile map)
def gridButtonMaker():
    currentColumn = 0
    currentRow = 0

    for byte in allLevelTileCSVs[sportType][sportDifficulty]:
        temp = currentRow * gridTileWidth + scroll
        if -32 <= temp <= screenHeight:  # don't need to draw things off screen
            SCREEN.blit(imageList[sportType][0][byte], (0 + currentColumn * gridTileWidth, 0 + currentRow * gridTileWidth + scroll))
            if effectsOn:
                SCREEN.blit(imageList[sportType][1][byte], (0 + currentColumn * gridTileWidth, 0 + currentRow * gridTileWidth + scroll))
        currentColumn += 1
        if currentColumn == 16:
            currentColumn = 0
            currentRow += 1


def checkerer():
    temp = (scroll % 32) - 32
    layer = 0
    thetangle = pygame.Surface((32, 32))
    thetangle.set_alpha(100)
    thetangle.fill((0, 0, 0))
    while temp < screenHeight:
        for i in range(16):
            if (i + layer) % 2 == 0:
                SCREEN.blit(thetangle, (i * 32, temp))
        layer += 1
        temp += 32


# tilemap data storage (lists in lists, where list[sport][diff] = the correct data)
for sport in range(6):
    tempCSVPair = []
    for difficulty in range(3):
        # loads every csv of the default maps
        tempCSVRead = re.split(",|\n", open(f"levels/{SPORTS[sport]}{DIFFICULTIES[difficulty]}.csv", "r").read())

        # sportHeights[sport][difficulty] = int(tempCSVRead[0])
        # bearsCourseHorizontalSpawns[sport][difficulty] = int(tempCSVRead[1])
        # bearsCourseCameras[sport][difficulty] = int(tempCSVRead[2]) already loaded in, but i'll keep it

        # reads data in said csv files (first 16 bytes are non-tile data)
        tempCSV = [int(byte) for byte in tempCSVRead[16:-1]]
        # fill rest with FF
        tempCSV += ([0xFF] * ((MAX_SPORT_HEIGHTS[sport][difficulty] * 0x10) - len(tempCSV)))
        tempCSVPair.append(tempCSV)
    allLevelTileCSVs.append(tempCSVPair)


# tile images (they change depending on the sport type)
def tileImageStorer(sport):
    sportTileLists = []
    tileList = []
    for i in range(NUMBER_OF_TILES):
        tile = pygame.image.load(
            f'tiles/{sport}/tile{i}.png').convert_alpha()  # you can replace i with ((hex(i)[2:]).zfill(2)).upper() if you want, just remember to generate tile names w/ hex as well
        tile = pygame.transform.scale(tile, (32, 32))
        tileList.append(tile)
    sportTileLists.append(tileList)
    tileList = []
    for i in range(NUMBER_OF_TILES):
        tile = pygame.image.load(
            f'tiles/{sport}_effects/tile{i}.png').convert_alpha()  # you can replace i with ((hex(i)[2:]).zfill(2)).upper() if you want, just remember to generate tile names w/ hex as well
        tile = pygame.transform.scale(tile, (32, 32))
        tile.set_alpha(215)  # transparency for effect tiles
        tileList.append(tile)
    sportTileLists.append(tileList)
    return sportTileLists


imageList = []
for sport in SPORTS:
    tempImages = tileImageStorer(sport)
    imageList.append(tempImages)


# clickable tile buttons (bottom right) for one sport
def buttonMaker(sportIndex):
    singleSportButtonList = []
    currentColumn = 0
    currentRow = 0
    for i in range(NUMBER_OF_TILES):
        singleSportButtonList.append(
            button.Button(529 + currentColumn * 18, 304 + currentRow * 18, imageList[sportIndex][0][i], 0.5))
        currentColumn += 1
        if currentColumn == 16:
            currentColumn = 0
            currentRow += 1

    return singleSportButtonList


# makes a list of the clickable bigtiles in the bottom right
clicky_tiles = []
for i in range(6):
    tempButtons = buttonMaker(i)
    clicky_tiles.append(tempButtons)

# setting up tiles in inventory
tileInvPictures = [0] * 10


##  course editor funcs
#  load a new course
def loadLevel(name, sportType, sportDifficulty):
    global allLevelTileCSVs
    global sportHeights
    global bearsCourseHorizontalSpawns
    global bearsCourseCameras
    with open(f"levels/modified_levels/{name}.gbc", "rb") as file:
        tempAllData = file.read()
        levelOffset = BEARS_LEVEL_DATA_OFFSET_RANGES[sportType][sportDifficulty]
        chunkStart = (0xA + sportType * 3 + sportDifficulty) * 0x4000
        sportHeights[sportType][sportDifficulty] = int.from_bytes(tempAllData[chunkStart + 2:chunkStart + 4], "little")
        bearsCourseHorizontalSpawns[sportType][sportDifficulty] = tempAllData[BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty]
        bearsCourseCameras[sportType][sportDifficulty] = tempAllData[BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty + 3]
        length = sportHeights[sportType][sportDifficulty] * 0x10
        data = tempAllData[levelOffset:levelOffset + length]
        liszt = []
        for byte in data:
            liszt.append(byte)
        allLevelTileCSVs[sportType][sportDifficulty] = liszt
        liszt += ([0xFF] * ((MAX_SPORT_HEIGHTS[sportType][sportDifficulty] * 0x10) - len(liszt)))

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


def stamp(X, Y, stamp):
    global sportType
    global sportDifficulty
    global allLevelTileCSVs
    global sportHeights
    height = min(sportHeights[sportType][sportDifficulty] - Y, len(stamp))
    length = min(16 - X, len(stamp[0]))
    for i in range(height):
        for j in range(length):
            allLevelTileCSVs[sportType][sportDifficulty][X + j + (Y + i) * 16] = stamp[i][j]
    return


##tile editor funcs
# loading in subtiles as images, for subtile mode
def loadSubtileData(sport):
    global frameCount
    global spriteHeight
    global spriteWidth
    global quadrantPixel
    frameCount = 256
    spriteHeight = [2]
    spriteWidth = [2]
    quadrantPixel = 15
    global hexCodes
    global subtileGraphics
    global spritePalettes
    global bigtileCollisions
    global spriteSubtiles
    global layerChosen
    global loadedSpriteType
    global loadedSportType
    global eyeMode
    layerChosen = 0
    # bigtileGraphicsOffsets = COLLISION_OFFSETS plys 0x40A
    # bigtilePaletteOffsets = COLLISION_OFFSETS plus 0x80A
    # subtileColoursOffsets = above two added, plus 0xA
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (leave blank to abort): ")
        while name.upper() == "E":
            if input("are you sure? (E again if yes): ").upper() == "E":
                hexCodes = [[0, 0, 0]] * 0x20
                spritePalettes = [[0] * 0x400]
                subtileGraphics = [["00000000"] * (SUBTILE_GRAPHICS_LENGTHS[sport]//2)]
                return
            name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as file:
                loadedSpriteType = 22
                eyeMode = False
                EYE_BUTTON = button.Button(856, 395, EYE_IMAGES[0], 1)
                byteLand = file.read()
                # check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} palette? (if no, don't enter anything): ")
                # if check != "":
                extraOffsets = [[0x4A98, 0, 0, 0x4AA5], [0x8AB0, 0, 0, 0x8ABD], [0, 0, 0xCA3C, 0xCA45],
                                [0, 0, 0x10A75, 0x10A7E], [0, 0, 0x14B62, 0x14B6B], [0, 0, 0x18B7B, 0x18B84]]
                hexCodes = []
                paletteOffset = SUBTILE_GRAPHICS_OFFSETS[sport] + SUBTILE_GRAPHICS_LENGTHS[sport] + 0xA
                paletteData = b''
                for i in range(4):
                    if extraOffsets[sport][i] == 0:
                        paletteData += byteLand[paletteOffset + (i * 2):paletteOffset + (i * 2) + 2]
                    else:
                        paletteData += byteLand[(extraOffsets[sport][i]):(extraOffsets[sport][i]) + 2]
                paletteData += byteLand[paletteOffset + 0x08:paletteOffset + 0x40]  # 0x40 bytes in a 7 colour palette
                for i in range(0, 0x40, 2):
                    hexCodes.append([int((paletteData[i] & 0x1F) << 3), int(((paletteData[i] >> 5) + ((paletteData[i + 1] & 0x3) << 3)) << 3), int(((
                                                                                                                         paletteData[
                                                                                                                             i + 1] & 0x7C) >> 2) << 3)])  # GGGRRRRR XBBBBBGG into hex (R, G, B). normal conversion to a val btwn 0 and 1f, then left shift three times cuz hex takes 0 to 255 (so we approx)
                    # possibly bad to do this in a global way but whatevs
                    # hmmmmm the colour conversion doesn't work perfectly, maybe there's something im missing, but it works well enough

                # check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} subtile graphics? (if no, don't enter anything): ")
                # if check != "":
                subtileGraphics = []
                subtileyOffset = SUBTILE_GRAPHICS_OFFSETS[sportType]
                lengthe = SUBTILE_GRAPHICS_LENGTHS[sportType]
                subtileData = byteLand[subtileyOffset:subtileyOffset + lengthe]
                for i in range(0, lengthe, 2):
                    subtileGraphics.append(str(int(bin(subtileData[i])[2:]) + int(bin(subtileData[i + 1])[2:]) * 2).zfill(8))
                    # either mult i by 2 or i+1 by 2 (with binary as integers)
                subtileGraphics = [subtileGraphics]  # others have layers, and i don't want 1000000 branches so w/e makin this a list in a list

                # check = input(f"Do you want to import this game's {CONST_SPORTS[sportType]} bigtile subtile graphic configurations and collisions? (if no, don't enter anything): ")
                # if check != "":
                bigtileCollisions = [numby for numby in byteLand[BIGTILE_COLLISION_OFFSETS[sport]: BIGTILE_COLLISION_OFFSETS[sport] + frameCount*4]]
                spriteSubtiles = [[numby for numby in byteLand[BIGTILE_COLLISION_OFFSETS[sport] + 0x40A:BIGTILE_COLLISION_OFFSETS[sport] + 0x40A + frameCount*4]]]
                spritePalettes = [[numby for numby in byteLand[BIGTILE_COLLISION_OFFSETS[sport] + 0x80A:BIGTILE_COLLISION_OFFSETS[sport] + 0x80A + frameCount*4]]]
            print("Loaded.")
            loadedSportType = sport
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return


# other things have different sizes and a cool lil 7 byte header (GRAPHICINTRO in the spreadsheet)
def loadSubtileDataWithHeader():
    global frameCount
    global spriteHeight
    global spriteWidth
    global spriteSubtiles
    global spritePalettes
    global subtileGraphics
    global hexCodes
    global groupNum
    global loadedSpriteType
    global loadedSportType
    global loadedBearType
    global layers
    global layerChosen
    global quadrantPixel
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as file:
                loadedSpriteType = spriteType
                loadedSportType = sportType
                loadedBearType = bearType
                spriteSubtiles = []
                spritePalettes = []
                subtileGraphics = []
                layerChosen = 0
                spriteWidth = []
                spriteHeight = []
                quadrantPixel = 15
                byteLand = file.read()

                if spriteType < 17:
                    if sportType == 0 or sportType == 2:
                        offsets = FAMILYBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paloff = FAMILY_OBJ_PALETTE_OFFSETS[sportType]
                    elif bearType == 0:
                        offsets = BROBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paloff = BRO_OBJ_PALETTE_OFFSETS[sportType]
                    else:
                        offsets = SISBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paloff = SIS_OBJ_PALETTE_OFFSETS[sportType]
                else:
                    offsets = MORE_SPRITEISH_OFFSETS[spriteType-17]
                    if spriteType < 19:
                        if sportType in (0, 2):
                            paloff = FAMILY_OBJ_PALETTE_OFFSETS[sportType]
                        elif bearType == 0:
                            paloff = BRO_OBJ_PALETTE_OFFSETS[sportType]
                        else:
                            paloff = SIS_OBJ_PALETTE_OFFSETS[sportType]
                    else:
                        paloff = MORE_PALETTEY_OFFSETS[spriteType-17]
                if type(offsets) is not int:
                    if type(offsets[0]) is list:
                        groupNum = input(f"Which group of sprites do you want to edit (from 1 to {len(offsets)}?): ")
                        while not groupNum.isnumeric() or int(groupNum) < 1 or int(groupNum) > (len(offsets)):
                            print("Invalid input.")
                            groupNum = input(f"Which group of sprites do you want to edit (from 1 to {len(offsets)}?): ")
                        groupNum = int(groupNum) - 1
                        offsets = offsets[groupNum]
                    layers = len(offsets)
                else:
                    layers = 1

                if type(offsets) is not tuple and type(offsets) is not list:
                    offsets = [offsets]
                for i, offset in enumerate(offsets):
                    graphicIntro = byteLand[offset:offset + 7]
                    frameCount = graphicIntro[0]
                    spriteWidth.append(graphicIntro[1])  # unfortunately these have to be lists because sometimes layers ahve different W and L, e.g. toboggan jump's shadow is 4x4
                    spriteHeight.append(graphicIntro[2])
                    paletteDataOffset = int.from_bytes(graphicIntro[3:5], "little") + offset
                    subtileGraphicDataOffset = int.from_bytes(graphicIntro[5:7], "little") + offset #todo standardize some of these variable names, and also maybe stop rewriting the same code so many times over? it works but i feel like it's bad practice and idk
                    spriteSubtiles.append([inty for inty in byteLand[offset + 7:paletteDataOffset]])
                    spritePalettes.append([0] + [inty for inty in byteLand[paletteDataOffset:subtileGraphicDataOffset]])  # ughh the colours are connected to subtiles now, i wish these two graphic types weren't so different lol. anyways the [0] is for the elusive 0 subtile, which isn't in memory because it's always fully transparent
                    tempLengthThing = (subtileGraphicDataOffset - paletteDataOffset) * 0x10
                    subtileGraphicData = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + byteLand[subtileGraphicDataOffset:subtileGraphicDataOffset + tempLengthThing]
                    tempSubtileGraphics = []
                    for i in range(0, tempLengthThing + 0x10, 2):
                        tempSubtileGraphics.append(str(int(bin(subtileGraphicData[i])[2:]) + int(bin(subtileGraphicData[i + 1])[2:]) * 2).zfill(8))
                        # either mult i by 2 or i+1 by 2 (with binary as integers)
                    subtileGraphics.append(tempSubtileGraphics)
                    paletteData = byteLand[paloff:paloff + 0x40]
                    hexCodes = []
                    for i in range(0, 0x40, 2):
                        hexCodes.append([int((paletteData[i] & 0x1F) << 3), int(((paletteData[i] >> 5) + ((paletteData[i + 1] & 0x3) << 3)) << 3), int(((paletteData[i + 1] & 0x7C) >> 2) << 3)])
        except FileNotFoundError:
            print("File not found.")

#and others still have a 10 byte LONGGRAPHICINTRO
def loadSubtileDataWithLongHeader():
    global frameCount
    global layers
    global layerChosen
    global spriteHeight
    global spriteWidth
    global spriteSubtiles
    global spritePalettes
    global subtileGraphics
    global hexCodes
    global groupNum
    global loadedSpriteType
    global loadedSportType
    global loadedBearType
    global quadrantPixel
    global loadedMenuPagePalette
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as file:
                loadedSpriteType = spriteType
                loadedSportType = sportType
                loadedBearType = bearType
                spriteSubtiles = []
                spritePalettes = []
                subtileGraphics = []
                layerChosen = 0
                frameCount = 1
                spriteWidth = []
                spriteHeight = []
                quadrantPixel = 2
                layers = 1
                byteLand = file.read()
                offset = LONG_GRAPHICS_OFFSETS[spriteType - 23]
                paloff = LONG_PALETTE_OFFSETS[spriteType - 23]
                tempLengthThing = LONG_GRAPHICS_LENGTHS[spriteType - 23]
                if spriteType == 26:
                    temp26 = input("Which screen's palette do you want to load (all 5 screens' graphics will still be loaded, but only your chosen palette will be loaded): ")
                    while not temp26.isnumeric() or int(temp26) > 5 or int(temp26) < 1:
                        print("Invalid input.")
                        temp26 = input("Which screen's palette do you want to load (all 5 screens' graphics will still be loaded, but only your chosen palette will be loaded): ")
                    loadedMenuPagePalette = int(temp26)
                    paloff = paloff[int(temp26)-1]
                elif spriteType == 29: #course intros
                    if sportType == 0:
                        indexThingFor29 = 8
                    elif sportType == 2:
                        indexThingFor29 = 9
                    else:
                        indexThingFor29 = bearType*4
                        if sportType == 3:
                            indexThingFor29 += 1
                        elif sportType == 4:
                            indexThingFor29 += 2
                        elif sportType == 5:
                            indexThingFor29 += 3
                    offset = offset[indexThingFor29]
                    paloff = paloff[indexThingFor29]
                    tempLengthThing = tempLengthThing[indexThingFor29]
                elif spriteType == 30:
                    print(paloff)
                    if sportType in (0, 1): #snowy scoreboard
                        paloff = paloff[1]
                    else:
                        paloff = paloff[0]
                    print(paloff)
                elif spriteType == 31:
                    if sportType in (0, 2):
                        offset = offset[2]
                        paloff = paloff[2]
                        tempLengthThing = tempLengthThing[2]
                    else:
                        offset = offset[bearType]
                        paloff = paloff[bearType]
                        tempLengthThing = tempLengthThing[bearType]



                """if type(offset) is not int:
                    if type(offset[0]) is list:
                        groupNum = input(f"Which group of sprites do you want to edit (from 1 to {len(offsets)}?): ")
                        while not groupNum.isnumeric() or int(groupNum) < 1 or int(groupNum) > (len(offsets)):
                            print("Invalid input.")
                            groupNum = input(f"Which group of sprites do you want to edit (from 1 to {len(offsets)}?): ")
                        groupNum = int(groupNum) - 1
                        offset = offset[groupNum]
                    layers = len(offset)
                else:"""
                layers = 1

                graphicIntro = byteLand[offset:offset + 10]
                spriteWidth.append(graphicIntro[0])  # unfortunately these have to be lists because sometimes layers ahve different W and L, e.g. toboggan jump's shadow is 4x4
                spriteHeight.append(graphicIntro[1])
                chunkAdderThingy = (offset//0x4000)*0x4000
                paletteLocationOffset = int.from_bytes(graphicIntro[2:4], "little")%0x4000 + chunkAdderThingy
                #graphicLocationOffset = int.from_bytes(graphicIntro[4:6], "little")^0x4000 + chunkAdderThingy is just offset + 10
                graphicMakerOffset = int.from_bytes(graphicIntro[6:8], "little")%0x4000 + chunkAdderThingy
                paletteMakerOffset = int.from_bytes(graphicIntro[8:10], "little")%0x4000 + chunkAdderThingy

                spriteSubtiles.append([inty for inty in byteLand[offset + 10:paletteLocationOffset]])
                spritePalettes.append([inty for inty in byteLand[paletteLocationOffset:paletteMakerOffset]])

                paletteData = byteLand[paloff:paloff+0x40]
                hexCodes = []
                for i in range(0, 0x40, 2):
                    hexCodes.append([int((paletteData[i] & 0x1F) << 3), int(((paletteData[i] >> 5) + ((paletteData[i + 1] & 0x3) << 3)) << 3), int(((paletteData[i + 1] & 0x7C) >> 2) << 3)])

                subtileGraphicData = byteLand[graphicMakerOffset:graphicMakerOffset+tempLengthThing]
                tempSubtileGraphics = []
                for i in range(0, tempLengthThing, 2):
                    tempSubtileGraphics.append(str(int(bin(subtileGraphicData[i])[2:]) + int(bin(subtileGraphicData[i + 1])[2:]) * 2).zfill(8))
                    # either mult i by 2 or i+1 by 2 (with binary as integers)
                subtileGraphics.append(tempSubtileGraphics)

        except FileNotFoundError:
            print("File not found.")



# saves tile editor data to a game
def saveThine22Data(sport):
    global hexCodes
    global subtileGraphics
    global spritePalettes
    global bigtileCollisions
    global spriteSubtiles
    bigtileCollisionOffsets = [0x4D6C, 0x8DCD, 0xCCE1, 0x10DAA, 0x14EF1, 0x19031]
    # bigtileGraphicsOffsets = above plus 0x40A
    # bigtilePaletteOffsets = above plus 0x80A
    subtileGraphicsOffsets = [0x5976, 0x99D7, 0xD8EB, 0x119B4, 0x15AFB, 0x19C3B]
    subtileGraphicsLengths = [0x1EA0, 0x1DC0, 0x1FA0, 0x1FD0, 0x1F70, 0x1900]
    # subtileColoursOffsets = above two added, plus 0xA
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as file:
                # check = input("Do you want to save your palette to the file? (if no, don't enter anything): ")
                # if check != "":
                extraOffsets = [[0x4A98, 0, 0, 0x4AA5], [0x8AB0, 0, 0, 0x8ABD], [0, 0, 0xCA3C, 0xCA45], [0, 0, 0x10A75, 0x10A7E], [0, 0, 0x14B62, 0x14B6B], [0, 0, 0x18B7B, 0x18B84]]
                paletteOffset = subtileGraphicsOffsets[sport] + subtileGraphicsLengths[sport] + 0xA
                for i in range(4):
                    RGB = hexCodes[i]
                    G = bin(RGB[1] >> 3)[2:].zfill(5)
                    temp = G[2:].zfill(3) + bin(RGB[0] >> 3)[2:].zfill(5) + "0" + bin(RGB[2] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                    bitey = int(temp, 2).to_bytes(2, "big")
                    if extraOffsets[sport][i] == 0:
                        file.seek(paletteOffset + i * 2, 0)
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
                # check = input("Do you want to save your subtile graphics to the file? (if no, don't enter anything): ")
                # if check != "":
                subtileyOffset = subtileGraphicsOffsets[sport]
                file.seek(subtileyOffset)
                for i in range(subtileGraphicsLengths[sport] // 2):
                    quaternary = subtileGraphics[0][i]
                    left = ""
                    right = ""
                    # prolly a bad way of doing this but can't think of a better one rn
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

                # check = input("Do you want to save your bigtile subtile graphic configurations and collisions to the file? (if no, don't enter anything): ")
                # if check != "":
                file.seek(bigtileCollisionOffsets[sport], 0)
                for bytten in bigtileCollisions:
                    file.write(bytten.to_bytes())
                file.seek(bigtileCollisionOffsets[sport] + 0x40A, 0)
                for bytten in spriteSubtiles[0]:
                    file.write(bytten.to_bytes())
                file.seek(bigtileCollisionOffsets[sport] + 0x80A, 0)
                for bytten in spritePalettes[0]:
                    file.write(bytten.to_bytes())
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return

def saveThineSub22Data():
    global hexCodes
    global spriteSubtiles
    global spritePalettes
    global subtileGraphics
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as file:
                if spriteType < 17:
                    if loadedSportType == 0 or loadedSportType == 2:
                        graphicIntroOffsets = FAMILYBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = FAMILY_OBJ_PALETTE_OFFSETS[loadedSportType]
                    elif loadedBearType == 0:
                        graphicIntroOffsets = BROBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = BRO_OBJ_PALETTE_OFFSETS[loadedSportType]
                    else:
                        graphicIntroOffsets = SISBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = SIS_OBJ_PALETTE_OFFSETS[loadedSportType]
                else:
                    graphicIntroOffsets = MORE_SPRITEISH_OFFSETS[spriteType - 17]
                    if spriteType < 19:
                        paletteOffset = BRO_OBJ_PALETTE_OFFSETS[sportType]
                    else:
                        paletteOffset = MORE_PALETTEY_OFFSETS[spriteType - 17]

                if type(graphicIntroOffsets) is not int:
                    if type(graphicIntroOffsets[0]) is list:
                        graphicIntroOffsets = graphicIntroOffsets[groupNum]

                if type(graphicIntroOffsets) is int:
                    graphicIntroOffsets = [graphicIntroOffsets]

                file.seek(paletteOffset)
                for i in range(0x20):
                    RGB = hexCodes[i]
                    G = bin(RGB[1] >> 3)[2:].zfill(5)
                    temp = G[2:].zfill(3) + bin(RGB[0] >> 3)[2:].zfill(5) + "0" + bin(RGB[2] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                    bitey = int(temp, 2).to_bytes(2, "big")
                    file.write(bitey)
                # check = input("Do you want to save your subtile graphics to the file? (if no, don't enter anything): ")
                # if check != "":
                for layerrr in range(len(graphicIntroOffsets)):
                    file.seek(graphicIntroOffsets[layerrr] + 7)
                    for bytten in spriteSubtiles[layerrr]:
                        file.write(bytten.to_bytes())
                    for bytten in spritePalettes[layerrr][1:]:  # skippa that 0 subtile
                        file.write(bytten.to_bytes())
                    for j in range(8, len(subtileGraphics[layerrr])):  # skippin 0 subtubsubt
                        quaternary = subtileGraphics[layerrr][j]
                        left = ""
                        right = ""
                        # prolly a bad way of doing this but can't think of a better one rn
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
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return

def saveThineSup22Data():
    global hexCodes
    global spriteSubtiles
    global spritePalettes
    global subtileGraphics
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as file:
                graphicIntroOffsets = LONG_GRAPHICS_OFFSETS[loadedSpriteType-23]
                paletteOffset = LONG_PALETTE_OFFSETS[loadedSpriteType-23]
                if spriteType == 26:
                    print(f"(saving page {loadedMenuPagePalette}'s palette)")
                    paletteOffset = paletteOffset[int(loadedMenuPagePalette-1)] #12345 to 01234
                elif spriteType == 29: #course intros
                    if sportType == 0:
                        indexThingFor29 = 8
                    elif sportType == 2:
                        indexThingFor29 = 9
                    else:
                        indexThingFor29 = bearType*4
                        if sportType == 3:
                            indexThingFor29 += 1
                        elif sportType == 4:
                            indexThingFor29 += 2
                        elif sportType == 5:
                            indexThingFor29 += 3
                    graphicIntroOffsets = graphicIntroOffsets[indexThingFor29]
                    paletteOffset = paletteOffset[indexThingFor29]
                elif spriteType == 30:
                    if sportType in (0, 1): #snowy scoreboard
                        paletteOffset = paletteOffset[1]
                    else:
                        paletteOffset = paletteOffset[0]
                elif spriteType == 31:
                    if sportType in (0, 2):
                        graphicIntroOffsets = graphicIntroOffsets[2]
                        paletteOffset = paletteOffset[2]
                    else:
                        graphicIntroOffsets = graphicIntroOffsets[bearType]
                        paletteOffset = paletteOffset[bearType]


                file.seek(paletteOffset)
                for i in range(0x20):
                    RGB = hexCodes[i]
                    G = bin(RGB[1] >> 3)[2:].zfill(5)
                    temp = G[2:].zfill(3) + bin(RGB[0] >> 3)[2:].zfill(5) + "0" + bin(RGB[2] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                    bitey = int(temp, 2).to_bytes(2, "big")
                    file.write(bitey)
                # check = input("Do you want to save your subtile graphics to the file? (if no, don't enter anything): ")
                # if check != "":
                file.seek(graphicIntroOffsets + 10)
                for bytten in spriteSubtiles[0]:
                    file.write(bytten.to_bytes())
                for bytten in spritePalettes[0]:
                    file.write(bytten.to_bytes())
                file.seek(0x40, 1)
                for j in range(len(subtileGraphics[0])):
                    quaternary = subtileGraphics[0][j]
                    left = ""
                    right = ""
                    # prolly a bad way of doing this but can't think of a better one rn
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
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
    print("No changes have been made.")
    return

def bmpPrintrer22up(bigtile, layaer, equalTo22):
    guaug = []
    for j in (range(spriteHeight[layaer])[::-1]):  # first j will add the bottom subtiles to guaug, second j will add the top ones
        if equalTo22:
            ox400er = (bigtile % 0x10) * 2 + (bigtile // 0x10) * 0x40 + (j) * 0x20  # weirdo address calculator because it's stored all messily
        else:
            ox400er = bigtile * (spriteWidth[0]*spriteHeight[0]) + j * (spriteWidth[0])
        P = spritePalettes[0][ox400er:ox400er + spriteWidth[0]]  # palette data at address and address + 1
        palettes = [pal & 7 for pal in P]  # and 7 to get the palette number (stored in bits 0 1 and 2)
        palettecode = []
        graphicsies = []
        for subtileHzNum in range(spriteWidth[layaer]):
            for l in range(4):  # converting hex code palette data into bitmap file palette data
                RGB = hexCodes[palettes[subtileHzNum] * 4 + l]
                G = bin(RGB[1] >> 3)[2:].zfill(5)  # next is a lil different as BMP uses GGGBBBBB XRRRRRGG
                temp = G[2:].zfill(3) + bin(RGB[2] >> 3)[2:].zfill(5) + "0" + bin(RGB[0] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                bitey = int(temp, 2).to_bytes(2, "big")
                palettecode.append(bitey)

            subtile = spriteSubtiles[0][ox400er + subtileHzNum] + (P[subtileHzNum] & 0x8) * 0x20  # add 0x100, the 02 is just b/c multed with 0x8 cuz less lines, so felt like it
            graphicsies.append(subtileGraphics[layaer][subtile * 8:subtile * 8 + 8][::-1])  # stores quaternary row graphics, so need to get the 8 starting at s*8
        for subtileHzNum in range(spriteWidth[layaer]):
            if spritePalettes[0][ox400er + subtileHzNum] & 0x40:  # vt flip
                graphicsies[subtileHzNum] = graphicsies[subtileHzNum][::-1]
            if spritePalettes[0][ox400er + subtileHzNum] & 0x20:  # hz flip
                for l in range(8):
                    graphicsies[subtileHzNum][l] = graphicsies[subtileHzNum][l][::-1]
        for byteNum in range(8):
            for subtileHzNum in range(spriteWidth[layaer]):
                for bit in graphicsies[subtileHzNum][byteNum]:  # graphicsies[0] has 8 bytes in its list (contains the left subtile's data.) ([1] has 8 bytes for the right subtile)
                    guaug.append(palettecode[int(bit) + 4 * subtileHzNum])  # would += to a b'' but that takes super long
    with open(f"tiles/temptiles/tile{str(bigtile).zfill(3)}.bmp", "wb") as bmp:
        bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (8 * spriteWidth[layaer]).to_bytes(4, "little") + (8 * spriteHeight[layaer]).to_bytes(4,"little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(guaug))
    ######
    ###### now collisions
    if equalTo22:
        gorg = b''
        for j in (range(spriteHeight[layaer])[::-1]):  # first j will add the bottom subtiles to guaug, second j will add the top ones (no idea why it needs to be 0 1, it just doesn't work as 1, 0 though my logic sayc it should wasawawawa)
            ox400er = bigtile * 4 + j * 2  # normal this time, since this only works for 22
            C = bigtileCollisions[ox400er:ox400er + spriteWidth[layaer]]
            wwwwww = b''
            for k in range(spriteWidth[layaer]):
                for l, key in enumerate(COLLISION_COLOUR_MAPPER):
                    if key == C[k]:
                        RGB = colours[l]
                        break
                G = bin(RGB[1] >> 3)[2:].zfill(5)  # next is a lil different as BMP uses GGGBBBBB XRRRRRGG
                temp = G[2:].zfill(3) + bin(RGB[2] >> 3)[2:].zfill(5) + "0" + bin(RGB[0] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                wwwwww += (int(temp, 2).to_bytes(2, "big") * 8)
            gorg += (wwwwww) * 8
        with open(f"tiles/efftemptiles/tile{str(i).zfill(3)}.bmp", "wb") as bmp:
            bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (8 * spriteWidth[layaer]).to_bytes(4, "little") + (8 * spriteHeight[layaer]).to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + gorg)

def bmpPrintrerSprite(frame, numberOLayers):
    guaug = []
    maxWidth = max(spriteWidth)
    dummyColour = b'\xFA\x69'
    for j in (range(spriteHeight[0])[::-1]):  # first j will add the bottom subtiles to guaug, second j will add the top ones
        palettecode = []
        graphicsies = []
        palettes = []
        for layaer in range(numberOLayers):
            ox400er = frame * spriteWidth[layaer] * spriteHeight[layaer] + j * spriteWidth[layaer]
            palettes.append([spritePalettes[layaer][subtileNumbah] for subtileNumbah in spriteSubtiles[layaer][ox400er:ox400er + spriteWidth[layaer]]])  # not using P since these tend not to use the extra bits in palette stuff
            tempGraphicsies = []
            tempPalettecode = []
            for k in range(spriteWidth[layaer]):
                for l in range(4):  # converting hex code palette data into bitmap file palette data
                    #try:
                    RGB = hexCodes[palettes[layaer][k] * 4 + l]
                    #except Exception:
                    #    print("aweawawr")
                    G = bin(RGB[1] >> 3)[2:].zfill(5)  # next is a lil different as BMP uses GGGBBBBB XRRRRRGG
                    temp = G[2:].zfill(3) + bin(RGB[2] >> 3)[2:].zfill(5) + "0" + bin(RGB[0] >> 3)[2:].zfill(5) + G[0:2].zfill(2)
                    bitey = int(temp, 2).to_bytes(2, "big")
                    tempPalettecode.append(bitey)

                subtile = spriteSubtiles[layaer][ox400er + k]
                tempGraphicsies.append(subtileGraphics[layaer][subtile * 8:subtile * 8 + 8][::-1])  # stores quaternary row graphics, so need to get the 8 starting at s*8
            thingeymabobbert = [dummyColour] * (8 * maxWidth * 8)
            palettecode.append(tempPalettecode)
            graphicsies.append(tempGraphicsies)

        for subtileVt in range(8):
            for subtileHrz in range(maxWidth):
                for bitNum in range(8):
                    for layaer in range(numberOLayers):
                        bitt = graphicsies[layaer][subtileHrz][subtileVt][bitNum]
                        if bitt != "0" and thingeymabobbert[subtileVt * (maxWidth * 8) + subtileHrz * 8 + bitNum] == dummyColour:
                            #try:
                            thingeymabobbert[subtileVt * (maxWidth * 8) + subtileHrz * 8 + bitNum] = palettecode[layaer][int(bitt) + 4 * subtileHrz]
                            #except Exception:
                            #    print("waeoaw")
                            break  # can break because after placing a colour, no lower layer can overwrite it, so saves a lil time
                # for bit in graphicsies[l][k]:  # graphicsies[0] has 8 bytes in its list (contains the left subtile's data.) ([1] has 8 bytes for the right subtile)

        guaug += thingeymabobbert  # would += to a b'' but that takes super long
    with open(f"tiles/temptiles/tile{str(frame).zfill(3)}.bmp", "wb") as bmp:
        bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (8 * spriteWidth[layaer]).to_bytes(4, "little") + (8 * spriteHeight[layaer]).to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(guaug))


# makes printed tiles from bmp into png
def pngify(name):
    if not os.path.exists(f"tiles/{name}"):
        os.makedirs(f"tiles/{name}")
    count = 0
    for bitmap in glob.glob(f"tiles/temptiles/*.bmp"):
        Image.open(bitmap).save(f"tiles/{name}/tile{count}.png")
        count += 1
        if count >= frameCount:
            break

    if loadedSpriteType == 22:
        if not os.path.exists(f"tiles/{name}_effects"):
            os.makedirs(f"tiles/{name}_effects")
        count = 0
        for bitmap in glob.glob(f"tiles/efftemptiles/*.bmp"):
            Image.open(bitmap).save(f"tiles/{name}_effects/tile{count}.png")
            count += 1
            if count >= frameCount:
                break


# draws all the tiny top right subtiles in tile mode
def tinySubtileDraw(subGraphics, hexCodes, palSelected, scroll):
    for k in range(512//NUM_OF_SMALLTILES_DISPLAYED_HZ):  # max 512 tiles, so 32 high
        for l in range(NUM_OF_SMALLTILES_DISPLAYED_HZ):  # 16 wide usually
            for i in range(8):  # and subtiles are 8x8px, handled by i and j

                Y = (50 + (i * SMALLTILE_PIXEL) + (k * SMALLTILE_PIXEL * 8)) + scroll
                if Y < 50:
                    break
                elif Y >= 370:
                    return

                for j in range(8):

                    X = (750 + (j * SMALLTILE_PIXEL) + (l * SMALLTILE_PIXEL * 8))
                    rectangle = pygame.Rect = (X, Y, SMALLTILE_PIXEL, SMALLTILE_PIXEL)
                    try:
                        colourSelected = int(subGraphics[((k * NUM_OF_SMALLTILES_DISPLAYED_HZ) + l) * 8 + i][j])
                    except Exception:  # outta tiles to draw
                        return
                    if loadedSpriteType >= 22: #course selections or longs
                        pygame.draw.rect(SCREEN, hexCodes[colourSelected + palSelected * 4], rectangle)  # gotta use paletteSelected for this because subtiles aren't connected to one palette, rather a palette is assigned upon bigtile construction
                    else:
                        palselels = spritePalettes[layerChosen][(l) + (k * NUM_OF_SMALLTILES_DISPLAYED_HZ)]
                        pygame.draw.rect(SCREEN, hexCodes[colourSelected + palselels * 4], rectangle)  # nevermind lol the non-connectedness doesn't apply for bear sprites and stuff because aaaarhghhsrh


def subtilesOnBigtile(layaaaa):
    for i in range(spriteHeight[layaaaa]):
        for j in range(spriteWidth[layaaaa]):
            hz_range = range(8)
            vt_range = range(8)
            if loadedSpriteType == 22:
                ox400LengthStartIndex = bigtileSelected * 2 + j + (i * 0x20) + (bigtileSelected // 16) * 0x20
                bankSwitch = (spritePalettes[0][ox400LengthStartIndex] & 0x8) * 0x100
                palalala = (spritePalettes[0][ox400LengthStartIndex])
            elif loadedSpriteType < 22:
                ox400LengthStartIndex = bigtileSelected * (spriteWidth[layaaaa] * spriteHeight[layaaaa]) + i * spriteWidth[layaaaa] + j
                bankSwitch = 0
                palalala = (spritePalettes[layaaaa][spriteSubtiles[layaaaa][ox400LengthStartIndex]])  # for these, colours are connected to subtiles, guh ...
            else:
                ox400LengthStartIndex = i * spriteWidth[layaaaa] + j
                bankSwitch = (spritePalettes[0][ox400LengthStartIndex] & 0x8) * 0x100
                palalala = (spritePalettes[0][ox400LengthStartIndex])

            if palalala & 0x20 == 0x20:
                hz_range = hz_range[::-1]
            if palalala & 0x40 == 0x40:  # vt flip
                vt_range = vt_range[::-1]
            for k, K in enumerate(vt_range):
                for l, L in enumerate(hz_range):
                    rectangle = pygame.Rect = ((l * quadrantPixel + j * quadrantPixel * 8), (k * quadrantPixel + i * quadrantPixel * 8 + 50), quadrantPixel, quadrantPixel)
                    # try:
                    theSubtileInQuestion = spriteSubtiles[layaaaa][ox400LengthStartIndex]
                    #try:
                    zeroOneTwoThreeColour = int(subtileGraphics[layaaaa][theSubtileInQuestion * 8 + K + bankSwitch][L])
                    #except Exception:
                    #    print("warawr")
                    #    break
                    if eyeMode and zeroOneTwoThreeColour == 0:
                        continue
                    pygame.draw.rect(SCREEN, hexCodes[(palalala & 7) * 4 + zeroOneTwoThreeColour], rectangle)  # what a Mess. palette*4 to get to the right palette, + 0 1 2 or 3 (found as 8-long strings in subtileGraphics. the right index is at the subtile number (in bigtilesubtiles at the ox400 index, which is an antequated name from when this only did bigtiles for levels) (*8 because each subtile has 64 pixels, so 8 of the 8-longs.) ([L] because 8-long string so need an index of it, and +K because 8 8-longs, but these can be from 0 to 7 or 7 to 0 if flips are needed.) (the &* *0x100 thing is to change the subtile bank)
                    # except Exception:
                    #    continue


# todo probably use this method more often? everything is so janky and spaghettish
# kind of a general tile editor updater
def infoUpdater(stackReset):
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
    if loadedSpriteType == 22:
        ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
        P = spritePalettes[0][ox400IndexThingForHere]
        collisionSelected = COLLISION_COLOUR_MAPPER[bigtileCollisions[bigtileSelected * 4 + bigtileQuadrantSelected % 4]]
        subtileSelected = spriteSubtiles[0][ox400IndexThingForHere] + (P & 0x8) * 0x20
        paletteSelected = P & 7
        subtileyPalleteyThingies[0] = P & 0x80 != 0  # priority
        subtileyPalleteyThingies[1] = P & 0x40 != 0  # vt_flip
        subtileyPalleteyThingies[2] = P & 0x20 != 0  # hz_flip
    elif loadedSpriteType < 22:
        ox400IndexThingForHere = bigtileSelected * spriteWidth[layerChosen] * spriteHeight[layerChosen] + bigtileQuadrantSelected
        subtileSelected = spriteSubtiles[layerChosen][ox400IndexThingForHere]
        P = spritePalettes[layerChosen][subtileSelected]
        paletteSelected = P & 7
    else:
        ox400IndexThingForHere = bigtileQuadrantSelected
        P = spritePalettes[0][ox400IndexThingForHere]
        subtileSelected = spriteSubtiles[0][ox400IndexThingForHere] + (P & 0x8) * 0x20
        paletteSelected = P & 7
        subtileyPalleteyThingies[0] = P & 0x80 != 0  # priority
        subtileyPalleteyThingies[1] = P & 0x40 != 0  # vt_flip
        subtileyPalleteyThingies[2] = P & 0x20 != 0  # hz_flip
    currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
    # if P & 0x8 != 0:  # bank
    #    subtileSelected += 0x100
    if stackReset:
        undoStack = []
        redoStack = []
    return

def subtileStackUpdate(msg):
    global currentSubtileStackInfo
    global undoStack
    global redoStack
    if subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8] != currentSubtileStackInfo:
        undoStack.append([subtileSelected, currentSubtileStackInfo])
        print(undoStack, msg)
        if len(undoStack) > 150:
            undoStack = undoStack[50:]
        redoStack = []
    return


def spriteCheck(sport, sprite):
    if sport < 2:  # snowy bad ones
        if sprite in (10, 11, 13, 15, 16):
            sprite = 0
    elif sport < 4:  # watery bad ones
        if sprite in (7, 8, 10, 11, 12, 15, 16):
            sprite = 0
    elif sport == 4:  # bike bad ones
        if sprite in (12, 13, 15):
            sprite = 0
    else:  # db baddies
        if sprite in (12, 13):
            sprite = 0
    return sprite


# making the font
pygame.font.init()
thefont = pygame.font.SysFont("Times New Roman", 32)

# game loop
running = True
while running:

    # fps (and title)
    clock.tick()
    frameseys = clock.get_fps()
    pygame.display.set_caption(f"bears tile editor: {frameseys} fps")

    # bg colour (blue!)
    SCREEN.fill((36, 45, 104))

    # mouse pos tracker
    mousePos = pygame.mouse.get_pos()
    mouseX = (mousePos[0])
    mouseY = (mousePos[1])

    # mode changing buttons
    if COURSE_EDITOR_BUTTON.draw(SCREEN):
        programMode = programModes.courseEditor
        sportTypeButtonMover(programMode)
    if TILE_EDITOR_BUTTON.draw(SCREEN):
        programMode = programModes.subtileDrawer
        sportTypeButtonMover(programMode)
        spriteType = spriteCheck(sportType, spriteType)

    # info mode, stops other modes to make things a bit quicker
    if infoMode:
        pygame.event.get()
        if programMode == programModes.courseEditor:
            SCREEN.blit(INFO_IMAGES[0], (0, 0))
        elif loadedSpriteType == 22:
            SCREEN.blit(INFO_IMAGES[1], (0, 0))
        elif loadedSpriteType < 22:
            SCREEN.blit(INFO_IMAGES[2], (0, 0))
        else:
            SCREEN.blit(INFO_IMAGES[3], (0, 0))
        pygame.display.update()
        pygame.display.set_caption(f"bears tile editor: paused fps")
        while not INFO_BUTTON.draw(SCREEN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            if event.type == pygame.MOUSEBUTTONUP:
                infoWait = 0

        infoMode = not infoMode
        pygame.time.wait(200) #no waiter thing since it doesn't affect the fps counter here and tbh i think the wait is more efficient, just changed it in other places because it feels worse
        #seems to be fine without any deltatime chicanery, maybe that's baked into wait idk

    #
    # COURSE EDITOR MODE (for editing course layout)
    #
    elif programMode == programModes.courseEditor:

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

            # scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll += 256 * scrollSpeed
                elif event.y == -1:
                    scroll -= 256 * scrollSpeed

            if event.type == pygame.MOUSEBUTTONUP:
                infoWait, buttonWait = 0, 0

        # scolling (up/down, or W/D)
        if scrollUp:
            scroll += 32 * scrollSpeed
        if scrollDown:
            scroll -= 32 * scrollSpeed

        if scroll > 0:
            scroll = 0

        # limit on the scroll
        if scroll < -(sportHeights[sportType][sportDifficulty]) * (gridTileWidth) + 600:  # this is prob very inefficient, should change the value every time diff/grid is changed and store it somrwhere future me pleeeeease :)
            scroll = -(sportHeights[sportType][sportDifficulty]) * (gridTileWidth) + 600

        # draw sport buttons, sport button memory, & actions
        sportCount = 0
        for sportCount, typeButton in enumerate(sportTypeButtons):
            if typeButton.draw(SCREEN):
                sportType = sportCount

        # draw diff buttons, difficulty button memory, & actions
        difficultyCount = 0
        for difficultyCount, difficultyButton in enumerate(sportDifficultyButtons):
            if difficultyButton.draw(SCREEN):
                sportDifficulty = difficultyCount
                imageList[sportType] = tileImageStorer(SPORTS[sportType])

        # draw clickable tiles, clicky tile memory, also changes inventory
        tileCount = 0
        for tileCount, i in enumerate(clicky_tiles[sportType]):
            if i.draw(SCREEN):
                chosenTile = tileCount
                tileInvPictures[inventoryIndex] = tileCount

        # highlighting (sport, diff, tile)
        pygame.draw.rect(SCREEN, (255, 0, 0), sportTypeButtons[sportType], 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), sportDifficultyButtons[sportDifficulty], 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), clicky_tiles[sportType][chosenTile], 1)

        invRect = pygame.Rect = (582 + inventoryIndex * 18, 274, 18, 18)  # maybe also bad? idk, im goin ta sleep
        pygame.draw.rect(SCREEN, (255, 0, 0), invRect)

        # draws grid tile images to screen
        gridButtonMaker()

        # drawing the height line
        lineHeight = sportHeights[sportType][sportDifficulty] * 32 + scroll * 1 + 2
        if 0 < lineHeight < 720:
            pygame.draw.line(SCREEN, (255, 0, 0), (0, lineHeight), (511, lineHeight), 5)

        # and the spawn rectangle
        spawnRect = pygame.rect = (bearsCourseHorizontalSpawns[sportType][sportDifficulty] * 2 - 16, sportHeights[sportType][sportDifficulty] * 32 + scroll * 1 - 64, 32, 32)
        pygame.draw.rect(SCREEN, (255, 0, 0), spawnRect, 2)

        # camera test
        cameraX = bearsCourseCameras[sportType][sportDifficulty] * 2
        cameraRect = pygame.rect = (cameraX, lineHeight - 0x122, 0x140, 0x120)
        pygame.draw.rect(SCREEN, (255, 200, 200), cameraRect, 2)

        # effect vision toggle
        if EFFECTS_BUTTON.draw(SCREEN):
            if buttonWait == 0:
                if effectsOn:
                    effectsOn = False
                else:
                    effectsOn = True
                imageList[sportType] = tileImageStorer(SPORTS[sportType])
                buttonWait = (frameseys+1)//8
            else:
                buttonWait -= 1
            # grid vision toggle
        if GRID_BUTTON.draw(SCREEN):
            if buttonWait == 0:
                checkerenate = not checkerenate
                buttonWait = (frameseys+1)//6
            else:
                buttonWait -= 1
        if checkerenate:
            checkerer()

        # saving features (and draw save)
        if SAVE_BUTTON.draw(SCREEN):
            CSVList = allLevelTileCSVs[sportType][sportDifficulty][0:0x10 * sportHeights[sportType][sportDifficulty]]
            if lockFileName:
                filename = lockedFileName + CONST_SPORTS[sportType] + DIFFICULTIES[difficulty]
            else:
                filename = input("Name your file (leave blank to skip): ")  # CSV maker
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
                        writenator.writerow([sportHeights[sportType][sportDifficulty], bearsCourseHorizontalSpawns[sportType][sportDifficulty], bearsCourseCameras[sportType][sportDifficulty]])
                        for i in range(0, len(CSVList), 16):
                            writenator.writerow(CSVList[i:i + 16])
                        print("File saved.")

            if lockFileName:
                bearsname = lockedFileName
            else:
                bearsname = input("enter the name of the bears file (in levels/modified_levels/) to which the data should be saved here (.gbc file format assumed, so don't type it)? (leave blank to skip): ")  # GBC editor
            if bearsname != "":
                try:
                    with open(f"levels/modified_levels/{bearsname}.gbc", "r+b") as file:
                        file.seek(BEARS_LEVEL_DATA_OFFSET_RANGES[sportType][sportDifficulty])
                        CSVByteArray = b''
                        for num in CSVList:
                            CSVByteArray += num.to_bytes(1, "little")
                        file.write(CSVByteArray)
                        # new height
                        file.seek((0xA + sportType * 3 + sportDifficulty) * 0x4000 + 2)
                        height = min(sportHeights[sportType][sportDifficulty], MAX_SPORT_HEIGHTS[sportType][sportDifficulty])
                        file.write(height.to_bytes(2, "little", signed=False))
                        # new spawn
                        file.seek(BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty)
                        file.write(bearsCourseHorizontalSpawns[sportType][sportDifficulty].to_bytes())
                        # new cam
                        file.seek(BEARS_COURSE_HEIGHT_OFFSETS[sportType] + sportDifficulty + 3)
                        file.write(bearsCourseCameras[sportType][sportDifficulty].to_bytes())
                        file.close()
                        print("Data saved.")
                except FileNotFoundError:
                    print("GBC file not found. No edits have been made.")

        # loading features
        if LOAD_BUTTON.draw(SCREEN):
            if lockFileName:
                filename = lockedFileName + CONST_SPORTS[sportType] + DIFFICULTIES[difficulty]
            else:
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
                        liszt = [int(byte) for byte in tempArrrgh[16:-1]]  # the -1 takes off the last \n of a csv file, and the 16 is to remove the empty header junk
                        courseSize = len(liszt)
                        if courseSize < sportHeights[sportType][sportDifficulty] * 0x10:
                            liszt += ([0xFF] * ((MAX_SPORT_HEIGHTS[sportType][sportDifficulty] * 0x10) - courseSize))  # if the height isn't the max, this fills the rest with sawdust (0xFF tiles cuz why not)
                        allLevelTileCSVs[sportType][sportDifficulty] = liszt
                        sportHeights[sportType][sportDifficulty] = int(header[0])
                        if MAX_SPORT_HEIGHTS[sportType][sportDifficulty] < int(header[0]):  # heights can't go past the orig cap yet sadly
                            print("the level height stored in this CSV is too long for this level and has been automatically shortened.")
                            sportHeights[sportType][sportDifficulty] = MAX_SPORT_HEIGHTS[sportType][sportDifficulty]
                        bearsCourseHorizontalSpawns[sportType][sportDifficulty] = int(header[1])
                        bearsCourseCameras[sportType][sportDifficulty] = int(header[2])
                        file.close()
                    except ValueError:
                        print("bad sport or diff :(")
                    except IndexError:
                        print("sport/diff num out of bounds :(")
                else:
                    print("File not found.")

        if LOAD_FROM_GAME_BUTTON.draw(SCREEN):
            if lockFileName:
                name = lockedFileName
            else:
                name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
            if name != "":
                try:
                    loadLevel(name, sportType, sportDifficulty)
                except IOError:
                    print("bad file .. ;( i will now cry")

        if LOAD_FULL_GAME_BUTTON.draw(SCREEN):
            if lockFileName:
                name = lockedFileName
            else:
                name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
            if name != "":
                try:
                    for i in range(6):
                        for j in range(3):
                            loadLevel(name, i, j)
                except IOError:
                    print("bad file .. ;( i will now cry")

        # loads one level's graphics
        if LOAD_LEVEL_TILES_BUTTON.draw(SCREEN):
            if lockFileName:
                name = lockedFileName + "_course bigtile_" + CONST_SPORTS[sportType]
            else:
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
                # make var to hold, also compare to original_heights, and add that in the last input message
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
                if 0x8 <= tempHoriz <= 0xF8:
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

        # mouse tracker (adjusted for tile grid clicking)
        mouseX = mouseX // (gridTileWidth)
        mouseY = (mouseY - scroll) // (gridTileWidth)

        if VERTICAL_LINE_COUNT > mouseX >= 0 and mouseY < sportHeights[sportType][sportDifficulty]:
            mouseOverTile = allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16]
            if pygame.mouse.get_pressed()[0] == 1:
                if drawMode == drawModes.draw and mouseOverTile != chosenTile:
                    mouseOverTile = chosenTile
                elif drawMode == drawModes.bucket and mouseOverTile != chosenTile:
                    paint(mouseX, mouseY, chosenTile, mouseOverTile, allLevelTileCSVs[sportType][sportDifficulty], sportHeights[sportType][sportDifficulty])
                elif drawMode == drawModes.stamp:
                    stamp(mouseX, mouseY, stampArr)
            elif pygame.mouse.get_pressed()[1] == 1 and mouseOverTile != chosenTile:
                chosenTile = mouseOverTile
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
                        stampArr.append(allLevelTileCSVs[sportType][sportDifficulty][topLeft[0] + (topLeft[1] + i) * 16:topLeft[0] + horizLen + (topLeft[1] + i) * 16])
                selectOrigCoords = []

        # buttons for drawing mode
        if PENCIL_BUTTON.draw(SCREEN):
            drawMode = drawModes.draw
        if BUCKET_BUTTON.draw(SCREEN):
            drawMode = drawModes.bucket
        if STAMP_BUTTON.draw(SCREEN):
            drawMode = drawModes.stamp
        # and highlight selected
        modangle = pygame.rect = (870 + drawMode * 40, 50, 32, 32)
        pygame.draw.rect(SCREEN, (255, 0, 0), modangle, 1)

        for i in range(10):  # draws inv items to the screen
            tempPic = pygame.transform.scale(imageList[sportType][0][tileInvPictures[i]], (16, 16))  # this seems bad, maybe use 2 lists, one which stores numbers and another which stores pictures?
            SCREEN.blit(tempPic, (583 + (i * 18), 275))
            if effectsOn:
                tempPic = pygame.transform.scale(imageList[sportType][1][tileInvPictures[i]], (16, 16))  # this seems bad, maybe use 2 lists, one which stores numbers and another which stores pictures?
                tempPic.set_alpha(215)
                SCREEN.blit(tempPic, (583 + (i * 18), 275))

    #
    # SUBTILE PAINT MODE AND BIGTILE CONSTRUCTOR MODE
    #
    elif programMode == programModes.subtileDrawer:

        if SUBTILE_EDITOR_BUTTON.draw(SCREEN):
            subtileMode = True
            currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]

        if BIGTILE_EDITOR_BUTTON.draw(SCREEN):
            if subtileMode:
                subtileStackUpdate("change")
            subtileMode = False

        SCREEN.blit(wawa, (750, 580))

        pygame.draw.rect(SCREEN, (255, 0, 0), tempRect, 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), tempRect2, 1)
        pygame.draw.rect(SCREEN, (255, 0, 0), bearRect, 1)

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

                # traverse subtiles with keys
                if event.key == pygame.K_t:
                    subtileMovement = 1
                if event.key == pygame.K_f:
                    subtileMovement = 2
                if event.key == pygame.K_g:
                    subtileMovement = 3
                if event.key == pygame.K_h:
                    subtileMovement = 4

                # changing bigtile:
                if not subtileMode:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        scrollLeft = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        scrollRight = True

                    # traverse bigtile with keys
                    if event.key == pygame.K_i:
                        bigQuadMovement = 1
                    if event.key == pygame.K_j:
                        bigQuadMovement = 2
                    if event.key == pygame.K_k:
                        bigQuadMovement = 3
                    if event.key == pygame.K_l:
                        bigQuadMovement = 4

                if event.key == pygame.K_z:
                    if undoStack != []:
                        latest = undoStack.pop()
                        undoneSubtileSelected = latest[0]
                        redoStack.append([undoneSubtileSelected, subtileGraphics[layerChosen][undoneSubtileSelected * 8:undoneSubtileSelected * 8 + 8]])
                        print(undoStack, "undo")
                        print(redoStack)
                        if len(redoStack) > 150:
                            redoStack = redoStack[50:]
                        subtileGraphics[layerChosen][undoneSubtileSelected * 8:undoneSubtileSelected * 8 + 8] = latest[1]
                        currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                elif event.key == pygame.K_y:
                    if redoStack != []:
                        latest = redoStack.pop()
                        undoneSubtileSelected = latest[0]
                        undoStack.append([undoneSubtileSelected, subtileGraphics[layerChosen][undoneSubtileSelected * 8:undoneSubtileSelected * 8 + 8]])
                        print(redoStack, "redo")
                        print(undoStack)
                        if len(undoStack) > 150:
                            undoStack = undoStack[50:]
                        subtileGraphics[layerChosen][undoneSubtileSelected * 8:undoneSubtileSelected * 8 + 8] = latest[1]
                        currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]

                # copying and pasting in subtile mode
                if event.key == pygame.K_c:
                    subtileClipboard[subtileClipboardNumber] = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                
                elif event.key == pygame.K_v:
                    currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                    if subtileClipboard[subtileClipboardNumber] != currentSubtileStackInfo:
                        undoStack.append([subtileSelected, currentSubtileStackInfo])
                        subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8] = subtileClipboard[subtileClipboardNumber]
                        currentSubtileStackInfo = subtileClipboard[subtileClipboardNumber]

                # changing the subtile mode copying clipboard
                match event.key:
                    case pygame.K_1:
                        subtileClipboardNumber = 0
                    case pygame.K_2:
                        subtileClipboardNumber = 1
                    case pygame.K_3:
                        subtileClipboardNumber = 2
                    case pygame.K_4:
                        subtileClipboardNumber = 3
                    case pygame.K_5:
                        subtileClipboardNumber = 4
                    case pygame.K_6:
                        subtileClipboardNumber = 5
                    case pygame.K_7:
                        subtileClipboardNumber = 6
                    case pygame.K_8:
                        subtileClipboardNumber = 7
                    case pygame.K_9:
                        subtileClipboardNumber = 8
                    case pygame.K_0:
                        subtileClipboardNumber = 9

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scrollUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scrollDown = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    scrollLeft = False
                    waiter = True
                    scrollLRWait = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    scrollRight = False
                    waiter = True
                    scrollLRWait = 0
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollSpeed = 1

                if event.key in (pygame.K_t, pygame.K_f, pygame.K_g, pygame.K_h):
                    subtileMovement = 0
                    subtileMovWait = 0

                if event.key in (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l):
                    bigQuadMovement = 0
                    bigQuadMovWait = 0

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # lmb up, check if undo stack should be updated
                subtileStackUpdate("lmb up")
                currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll2 += 16 * SMALLTILE_PIXEL * scrollSpeed
                elif event.y == -1:
                    scroll2 -= 16 * SMALLTILE_PIXEL * scrollSpeed

            if event.type == pygame.MOUSEBUTTONUP:
                infoWait, thingyWait, subtileUsageWait = 0, 0, 0

        # scolling (up/down, or W/D)
        if scrollUp:
            scroll2 += 8 * SMALLTILE_PIXEL * scrollSpeed
        if scrollDown:
            scroll2 -= 8 * SMALLTILE_PIXEL * scrollSpeed
        # and L/R
        if scrollLeft or scrollRight:
            if scrollLRWait == 0:
                if scrollLeft:
                    bigtileSelected -= 1
                if scrollRight:
                    bigtileSelected += 1
                scrollLRWait = ((frameseys+1)//25) // (scrollSpeed ** 4)
                if waiter or loadedSpriteType != 22:
                    scrollLRWait *= 4
                    waiter = False
            else:
                scrollLRWait -= 1
            if bigtileSelected < 0:
                bigtileSelected = frameCount - 1
            elif bigtileSelected > frameCount - 1:
                bigtileSelected = 0
            infoUpdater(False)

        if scroll2 < MAX_SCROLL2: #-(320 + 1344*SMALLTILE_PIXEL//NUM_OF_SMALLTILES_DISPLAYED_HZ): #tried to make this work with smalltilepixel but idk how, o well
            scroll2 = MAX_SCROLL2 #-(320 + 1344*SMALLTILE_PIXEL//NUM_OF_SMALLTILES_DISPLAYED_HZ)

            #0, 704, 3776 for 2, 4, 8. trick e i say, verily

        if scroll2 > 0:
            scroll2 = 0

        # != 0 means scrolling thru subtiles with tfgh keys
        if subtileMovement != 0:
            if subtileMovWait == 0:
                match subtileMovement:
                    case 1:
                        subtileSelected -= 16
                        if subtileSelected < 0:
                            subtileSelected = 0
                    case 2:
                        subtileSelected -= 1
                        if subtileSelected < 0:
                            subtileSelected = 0
                    case 3:
                        subtileSelected += 16
                        if subtileSelected >= len(subtileGraphics[layerChosen]) // 8:
                            subtileSelected = (len(subtileGraphics[layerChosen]) // 8) - 1
                    case 4:
                        subtileSelected += 1
                        if subtileSelected >= len(subtileGraphics[layerChosen]) // 8:
                            subtileSelected = (len(subtileGraphics[layerChosen]) // 8) - 1
                subtileMovWait = ((frameseys+1)//8) // (scrollSpeed ** 3)
                subtileStackUpdate("subtile mov")
                infoUpdater(False)
                currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                print(currentSubtileStackInfo, undoStack)
            else:
                subtileMovWait -= 1

        # != 0 means scrolling thru bigtile with ijkl keys
        if bigQuadMovement != 0:
            if bigQuadMovWait == 0:
                match bigQuadMovement:
                    case 1:
                        bigtileQuadrantSelected -= spriteWidth[layerChosen]
                        if bigtileQuadrantSelected < 0:
                            bigtileQuadrantSelected = 0
                    case 2:
                        bigtileQuadrantSelected -= 1
                        if bigtileQuadrantSelected < 0:
                            bigtileQuadrantSelected = 0
                    case 3:
                        bigtileQuadrantSelected += spriteWidth[layerChosen]
                        if bigtileQuadrantSelected >= spriteWidth[layerChosen] * spriteHeight[layerChosen]:
                            bigtileQuadrantSelected = (spriteWidth[layerChosen] * spriteHeight[layerChosen]) - 1
                    case 4:
                        bigtileQuadrantSelected += 1
                        if bigtileQuadrantSelected >= spriteWidth[layerChosen] * spriteHeight[layerChosen]:
                            bigtileQuadrantSelected = (spriteWidth[layerChosen] * spriteHeight[layerChosen]) - 1
                bigQuadMovWait = ((frameseys+1)//8) // scrollSpeed**2
                subtileStackUpdate("bigquad mov")
                infoUpdater(False)
                currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                print(currentSubtileStackInfo, undoStack)
            else:
                bigQuadMovWait -= 1

            """if loadedSpriteType >= 22:
                if loadedSpriteType == 22:
                    ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
                elif loadedSpriteType > 22:
                    ox400IndexThingForHere = bigtileQuadrantSelected
                #else:
                    #ox400IndexThingForHere = bigtileSelected * spriteWidth[layerChosen] * spriteHeight[layerChosen] + bigtileQuadrantSelected
                P = spritePalettes[0][ox400IndexThingForHere]
                subtileyPalleteyThingies = [P & 0x80 != 0, P & 0x40 != 0, P & 0x20 != 0]"""

        # clicks
        if pygame.mouse.get_pressed()[0] == 1:
            # print(mouseX, mouseY)
            # clicking a palette and colour (choose them and change cur quadrant)
            if 750 < mouseX < 750 + (PALETTE_PIXEL * 4) and 385 < mouseY < 385 + (PALETTE_PIXEL * 8):
                colourSelected = (mouseX - 750) // PALETTE_PIXEL
                paletteSelected = (mouseY - 385) // PALETTE_PIXEL
                if loadedSpriteType == 22:
                    if not subtileMode:
                        ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
                        spritePalettes[0][ox400IndexThingForHere] = (spritePalettes[0][ox400IndexThingForHere] & 0b11111000) | paletteSelected
                elif loadedSpriteType < 22:
                    spritePalettes[layerChosen][bigtileQuadrantSelected] = paletteSelected
                else:
                    spritePalettes[0][bigtileQuadrantSelected] = (spritePalettes[0][bigtileQuadrantSelected] & 0b11111000) | paletteSelected

            # clicking a big subtile thingy to change it
            elif subtileMode and 0 < mouseX < (quadrantPixel * 2 * 8) and 50 < mouseY < 50 + (quadrantPixel * 2 * 8) and (loadedSpriteType >= 22 or subtileSelected != 0):  # end part is so the ghost tile isn't editable
                colnum = ((mouseX) // (quadrantPixel * 2))
                rownum = ((mouseY - 50) // (quadrantPixel * 2))
                index = subtileSelected * 8 + rownum
                if index < len(subtileGraphics[layerChosen]) + 1:
                    subtileGraphics[layerChosen][index] = subtileGraphics[layerChosen][index][0:colnum] + str(colourSelected) + subtileGraphics[layerChosen][index][colnum + 1:]

            # clicking a big bigtile quadrant
            elif not subtileMode and 0 < mouseX < (quadrantPixel * 8 * spriteWidth[layerChosen]) and 50 < mouseY < 50 + (quadrantPixel * 8 * spriteHeight[layerChosen]):
                bigtileQuadrantSelected = mouseX // (quadrantPixel * 8) + ((mouseY - 50) // (quadrantPixel * 8)) * spriteWidth[layerChosen]
                subtileStackUpdate("bigquad click")
                infoUpdater(False)
                currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                print(currentSubtileStackInfo, undoStack)

            # clicking a small subtile
            elif 750 < mouseX < 750 + SMALLTILE_PIXEL * 8 * NUM_OF_SMALLTILES_DISPLAYED_HZ and 50 < mouseY < 50 + SMALLTILE_PIXEL * 8 * (320 // (SMALLTILE_PIXEL * 8)):  # for how many things can fit, usually 10 for 320px but i want to make this a little more editable so ha !
                subtileStackUpdate("small subtile")
                ###print("C")
                subtileSelected = int(((mouseY - scroll2 - 50) // (SMALLTILE_PIXEL * 8)) * NUM_OF_SMALLTILES_DISPLAYED_HZ + ((mouseX - 750) // (SMALLTILE_PIXEL * 8)))
                currentSubtileStackInfo = subtileGraphics[layerChosen][subtileSelected * 8:subtileSelected * 8 + 8]
                if subtileSelected > (len(subtileGraphics[layerChosen]) // 8) - 1:
                    subtileSelected = (len(subtileGraphics[layerChosen]) // 8) - 1
                if loadedSpriteType < 22:
                    paletteSelected = spritePalettes[layerChosen][subtileSelected]
                if not subtileMode:
                    if loadedSpriteType == 22:
                        ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
                        spriteSubtiles[0][ox400IndexThingForHere] = subtileSelected % 0x100
                        if subtileSelected >= 0x100:
                            spritePalettes[0][ox400IndexThingForHere] |= 0x8
                        else:
                            spritePalettes[0][ox400IndexThingForHere] &= 0xF7  # gets rid of 0x8
                    elif loadedSpriteType < 22:
                        ox400IndexThingForHere = bigtileSelected * spriteWidth[layerChosen] * spriteHeight[layerChosen] + bigtileQuadrantSelected
                        spriteSubtiles[layerChosen][ox400IndexThingForHere] = subtileSelected
                    else:
                        ox400IndexThingForHere = bigtileQuadrantSelected
                        spriteSubtiles[0][ox400IndexThingForHere] = subtileSelected % 0x100
                        if subtileSelected >= 0x100:
                            spritePalettes[0][ox400IndexThingForHere] |= 0x8
                        else:
                            spritePalettes[0][ox400IndexThingForHere] &= 0xF7  # gets rid of 0x8

            # clicking a collision colour (and change cur quadrant)
            elif 0 < mouseX < COLLISION_PIXEL * 3 and 400 < mouseY < 400 + COLLISION_PIXEL * 5 and not subtileMode and loadedSpriteType == 22:
                ###print("D")
                collisionSelected = ((mouseY - 400) // COLLISION_PIXEL) * 3 + (mouseX // COLLISION_PIXEL)
                for key in COLLISION_COLOUR_MAPPER:
                    if COLLISION_COLOUR_MAPPER[key] == collisionSelected:
                        bigtileCollisions[bigtileSelected * 4 + bigtileQuadrantSelected % 4] = key
                        break

            # clicking a subtileythingy
            elif 856 < mouseX < 856 + THINGY_PIXEL and 395 < mouseY < 395 + THINGY_PIXEL * 3 + 20 and not subtileMode and loadedSpriteType >= 22:
                if thingyWait == 0:
                    if loadedSpriteType == 22:
                        ox400IndexThingForHere = bigtileSelected * 2 + bigtileQuadrantSelected % 2 + (bigtileQuadrantSelected // 2) * 0x20 + (bigtileSelected // 0x10) * 0x20
                    else: # > 22
                        ox400IndexThingForHere = bigtileQuadrantSelected
                    ###print("E")
                    if mouseY < 395 + THINGY_PIXEL:  # button 1 (prio)   and loadedSpriteType == 22?
                        subtileyPalleteyThingies[0] = not subtileyPalleteyThingies[0]
                        spritePalettes[0][ox400IndexThingForHere] ^= 0x80
                    elif 395 + THINGY_PIXEL + 10 < mouseY < 395 + THINGY_PIXEL * 2 + 10:  # button 2 (vt flip)
                        subtileyPalleteyThingies[1] = not subtileyPalleteyThingies[1]
                        spritePalettes[0][ox400IndexThingForHere] ^= 0x40
                    elif 395 + THINGY_PIXEL * 2 + 20 < mouseY < 395 + THINGY_PIXEL * 3 + 20:  # button 3 (hz flip)
                        subtileyPalleteyThingies[2] = not subtileyPalleteyThingies[2]
                        spritePalettes[0][ox400IndexThingForHere] ^= 0x20
                    thingyWait = (frameseys+1)//6
                else:
                    thingyWait -= 1

            # non 17 thingies (vision of the layers of the bayers with the big wayers)
            elif 856 < mouseX < 856 + THINGY_PIXEL and 445 < mouseY < 445 + THINGY_PIXEL * (layers + 1) + 10 * layers and loadedSpriteType < 22:
                for i in range(layers):
                    if 445 + (THINGY_PIXEL + 10) * (i) < mouseY < 445 + THINGY_PIXEL * (i + 1) + 10 * (i):  # button 1 (prio)
                        if spriteWidth[i] != spriteWidth[layerChosen] or spriteHeight[i] != spriteHeight[layerChosen]:
                            bigtileQuadrantSelected = 0
                        layerChosen = i
                        infoUpdater(False)
                        break

            ##
            # sprite types
            elif 972 < mouseX < 990 and 596 < mouseY < 615:  # ramp left
                spriteType = 7
                if sportType == 0 or sportType == 1 or sportType == 4:
                    tempRect2 = pygame.Rect = (1014, 596, 18, 18)
            elif 993 < mouseX < 1012 and 596 < mouseY < 615:  # ramp mid
                spriteType = 9
            elif 1014 < mouseX < 1033 and 596 < mouseY < 615:  # ramp right
                spriteType = 8
                if sportType == 0 or sportType == 1 or sportType == 4:
                    spriteType = 7
                    tempRect2 = pygame.Rect = (1014, 596, 18, 18)
            elif 960 < mouseX < 979 and 631 < mouseY < 650:  # course bigtiles
                spriteType = 22
            elif 981 < mouseX < 1000 and 631 < mouseY < 650:  # slowing
                spriteType = 0
            elif 1002 < mouseX < 1021 and 631 < mouseY < 650:  # slowing
                spriteType = 15
            elif 1023 < mouseX < 1042 and 631 < mouseY < 650:  # stopped
                spriteType = 16
            elif 1082 < mouseX < 1100 and 608 < mouseY < 627:  # A
                spriteType = 1
            elif 1103 < mouseX < 1121 and 608 < mouseY < 627:  # B
                spriteType = 2
            elif 1082 < mouseX < 1100 and 629 < mouseY < 648:  # AUL
                spriteType = 3
            elif 1103 < mouseX < 1121 and 629 < mouseY < 648:  # BUL
                spriteType = 4
            elif 1082 < mouseX < 1100 and 650 < mouseY < 669:  # AUR
                spriteType = 5
            elif 1103 < mouseX < 1121 and 650 < mouseY < 669:  # BUR
                spriteType = 6
            elif 1156 < mouseX < 1174 and 596 < mouseY < 615:  # mud
                spriteType = 10
            elif 1177 < mouseX < 1195 and 596 < mouseY < 615:  # pud
                spriteType = 11
            elif 1156 < mouseX < 1174 and 617 < mouseY < 646:  # whirlpool
                spriteType = 13
            elif 1177 < mouseX < 1195 and 617 < mouseY < 636:  # ice
                spriteType = 12
            elif 1167 < mouseX < 1185 and 638 < mouseY < 657:  # collision
                spriteType = 14
            elif 1230 < mouseX < 1268 and 592 < mouseY < 630:  # brobear
                bearType = 0
            elif 1230 < mouseX < 1268 and 633 < mouseY < 671:  # sisbear
                bearType = 1
            elif 950 < mouseX < 968 and 651 < mouseY < 669:  # HUD diffs
                spriteType = 17
            elif 971 < mouseX < 989 and 651 < mouseY < 669:  # HUD sports
                spriteType = 18
            elif 992 < mouseX < 1010 and 651 < mouseY < 669:  # 5x5 selectangle
                spriteType = 19
            elif 1013 < mouseX < 1031 and 651 < mouseY < 669:  # 4x3 selectangle
                spriteType = 20
            elif 1034 < mouseX < 1052 and 651 < mouseY < 669:  # the medal!
                spriteType = 21
            elif 772 < mouseX < 790 and 608 < mouseY < 626:  # dev/publisher credit intro
                spriteType = 23
            elif 793 < mouseX < 811 and 608 < mouseY < 626:  # brobear is soo cool!
                spriteType = 24
            elif 814 < mouseX < 832 and 608 < mouseY < 626:  # car intro
                spriteType = 25
            elif 772 < mouseX < 790 and 629 < mouseY < 640:  # various menu items
                spriteType = 26
            elif 793 < mouseX < 811 and 629 < mouseY < 640:  # font 1
                spriteType = 27
            elif 814 < mouseX < 832 and 629 < mouseY < 640:  # font 2
                spriteType = 28
            elif 772 < mouseX < 790 and 650 < mouseY < 668:  # course intro
                spriteType = 29
            elif 793 < mouseX < 811 and 650 < mouseY < 668:  # scoreboard
                spriteType = 30
            elif 814 < mouseX < 832 and 650 < mouseY < 668:  # podium finish
                spriteType = 31

            spriteType = spriteCheck(sportType, spriteType)
            tempRect = pygame.Rect = HIGHLIGHTY_SPRITE_RECTANGLE_POSITIONS[spriteType]
            if spriteType != 7:
                tempRect2 = pygame.Rect = (0, 0, 0, 0)
            bearRect = pygame.Rect = HIGHLIGHTY_BEAR_RECTANGLE_POSITIONS[bearType]

        # right clicks
        elif pygame.mouse.get_pressed()[2] == 1:
            # clicking a palette colour (change it)
            if 750 < mouseX < 750 + PALETTE_PIXEL * 4 and 385 < mouseY < 385 + PALETTE_PIXEL * 8:
                gogo = False
                while not gogo:
                    newHex = input(f"input new rgb values, separated by spaces (e.g. 12 23 255) (currently {hexCodes[((mouseY - 385) // 20) * 4 + ((mouseX - 750) // 20)]}) (leave blank to abort): ")
                    if newHex != "":
                        newHex = newHex.split(" ", 3)
                        if len(newHex) != 3:
                            print("Invalid input.")
                        else:
                            try:
                                for i in range(3):
                                    newHex[i] = int(newHex[i])
                                hexCodes[((mouseY - 385) // 20) * 4 + ((mouseX - 750) // 20)] = newHex
                                gogo = True
                            except Exception:
                                print("Invalid input.")
                    else:
                        gogo = True

        # loading palettes, and later subtiles and bigtiles
        if LOAD_BUTTON.draw(SCREEN):
            if spriteType == 22:
                loadSubtileData(sportType)
            elif spriteType > 22:
                loadSubtileDataWithLongHeader()
            else:
                loadSubtileDataWithHeader()
            bigtileSelected = 0
            bigtileQuadrantSelected = 0
            infoUpdater(True)

        # saving palette and tile data to a game
        if SAVE_BUTTON.draw(SCREEN):
            print("Currently, you are saving ", end="")
            if loadedSpriteType < 17 or loadedSpriteType > 28 or loadedSpriteType == 22:
                if loadedSpriteType != 22:
                    if loadedSportType in (0, 2):
                        print("the Berenstain family's ", end="")
                    else:
                        print(f"{BEARTYPES[loadedBearType]} bear's ", end="")
                print(f"{SPRITES[loadedSpriteType]} graphics for {SPORTS[loadedSportType]}. ", end="")
            else:
                print(f"{SPRITES[loadedSpriteType]} graphics. ")
            if loadedSpriteType in (27, 28):
                print(f"(Note that this palette is for the selected level, and that changing this palette changes only this level's colours.)")
            if loadedSpriteType == 22:
                saveThine22Data(loadedSportType)
            elif loadedSpriteType < 22:
                saveThineSub22Data()
            else:
                saveThineSup22Data()

        # making pngs of bigtiles
        if PRINT_BUTTON.draw(SCREEN):
            # making folders if needed
            gogogo = False
            if not os.path.exists(f"tiles/temptiles"):
                os.makedirs(f"tiles/temptiles")
            if not os.path.exists(f"tiles/efftemptiles"):
                os.makedirs(f"tiles/efftemptiles")
            print("(Remember that if the temptiles or efftemptiles folders are already full, then there may be extra tiles when saving PNGs)")

            # loop for each bigtile
            for i in range(frameCount):
                if loadedSpriteType == 22:
                    bmpPrintrer22up(i, layerChosen, True)
                elif loadedSpriteType < 22:
                    lengthery = layers
                    if loadedSpriteType in (3, 4, 9) or (loadedSpriteType in (1, 2, 5, 6) and loadedSportType not in (2, 3)):
                        lengthery -= 1  # shadow hider in eye land
                    bmpPrintrerSprite(i, lengthery)
                else:
                    bmpPrintrer22up(i, layerChosen, False)
            print("tiles saved to temp folders in levels as bmp files!")
            if lockFileName:
                name = lockedFileName + "_" + SPRITES[loadedSpriteType] + "_" + CONST_SPORTS[loadedSportType]
            else:
                name = input("do you want to turn these into png files, and if so to which folder should they be saved? (makes folders called 'name' and 'name_effects' in the tiles folder, unless they exist already) (leave blank for no): ")
            if name != "":
                go_ahead = True
                if os.path.exists(f"tiles/{name}") or os.path.exists(f"tiles/{name}_effects"):
                    if input(f'a folder with this name ({name} or {name}_effects exists. Do you want to overwrite it? ("Y" for yes) ').upper() != "Y":
                        go_ahead = False
                if go_ahead:
                    print("working...")
                    pngify(name)
                    print("done! :)")
                else:
                    print("no changes have been made.")

        # locks file name so you don't need to go back to the console all the time.
        # a bit scary since it's easier to overwrite stuff by accident
        if LOCK_FILE_NAME_BUTTON.draw(SCREEN):
            print(f"The current file name is {lockedFileName}.")
            lockedFileName = input("Input a file name (without the extension) to have it be used for all future commands (or leave empty to turn the lock off): ")
            if lockedFileName != "":
                lockFileName = True
            else:
                lockFileName = False
            pass

        # prints where subtiles are used in bigtiles
        if SUBTILE_USAGE_BUTTON.draw(SCREEN):
            if subtileUsageWait == 0:
                bigtilesUsing = []
                breakFlag = False
                for i in range(frameCount):  # for each bigtile
                    if breakFlag:
                        break
                    for j in range(spriteWidth[layerChosen] * spriteHeight[layerChosen]):
                        if loadedSpriteType == 22:
                            ox400PainIndex = (i % 0x10) * 2 + (i // 0x10) * 0x40 + (j % 2) + (j // 2) * 0x20  # why must these be stored in such a strange order :(
                            if spriteSubtiles[0][ox400PainIndex] + ((spritePalettes[0][ox400PainIndex] & 0x8) * 0x20) == subtileSelected:
                                bigtilesUsing.append(str(i) + QUADRANT_MAPPER[j])
                        elif loadedSpriteType < 22:
                            ox400PainIndex = i * (spriteWidth[layerChosen] * spriteHeight[layerChosen]) + j
                            if spriteSubtiles[layerChosen][ox400PainIndex] == subtileSelected:
                                bigtilesUsing.append(f"{str(i)} ({j % spriteWidth[layerChosen]}, {j // spriteWidth[layerChosen]})")
                        else:
                            ox400PainIndex = i * (spriteWidth[layerChosen] * spriteHeight[layerChosen]) + j
                            if spriteSubtiles[0][ox400PainIndex] + ((spritePalettes[0][ox400PainIndex] & 0x8) * 0x20) == subtileSelected:
                                bigtilesUsing.append(f"{str(i)} ({j % spriteWidth[layerChosen]}, {j // spriteWidth[layerChosen]})")
                if bigtilesUsing == []:
                    print(f"subtile {subtileSelected} is never used in any bigtile.")
                else:
                    print(f"subtile {subtileSelected} is used in these bigtiles: {[i for i in bigtilesUsing]}")
                subtileUsageWait = (frameseys+1)//4
            else:
                subtileUsageWait -= 1

        # drawing palettes and highlight
        for i in range(0x20):
            rectangle = pygame.Rect = ((i * PALETTE_PIXEL) % (PALETTE_PIXEL * 4) + 750, (i // 4) * PALETTE_PIXEL + 385, PALETTE_PIXEL, PALETTE_PIXEL)
            pygame.draw.rect(SCREEN, hexCodes[i], rectangle)
        # and highlight the selected one
        highlightangle = (PALETTE_PIXEL * colourSelected + 750, PALETTE_PIXEL * paletteSelected + 385, PALETTE_PIXEL, PALETTE_PIXEL)
        pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

        # drawing editable subtile/bigtile
        if subtileMode:
            for i in range(8):
                for j in range(8):
                    rectangle = pygame.Rect = ((j * quadrantPixel * 2), (i * quadrantPixel * 2) + 50, quadrantPixel * 2, quadrantPixel * 2)
                    #try:
                    wower = (subtileGraphics[layerChosen][(subtileSelected) * 8 + i][j])
                    pygame.draw.rect(SCREEN, hexCodes[paletteSelected * 4 + (int(wower))], rectangle)
                    #except Exception:
                    #    print("wodawr")
                    #    break
        # and drawing changeable bigtiles:
        else:
            if displayBigtileSubtiles:
                #try:
                # drawing subtiles on big bigtile:
                if loadedSpriteType >= 22 or not eyeMode:
                    subtilesOnBigtile(layerChosen)
                else:
                    lengthery = layers
                    if loadedSpriteType in (3, 4, 9) or (loadedSpriteType in (1, 2, 5, 6) and loadedSportType not in (2, 3)):
                        lengthery -= 1  # shadow hider in eye land
                    for i in range(lengthery)[::-1]:
                        subtilesOnBigtile(i)
                #except Exception:
                    #print("wawawfa")

            if loadedSpriteType == 22:
                # drawing collision colours
                for i in range(5):
                    for j in range(3):
                        rectangle = pygame.Rect = ((j * COLLISION_PIXEL), (400 + i * COLLISION_PIXEL), COLLISION_PIXEL, COLLISION_PIXEL)
                        pygame.draw.rect(SCREEN, colours[i * 3 + j], rectangle)
                # and highlight the selected one
                highlightangle = (COLLISION_PIXEL * (collisionSelected % 3) + 0, COLLISION_PIXEL * (collisionSelected // 3) + 400, COLLISION_PIXEL, COLLISION_PIXEL)
                pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

                if displayBigtileCollision:
                    # drawing collision on big bigtile
                    for i in range(2):
                        for j in range(2):
                            s = pygame.Surface((quadrantPixel * 8, quadrantPixel * 8))
                            if alpher:
                                s.set_alpha(150)
                            s.fill(colours[COLLISION_COLOUR_MAPPER[bigtileCollisions[bigtileSelected * 4 + j + i * 2]]])
                            SCREEN.blit(s, (j * quadrantPixel * 8, i * quadrantPixel * 8 + 50))

        # highlight the selected quadrant
        if not subtileMode:
            highlightangle = ((bigtileQuadrantSelected % spriteWidth[layerChosen]) * quadrantPixel * 8, (bigtileQuadrantSelected // spriteWidth[layerChosen]) * quadrantPixel * 8 + 50, quadrantPixel * 8, quadrantPixel * 8)
            pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)

        # drawing the subtile menu and selected subtile thing in top right
        tinySubtileDraw(subtileGraphics[layerChosen], hexCodes, paletteSelected, scroll2)
        # and highlight the selected one
        Y = (SMALLTILE_PIXEL * 8 * (subtileSelected // NUM_OF_SMALLTILES_DISPLAYED_HZ) + 50 + scroll2)
        NUM_OF_SMALLTILES_DISPLAYED_VT = ((320 + SMALLTILE_PIXEL) // (SMALLTILE_PIXEL * 8))
        if Y < 50:
            pygame.draw.line(SCREEN, (255, 0, 0), (750, 50), (1261, 50))
        elif Y < 50 + NUM_OF_SMALLTILES_DISPLAYED_VT * 8 * SMALLTILE_PIXEL:  # another not *10 so ha for the 336 part
            highlightangle = (SMALLTILE_PIXEL * 8 * (subtileSelected % NUM_OF_SMALLTILES_DISPLAYED_HZ) + 750, Y, SMALLTILE_PIXEL * 8, SMALLTILE_PIXEL * 8)
            pygame.draw.rect(SCREEN, (255, 0, 0), highlightangle, 1)
        else:
            pygame.draw.line(SCREEN, (255, 0, 0), (750, 50 + NUM_OF_SMALLTILES_DISPLAYED_VT * 8 * SMALLTILE_PIXEL), (750 + SMALLTILE_PIXEL * 8 * NUM_OF_SMALLTILES_DISPLAYED_HZ, 50 + NUM_OF_SMALLTILES_DISPLAYED_VT * 8 * SMALLTILE_PIXEL))

        # draw sport buttons, sport button memory, & actions
        sportCount = 0
        for sportCount, typeButton in enumerate(sportTypeButtons):
            if typeButton.draw(SCREEN):
                sportType = sportCount
                spriteType = spriteCheck(sportType, spriteType)
                if (spriteType == 7 or spriteType == 8) and (sportType == 0 or sportType == 1 or sportType == 4):
                    spriteType = 7
                    tempRect2 = pygame.Rect = (1004, 596, 18, 18)
                elif spriteType == 7 and sportType == 5:
                    tempRect2 = pygame.Rect = (0, 0, 0, 0)

        # highlight for sport type
        pygame.draw.rect(SCREEN, (255, 0, 0), sportTypeButtons[sportType], 1)

        # drawing subtile palettey extra thingies
        if not subtileMode:
            if loadedSpriteType >= 22:  # since palettes are connected to tiles i dont think these would be useful for bear sprites
                for i, thingy in enumerate(subtileyPalleteyThingies):
                    # if i == 0 and loadedSpriteType != 17:
                    #    continue
                    rectangle = pygame.Rect = (856, 395 + i * (THINGY_PIXEL + 10), THINGY_PIXEL, THINGY_PIXEL)
                    if thingy:
                        pygame.draw.rect(SCREEN, (255, 255, 0), rectangle)
                    else:
                        pygame.draw.rect(SCREEN, (75, 75, 100), rectangle)

                # and the display toggler buttons
                if loadedSpriteType == 22:
                    if TOGGLE_SUBTILES_BUTTON.draw(SCREEN):
                        if thingyWait == 0:
                            displayBigtileSubtiles = not displayBigtileSubtiles
                            alpher = not alpher
                            thingyWait = (frameseys+1)//6
                        else:
                            thingyWait -= 1
                    if TOGGLE_COLLISIONS_BUTTON.draw(SCREEN):
                        if thingyWait == 0:
                            displayBigtileCollision = not displayBigtileCollision
                            thingyWait = (frameseys+1)//6
                        else:
                            thingyWait -= 1

            SCREEN.blit(thefont.render(f"bigtile: {bigtileSelected}", True, (0, 0, 0)), (18, 8))

        # drawing layer button things
        if loadedSpriteType < 22:
            if EYE_BUTTON.draw(SCREEN):
                if thingyWait == 0:
                    if eyeMode:
                        EYE_BUTTON = button.Button(856, 395, EYE_IMAGES[0], 1)
                    else:
                        EYE_BUTTON = button.Button(856, 395, EYE_IMAGES[1], 1)
                    eyeMode = not eyeMode
                thingyWait = (frameseys+1)//6
            thingyWait -= 1
            if thingyWait < 0:
                thingyWait = 0

            for i in range(layers):
                # if i == 0 and loadedSpriteType != 17:
                #    continue
                rectangle = pygame.Rect = (856, 445 + i * (THINGY_PIXEL + 10), THINGY_PIXEL, THINGY_PIXEL)
                if i == layerChosen:
                    pygame.draw.rect(SCREEN, (200, 255, 50), rectangle)
                else:
                    pygame.draw.rect(SCREEN, (75, 100, 150), rectangle)

        SCREEN.blit(thefont.render(f"subtile: {subtileSelected}", True, (0, 0, 0)), (950, 8))

        if INFO_BUTTON.draw(SCREEN):
            infoMode = not infoMode
            pygame.time.wait(200)

    pygame.display.update()
