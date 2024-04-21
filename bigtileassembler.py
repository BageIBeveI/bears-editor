sport_to_bigtilestructure_offset = {
    0: 0x5176,
    1: 0x91D7,
    2: 0xD0EB,
    3: 0x111B4,
    4: 0x152FB,
    5: 0x1943B}

name = input("What's the name of the game to write to?")

current_sport = int(input("\nWhich sport's tile collisions are you editing?\n"
                          "(0 for toboggan, 1 for sled, 2 for raft, ... -1 to exit)\n> "))


while current_sport != -1:

    current_bigtile = input(
        "\nWhich bigtile? (0, 1, 2, ..., 255 OR 0x00, 0x01, ..., 0xFF (use the 0x.) -1 to exit)\n> ")

    while current_bigtile != "-1":

        final_palettes = []

        try:
            current_bigtile = int(current_bigtile)
        except ValueError:
            current_bigtile = int(current_bigtile, 16)

        subtiles = input("\nEnter the 4 subtile indices (0 1 2... or 0x00 0x01 0x02... (with the 0x).\nyou may have "
                        "more than 0xFF subtiles, so if you want one of those then type 256 or 0x100, etc.\nif you"
                        "don't know the subtile number, use tile layer pro, ctrl+g to go to the 'subtile graphics "
                        "maker' offsets\n(0x5976, 0x99D7, 0xD8EB, 0x119B4, 0x15AFB, 0x19C3B), make it so that 10 or 16 "
                         "are displayed per row,\nand it should be easier to "
                        "count\n> ").split()

        colours = input("\nEnter the 4 subtiles' palette numbers (0 1 2 3 4 5 6 7)\n> ").split()
        for i in range(4):
            # i'll write all the changes as bitwise ops. that's probably the most intuitive way to visualize
            # this palette anyways, since so much is stored in a "check the nth bit" sense
            final_palettes.append(int(colours[i]))


        flips = input("\nEnter the 4 subtiles' flips, separated by spaces (N for none, H for horizontal flip, V for"
                      " vertical flip, B for hz. flip and vt. flip\n> ").split()
        #print(final_palettes)
        for i in range(4):
            if flips[i].upper() == "H":
                final_palettes[i] |= 0b00100000
            elif flips[i].upper() == "V":
                final_palettes[i] |= 0b01000000
            elif flips[i].upper() == "B":
                final_palettes[i] |= 0b01100000

        priority = input("\nEnter whether any subtile has priority (if it should be drawn over the bears) when being "
                         "drawn, separated by spaces (1 for prio, 0 for none)\n> ").split()
        for i in range(4):
            if flips[i].upper() == "1":
                final_palettes[i] |= 0b10000000

        #store subtile values as bytes (make sure num is FF or lower, and edit palette if needed)
        #print(final_palettes)
        try:
            for i in range(4): #dec input
                subtiles[i] = int(subtiles[i])
                if subtiles[i] > 255:
                    subtiles[i] -= 255
                    final_palettes[i] |= 0b00001000
        except ValueError: #hex input
            for i in range(4):
                subtiles[i] = int(subtiles[i], 16)
                if subtiles[i] > 255:
                    subtiles[i] -= 255
                    final_palettes[i] |= 0b00001000




        with open(f"levels/modified levels/{name}.gbc", "r+b") as f:
            # this lines a bit messy, but: the left one loops depending on whether you're looking at the
            # 0th tile in a range, the 1st tile in a range, the 2nd, ... up to the Fth, since afterwards,
            # you'd reset back to the 0th tile of the next range.
            # the right one checks if the subtile is in the 0-F range, the 10-1F range, ... and adds
            # (64*range number) if it is, so the offset starts at the correct bunch)
            # it's a bit weird since it's stored like "00-TL 00-TR 01-TL 01-TR... 0F-TR 00-BL 00-BR"
            # as seen in big_bears 5176, theres a visual in the picture land
            temp_offset = sport_to_bigtilestructure_offset[current_sport]\
                    + (2 * (current_bigtile % 16)) + ((current_bigtile) // 16) * 64

            #go to the correct subtile number assigner offset
            print(current_bigtile)
            print(subtiles)
            print(final_palettes)
            f.seek(temp_offset)
            f.write(subtiles[0].to_bytes(1))  # top left
            f.write(subtiles[1].to_bytes(1))  # top right
            f.seek(30, 1)  # go 30 bytes ahead now so the bottom half of subtile assigners can be written
            f.write(subtiles[2].to_bytes(1))  # bottom left
            f.write(subtiles[3].to_bytes(1))  # bottom right

            #heading to palette assigners now, same format as above but now add 0x400 since these subtile assigners
            # are 0x400 long
            #print(temp_offset)
            f.seek(temp_offset + 0x400)
            f.write(final_palettes[0].to_bytes(1)) # same as above
            f.write(final_palettes[1].to_bytes(1))
            f.seek(30, 1)
            f.write(final_palettes[2].to_bytes(1))
            f.write(final_palettes[3].to_bytes(1))

            #changing subtile grapics data seems like it'd be a bit hard, or at least hard to
            # make something easier to use than tile layer pro (i could make another tile editor
            # and i can think of a few good things to add e.g. palette visualization, and 7 editable
            # palettes, but for now TLP is good

            #and for changing palettes, ill just make some other code prob

        print("done done, next please")

        current_bigtile = input("\nWhich bigtile? (0, 1, 2, ..., 255 OR 0x00, 0x01, ..., 0xFF (use the 0x.)"
                                " -1 to exit.)\n> ")
    current_sport = int(input("\nWhich sport's tile collisions are you editing?\n"
                              "(0 for toboggan, 1 for sled, 2 for raft, ... -1 to exit)\n> "))