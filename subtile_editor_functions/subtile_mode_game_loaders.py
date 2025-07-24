### HELPERS
def rgbToGbcBytes(hexCodes, paletteData):
    paletteLength = 0x40
    for i in range(0, paletteLength, 2):  # groups of 2 bytes
        # turning GGGRRRRR 0BBBBBGG to normal (rounded to most significant)
        R = (paletteData[i] & 0b00011111) << 3
        G = ((paletteData[i] & 0b11100000) >> 2) + ((paletteData[i + 1] & 0b00000011) << 6)
        B = (paletteData[i + 1] & 0b01111100) << 1
        hexCodes.append([int(R), int(G), int(B)])
        # hmmmmm the colour conversion doesn't work perfectly, maybe there's something im missing, but it works well enough
    return

### ----------

# loading in subtiles as images, for subtile mode
def loadCourseBigtileData(lockFileName, lockedFileName, sportType,
                          SUBTILE_GRAPHICS_LENGTHS, SUBTILE_GRAPHICS_OFFSETS, BIGTILE_COLLISION_OFFSETS):
    returnVals = []
    bigtileCollisions = []
    spriteSubtiles = []
    spritePalettes = []
    subtileGraphics = []
    hexCodes = []

    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (leave blank to abort): ")
        while name.upper() == "E":
            if input("are you sure? (E again if yes): ").upper() == "E":
                bigtileCollisions = [0] * 0x400
                spriteSubtiles = [0] * 0x400
                spritePalettes = [[0] * 0x400]
                subtileGraphics = [["00000000"] * (SUBTILE_GRAPHICS_LENGTHS[sportType]//2)]
                hexCodes = [[0, 0, 0]] * 0x20
                returnVals = [1, bigtileCollisions, spriteSubtiles, spritePalettes, subtileGraphics, hexCodes]
                return returnVals
            name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (say E for empty subtiles) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as gbcFile:
                frameCount = 256
                # bigtileGraphicsOffsets = COLLISION_OFFSETS plus 0x40A
                # bigtilePaletteOffsets = COLLISION_OFFSETS plus 0x80A
                # subtileColoursOffsets = above two added, plus 0xA
                gbcFileBytes = gbcFile.read()

                # getting palettes
                extraOffsets = [[0x4A98, 0, 0, 0x4AA5], [0x8AB0, 0, 0, 0x8ABD], [0, 0, 0xCA3C, 0xCA45],
                                [0, 0, 0x10A75, 0x10A7E], [0, 0, 0x14B62, 0x14B6B], [0, 0, 0x18B7B, 0x18B84]]
                paletteOffset = SUBTILE_GRAPHICS_OFFSETS[sportType] + SUBTILE_GRAPHICS_LENGTHS[sportType] + 0xA
                paletteData = b''
                firstColourLength = 8
                paletteLength = 0x40
                for i in range(0, firstColourLength, 2): # 2 bytes per colour, 4 colours. using the quaternary thing
                    if extraOffsets[sportType][i//2] == 0:
                        paletteData += gbcFileBytes[paletteOffset + (i):paletteOffset + (i) + 2]
                    else:
                        paletteData += gbcFileBytes[(extraOffsets[sportType][i//2]):(extraOffsets[sportType][i//2]) + 2]
                paletteData += gbcFileBytes[paletteOffset+firstColourLength:paletteOffset+paletteLength]  # 0x40 bytes in a 7 colour palette

                # getting colours from palette
                rgbToGbcBytes(hexCodes, paletteData)

                # getting subtile graphics
                subtileGraphics = []
                subtileyOffset = SUBTILE_GRAPHICS_OFFSETS[sportType]
                length = SUBTILE_GRAPHICS_LENGTHS[sportType]
                subtileData = gbcFileBytes[subtileyOffset:subtileyOffset + length]
                for i in range(0, length, 2):
                    # making a quaternary kinda byte here: 00=0, 10=1, 01=2, 11=3
                    byteish1 = int(bin(subtileData[i])[2:])
                    byteish2 = int(bin(subtileData[i + 1])[2:]) * 2
                    quaternary = str(byteish1 + byteish2).zfill(8)
                    subtileGraphics.append(quaternary)
                subtileGraphics = [subtileGraphics]
                # others have layers, and i don't want 1000000 branches so w/e makin this a list in a list
                # so every loop is nicer

                # getting collisions, bigtile-subtiles and bigtile-palettes
                bigtileCollisions = [numby for numby in gbcFileBytes[BIGTILE_COLLISION_OFFSETS[sportType]: BIGTILE_COLLISION_OFFSETS[sportType] + frameCount*4]]
                spriteSubtiles = [[numby for numby in gbcFileBytes[BIGTILE_COLLISION_OFFSETS[sportType] + 0x40A:BIGTILE_COLLISION_OFFSETS[sportType] + 0x40A + frameCount*4]]]
                spritePalettes = [[numby for numby in gbcFileBytes[BIGTILE_COLLISION_OFFSETS[sportType] + 0x80A:BIGTILE_COLLISION_OFFSETS[sportType] + 0x80A + frameCount*4]]]

                returnVals = [1, bigtileCollisions, spriteSubtiles, spritePalettes, subtileGraphics, hexCodes]

            print("Loaded.")
            return returnVals
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    print("No changes have been made.")
    return [0]

# other things have different sizes and a cool lil 7 byte header (GRAPHICINTRO in the spreadsheet)
def loadSmallGraphicsData(lockFileName, lockedFileName, sportType, spriteType, bearType, sprites,
                          FAMILYBEAR_SPRITE_OFFSETS, FAMILY_OBJ_PALETTE_OFFSETS, BROBEAR_SPRITE_OFFSETS,
                          BRO_OBJ_PALETTE_OFFSETS, SISBEAR_SPRITE_OFFSETS, SIS_OBJ_PALETTE_OFFSETS,
                          MORE_SPRITEISH_OFFSETS, MORE_PALETTEY_OFFSETS):

    # subdividing small sprites
    bearSprites = range(0, 17)
    hudSprites = (sprites.hudSports.value, sprites.hudDifficulties.value)

    # returny stuff
    returnVals = []

    spriteSubtiles = []
    spritePalettes = []
    subtileGraphics = []
    hexCodes = []
    spriteWidth = []
    spriteHeight = []

    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as gbcFile:
                frameCount = 0
                groupNum = 0
                layers = 0

                gbcFileBytes = gbcFile.read()

                # loading offsets based on sprite type
                if spriteType in bearSprites:
                    if sportType == 0 or sportType == 2:
                        offsets = FAMILYBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paletteOffset = FAMILY_OBJ_PALETTE_OFFSETS[sportType]
                    elif bearType == 0:
                        offsets = BROBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paletteOffset = BRO_OBJ_PALETTE_OFFSETS[sportType]
                    else:
                        offsets = SISBEAR_SPRITE_OFFSETS[sportType][spriteType]
                        paletteOffset = SIS_OBJ_PALETTE_OFFSETS[sportType]
                # other small sprites that aren't bears exist
                else:
                    offsets = MORE_SPRITEISH_OFFSETS[spriteType-17]
                    if spriteType in hudSprites:
                        if sportType in (0, 2):
                            paletteOffset = FAMILY_OBJ_PALETTE_OFFSETS[sportType]
                        elif bearType == 0:
                            paletteOffset = BRO_OBJ_PALETTE_OFFSETS[sportType]
                        else:
                            paletteOffset = SIS_OBJ_PALETTE_OFFSETS[sportType]
                    else:
                        paletteOffset = MORE_PALETTEY_OFFSETS[spriteType-17]
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

                shortHeaderLength = 7
                if type(offsets) is not tuple and type(offsets) is not list:
                    offsets = [offsets]
                for i, offset in enumerate(offsets):
                    graphicIntro = gbcFileBytes[offset:offset + shortHeaderLength]
                    frameCount = graphicIntro[0]
                    spriteWidth.append(graphicIntro[1])  # unfortunately these have to be lists because sometimes layers ahve different W and L, e.g. toboggan jump's shadow is 4x4
                    spriteHeight.append(graphicIntro[2])
                    paletteDataOffset = int.from_bytes(graphicIntro[3:5], "little") + offset
                    subtileGraphicDataOffset = int.from_bytes(graphicIntro[5:7], "little") + offset #todo standardize some of these variable names, and also maybe stop rewriting the same code so many times over? it works but i feel like it's bad practice and idk

                    spriteSubtiles.append([inty for inty in gbcFileBytes[offset + shortHeaderLength:paletteDataOffset]])

                    spritePalettes.append([0] + [inty for inty in gbcFileBytes[paletteDataOffset:subtileGraphicDataOffset]])  # ughh the colours are connected to subtiles now, i wish these two graphic types weren't so different lol. anyways the [0] is for the elusive 0 subtile, which isn't in memory because it's always fully transparent

                    tempLengthThing = (subtileGraphicDataOffset - paletteDataOffset) * 0x10

                    # gettin graphics
                    subtileGraphicData = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + gbcFileBytes[subtileGraphicDataOffset:subtileGraphicDataOffset + tempLengthThing]
                    tempSubtileGraphics = []
                    for i in range(0, tempLengthThing + 0x10, 2):
                        tempSubtileGraphics.append(str(int(bin(subtileGraphicData[i])[2:]) + int(bin(subtileGraphicData[i + 1])[2:]) * 2).zfill(8))
                        # either mult i by 2 or i+1 by 2 (with binary as integers)
                    subtileGraphics.append(tempSubtileGraphics)

                    paletteData = gbcFileBytes[paletteOffset:paletteOffset + 0x40]

                    # writing to hexcodes
                    hexCodes.clear()
                    rgbToGbcBytes(hexCodes, paletteData)

                returnVals = [1, frameCount, groupNum, layers, spriteSubtiles, spritePalettes, subtileGraphics,
                              hexCodes, spriteHeight, spriteWidth]

            return returnVals
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    return [0]

#and others still have a 10 byte LONGGRAPHICINTRO
def loadBigGraphicsData(lockFileName, lockedFileName, sportType, bearType, sprites, courseIntros,
                        spriteType, LONG_GRAPHICS_OFFSETS, LONG_PALETTE_OFFSETS, LONG_GRAPHICS_LENGTHS):

    returnVals = []
    spriteSubtiles = []
    spritePalettes = []
    subtileGraphics = []
    spriteWidth = []
    spriteHeight = []
    hexCodes = []

    if lockFileName:
        name = lockedFileName
    else:
        name = input("enter the name of the bears file (in levels/modified_levels/) here (.gbc file format assumed, so don't type it) (leave blank to abort): ")
    if name != "":
        try:
            with open(f"levels/modified_levels/{name}.gbc", 'rb') as gbcFile:
                # big refresher for variables. some are updated later while others are good to start how they are now

                loadedMenuPagePalette = -1

                # the others shadow global vars which will need to be updated elsewhere

                gbcFileBytes = gbcFile.read()

                # storing offsets
                # -23 because this function covers types 23 onwards, so index 0 of the array corresponds to 23, etc.
                offset = LONG_GRAPHICS_OFFSETS[spriteType - 23]
                paletteOffset = LONG_PALETTE_OFFSETS[spriteType - 23]
                tempLengthThing = LONG_GRAPHICS_LENGTHS[spriteType - 23]

                # if menu items, only gonna load one of the pages
                if spriteType == sprites.variousMenuItems.value:
                    temp26 = input("Which screen's palette do you want to load (all 5 screens' graphics will still be loaded, but only your chosen palette will be loaded): ")
                    while not temp26.isnumeric() or int(temp26) > 5 or int(temp26) < 1:
                        print("Invalid input.")
                        temp26 = input("Which screen's palette do you want to load (all 5 screens' graphics will still be loaded, but only your chosen palette will be loaded): ")
                    loadedMenuPagePalette = int(temp26)
                    paletteOffset = paletteOffset[int(temp26)-1]
                # if a course intro, figure out which
                elif spriteType == sprites.courseIntro.value: # one for each family sport, 2 for each
                    if sportType == 0:
                        indexThingFor29 = courseIntros.toboggan.value
                    elif sportType == 2:
                        indexThingFor29 = courseIntros.raft.value
                    else:
                        if bearType == 0:
                            if sportType == 1:
                                indexThingFor29 = courseIntros.broSled.value
                            elif sportType == 3:
                                indexThingFor29 = courseIntros.broKayak.value
                            elif sportType == 4:
                                indexThingFor29 = courseIntros.broBike.value
                            else:
                                indexThingFor29 = courseIntros.broDirtboard.value
                        else:
                            if sportType == 1:
                                indexThingFor29 = courseIntros.sisSled.value
                            elif sportType == 3:
                                indexThingFor29 = courseIntros.sisKayak.value
                            elif sportType == 4:
                                indexThingFor29 = courseIntros.sisBike.value
                            else:
                                indexThingFor29 = courseIntros.sisDirtboard.value

                    offset = offset[indexThingFor29]
                    paletteOffset = paletteOffset[indexThingFor29]
                    tempLengthThing = tempLengthThing[indexThingFor29]
                # if scoreboard, check if snowy or grassy
                elif spriteType == sprites.scoreboard.value:
                    if sportType in (0, 1): #snowy scoreboard
                        paletteOffset = paletteOffset[1]
                    else:
                        paletteOffset = paletteOffset[0]
                # if podium, check if family bear or no
                elif spriteType == sprites.podiumFinish.value:
                    if sportType in (0, 2):
                        offset = offset[2]
                        paletteOffset = paletteOffset[2]
                        tempLengthThing = tempLengthThing[2]
                    else:
                        offset = offset[bearType]
                        paletteOffset = paletteOffset[bearType]
                        tempLengthThing = tempLengthThing[bearType]

                # getting offsets and header data
                longHeaderLength = 10
                chunkSize = 0x4000
                graphicIntro = gbcFileBytes[offset:offset + longHeaderLength]
                spriteWidth.append(graphicIntro[0])  # unfortunately these have to be lists because sometimes layers ahve different W and L, e.g. toboggan jump's shadow is 4x4
                spriteHeight.append(graphicIntro[1])
                chunkAdderThingy = (offset//chunkSize)*chunkSize
                paletteLocationOffset = int.from_bytes(graphicIntro[2:4], "little")%chunkSize + chunkAdderThingy
                #graphicLocationOffset = int.from_bytes(graphicIntro[4:6], "little")^0x4000 + chunkAdderThingy is just offset + 10
                graphicMakerOffset = int.from_bytes(graphicIntro[6:8], "little")%chunkSize + chunkAdderThingy
                paletteMakerOffset = int.from_bytes(graphicIntro[8:10], "little")%chunkSize + chunkAdderThingy

                spriteSubtiles.append([inty for inty in gbcFileBytes[offset + longHeaderLength:paletteLocationOffset]])
                spritePalettes.append([inty for inty in gbcFileBytes[paletteLocationOffset:paletteMakerOffset]])

                # and palettes
                paletteLength = 0x40
                paletteData = gbcFileBytes[paletteOffset:paletteOffset+paletteLength]
                # storing in hexcodes
                hexCodes.clear()
                rgbToGbcBytes(hexCodes, paletteData)

                # subtile pixels
                subtileGraphicData = gbcFileBytes[graphicMakerOffset:graphicMakerOffset+tempLengthThing]
                tempSubtileGraphics = []
                for i in range(0, tempLengthThing, 2):
                    tempSubtileGraphics.append(str(int(bin(subtileGraphicData[i])[2:]) + int(bin(subtileGraphicData[i + 1])[2:]) * 2).zfill(8))
                    # either mult i by 2 or i+1 by 2 (with binary as integers)
                subtileGraphics.append(tempSubtileGraphics)
                
                #todo: die
                #now i gotta return a bunch of stuff s.t. i can change vars in the main loop
                #laziest way is with an array, but maybe an enum could make it a lil nicer
                #need to pass enums in ig? i miss my global vars... this should make things cleaner though i hope
                returnVals = [1, loadedMenuPagePalette, spriteSubtiles, spritePalettes, subtileGraphics,
                              hexCodes, spriteHeight, spriteWidth]
                # arrays like hexCodes don't need to be passed back

            return returnVals
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("permission error!")
        except Exception:
            print("error!")
    return [0]