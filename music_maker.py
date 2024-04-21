def main():
    delimiter = input("What delimiter should be used for separating note inputs? (e.g. a comma or a space, for C1,C2, "
                      "C3 or C1 C2 C3): ")

    frames_per_quarter_note = int(input(
        "\nPlease enter the # of frames that should represent one quarter note (divide 3600 by your BPM\n"
        "in quarter notes, and take the nearest integer.) If you want n-tuplets, you'll want to make sure\n"
        "the integer you're typing is divisible by n. if it isn't the program won't crash, but things will\n"
        "prob stop syncing up because of the rounding. (e.g. for 60bpm, frames per quarter = 3600 / 60 = 60): "))

    # since i don't want to make 2 dictionaries, i'll just subtract 12 from anything for channels 1 and 2 (since they'd
    # be more like "C2": 24
    # one more thing, i would store them like "C2": b'\x18', but doing it this way makes transposing easier
    PITCH_TO_BYTE = {
        "C1": 24,
        "C#1": 25,
        "D1": 26,
        "D#1": 27,
        "E1": 28,
        "F1": 29,
        "F#1": 30,
        "G1": 31,
        "G#1": 32,
        "A1": 33,
        "A#1": 34,
        "B1": 35,
        "C2": 36,
        "C#2": 37,
        "D2": 38,
        "D#2": 39,
        "E2": 40,
        "F2": 41,
        "F#2": 42,
        "G2": 43,
        "G#2": 44,
        "A2": 45,
        "A#2": 46,
        "B2": 47,
        "C3": 48,
        "C#3": 49,
        "D3": 50,
        "D#3": 51,
        "E3": 52,
        "F3": 53,
        "F#3": 54,
        "G3": 55,
        "G#3": 56,
        "A3": 57,
        "A#3": 58,
        "B3": 59,
        "C4": 60,
        "C#4": 61,
        "D4": 62,
        "D#4": 63,
        "E4": 64,
        "F4": 65,
        "F#4": 66,
        "G4": 67,
        "G#4": 68,
        "A4": 69,
        "A#4": 70,
        "B4": 71,
        "C5": 72,
        "C#5": 73,
        "D5": 74,
        "D#5": 75,
        "E5": 76,
        "F5": 77,
        "F#5": 78,
        "G5": 79,
        "G#5": 80,
        "A5": 81,
        "A#5": 82,
        "B5": 83,
        "C6": 84,
        "C#6": 85,
        "D6": 86,
        "D#6": 87,
        "E6": 88,
        "F6": 89,
        "F#6": 90,
        "G6": 91,
        "G#6": 92,
        "A6": 93,
        "A#6": 94,
        "B6": 95,
        "C7": 96,
        "C#7": 97,
        "D7": 98,
        "D#7": 99,
        "E7": 100,
        "F7": 101,
        "F#7": 102,
        "G7": 103,
        "G#7": 104,
        "A7": 105,
        "A#7": 106,
        "B7": 107,
        "C8": 108,
        "C#8": 109,
        "D8": 110,
        "D#8": 111,
        "E8": 112,
        "F8": 113,
        "F#8": 114,
        "G8": 115,
        "G#8": 116,
        "A8": 117,
        "A#8": 118,
        "B8": 119,
        "C9": 120,
        "H": 1,
        "B": 35,
        "S": 38,
        "C": 44}

    # 4 empty lists, one for each channel
    notes = [[]] * 4
    note_lengths = [[]] * 4

    while True:
        print_menu()
        user_choice = input("Make your choice  .....")
        if user_choice == "1":
            music_adder(notes, note_lengths, delimiter)
        elif user_choice == "2":
            music_deleter(notes, note_lengths)
        elif user_choice == "3":
            for i in range(4):
                print(f"\n  Channel {i + 1}:")
                print("Notes:", notes[i])
                print("Note Lengths:", note_lengths[i])
        elif user_choice == "4":
            file_saver(notes, note_lengths)
        elif user_choice == "5":
            game_writer(notes, note_lengths, PITCH_TO_BYTE, frames_per_quarter_note)
        elif user_choice == "6":
            frames_per_quarter_note = file_loader(notes, note_lengths)
        elif user_choice == "Q":
            if input("You sure? Y to quit") == "Y":
                exit()


def print_menu():
    print("\n1: Add new data")
    print("2: Delete some data")
    print("3: View current tracks")
    print("4: Save data as csv")
    print("5: Save data to game")
    print("6: Load track data")
    print("Q: Quit")
    return


