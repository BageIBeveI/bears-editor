# heavily based off of Coding With Russ' videos, so figured i should give credit here

import pygame
import button
import csv
import re

#pygame initializer
pygame.init()

#window maker
SCREEN = pygame.display.set_mode((830, 600))

#title & icon
pygame.display.set_caption("bears tile editor")
ICON = pygame.image.load("tile_editor_pictures/raftin.png")
pygame.display.set_icon(ICON)

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

#buttons for the tile map
def gridButtonMaker():
    currentColumn = 0
    currentRow = 0

    for byte in allLevelTileCSVs[sportType][sportDifficulty]:
        SCREEN.blit(imageList[sportType][byte], (0 + currentColumn * gridTileWidth, 0 + currentRow * gridTileWidth + scroll))

        currentColumn += 1
        if currentColumn == 16:
            currentColumn = 0
            currentRow += 1


#variables
SPORTS = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
DIFFICULTIES = ["Beginner", "Intermediate", "Expert"]
HORIZONTAL_LINE_VALUES = [0x21B, 0x2A1, 0x31E]
BEARS_LEVEL_DATA_OFFSET_RANGES = [[0x28004, 0x2C004, 0x30004], [0x34004, 0x38004, 0x3C004], [0x40004, 0x44004, 0x48004], [0x4C004, 0x50004, 0x54004], [0x58004, 0x5C004, 0x60004], [0x64004, 0x68004, 0x6C004]]
sportType = 0
sportDifficulty = 0
scrollUp = False
scrollDown = False
scroll = 0
#scrollSpeed = 1
#scalingFactor = 2 (if ever you do want to bring this back, you'll have to a bunch of grid/tile related stuff by it (imagestorer, grid, etc) or maybe not since pygame can transform)
horizontalLineCount = 538
VERTICAL_LINE_COUNT = 16
NUMBER_OF_TILES = 256
chosenTile = 0
gridTileWidth = 32
allLevelTileCSVs = []
inventoryIndex = 0
effects = False

#tilemap data storage (lists in lists, where list[sport][diff] = the correct data)
for sport in range(6):
    tempCSV = []
    for difficulty in range(3):
        try:
            tempCSV.append([int(byte) for byte in (re.split(",|\n", open(f"levels/{SPORTS[sport]}{DIFFICULTIES[difficulty]}Level.csv", "r").read()))])
        except FileNotFoundError:
            if SPORTS[sport][-8:] == "_effects":
                namelength = len(SPORTS[sport])
                tempCSV.append([int(byte) for byte in (re.split(",|\n", open(f"levels/{SPORTS[sport][0:namelength - 8]}{DIFFICULTIES[difficulty]}Level.csv", "r").read()))])
            else:
                raise FileNotFoundError
    allLevelTileCSVs.append(tempCSV)

#tile images (they change depending on the sport type)
def tileImageStorer():
    allTileLists = []

    for sport in SPORTS:
        tileList = []
        for i in range(NUMBER_OF_TILES):
            tile = pygame.image.load(f'tiles/{sport}/tile{i}.png').convert_alpha() #you can replace i with ((hex(i)[2:]).zfill(2)).upper() if you want, just remember to generate tile names w/ hex as well
            tile = pygame.transform.scale(tile, (32, 32))
            tileList.append(tile)
        allTileLists.append(tileList)
    return allTileLists
imageList = tileImageStorer()

#button instances
sportTypeButtons = []
sportDifficultyButtons = []
tileInvButtons = []

sportTypeButtons.append(button.Button(560, 45, TOBOGGAN_IMAGE, 2))
sportTypeButtons.append(button.Button(704, 45, SLED_IMAGE, 2))
sportTypeButtons.append(button.Button(560, 90, RAFT_IMAGE, 2))
sportTypeButtons.append(button.Button(704, 90, KAYAK_IMAGE, 2))
sportTypeButtons.append(button.Button(560, 135, BIKE_IMAGE, 2))
sportTypeButtons.append(button.Button(704, 135, DIRTBOARD_IMAGE, 2))

sportDifficultyButtons.append(button.Button(550, 190, BEGINNER_IMAGE, 2))
sportDifficultyButtons.append(button.Button(640, 190, INTERMEDIATE_IMAGE, 2))
sportDifficultyButtons.append(button.Button(730, 190, EXPERT_IMAGE, 2))

