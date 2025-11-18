## YOUTUBE DEMO: https://www.youtube.com/watch?v=p_BWKyv7Rn8

- first things first, you'll need python and a python IDE for most of the tiny programs, so you can make a virtual environment for the py files (e.g. VScode or PyCharm)
- or, you can use the major programs' (course and music editors) exe files.

----------------------------------------------------------------------------------------

# **course_editor.py (or exe):**
click the top right info button to get a better idea of where everything is!)


### **COURSE EDITOR INFO**
- left click to select/place tiles
- middle click is an eyedropper tool for tiles
- right click lets you select a group of tiles, for use in the stamp draw mode
- up/down or scroll to move

- draw modes include pencil (draws one at a time), bucket (fills tiles of the same type), and stamp (draws the stamp chosen by the right click select thing)

- sports and difficulties are usually represented via a number instead of by name (toboggan = 0, sled = 1, raft = 2, kayak = 3, bike = 4, dirtboard = 5) (beginner = 1, intermediate = 2, advanced = 3)

- no file extensions needed when saving/loading, but make sure your files to load are .csv files and are in the proper file (levels/modified levels/)

- when saving to a game, leave a gbc file in levels/modified levels/

- in lieu of having whole objects to add, you'll have to paste numbers around in a csv file editor (i like libreoffice calc) (or if you prefer, maybe load all sprites into the "inventory" with buttons 0 thru 9, and draw them in course_editor)

- when loading, try to refrain from mixing difficulties, unless you're ok with manually deleting some of the saved csv file before loading it and adding it to a gbc file (else it will overwrite important data and break some sprites)

- there is also a button to show collisions (what hitting each 8x8 tile will do to your bear) and a checkerboard (to distinguish where one bigtile starts and another ends)

- if you want to make new course graphics, you can copy an existing folder pair and edit those pngs (so for instance if you wanted to make ski, you could create a ski and ski_effects folder, and then replace some other sport name on line 49 of the code with the new name. but if you don't care about seeing new graphics in the tile editor, no need to make any new files)

- loading from a game/a full game loads course data from a bears game, instead of from a csv file.

- loading tiles allows you to change the bigtile graphics/collsiion graphics in some stage (and are loaded from folders in the tiles folder. the print button in the tile editor can make these folders.)

- changing the course height and spawn location are self explanatory, and are represented by the red shapes at the bottom of the course. the pink rectangle represents the spawning camera (assuming the code works)

### **TILE EDITOR INFO**
- left click on a palette/colour (top left) to choose it, and right click on a colour to be prompted to change it (in the console, using RGB values from 0 to 255)
- if in subtile editor mode, it'll be your paintbrush colour (in the context of "colour 0, colour 1, colour 2, colour 3")
- if in bigtile editor mode, it'll replace the selected bigtile quadrant's palette
- in both modes, it changes the display colour of subtiles in the top right (just a graphical thing; subtiles aren't connected to a specific palette)

- left click on a subtile in the top right to select it
- if in subtile editor mode, it'll put it in the big screen and you can then draw on it
- if in bigtile editor mode, it'll replace the selected bigtile quadrant's subtile

- left click on a collision colour in the bottom left to select it (only works in bigtile editor mode, where it replaces the bigtile quadrant's collision

- left click on one of the three grey/yellow buttons (only in bigtile editor mode) to (from left to right):
   - change the priority (turning it on means the last 3 colours in the palette are drawn over bears' sprites)
   - flip the subtile vertically
   - flip the subtile horizontally

- save/load buttons also require responses in the console (levels should be stored in levels/modified_levels. type the whole file name in (i don't remember if that's the same as it was done in the other mode, but if it's different oops sorry i'll fix it one day)

- the print button makes images of all bigtiles in the tiles folder

- the s-tile usage button prints everywhere your selected subtile is used in the current bigtiles

----------------------------------------------------------------------------------------

# **music_maker.py** (for editing GBC game music tracks)
i'd recommend getting/making sheet music first, as you'll need to make two lists of values: one with note names (e.g. C1, F#4, H B S C for drums. i haven't implemented rests yet, since i'm not too sure how to stop a note early in game code), and one with note lengths (e.g. 1 for a quarter note, 4 for a full note, 0.5 for an eighth note)

----------------------------------------------------------------------------------------

# **(bonus tools and supplementary recommendations)**
- colours.py: convert hex colour codes to 15-bit colour codes (either for bears or a bitmap, but you'll need to specify which mode you want in the python code at the moment.)
- pngifier.py: takes all bmp images in a folder and converts them to pngs (not sure how to keep the correct name yet) (also it's set up to do bigtilebmp stuff right now, so change the input and output folders as wanted)
- bigtilebmp.py: for making bmp images of whole course graphics and collisions (very spaghettish, i don't remember writing it lol) (if you want to use it, you'll have to make two folders in gaming called atesting and atesting2)
- Tile Layer Pro (not mine!): nice program for editing subtile graphics (use ctrl+g to make things easier)
- bears spreadsheet: gives a bunch of addresses (useful for finding subtile graphics offsets in tile layer pro)
- HxD, Notepad++, or some other hex editor (not mine!): could be useful if you need to look at game hex code (also not in here)

----------------------------------------------------------------------------------------

# **todo in future:**
- make a button to reset to blank levels, with any height/width (can be accomplished with stamp tool for now)
- make a program for sprite editing (in theory easy? also easy to do manually with tile layer pro, i think. but it could be nicer)
- start making a music editor in pygame
- make the code less messy
- make the programs easier to use (not sure how at the moment, maybe more guis, or some youtube explanations)
- make different resolution sizes?
- mario maker dropdown menu?
- find where i put the other bmp maker files? they're just gone idk

