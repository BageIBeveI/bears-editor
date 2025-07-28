import glob
import os
from PIL import Image

### HELPERS
def rgbToBmpBytes(RGB): # [R,G,B] 0-255
    # bmp uses 5-5-5 bytes, so each colour uses 5 most significant bytes (may wanna round instead?)
    R = bin(RGB[0] >> 3)[2:].zfill(5)
    G = bin(RGB[1] >> 3)[2:].zfill(5)
    B = bin(RGB[2] >> 3)[2:].zfill(5)
    # next is a lil different from savers' gbc code, as BMP uses GGGBBBBB XRRRRRGG
    temp = "0" + R + G + B
    littleEndianHex = int(temp, 2).to_bytes(2, "little")
    return littleEndianHex

### ----------

def bmpPrintNonSmallSprites(bigtile, courseBigtilesSelected, spriteWidth, spriteHeight, spritePalettes,
                            hexCodes, spriteSubtiles, subtileGraphics, bigtileCollisions, COLLISION_COLOUR_MAPPER,
                            colours):
    bmpImageBytes = []
    subtileByteHeight = 8  # my name is subtile i am 8 bytes tall
    paletteSize = 4  # my name palette i am 4 colours tall
    pixelsInSubtile = 8 # my name is subtile i am 8x8 pixels

    layer = 0

    # subtileRow loops from bottom subtiles of bigtile to the top (bmp uses cartesian Q1 coords so this is nicer)
    for subtileRow in (range(spriteHeight[layer])[::-1]):

        # where are the bigtile's four subtiles stored? course ones are a lil weird (unless treated like one full image but that's less useful)
        bigtileSubtileRowOffset0x400 = 0
        if courseBigtilesSelected:
            # 0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 13 13 14 14 15 15
            # 0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 13 13 14 14 15 15
            # 16 16 17 17 18 18 19 19 ...
            # tiles are stored like this in memory, so for instance 0's top left is the first thing, but its bottom
            # left is under it, which is 32 = 0x20 tiles in the future which is where subtileRow comes in (skip by row)
            # the mod part chooses the left part of a sprite row
            # the floor part skips to the right chunk of 0x40 data
            bigtileSubtileRowOffset0x400 = (bigtile % 0x10) * spriteWidth[0] + (bigtile // 0x10) * 0x40 + (subtileRow) * 0x20  # weirdo address calculator because it's stored all messily
        else:
            # other big stuff is just well behaved and so no overcomplicated indexer.
            # only one 'bigtile', so just use width to find where each row starts
            # if there were more bigtiles then could just revert to doing 'bigtile * w * h + that stuff' again
            bigtileSubtileRowOffset0x400 = subtileRow * (spriteWidth[0])

        fullPalettes = spritePalettes[layer][bigtileSubtileRowOffset0x400:bigtileSubtileRowOffset0x400 + spriteWidth[layer]]  # palette data for each subtile in row
        palettes = [pal & 7 for pal in fullPalettes]  # and 7 to get the palette number (stored in bits 0 1 and 2)

        paletteCode = []
        graphicsCode = []
        # for each subtile in a row
        for subtileHorizontalIndex in range(spriteWidth[layer]):
            # converting hex code palette data into bitmap file palette data for ease of use later
            for colourIndex in range(paletteSize):
                RGB = hexCodes[palettes[subtileHorizontalIndex] * 4 + colourIndex]
                colourBytes = rgbToBmpBytes(RGB)
                paletteCode.append(colourBytes)
            # if bit 0x8 on, add 0x100 to the subtile num
            bankSwap = (fullPalettes[subtileHorizontalIndex] & 0x8) != 0
            subtile = spriteSubtiles[layer][bigtileSubtileRowOffset0x400 + subtileHorizontalIndex] + bankSwap * 0x100
            # stores quaternary row graphics, so need to get the 8 starting at s*8
            graphicsCode.append(subtileGraphics[layer][subtile * 8:subtile * 8 + 8][::-1])

        # for each subtile in a row (again ... for flips)
        for subtileHorizontalIndex in range(spriteWidth[layer]):
            if spritePalettes[layer][bigtileSubtileRowOffset0x400 + subtileHorizontalIndex] & 0x40:  # vt flip
                graphicsCode[subtileHorizontalIndex] = graphicsCode[subtileHorizontalIndex][::-1]
            if spritePalettes[layer][bigtileSubtileRowOffset0x400 + subtileHorizontalIndex] & 0x20:  # hz flip
                for l in range(subtileByteHeight):
                    graphicsCode[subtileHorizontalIndex][l] = graphicsCode[subtileHorizontalIndex][l][::-1]

        # append the bottom row (byte) of each subtile, then the next row, etc
        for byteNum in range(subtileByteHeight):
            # for each subtile (left to right)
            for subtileHorizontalIndex in range(spriteWidth[layer]):
                # for bit in byte
                # graphicsies[0] has 8 bytes in its list (contains the left subtile's data.) ([1] has 8 bytes for the right subtile)
                for bit in graphicsCode[subtileHorizontalIndex][byteNum]:
                    # draw correct colour per 2 pixels
                    bmpImageBytes.append(paletteCode[int(bit) + 4 * subtileHorizontalIndex])  # would += to a b'' but that takes super long

    with open(f"tiles/temptiles/tile{str(bigtile).zfill(3)}.bmp", "wb") as bmp:
        bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' +
                  (8 * spriteWidth[layer]).to_bytes(4, "little") + (8 * spriteHeight[layer]).to_bytes(4, "little") +
                  b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(bmpImageBytes))
    ######
    ###### now collisions
    if courseBigtilesSelected:
        bmpImageBytes = []
        # first j will add the bottom subtiles to bmpImageBytes, second j will add the top ones
        # (no idea why it needs to be 0 1, it just doesn't work as 1, 0 though my logic sayc it should wasawawawa)
        for subtileRow in (range(spriteHeight[layer])[::-1]): #range(spriteHeight[layer])[::-1] again, but less general
            bigtileSubtileRowOffset0x400 = bigtile * 4 + subtileRow * 2  # looks cleaner this time, since this only works for course bigtiles
            C = bigtileCollisions[bigtileSubtileRowOffset0x400:bigtileSubtileRowOffset0x400 + spriteWidth[layer]]

            tempBytes = []
            for k in range(spriteWidth[layer]):
                for index, key in enumerate(COLLISION_COLOUR_MAPPER):
                    if key == C[k]:
                        RGB = colours[index]
                        break
                raar = rgbToBmpBytes(RGB)
                tempBytes.append(raar * pixelsInSubtile)
            bmpImageBytes.append((b''.join(tempBytes)) * pixelsInSubtile)

        with open(f"tiles/efftemptiles/tile{str(bigtile).zfill(3)}.bmp", "wb") as bmp:
            bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' +
                      (8 * spriteWidth[layer]).to_bytes(4, "little") + (8 * spriteHeight[layer]).to_bytes(4, "little")
                      + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(bmpImageBytes))

