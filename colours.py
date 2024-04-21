# 32 hex codes as strings -> 8 bears palettes out (little endian BRG-15 data)
# remember that for some things (e.g. bigtiles), palette 0 isn't for bigtiles (it's for the HUD)

bstring = b''

"""colours = "000000 E63321 8C8C8C 3F48CC " \
          "000000 A349A4 8C8C8C 67DFAC " \
          "000000 FFF200 8C8C8C 71F24B " \
          "000000 FF5900 8C8C8C 3F48CC " \
          "000000 FF5900 8C8C8C FFFFFF " \
          "000000 E63321-1" \
          "-1 8C8C8C FFFFFF " \
          "000000 A349A4 8C8C8C FFFFFF ".split()"""
        #"383838 472F22 B97A57 C3C3C3 " \
# = input("Enter some hex codes, separated by spaces: ").split()
colours = ["FFDBB6", "666666", "81D41A", "B4C7DC", "FFA6A6", "6B5E9B", "81ACA6", "813709", "3465A4", "FF8000", "780373", "158466", "F10D0C", "224B12", "ACB20C"]
for colour in colours:
    hexcode = colour
    red = int(hexcode[0:2], 16)
    green = int(hexcode[2:4], 16)
    blue = int(hexcode[4:6], 16)

    newred = round((31/255) * red)
    newgreen = round((31/255) * green)
    newblue = round((31/255) * blue)

    newred = bin(newred)[2:].zfill(5)
    newgreen = bin(newgreen)[2:].zfill(5)
    newblue = bin(newblue)[2:].zfill(5)

    #this is how bears does it (GGGRRRRR XBBBBBGG)
    GRBG = (newgreen[2:] + newred + "0" + newblue + newgreen[:2])
    #print(GRBG)

    #this is how bmp does it (XRRRRRGG GGGBBBBB) (i think?)
    GBRG = (newgreen[2:] + newblue + "0" + newred + newgreen[:2])

        #the bmp stuff was just for me to find what the effects tiles' colours should be, prob not useful for bears editing
        #print(GBRG[0] + ' ' + GBRG[1], end=" ")
    print(hex(int(GBRG,2))[2:].upper().zfill(4))
    bstring += int(GBRG, 2).to_bytes(2, "big")

print(bstring, [b for b in bstring])
for i in range(0, 30, 2):
    print(bstring[i:i+2])