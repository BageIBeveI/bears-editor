import glob
import os
from PIL import Image

def bmpPrintrer22up(bigtile, layaer, courseBigtilesSelected, spriteWidth, spriteHeight, spritePalettes, hexCodes, spriteSubtiles, subtileGraphics, bigtileCollisions, COLLISION_COLOUR_MAPPER, colours, ):
    guaug = []
    # who names an array guaug?
    # i think i was going mad when crunching these out
    # forget this, i'm gonna focus on the save/load mess first
    for j in (range(spriteHeight[layaer])[::-1]):  # first j will add the bottom subtiles to guaug, second j will add the top ones
        ox400er = 0
        if courseBigtilesSelected:
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
    if courseBigtilesSelected:
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
            # WHAT DO YOU MEAN THERE'S NO i IN HERE??? WHAT WHO ARE YOU MYSTERY VAR????
            # now i see the error of my ways
        with open(f"tiles/efftemptiles/tile{str(i).zfill(3)}.bmp", "wb") as bmp:
            bmp.write(b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + (8 * spriteWidth[layaer]).to_bytes(4, "little") + (8 * spriteHeight[layaer]).to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + gorg)

def bmpPrintrerSprite(frame, numberOLayers, spriteHeight, spriteWidth, spritePalettes, spriteSubtiles, hexCodes, subtileGraphics):
    guaug = []
    maxWidth = max(spriteWidth)
    dummyColour = b'\xFA\x69'
    for j in (range(spriteHeight[0])[::-1]):  # first j will add the bottom subtiles to guaug, second j will add the top ones
        palettecode = []
        graphicsies = []
        palettes = []
        for layaer in range(numberOLayers):
            ox400er = frame * spriteWidth[layaer] * spriteWidth[layaer] + j * spriteWidth[layaer]
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