#this code is a mess, but if you want collision pictures change this flag
collisions = True

NAMES = ["toboggan", "sled", "raft", "kayak", "bike", "dirtboard"]
DIFFICULTIES = ["beginner", "intermediate", "advanced"]
STARTING_OFFSETS = [0x5176, 0x91D7, 0xD0EB, 0x111B4, 0x152FB, 0x1943B]
GRAPHICS_LENGTHS = [0x1EA0, 0x1DC0, 0x1FA0, 0x1FD0, 0x1F70, 0x1900]
LEVEL_DESIGN_OFFSETS = [0x28000, 0x2C000, 0x30000, 0x34000, 0x38000, 0x3C000, 0x40000, 0x44000, 0x48000, 0x4C000,
                        0x50000, 0x54000, 0x58000, 0x5C000, 0x60000, 0x64000, 0x68000, 0x6C000]
COLLISION_OFFSETS = [0x4D6C, 0x8DCD, 0xCCE1, 0x10DAA, 0x14EF1, 0x19031]

with open("levels/modified levels/bears.gbc", "rb") as file:
    binary_data = file.read()
    for num in range(6):
        #"""
        #gonna be doing this for all level bigtiles: taking the offset start, then adding the lengths of each respective data portion (usually 0x400 or 0x40, though the subtile_data length varies)
        offset = STARTING_OFFSETS[num]
        data_len = GRAPHICS_LENGTHS[num]
        subtile_locations = binary_data[offset:offset + 0x400]
        palette_locations = binary_data[offset + 0x400:offset + 0x800]
        subtile_data = binary_data[offset + 0x800:offset + 0x800 + data_len]
        palette_data = binary_data[offset + 0x800 + data_len + 0xA:offset + 0x800 + data_len + 0xA + 0x40]

        # this is just to change a few palette things. a few red things need to be white or grey, so getting that out
        # of the way now
        for i in range(0, 8, 2):
            if palette_data[i:i+2] == b'\x1f\x00':
                palette_data = palette_data[:i] + b'\xff\x7f' + palette_data[i+2:]
            elif palette_data[i:i+2] == b'\x15\x00':
                palette_data = palette_data[:i] + b'\xef\x3d' + palette_data[i+2:]

        #gonna combine the subtile data bytes into "quaternary" data, aka just getting distinct nums for each colour
        #turn byte to binary, then the digits of the bin number into an integer. these are in pairs of 2, so the second
        # byte will be multiplied by 2 so the 2nd colour being "true" is different from the first colour being true.
        # then the two decimal numbers are added, and it leaves a "quaternary" representation of the pixels. finally,
        # turn to strings and zfill because that looks nicer
        quaternaries = []
        for byte_number in range(0, data_len, 2):
            num_1 = int(bin(subtile_data[byte_number])[2:])
            num_2 = int(bin(subtile_data[byte_number + 1])[2:])
            quaternaries.append(str(num_1 + num_2 * 2).zfill(8))
        ##print(quaternaries)
        #now gonna group these strings in pairs of 8, to represent each subtile's graphics data (will make working with
        # the bigtile_assembler hex data easy)
        subtile_quaternaries = []
        for i in range(0, data_len // 2, 8):
            subtile_quaternaries.append(quaternaries[i:i+8])
        ##print(subtile_quaternaries)
        ##print(len(subtile_quaternaries))

        #brief foray to convert the RGB in code to BMP compatible RGB stuff:
        #bears stores as GGGRRRRR XBBBBBGG
        #BMP stores as XRRRRRGG GGGBBBBB
        #so this just flips the RRRRR and BBBBB bits, and turns X to zero since it doesn't do anything
        #after that, convert back into bytes, since they're gonna be used when writing to the BMPs
        BMP_colours = []
        test = []
        for i in range(0, 0x40, 2):
            bin_bytes = bin(palette_data[i])[2:].zfill(8) + bin(palette_data[i+1])[2:].zfill(8)
            BMP_colours.append(int("0" + bin_bytes[3:8] + bin_bytes[14:16] + bin_bytes[0:3] + bin_bytes[9:14], 2).to_bytes(2, "little"))
        ##print(BMP_colours)
        # gonna group these 2-byte palleties in pairs of 4, to represent each palette (makes future stuff easier)
        palettes = []
        for i in range(0, 0x20, 4):
            palettes.append(BMP_colours[i:i + 4])
        ##print(palettes)


        # foray #2 to use palette_locations: both to assign palettes to bits (bits 2 1 and 0), and to check which
        # subtiles should be assigned in which places (bit 4)
        biglist = []
        ##print(subtile_locations)
        ##print(palette_locations)
        for i in range(0, 0x400):
            current_subtile = int(subtile_locations[i])
            # if the 4th bit is set, add 0x100 to the subtile location. this is because it's stored in the next video
            # RAM bank, as there are more than FF subtiles in use
            if palette_locations[i] & 0b00001000 != 0:
                ##print(bin(palette_locations[i]))
                current_subtile += 0x100
            ##print(i)

            palette = palette_locations[i] & 0b00000111
            ##print(current_subtile)
            current_quaternaries = subtile_quaternaries[current_subtile]
            ##print(palette_locations[i])
            ##print(palette)

            #checks if the subtile data should be hz flipped
            if palette_locations[i] & 0b00100000 != 0:
                current_quaternaries = [line[::-1] for line in current_quaternaries]
                ##print("hz")

            # checks if the subtile data should be vt flipped
            if palette_locations[i] & 0b01000000 != 0:
                current_quaternaries = current_quaternaries[::-1]
                ##print("vt")
            ##print("-----")
            temporary_quaternary_into_byte_storage = []
            for line in current_quaternaries:
                temp_bytestring = b''
                for bit in line:
                    temp_bytestring += palettes[palette][int(bit)]
                temporary_quaternary_into_byte_storage.append(temp_bytestring)

            biglist.append(temporary_quaternary_into_byte_storage)

        chow = []
        #print(len(biglist))
        for i in range(0, 0x10):
            for j in range(0, 0x20, 2):
                for k in range(7, -1, -1):
                    chow.append(biglist[j+0x20+0x40*i][k] + biglist[j+0x21+0x40*i][k])
                for k in range(7, -1, -1):
                    chow.append(biglist[j+0+0x40*i][k] + biglist[j+1+0x40*i][k])

        chow2 = []
        for i in range(0, 4096, 16):
            chow2.append(chow[i:i+16])

        #print(chow2)
        #print(len(chow2))
        #weg
        #"""

        """
                # writing each bigtile
        for i in range(0x100):
            with open(f"a_new{NAMES[num]}/tile{i}.bmp", "wb") as bmp:
                bmp.write(b'BM\x35\x02\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(chow[0+i*16:16+i*16]))
        """

        ## this code makes the big pictures
        #"""
        #not sure if this does anything useful
        chow = []
        print(len(biglist))
        for i in range(0, 0x10):
            for j in range(0, 0x20, 2):
                for k in range(7, -1, -1):
                    chow.append(biglist[j + 0x20 + 0x40 * i][k] + biglist[j + 0x21 + 0x40 * i][k])
                for k in range(7, -1, -1):
                    chow.append(biglist[j + 0 + 0x40 * i][k] + biglist[j + 1 + 0x40 * i][k])
        #print(chow)
        #print(len(chow))
        #"""

        ####"""
        mm = ""
        if collisions == True:
            mm = "collision_"
            # chow2 is a list of mini lists, each of which contain a bunch of bytestrings of length 16, each corr to the hz
            # layers of a bigtile
            # so each mini list corresponds to a biglist, and there are 255 of them in chow2
            # ok now i just gotta redo allat, but for collisions

            conversion_dictionary = {0x00: b'v\x7f',
            0x02: b'\x8c1',
            0x03: b'CC',
            0x08: b'\x1b[',
            0x0C: b'\x94~',
            0x11: b's5',
            0x21: b'\xb4B',
            0x31: b'\xe1@',
            0x32: b'\x94\x19',
            0x33: b'\x00~',
            0x42: b'\x0e<',
            0x73: b'\x0c\x0e',
            0x82: b'At',
            0xB3: b'"\x11',
            0xC0: b'\xc1V'}


            #trying to adapt this to making a map, instead of individual tiles
            collision_data = binary_data[COLLISION_OFFSETS[num]:COLLISION_OFFSETS[num] + 0x400]
            #print(collision_data)
            chow2 = []
            for i in range(0x100):
                chow2.append([conversion_dictionary[collision_data[0x02 + i*0x04]] * 8
                              + conversion_dictionary[collision_data[0x03 + i*0x04]] * 8] * 8
                             + [conversion_dictionary[collision_data[0x00 + i*0x04]] * 8
                              + conversion_dictionary[collision_data[0x01 + i*0x04]] * 8] * 8)
            #print(chow2)
            #print(len(chow2))
            #okjihuoyiuy
        ####"""
        #amwofa
        ###print(conversion_dictionary[collision_data[0x20 + j + i*0x40]]*8)
        ###print(conversion_dictionary[collision_data[0x21 + j + i*0x40]]*8)
        ###print(collision_data)

        for difficulty in range(3):
            curr_level_offset = LEVEL_DESIGN_OFFSETS[num*3+difficulty]
            height_bytes = int.from_bytes(binary_data[curr_level_offset+2:curr_level_offset+4], "little")
            zwawawow = []
            ####temporary_bytestring = b''
            ##print(height_bytes)
            guaug = []
            ###print(height_bytes)
            for i in range(height_bytes):
                temporary_bytestring = b''
                ####print(i)
                tempy = []
                for j in range(0x10):
                    tempy.append(binary_data[curr_level_offset + 4 + i*0x10 + j])
                ##print(tempy)
                for k in range(16):
                    for bigtile in tempy:
                        #print(bigtile, k)
                        #print(len(chow2))
                        temporary_bytestring += chow2[bigtile][k]
                guaug.append(temporary_bytestring)
                ##print(temporary_bytestring)
                ##ssef

            ##print(guaug)
            #zwawawow.append(tempy)
            ##print(zwawawow)
            ##print(height_bytes)
                with open(f"atesting/{mm}{NAMES[num]}_{DIFFICULTIES[difficulty]}.bmp", "wb") as bmp:
                    bmp.write(
                    b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\x00\x01\x00\x00' + (height_bytes*16).
                    to_bytes(4, "little") + b'\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b''.join(guaug[::-1]))


"""
        #now gonna use this data to convert the quaternary strings into lots of byte data, which can be put in a bmp
        huge_bmp_data_list = []
        for subtile_minilist in subtile_quaternaties:
            for quaternary in subtile_minilist:
                for bit in quaternary:
"""