def music_adder(notes, note_lengths, delimiter):
    channel = int(input("\nPlease choose a channel (1, 2, 3, 4).")) - 1

    #idk why i only have error handling here, but whatevah
    try:
        starting = int(input("Notes: At which index do you want to start?"))
    except ValueError:
        print("Bad!")
        return

    #this just takes the array and some starting index, then saves left + new + right
    notes[channel] = notes[channel][:starting] + input(
        "\nFOR CHANNELS 1 2 AND 3:\n"
        "please enter the notes, separated by your delimiter (e.g. anything from C2 to C9 (or C1 to "
        "C8 in channel 3), like C2 D#3 F5)\n"
        "Use # for accidentals. (no rests yet) \n\nFOR CHANNEL 4: write H B S C (for drum/water/bike/puddle sfx) as "
        "many times as needed. once i figure out how to get more stuff out\nof the noise channel, more will come, but "
        "for now, H is hi-hat ish, B is beep-ish?, S is snare-y, and C can be used as a very weak splash cymbal\n>"
         ).split(delimiter) + notes[channel][starting:]

    try:
        starting = int(input("\nNote lengths: At which index do you want to start?"))
    except ValueError:
        print("Bad!")
        return
    note_lengths[channel] = note_lengths[channel][:starting] + input("Now enter the note lengths in terms of quarter "
                                                                     "notes, (e.g. whole = 4,\ndot half = 3, quarter = "
                                                                     "1, eighth = 0.5, triplet on a quarter = 0.33)\n"
                                                                     "(and same #of inputs as last time.)"
                                                                     ).split(delimiter) + note_lengths[channel][
                                                                                          starting:]

    #quick check to make sure there are as many notes as there are lengths, can be fixed via add/delete
    if len(notes[channel]) != len(note_lengths[channel]):
        input(f"\nWarning: #of notes ({len(notes[channel])}) != #of note_lengths ({len(note_lengths[channel])})")

    print("\nNotes:", notes[channel])
    print("note_lengths:", note_lengths[channel])
    return


def music_deleter(notes, note_lengths):
    #just loops and keeps asking the user to delete some note/length until they're done

    channel = int(input("Which channel do you want to delete from (1 2 3 4)? ")) - 1
    mus_index = 0
    # maybe ask if we want to delete from notes and note_lengths at once?
    print(notes[channel])
    mus_index = int(input("\nWhich index do you want to delete? (-1 to exit): "))
    while mus_index != -1:
        notes[channel].pop(mus_index)
        print(notes[channel])
        mus_index = int(input("\nNext: (-1 to exit) "))

    print(note_lengths[channel])
    mus_index = int(input("\nWhich index do you want to delete? (-1 to exit): "))
    while mus_index != -1:
        note_lengths[channel].pop(mus_index)
        print(note_lengths[channel])
        mus_index = int(input("\nNext: (-1 to exit) "))

    if len(notes[channel]) != len(note_lengths[channel]):
        input(f"\nWarning: #of notes ({len(notes[channel])}) != #of note_lengths ({len(note_lengths[channel])})")
    print("\nFinal data:")
    print("Notes:", notes[channel])
    print("note_lengths:", note_lengths[channel])


def file_saver(notes, note_lengths):
    name = input('Enter a filename (leave empty to skip):')
    if name != "":
        with open(f"music_csv/{name}.csv", "w") as file:
            for channel in range(0, 4):
                try:
                    file.write(notes[channel][0])
                except IndexError:
                    file.write("\n\n")
                    continue
                for note in notes[channel][1:]:
                    file.write(f",{note}")

                file.write("\n")

                try:
                    file.write(note_lengths[channel][0])
                except IndexError:
                    file.write("\n")
                    continue
                for note_length in note_lengths[channel][1:]:
                    file.write(f",{note_length}")

                file.write("\n")

            file.write("end")
        print("Save successful.")
    return


