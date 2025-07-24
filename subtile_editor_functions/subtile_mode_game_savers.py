### HELPERS
def rgbToGbcBytes(hexCode):
    RGB = hexCode  # [R,G,B] 0-255
    # gbc uses 555 bytes, so each colour uses 5 most significant bytes in this green
    R = bin(RGB[0] >> 3)[2:].zfill(5)
    G = bin(RGB[1] >> 3)[2:].zfill(5)
    B = bin(RGB[2] >> 3)[2:].zfill(5)
    # need this to be in the little endian form GGGRRRRR 0BBBBBGG
    temp = "0" + B + G + R
    littleEndianHex = int(temp, 2).to_bytes(2, "little")
    return littleEndianHex
def quaternaryToBytes(quaternary):
    left, right = "", ""
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
    return (left, right)


### ----------

# saves tile editor data to a game
def saveCourseBigtileData(loadedSportType, hexCodes, subtileGraphics, spritePalettes, bigtileCollisions, spriteSubtiles, lockFileName,
                    lockedFileName):
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
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as gbcFile:

                # sometimes the real palette values for the first are stored in rando places, so use them when needed
                extraOffsets = [[0x4A98, 0, 0, 0x4AA5], [0x8AB0, 0, 0, 0x8ABD], [0, 0, 0xCA3C, 0xCA45], [0, 0, 0x10A75, 0x10A7E], [0, 0, 0x14B62, 0x14B6B], [0, 0, 0x18B7B, 0x18B84]]
                paletteOffset = subtileGraphicsOffsets[loadedSportType] + subtileGraphicsLengths[loadedSportType] + 0xA

                # first palette is 4 colours long. writing it here
                # needs to be separate because not all palettes are near the rest of the data
                firstPaletteLength = 4
                fromBeginning = 0
                for i in range(firstPaletteLength):
                    littleEndianHex = rgbToGbcBytes(hexCodes[i]) #GGGRRRRR 0BBBBBGG as bytes
                    if extraOffsets[loadedSportType][i] == 0:
                        gbcFile.seek(paletteOffset + i * 2, fromBeginning)
                        gbcFile.write(littleEndianHex)
                    else:
                        gbcFile.seek(extraOffsets[loadedSportType][i], fromBeginning)
                        gbcFile.write(littleEndianHex)

                # writing the other 7 palettes
                gbcFile.seek(paletteOffset + firstPaletteLength * 2, fromBeginning)
                fullPaletteLength = 0x20
                for i in range(firstPaletteLength, fullPaletteLength):
                    littleEndianHex = rgbToGbcBytes(hexCodes[i])
                    gbcFile.write(littleEndianHex)

                # writing subtile data
                subtileyOffset = subtileGraphicsOffsets[loadedSportType]
                gbcFile.seek(subtileyOffset)
                for i in range(subtileGraphicsLengths[loadedSportType] // 2):
                    quaternary = subtileGraphics[0][i]

                    bytes = quaternaryToBytes(quaternary)
                    left = bytes[0]
                    right = bytes[1]

                    gbcFile.write(int(left, 2).to_bytes(1, 'little'))
                    gbcFile.write(int(right, 2).to_bytes(1, 'little'))

                # writing collisions and subtile-bigtile arrangements
                longHeaderLength = 10
                bigtileOrCollisionLength = 0x400
                relativeSearch = 1
                gbcFile.seek(bigtileCollisionOffsets[loadedSportType], fromBeginning)
                for byte in bigtileCollisions:
                    gbcFile.write(byte.to_bytes())
                gbcFile.seek(longHeaderLength, relativeSearch)
                for byte in spriteSubtiles[0]:
                    gbcFile.write(byte.to_bytes())
                #gbcFile.seek(bigtileCollisionOffsets[sport] + bigtileOrCollisionLength + (longHeaderLength + bigtileOrCollisionLength), fromBeginning)
                # shouldn't be needed?
                for byte in spritePalettes[0]:
                    gbcFile.write(byte.to_bytes())
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    print("No changes have been made.")
    return

def saveSmallGraphicsData(hexCodes, lockFileName, lockedFileName, loadedSpriteType, loadedSportType, subtileGraphics,
                          spriteSubtiles, spritePalettes, groupNum, loadedBearType, sprites,
                          FAMILYBEAR_SPRITE_OFFSETS,  FAMILY_OBJ_PALETTE_OFFSETS, BROBEAR_SPRITE_OFFSETS,
                          BRO_OBJ_PALETTE_OFFSETS, SISBEAR_SPRITE_OFFSETS, SIS_OBJ_PALETTE_OFFSETS,
                          MORE_SPRITEISH_OFFSETS, MORE_PALETTEY_OFFSETS):

    # subdividing small sprites
    bearSprites = range(0, 17)
    hudSprites = (sprites.hudSports.value, sprites.hudDifficulties.value)

    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as gbcFile:

                # what offsets we use depends on what sprite we're saving. first check if it's a bear
                if loadedSpriteType in bearSprites:
                    # family sports
                    if loadedSportType in (0, 2): #familySports = (0, 2) ?
                        graphicIntroOffsets = FAMILYBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = FAMILY_OBJ_PALETTE_OFFSETS[loadedSportType]
                    # brother bear
                    elif loadedBearType == 0:
                        graphicIntroOffsets = BROBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = BRO_OBJ_PALETTE_OFFSETS[loadedSportType]
                    # sister bear
                    else:
                        graphicIntroOffsets = SISBEAR_SPRITE_OFFSETS[loadedSportType][loadedSpriteType]
                        paletteOffset = SIS_OBJ_PALETTE_OFFSETS[loadedSportType]

                # if not a bear, it's another small sprite
                else:
                    graphicIntroOffsets = MORE_SPRITEISH_OFFSETS[loadedSpriteType - 17]
                    # hud vs not hud, as hud shares the OBJECT palette for the course
                    # maybe needs to change brother and sister bear palette offsets then?
                    # todo: check that out :(
                    if loadedSpriteType in hudSprites:
                        paletteOffset = BRO_OBJ_PALETTE_OFFSETS[loadedSportType]
                    else:
                        paletteOffset = MORE_PALETTEY_OFFSETS[loadedSpriteType - 17]

                # for sprites that have separate groups of data (e.g. raft course movement.), gotta pick which group
                if type(graphicIntroOffsets) is not int and type(graphicIntroOffsets[0]) is list:
                    graphicIntroOffsets = graphicIntroOffsets[groupNum]

                # if it only has one layer, package as a list for now to avoid headaches in the for loops later
                if type(graphicIntroOffsets) is int:
                    graphicIntroOffsets = [graphicIntroOffsets]

                # writing palette data
                gbcFile.seek(paletteOffset)
                paletteLength = 0x20
                for i in range(paletteLength):
                    littleEndianHex = rgbToGbcBytes(hexCodes[i])
                    gbcFile.write(littleEndianHex)

                shortHeaderLength = 7
                # writing bigtile-subtiles, bigtile-palettes, and subtiles, for each layer in the sprite
                for layer in range(len(graphicIntroOffsets)):
                    gbcFile.seek(graphicIntroOffsets[layer] + shortHeaderLength)
                    for byte in spriteSubtiles[layer]:
                        gbcFile.write(byte.to_bytes())
                    for byte in spritePalettes[layer][1:]:  # skippa that 0 subtile
                        gbcFile.write(byte.to_bytes())
                    for j in range(8, len(subtileGraphics[layer])):  # skippin 0 subtubsubt
                        quaternary = subtileGraphics[layer][j]

                        bytes = quaternaryToBytes(quaternary)
                        left = bytes[0]
                        right = bytes[1]

                        gbcFile.write(int(left, 2).to_bytes(1, 'little'))
                        gbcFile.write(int(right, 2).to_bytes(1, 'little'))
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    print("No changes have been made.")
    return

def saveBigGraphicsData(hexCodes, lockFileName, lockedFileName, loadedSpriteType, loadedSportType, subtileGraphics,
                        spriteSubtiles, spritePalettes, loadedBearType, sprites, loadedMenuPagePalette, courseIntros,
                        LONG_GRAPHICS_OFFSETS, LONG_PALETTE_OFFSETS):
    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'r+b') as gbcFile:
                # easy offsets to find based on sprite
                graphicIntroOffsets = LONG_GRAPHICS_OFFSETS[loadedSpriteType-23]
                paletteOffset = LONG_PALETTE_OFFSETS[loadedSpriteType-23]

                # if menu items, only gonna save one of the pages
                if loadedSpriteType == sprites.variousMenuItems.value:
                    print(f"(saving page {loadedMenuPagePalette}'s palette)")
                    paletteOffset = paletteOffset[int(loadedMenuPagePalette-1)] # -1 to convert 12345 to 01234
                # if a course intro, figure out which
                elif loadedSpriteType == sprites.courseIntro.value: # one for each family sport, 2 for each
                    if loadedSportType == 0:
                        indexThingFor29 = courseIntros.toboggan.value
                    elif loadedSportType == 2:
                        indexThingFor29 = courseIntros.raft.value
                    else:
                        if loadedBearType == 0:
                            if loadedSportType == 1:
                                indexThingFor29 = courseIntros.broSled.value
                            elif loadedSportType == 3:
                                indexThingFor29 = courseIntros.broKayak.value
                            elif loadedSportType == 4:
                                indexThingFor29 = courseIntros.broBike.value
                            else:
                                indexThingFor29 = courseIntros.broDirtboard.value
                        else:
                            if loadedSportType == 1:
                                indexThingFor29 = courseIntros.sisSled.value
                            elif loadedSportType == 3:
                                indexThingFor29 = courseIntros.sisKayak.value
                            elif loadedSportType == 4:
                                indexThingFor29 = courseIntros.sisBike.value
                            else:
                                indexThingFor29 = courseIntros.sisDirtboard.value

                    graphicIntroOffsets = graphicIntroOffsets[indexThingFor29]
                    paletteOffset = paletteOffset[indexThingFor29]
                # if scoreboard, check if snowy or grassy
                elif loadedSpriteType == sprites.scoreboard.value:
                    if loadedSportType in (0, 1): #snowy scoreboard
                        paletteOffset = paletteOffset[1]
                    else:
                        paletteOffset = paletteOffset[0]
                # if podium, check if family bear or no
                elif loadedSpriteType == sprites.podiumFinish.value:
                    if loadedSportType in (0, 2):
                        graphicIntroOffsets = graphicIntroOffsets[2]
                        paletteOffset = paletteOffset[2]
                    else:
                        graphicIntroOffsets = graphicIntroOffsets[loadedBearType]
                        paletteOffset = paletteOffset[loadedBearType]

                # writing palette data
                gbcFile.seek(paletteOffset)
                paletteLength = 0x20
                for index in range(paletteLength):
                    littleEndianHex = rgbToGbcBytes(hexCodes[index])
                    gbcFile.write(littleEndianHex)

                # writing bigtile-subtiles, bigtile-palettes, and subtiles
                longHeaderLength = 10
                gbcFile.seek(graphicIntroOffsets + longHeaderLength)
                for byte in spriteSubtiles[0]:
                    gbcFile.write(byte.to_bytes())
                for byte in spritePalettes[0]:
                    gbcFile.write(byte.to_bytes())
                relativeSearch = 1
                gbcFile.seek(0x40, relativeSearch)
                for quaternaryByte in range(len(subtileGraphics[0])):
                    quaternary = subtileGraphics[0][quaternaryByte]

                    bytes = quaternaryToBytes(quaternary)
                    left = bytes[0]
                    right = bytes[1]

                    gbcFile.write(int(left, 2).to_bytes(1, 'little'))
                    gbcFile.write(int(right, 2).to_bytes(1, 'little'))
            print("Saved.")
            return
        except FileNotFoundError:
            print("bad file. get outta here! ...")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    print("No changes have been made.")
    return