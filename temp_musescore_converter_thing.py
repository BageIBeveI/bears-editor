# originally made to play with automating DECTALK code, but works pretty well for this program too

# NOTE: DOESN'T work with rests yet since i don't know how to implement them in the bears code. replace all rests
# with notes in the musescore file or csv (gbc decay will take care of things, unless you want staccato in which case sorry)

def main():
    name = input("Input name of mei file (without .mei at the end)): ")
    try:
        MEI = open(f"mei/{name}.mei", 'r')
        meiFile = MEI.read()
        MEI.close()

        accentmap = {
            "s": "#",
            "n": "",
            "f": "b"
        }

        ids = []
        lengths = []
        notes = []
        ties = []

        splinput = meiFile.split("\n")

        meiLine = 0
        numlines = len(splinput)
        while meiLine < numlines:
            line = splinput[meiLine]
            goodline = line.strip()
            linestart = goodline[0:5] #for checking line types
            splitlist = goodline[1:-1].split(" ") #removes <>, and splits parts up for ease of use
            ######print(splitlist)

            dotted = 0
            notename = ""

            if linestart == "<note":
                listIndex = 1
                # checks each thing in the list for an xml id, dot, duration, note name, and octave
                while listIndex < len(splitlist):
                    item = splitlist[listIndex]
                    match item[0:3]:
                        case "xml":
                            ids.append(item[8:-1])
                        case "dot":
                            dotted = int(item[6:-1])
                        case "dur":
                            # maps 16 to 0.25, 4 to 1, etc
                            templength = 4 / int(item[5:-1])
                            if dotted != 0:
                                # 1 becomes length/2, 2 becomes length/2 + length/4 = 3length/4, 3 becomes 7l/8, etc.
                                pow2 = 2 ** dotted
                                dotted = ((pow2 - 1) * templength) / (pow2)
                                templength += dotted
                            lengths.append(templength)
                        case "pna":
                            notename = (item[7:-1]).upper()
                        case "oct":
                            notename += item[5:-1]
                            notes.append(notename)

                    listIndex += 1

            elif linestart == "<rest":
                listIndex = 1
                while listIndex < len(splitlist):
                    item = splitlist[listIndex]
                    match item[0:3]:
                        case "xml":
                            ids.append(item[8:-1])
                        case "dot":
                            dotted = int(item[6:-1])
                        case "dur":
                            # maps 16 to 0.25, 4 to 1, etc
                            lengthy = item[5:-1:]
                            # idk what long means, sometimes it shows up though. maybe it's a full bar?
                            # in which case would need to log the time signature somewhere
                            # but for now i'll make it default to a whole note
                            tempLength = 0
                            if lengthy == "long":
                                tempLength = 1
                            else:
                                tempLength = 4 / int(lengthy)
                            if dotted != 0:
                                # 1 becomes length/2,
                                # 2 becomes length/2 + length/4 = 3length/4,
                                # 3 becomes 7l/8,
                                # etc.
                                # would be really easy to make this out of a float manually but i don't think it needs to be that efficient
                                pow2 = 2 ** dotted
                                dotted = ((pow2 - 1) * tempLength) / pow2
                                tempLength += dotted
                            lengths.append(tempLength)

                            if __name__ == "__main__":
                                notes.append("_")
                            else:
                                notes.append("C1") #can't use rests in music maker, so filling em with sawdust
                    listIndex += 1

            elif linestart == "<acci":
                endnote = notes[-1]
                # for some reason accid isn't consistent? xmlid is sometimes in pos1 or later
                accentString = splitlist[2]
                if accentString == "/":
                    accentString = splitlist[1]
                notes[-1] = endnote[0] + accentmap[accentString[-2:-1]] + endnote[1]

            # will deal with this later. can just manually merge for now
            ##elif linestart == "<tie ":
            ##    splitlist = goodline[1:-3].split(" ")
            ##    print(splitlist)

            meiLine += 1
        for i in notes:
            print(i, end=" ")
        print()
        for i in lengths:
            print(i, end=" ")
        print()
        ## dectalk phoneme filler. bit useless without anything to assemble it into the duw<100,1> packets but whatevs
        ##print()
        ##for i in lengths:
        ##    print("duw", end=" ")

        return (notes, lengths)
    except FileNotFoundError:
        print("File not found.")
    except Exception:
        print("Error! No changes made.")
    return ()

# only run self when isolated running
if __name__ == "__main__":
    main()