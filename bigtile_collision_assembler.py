# was gonna print the menu with ANSI colours, might do it
# zero = '\x1b[0;93;40m' + '0' + '\x1b[0m'
# two = '\x1b[0;90;40m' + '2' + '\x1b[0m'
# three = '\x1b[0;32;40m' + '3' + '\x1b[0m'
# eight = '\x1b[0;96;40m' + '8' + '\x1b[0m'
# c = '\x1b[0;91;40m' + 'C' + '\x1b[0m'
# oneone = '\x1b[0;33;40m' + '11' + '\x1b[0m'
# twoone = '\x1b[0;33;40m' + '21' + '\x1b[0m'
# threeone = '\x1b[0;33;40m' + '31' + '\x1b[0m'
# threetwo = '\x1b[0;33;40m' + '32' + '\x1b[0m'
# hreethree = '\x1b[0;33;40m' + '33' + '\x1b[0m'
# fourtwo = '\x1b[0;33;40m' + '42' + '\x1b[0m'
# seventhree = '\x1b[0;33;40m' + '73' + '\x1b[0m'
# eighttwo = '\x1b[0;33;40m' + '82' + '\x1b[0m'
# bthree = '\x1b[0;33;40m' + 'B3' + '\x1b[0m'
# czero = '\x1b[0;33;40m' + 'C0' + '\x1b[0m'
# exit()

sport_to_collision_offset = {
    0: 0x4D6C,
    1: 0x8DCD,
    2: 0xCCE1,
    3: 0x10DAA,
    4: 0x14EF1,
    5: 0x19031}

number_to_effect_byte = {
    0: 0x00,
    1: 0x02,
    2: 0x03,
    3: 0x08,
    4: 0x0C,
    5: 0x11,
    6: 0x21,
    7: 0x31,
    8: 0x32,
    9: 0x33,
    10: 0x42,
    11: 0x73,
    12: 0x82,
    13: 0xB3,
    14: 0xC0}

name = input("What's the name of the game to write to (no file extension)?")

hexyes = bool(input("\nHow do you want to input effect tiles?\n(leave empty for numbers (0 1 2 3 4..)\n(type "
                    "anything for bytes (0x00 0x02 0x03 0x08 0x0C.. or 0 2 3 8 C..) allows for any byte input, but "
                    "no promise that other bytes will have cool effects"))

print(f"\nByte mode: {hexyes}")

current_sport = int(input("\nWhich sport's tile collisions are you editing?\n"
                          "(0 for toboggan, 1 for sled, 2 for raft, ... -1 to exit)\n> "))

current_tile = input("\nWhich tile's collision? (0, 1, 2, ..., 255 OR 0x00, 0x01, ..., 0xFF. -1 to exit)\n> ")
try:
    current_tile = int(current_tile)
except ValueError:
    current_tile = int(current_tile, 16)

if hexyes:
    while current_sport != -1:
        while current_tile != -1:
            effects = input("\nEnter the 4 effects of the top left, top right, bottom left, and bottom right subtiles "
                            "(e.g. 1 3 5 4)\n0x00 = OOB tile\t\t\t\t\t\t\t\t\t\t\t0x02 = slowdown tile\t\t\t\t0x03 = "
                            "normal tile\n0x08 = small ramp jump\t\t\t\t\t\t\t\t\t0x0C = big ramp jump\t\t\t\t0x11 = "
                            "LS of ramp\n0x21 = RS of ramp\t\t\t\t\t\t\t\t\t\t0x31 = mud puddle\t\t\t\t\t0x32 = early "
                            "ice tile OR whirlpool OR water puddle\n0x33 = far ice tile OR rapid tile OR bridge\t\t\t\t"
                            "0x42 = right wall\t\t\t\t\t0x73 = bridge right wall\n0x82 = left wall\t\t\t\t\t\t\t\t\t"
                            "\t0xB3 = bridge left wall\t\t\t\t0xC0 = wipeout\n(both ice tiles make you slide when your "
                            "speed is over 3, but an early tile will slow you down while a far tile doesn't affect "
                            "speed (if you slide, it doesn't let your speed increase, but if you're not sliding then "
                            "you can speed up, until you do slide))\n> ").split()
            # this comment doesn't capture every effect, just the ones used in game
            # i haven't tried many, but an effect of 5 is a tiny hop, 9 is a longer hop
            # those could be useful for a choco mountain kinda track
            with open(f"levels/modified levels/{name}.gbc", "r+b") as f:
                f.seek(sport_to_collision_offset[current_sport] + (4 * current_tile))
                for i in range(4):
                    f.write(int(effects[i], 16).to_bytes(1))

            current_tile = int(input("Which tile's collision? (0, 1, 2, ..., 255. -1 to exit)\n> "))
        current_sport = int(input("Which sport's tile collisions are you editing?\n"
                                  "(0 for toboggan, 1 for sled, 2 for raft, ... -1 to exit)\n> "))

else:
    while current_sport != -1:
        while current_tile != -1:
            effects = input("\nEnter the 4 effects of the top left, top right, bottom left, and bottom right subtiles "
                            "(e.g. 1 3 5 4)\n0 = OOB tile\t\t\t\t\t\t\t\t\t\t1 = slowdown tile\t\t\t\t2 = normal tile\n"
                            "3 = small ramp jump\t\t\t\t\t\t\t\t\t4 = big ramp jump\t\t\t\t5 = LS of ramp\n6 = RS of "
                            "ramp\t\t\t\t\t\t\t\t\t\t7 = mud puddle\t\t\t\t\t8 = early ice tile OR whirlpool OR water "
                            "puddle\n9 = far ice tile OR rapid tile OR bridge\t\t\t10 = right wall\t\t\t\t\t11 = "
                            "bridge right wall\n12 = left wall\t\t\t\t\t\t\t\t\t\t13 = bridge left wall\t\t\t14 = "
                            "wipeout\n(both ice tiles make you slide when your speed is over 3, but an early tile will "
                            "slow you down while a far tile doesn't affect speed (if you slide, it doesn't let your "
                            "speed increase, but if you're not sliding then you can speed up, until you do slide))\n> "
                            ).split()
            # this comment doesn't capture every effect, just the ones used in game
            # i haven't tried many, but an effect of 5 is a tiny hop, 9 is a longer hop
            # those could be useful for a choco mountain kinda track
            with open(f"levels/modified levels/{name}.gbc", "r+b") as f:
                f.seek(sport_to_collision_offset[current_sport] + (4 * current_tile))
                for i in range(4):
                    f.write(number_to_effect_byte[int(effects[i])].to_bytes(1))

            current_tile = int(input("Which tile's collision? (0, 1, 2, ..., 255. -1 to exit)\n> "))
        current_sport = int(input("Which sport's tile collisions are you editing?\n"
                                  "(0 for toboggan, 1 for sled, 2 for raft, ... -1 to exit)\n> "))
