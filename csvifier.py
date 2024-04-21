import os
import csv

folder = "levels"

#this is the only important part, it just turns the txt files into csv files in case you want to reset them
for filename in os.listdir(folder):
    if filename[-1] == "t":
        filenameNoType = filename[0:len(filename) - 4]
        with open(f"levels/{filenameNoType}.csv", 'w', newline="") as file:
            with open(f"levels/{filename}", "rb") as level:
                levelBytes = level.read()
                writaaa = csv.writer(file, delimiter=",")
                for i in range(0, len(levelBytes), 16):
                    writaaa.writerow(levelBytes[i:i + 16])
                file.truncate(file.tell() - 2)