#for i in range(10):
    #tileInvButtons.append(button.Button())



GRID_BUTTON = button.Button(710, 10, GRID_IMAGE, 1)
SAVE_BUTTON = button.Button(750, 10, SAVE_IMAGE, 1)
LOAD_BUTTON = button.Button(790, 10, LOAD_IMAGE, 1)
EFFECTS_BUTTON = button.Button(658, 10, EFFECTS_IMAGE, 2)

#clickable tile buttons
def buttonMaker():
    clickableTileButtonLists = []
    imageList = tileImageStorer()
    for sportIndex in range(6):
        singleSportButtonList = []
        currentColumn = 0
        currentRow = 0
        for i in range(NUMBER_OF_TILES):
            singleSportButtonList.append(button.Button(529 + currentColumn * 18, 304 + currentRow * 18, imageList[sportIndex][i], 0.5))
            currentColumn += 1
            if currentColumn == 16:
                currentColumn = 0
                currentRow += 1
        clickableTileButtonLists.append(singleSportButtonList)

    return clickableTileButtonLists


CLICKY_TILES = buttonMaker()

#grid line drawing
# def gridPlacer():
#     for c in range(VERTICAL_LINE_COUNT + 1):
#         pygame.draw.line(screen, (255, 255, 255), (c * gridTileWidth, 0 + scroll), (c * gridTileWidth, horizontalLineCount * gridTileWidth + scroll))
#     for c in range(horizontalLineCount + 1):
#         pygame.draw.line(screen, (255, 255, 255), (0, c * gridTileWidth + scroll), (512, c * gridTileWidth + scroll))

#setting up tiles in inventory
tileInvPictures = [0] * 10

