"""
from PIL import Image
import glob

sport = "bike_events"
the_number = len(sport) + 1
count = 0
for bitmapChar in glob.glob(f"{sport}/*.bmp"):
    Image.open(bitmapChar).save(f"{sport}/{bitmapChar[the_number:len(bitmapChar) - 4]}.png")
    count += 1
"""

from PIL import Image
import glob

sport = ["bike", "collision_bike", "collision_dirtboard", "collision_kayak", "collision_raft", "collision_sled", "collision_toboggan", "dirtboard", "kayak", "raft", "sled", "toboggan"]
diff = ["_advanced", "_beginner", "_intermediate"]
the_number = len(sport) + 1
count = 0
for bitmapChar in glob.glob(f"atesting/*.bmp"):
    Image.open(bitmapChar).save(f"atesting2/{sport[count//3]}{diff[count%3]}.png")
    count += 1