def game_writer(notes, note_lengths, P2B, FPQ):
    # this'll write the song right into game data once it's done
    # remember to check if it's gonna overwrite something else (and possibly learn how to modify the offsets stored
    # in rom so length won't be an issue
    pass
    # id:[offset, length]
    song_ID_map = {
        "0": [0x7C49D, 0x9A4],
        "1": [0x7CE41, 0x904],
        "2": [0x7D745, 0x4E],
        "3": [0x7D793, 0x6C],
        "4": [0x7D7FF, 0x15C],
        "5": [0x7D95B, 0x25B],
        "6": [0x7DBB6, 0x33C],
        "7": [0x7DEF2, 0x2F6]}

    # ================
    loopin = int(input("Do you want the song to loop? (0 no, 1 yes)"))

    #big_list = []
    offset_sum = 8

    # will store the byte data of the music file
    temp_bytes = b'\x08\x00'
    #adding the other 3 offsets in the header
    for i in range(0, 3):
        # each note takes 5 bytes, and if looping then there's one extra entry at the end of the data so there needs to
        # be one more added to the length
        # also, taking a min just in case i accidentally add too many notes/lengths
        offset_sum += (min(len(notes[i]), len(note_lengths[i])) + loopin) * 5
        temp_bytes += offset_sum.to_bytes(2, "little")

    name = input('Enter a game to save the data to (leave empty to skip):')
    if name != "":
        song_ID = input("Which song ID?")
        gamefile = open(f"levels/modified levels/{name}.gbc", "r+b")

        for channel in range(4):
            transpose = int(
                input(f"Transpose channel {channel}? (if not, enter 0. otherwise, enter some integer of semitones)"))

            relative_offset = 0

            # just storing these to save a bit o time
            curr_note_channel = notes[channel]
            curr_note_len_channel = note_lengths[channel]

            length = min(len(curr_note_channel), len(curr_note_len_channel))
            for i in range(length):
                # the first offset is 0, and the next one is 0 + (length in quarter notes * frames per quarter note)
                temp_bytes += relative_offset.to_bytes(2, "little")
                relative_offset += round(float(curr_note_len_channel[i]) * FPQ)

                # take the current note, convert it to a number (the byte as an integer) (via the dict), add whatever
                # transposition is needed, then convert to a byte and add it to the music file
                if channel in (2, 3):
                    temp_bytes += (P2B[curr_note_channel[i].upper()] + transpose).to_bytes(1)
                # this one's different because the big dictionary maps pitches too low for these channels (it works fine for
                # bass, but here, it needs to go down an octave)
                else:
                    temp_bytes += (P2B[curr_note_channel[i].upper()] + transpose - 12).to_bytes(1)

                #not changeable for now, since idk what 64 does, and effects have different... effects depending on channel
                temp_bytes += b'\x64\x30'

            #the bears code checks whether pitch is 0 at every offset, and if it is then the channel gets sent
            #to loop land until all 4 channels are there, which signifies they're all done and things can reset
            #so this just adds an extra offset where pitch is zero. the actual offset doesn't matter i don't think
            #(maybe if the offset is less than the prev offset? i don't remember)
            #but as long as all 4 eventually hit their offsets it loops fine

            #one thing, the bass wave of the menu song seems to change after my edits, idk why that is
            if loopin:
                if relative_offset != 0:
                    temp_bytes += (relative_offset - 1).to_bytes(2, "little")
                    temp_bytes += b'\x00\x00\x00'
                else:
                    temp_bytes += b'\x01\x00\x00\x00\x00'

        #i think it'd be easiest if it always had the same length, so i'll add a bunch of filler after
        temp_bytes += (song_ID_map[song_ID][1] - len(temp_bytes)) * b'\x00'
        print(temp_bytes, (song_ID_map[song_ID][1] - len(temp_bytes)))
        gamefile.seek(song_ID_map[song_ID][0])
        gamefile.write(temp_bytes)
        gamefile.close()

    # as one extra comment, some edge cases can happen if you choose no loops & leave some channels
    # empty, but i don't think it'd be worth fixing, so it shall stay like that.


    return


def file_loader(notes, note_lengths):
    name = input("\nEnter a filename for the data:")

    with open(f"music_csv/{name}.csv", "r") as file:
        for channel in range(4):
            #remove the rightmost \n, then any trailing commas, and finally split with commas as delim.
            #the trailing commas are a result of editing in libreoffice, idk if anyone will do that but
            #it seems like a good way to visualize things/edit things as a whole
            temp = file.readline().rstrip().rstrip(",").split(",")
            #without this there'd be icky empty strings left in all the empty channels and i dont want them
            if temp == ['']:
                temp = []
            #print(temp)
            notes[channel] = temp

            #same, but for lengths instead of notes
            temp = file.readline().rstrip().rstrip(",").split(",")
            if temp == ['']:
                temp = []
            #print(temp)
            note_lengths[channel] = temp

    print("\nLoad successful.")

    return int(input("\nWhat is the FPQ (frames per quarter note) of this track?"))


main()

# i think it'd be best to leave fades up to manual input. (also how
# do you stop a channel/start a rest? i'll need to check)