#game loop
running = True
while running:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keystrokes
        if event.type == pygame.KEYDOWN:
            #grid scrolling
            if event.key == pygame.K_UP:
                scrollUp = True
            if event.key == pygame.K_DOWN:
                scrollDown = True
            #if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                #scrollSpeed = 5

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
            if event.key == pygame.K_UP:
                scrollUp = False
            if event.key == pygame.K_DOWN:
                scrollDown = False
            #if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                #scrollSpeed = 1

        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                scroll += 256
            elif event.y == -1:
                scroll -= 256

    #scolling
    if scrollUp == True:
        scroll += 32
    if scrollDown == True:
        scroll -= 32

    if scroll > 0:
        scroll = 0

    if scroll < -(HORIZONTAL_LINE_VALUES[sportDifficulty]) * (gridTileWidth) + 600: #this is prob very inefficient, should change the value every time diff/grid is changed and store it somrwhere future me pleeeeease :)
        #print(-(HORIZONTAL_LINE_VALUES[sportDifficulty]), gridTileWidth)
        scroll = -(HORIZONTAL_LINE_VALUES[sportDifficulty]) * (gridTileWidth) + 600

    #bg colour
    SCREEN.fill((36, 45, 104))

    #draw sport buttons, sport button memory, & actions
    sportCount = 0
    for sportCount, i in enumerate(sportTypeButtons):
        if i.draw(SCREEN):
            sportType = sportCount
            if sportDifficulty == 0:
                if sportType == 0 or sportType == 1:
                    horizontalLineCount = 0x21A
                else:
                    horizontalLineCount = 0x21B

            imageList = tileImageStorer()

    #draw diff buttons, difficulty button memory, & actions
    difficultyCount = 0
    for difficultyCount, i in enumerate(sportDifficultyButtons):
        if i.draw(SCREEN):
            sportDifficulty = difficultyCount
            if sportDifficulty == 0 and sportType == 0 or sportDifficulty == 0 and sportType == 1:
                horizontalLineCount = 0x21A
            else:
                horizontalLineCount = HORIZONTAL_LINE_VALUES[difficultyCount]

            imageList = tileImageStorer()

    #draw clickable tiles, clicky tile memory, also changes inventory
    tileCount = 0
    for tileCount, i in enumerate(CLICKY_TILES[sportType]):
        if i.draw(SCREEN):
            chosenTile = tileCount
            tileInvPictures[inventoryIndex] = tileCount

    #highlighting (sport, diff, tile)
    pygame.draw.rect(SCREEN, (255, 0, 0), sportTypeButtons[sportType], 1)
    pygame.draw.rect(SCREEN, (255, 0, 0), sportDifficultyButtons[sportDifficulty], 1)
    pygame.draw.rect(SCREEN, (255, 0, 0), CLICKY_TILES[sportType][chosenTile], 1)

    invRect = pygame.Rect = (582 + inventoryIndex * 18, 274, 18, 18) #maybe also bad? idk, im goin ta sleep
    pygame.draw.rect(SCREEN, (255, 0, 0), invRect)

    #gridline drawer
    #gridPlacer()

    #draws grid tile images to screen
    gridButtonMaker()

    # toggles the grid spacings (and draws grid button)
    if GRID_BUTTON.slowDraw(SCREEN):
        if gridTileWidth == 32:
            gridTileWidth = 33
        else:
            gridTileWidth = 32

    # saving features (and draw save)
    if SAVE_BUTTON.draw(SCREEN):
        CSVList = allLevelTileCSVs[sportType][sportDifficulty]

        filename = input("Name your file (. to skip):") #CSV maker
        if filename != ".":
            with open(f"levels/modified levels/{filename}.csv", "w", newline="") as file:
                writenator = csv.writer(file, delimiter=",")
                for i in range(0, len(CSVList), 16):
                    writenator.writerow(CSVList[i:i + 16])
                print("File saved.")

        bearsname = input("Which bears file should it be saved to? (. to skip):") #GBC editor
        if bearsname != ".":
            try:
                with open(f"levels/modified levels/{bearsname}.gbc", "r+b") as file:
                    file.seek(BEARS_LEVEL_DATA_OFFSET_RANGES[sportType][sportDifficulty])
                    CSVByteArray = b''
                    for num in CSVList:
                        CSVByteArray += num.to_bytes(1, "little")
                    file.write(CSVByteArray)
                    file.close()
                    print("Data saved.")
            except FileNotFoundError:
                print("GBC file not found. No edits have been made.")

    # loading features
    if LOAD_BUTTON.draw(SCREEN):
        filename = input("input CSV file name here (. to abort):")
        if filename != ".":
            try:
                with open(f"levels/modified levels/{filename}.csv", "r") as file:
                    liszt = [int(byte) for byte in re.split(",|\n", file.read())[:-1]] #the -1 takes off the last \n of a csv file
                    allLevelTileCSVs[int(input("input sport here (toboggan = 0, sled = 1, ..., dirtboard = 6):"))][int(input("input difficulty here (beginner = 0, intermediate = 1, expert = 2):"))] = liszt
            except FileNotFoundError:
                print("File not found.")

    # effect vision toggle
    if EFFECTS_BUTTON.slowDraw(SCREEN):
        if effects: # gotta take _effects off
            for i in range(6):
                SPORTS[i] = SPORTS[i][:len(SPORTS[i]) - 8]
            effects = False
        else: # gotta add _effects
            for i in range(6):
                SPORTS[i] += "_effects"
            effects = True

        imageList = tileImageStorer()

        pygame.time.wait(200)

    #mouse tracker (for tile grid clicking)
    mousePos = pygame.mouse.get_pos()
    mouseX = (mousePos[0]) // (gridTileWidth)
    mouseY = (mousePos[1] - scroll) // (gridTileWidth)

    if mouseX < VERTICAL_LINE_COUNT and mouseX >= 0 and mouseY < horizontalLineCount:
        if pygame.mouse.get_pressed()[0] == 1 and allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] != chosenTile:
            allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] = chosenTile
            #print(mouseX)
        elif pygame.mouse.get_pressed()[2] == 1 and allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16] != chosenTile:
            chosenTile = allLevelTileCSVs[sportType][sportDifficulty][mouseX + mouseY * 16]
            tileInvPictures[inventoryIndex] = chosenTile

    for i in range(10):
        tempPic = pygame.transform.scale(imageList[sportType][tileInvPictures[i]], (16, 16)) #this seems bad, maybe use 2 lists, one which stores numbers and another which stores pictures?
        SCREEN.blit(tempPic, (583 + (i * 18), 275))


    pygame.display.update()