def bmpPrintSmallSprites(frame, numberOLayers, spriteHeight, spriteWidth, spritePalettes, spriteSubtiles, hexCodes,
                         subtileGraphics):
    bmpImageBytes = []
    subtileByteHeight = 8  # my name is subtile i am 8 bytes (8 pixels tall)
    paletteSize = 4  # my name palette i am 4 colours tall
    subtilePixelWidth = 8 # my name is subtile i am 8 pixels wide
    byteSize = 8 # name byte 8 bit
    maxWidth = max(spriteWidth)
    dummyColour = b'\xFA\x69'\

    # first will add the bottom subtile row to bmpImageBytes, second will add the ones above, etc
    # can do layer 0 because the only width/height discrepancy comes from shadows, which are smaller than other layers
    for subtileRow in (range(spriteHeight[0])[::-1]):
        graphicsCode = []
        paletteCode = []
        palettes = []
        for layer in range(numberOLayers):
            bigtileSubtileRowOffset0x400 = (frame * spriteWidth[layer] * spriteHeight[layer]) + (subtileRow * spriteWidth[layer])
            palettes.append([spritePalettes[layer][subtileNumbah] for subtileNumbah in spriteSubtiles[layer][bigtileSubtileRowOffset0x400:bigtileSubtileRowOffset0x400 + spriteWidth[layer]]])  # not using P since these tend not to use the extra bits in palette stuff

            tempGraphicsies = []
            tempPaletteCode = []
            for column in range(spriteWidth[layer]):
                for colour in range(paletteSize):  # converting hex code palette data into bitmap file palette data
                    RGB = hexCodes[palettes[layer][column] * paletteSize + colour]
                    colourBytes = rgbToBmpBytes(RGB)
                    tempPaletteCode.append(colourBytes)

                subtile = spriteSubtiles[layer][bigtileSubtileRowOffset0x400 + column]
                # * height because each subtile is 8 quaternaries long
                tempGraphicsies.append(subtileGraphics[layer][subtile * subtileByteHeight:(subtile + 1) * subtileByteHeight][::-1])  # stores quaternary row graphics, so need to get the 8 starting at s*8
            # array filled with dummy colours for every pixel
            superBigPixelRowArray = [dummyColour] * (subtileByteHeight * maxWidth * subtilePixelWidth)
            paletteCode.append(tempPaletteCode)
            graphicsCode.append(tempGraphicsies)

        # for every pixel if the len * wid image, check layers from 0 up to see if there should be any colour there or no
        # 0 is the empty colour most of the time, so it gets ignored or is dummy colour when not eyemode
        for subtileVt in range(subtileByteHeight):
            for subtileHrz in range(maxWidth):
                for bitNum in range(byteSize):
                    for layer in range(numberOLayers):
                        quaternaryBit = graphicsCode[layer][subtileHrz][subtileVt][bitNum]
                        pixelsInARow = (maxWidth * subtilePixelWidth)
                        pixelColumn = subtileHrz * subtilePixelWidth
                        pixelIndex = subtileVt * pixelsInARow + pixelColumn + bitNum
                        if quaternaryBit != "0" and superBigPixelRowArray[pixelIndex] == dummyColour:
                            superBigPixelRowArray[pixelIndex] = paletteCode[layer][int(quaternaryBit) + (paletteSize * subtileHrz)]
                            # can break because after placing a colour, no lower layer can overwrite it, so saves a lil time
                            break
                # for bit in graphicsies[l][k]:  # graphicsies[0] has 8 bytes in its list (contains the left subtile's data.) ([1] has 8 bytes for the right subtile)

        bmpImageBytes.append(b''.join(superBigPixelRowArray))  # would += to a b'' but that takes super long
    with open(f"tiles/temptiles/tile{str(frame).zfill(3)}.bmp", "wb") as bmp:
        bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' +
                  (subtilePixelWidth * spriteWidth[0]).to_bytes(4, "little") +
                  (subtileByteHeight * spriteHeight[0]).to_bytes(4, "little") +
                  b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(bmpImageBytes))

# makes printed tiles from bmp into png
def pngify(name, frameCount, courseBigtilesSelected):
    if not os.path.exists(f"tiles/{name}"):
        os.makedirs(f"tiles/{name}")
    count = 0
    for bitmap in glob.glob(f"tiles/temptiles/*.bmp"):
        Image.open(bitmap).save(f"tiles/{name}/tile{count}.png")
        count += 1
        if count >= frameCount:
            break

    if courseBigtilesSelected: ##loadedSpriteType == sprites.courseBigtile.value:
        if not os.path.exists(f"tiles/{name}_effects"):
            os.makedirs(f"tiles/{name}_effects")
        count = 0
        for bitmap in glob.glob(f"tiles/efftemptiles/*.bmp"):
            Image.open(bitmap).save(f"tiles/{name}_effects/tile{count}.png")
            count += 1
            if count >= frameCount:
                break