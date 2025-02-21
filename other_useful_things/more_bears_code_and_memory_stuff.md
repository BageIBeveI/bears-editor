when hitting something:
4548 EA 7F C2  -  ld (C27F), a       (a = 40)
454B FA 79 C2  -  ld a, (C279)       (mem = 00)
and a
jp nz 460B (yez)
ld a C2F0 (40)
cp a C0 (40 - C0 = 

------------\
on ice (no slide)
46AA cp a 3-



46E7 ld a, C221     seems important, speed check?
then cp a, 04
jr c 4700 (c is deactivated if a >= 4?)

------------ TIMER MEMORY INCREMENTATION
0367


ld hl c235
inc hl
ld a, hl
cp a, 06 (activates the zero flag when a == 6) (leads to the next timer incrementation)
jr nz 039F

ld a 01
ld C266, a (idk why)
xor a (a = 0 now)
ldd (hl), a (load zero into c235, and load c234 into hl)
inc (hl) (+1 to the ms tens counter)
ld a, (hl) (a = counter)
cp a, 0a (zTrue if a == 0a, also makes f flag 0xC0)
jr nz, 039f

xor a (af = 80)
ldd (hl), a (load zero into c234, and load c233 into hl)
inc (hl) (+1 to the s ones counter)
ld a, (hl) (a = counter)
cp a, 0a (zTrue if equal)
jr nz, 039f

xor a (af = 80)
ldd (hl), a (load zero into c233, and load c232 into hl)
inc (hl) (+1 to the s tens counter)
ld a, (hl) (a = counter)
cp a, 06 (zTrue if equal)
jr nz, 039f

xor a (af = 80)
ldd (hl), a (load zero into c234, and load c233 into hl)
inc (hl) (+1 to the m ones counter)
ld a, (hl) (a = counter)
cp a, 0a (zTrue if equal)
jr nz, 039f

xor a (af = 80)
ldd (hl), a (load zero into c234, and load c233 into hl)
inc (hl) (+1 to the m tens counter)
ld a, (hl) (a = counter)
cp a, 0a (zTrue if equal)
jr nz, 039f

-------------
   4287:
call 4079

   4079:

   40CC:
ld (FF26), a
ld a, 0f
ld c330, a (c330 = 0f)
pop hl (to c331)
pop de (to c331)
pop bc (to 0735)
pop af (to 8220)
ld c32e, a
and a (set z if a = 0?)
jr z 4062
ret (to 428a)

   428a:
jr 429f

   429f:
ret (to 0335)

   0335:
ld a, 01        |(2000) = 01
ld (2000), a  |
ld a, (c201)    |increment c201 by 1
inc a
ld (c201), a    |
ld a, (c267)  |check if c267 == 0
and a
jr z, 039f      |

   039f:
ld a, (c29b) |check if c29b == 0
and a
jr z, 03cf     |

   0c3f:
ld a, (c29a) |check if c29a == 0
and a
jr z, 03f1     |

   03f1:
pop af (af = 3a80)
ld (2000), a
pop de (4483)
pop bc (0000)
pop af (1080)
pop hl (625c)
ei
reti (skip to 040b?)

ld (ff00+00),a (df?)
ld a,(ff00+00) (six times?)
cpl (af => 20e0)
and a,0f (a => 00)
or b (af => 0080)
ld c, a
ld a,(ff8b)
xor c
and c
ld (ff8c),a

-------------
(log all things during time result, then break when click) (non-podium)
1BBD:
ld a,(c202)
inc a
ld (c202),a

-------------
18F5 - 1904 (happens when raft L1+ movement instead of straight)
  ROM3: 44B4 - 44BA (when raft L2+ movement)
     07f7 (raft L3+)

raft right rom3 48C0
07f7

------------
bumps and bumper car physics

451D is new when bumping a wall

------------
call 18A8:
b = A0
(c290) = (c28c) xor 28 (flip bits 4 5 6)
if (c290) is zero:
   turn (C100) thru (C19F) to 00
   load c100 into hl
   call 0a3f:
      (c293) = 00
      (c294) = c1
   (c28d) = 00
   (c28e) = 80

---

0:a6d
maybe just loads a palette into wram1 as long as it's pointing to something in one of the ROM blocks (0000-7FFF), and then (C29B), (C29C) = 01, 01?


----------

ROM2 481f - 4825: huuuuge (infinite-ish?) loop, changes stat/ly and does something to OAM and I/O to render sprite/level graphics one row at a time (top to bottom) (also it does them in separate loops, so like itll do all the level stuff and then all the bear stuff) idk how it works, loop ends when ly reaches 8f again though: LDC interrupt brings it to 0048:
   jp 032f
      di
      push hl af bc de
      ld a,(7fff) (the # of the current chunk stored in ROM) (always 02 or 1e?)
      push af
      ld a, (c203)
      ld (2000), a   (weird notation, but this swaps out the chunk stored in 0x4000-0x7fff)
      l = (c204)
      h = (c205)
      jp hl (seemingly always (4a91)?)
         4a91:
         if LY != 7
             jr 4b08 (cont. elsewhere)
         if bit #1 of STAT is set:
             jr 4a97 (go back one, and check if bit is set. tell me... again)
         LCDC = e3
         WINX = a7
         if (c29c) == 0:
             jr 4ac5 (cont later, look for the !!!)
         BGPALSEL = 80 (nope thats not it, idk whats goin on here but weird stuffs happening)
         PGPALDATA = ff
         PGPALDATA = 7f
         BGPALSEL = 86
         PGPALDATA = ef
         PGPALDATA = 3d (wha its like it already knows the value before it gets assigned, watz apnin)
         if (c27d) != 0:                               (!!!)
             
         


---------
4b08:

------------
4a97:

-------
sound loopin stuff (1F) (this loop logs all the normal menu stuff, and documents new things that happen when menu music loops)
4017:
res 0, (c330)
jr 4149

(old stuff)
416c:
res 1, (c330)
jr 41a9

(old stuff)
41cc:
res 2, (c330)
jr 4202

(old)
4225:
res 2, (c330)
jr 4271

(old)
4280:
if bit 7 of (c32e) != 0,
    dw about it
call 4079
    push af bc de hl
    and a 7f (7th byte to 0)
    if (c32e) == a:
        jr 40d4    (from what ive seen, during the 2nd write to song_id in a crash, this one happens. 
                       makes sense i think since the new song_id is equal to the old song_id)
                          (look for ooo)
    if (((a * 2) + 80 if the orig song id had it) + 8b) not < FF:
        inc b
	 ld a, (bc)    (448f = 41)    (aka 7c48f)
	 ld e, a
	 inc bc
	 ld a, (bc)    (4490 = 4e)
	 ld d, a
	 or e
	 (if both are zero):     (tends to happen during a scene change, e.g. loading/leaving a level)
	     jr 40d4          (look for ooo)
	     (dw about it)
	 bc = de
	 hl = c333
	 a = (de)     (08, since this is menu musicintro (4e41); 4e43 is 10; 90; 51) ( *** )
	 inc de
	 add c         (c = 41, so a = 49; 51; d1; 92) (prob to skip to the address eight after 
	                    the start, since the MUSICINTRO is 8 bytes long)
	 ldi (hl), a     (load 49 into c333; 51 into c335; d1 c337, 92 c339)
	 ld a, (de)    (4e42 is 7ce42 is 00; 4e44 is 02; 04; 07)
	 inc de
	 adc b       (cflag is 0 atm, b is 4e) (a becomes 4e; 50; 52; 55)
	 ldi (hl), a     (load 4e into c334; 50 to c336; 52 c338; 55 c33a)
	 a = l          (35; 37; 39; 3b)
	 cp a, 3b
	 if not zero:
	     jr 409b                                                                                                      (go back to the *** )
	 ld hl, c331
	 xor a
	 ldi (hl), a     (00 into c332)
	 ld (hl), a      (00 into c333)
	 ld hl, ff30    (address waveform stuff)
	 ld a, ff
	 ldi (hl), a         ----- eight times (to turn waveforms in ff30 to ff37 to ff)
	 ld a, 00
	 ldi (hl), a         ----- eight times (to turn waveforms in ff38 to ff3f to 00)
	 (ff25) = ff
	 (ff25) = 80
	 (c330) = 0f
	 pop af bc de hl    (ooo)
	 ld (c32e), a      (82 this time) (this val in a came from ld a, (c32e), wha)
	 and a
	 jr z 4062 (dw abt it rn)
	 ret
 jr 429f
 ret
 
0355:
(old)

 
	 



-------
179b:
if (c201) - hl > 3c,
   jr 

----
0273:
push bc
ld c, 81
call 0482
  0482 (related to music stuff, for setting c32e initially, leads into 1F:4079):
  push af
  ld a, (7fff)
  push af
  ld a, 1f
  ld (2000), a
  ld a, c            (c has the 81 song id that starts it all)
  call 4079
-------
0006
overwrite a buncha writeram1 stuff with 00s (dd00? to ddbf?)
0012:
inf loop i think, wait until LY reaches 8F so interrupt brings it to 0048
jp 032f

------
023e adds one to the x_pos of where the title screen is (00 means no scroll, 70 means fully scrolled)

-------
19a3
...

1E:4047
lcd ctrl = c1
x scroll = 0
y scroll = 0

-------
1E: 4014 (when intro credits text gets stored in memory)
documentation in ghidra, though var names kinda suck so comments are added if theyre faulty

----------
1:477B (happens when hitting rocky snow toboggan)

------
1:4C26 has an 0x07, which is loaded into $C284 to load chunk 7

1:4C30 has 0x1C for tob crash

------
5:44AD's lines (and the values stored in 5:4F?? or 5:51?? range? maybe 14CDB to 152FA in chunk 5?) have something to do with collisions/effects of tiles, though the formatting on the values is weird

5:4495:
load current tile into de (00XX, XX = tile ID)
bitshift e left (arith)                                       (overflow goes to d, since it activates the carry flag)
rotate d left                                                   (and an activated carry flag does stuff with this oper.)
bitshift e left (arith)
rotate d left                                                    (basically, de = tile ID times four)
e = (C2EE) or e                                         (what is at c2ee?) (bit more info below)
                                                                     de = AABB
                                                                     AA = {0 if 0x00 <= ID <= 0x3F
                                                                               1 if 0x40 <= ID <= 0x7F
                                                                               2 if 0x80 <= ID <= 0xBF
                                                                               3 if 0xC0 <= ID <= 0xFF}                                                                               
                                                                    BB = tile ID times four (1 byte) OR'd with:
                                                                             {0 if you're on the top left corner of a tile?
                                                                              1 if you're on the top right corner of a tile?
                                                                              2 if you're on the bottom left corner of a tile?
                                                                              3 if you're on the top right corner of a tile?}                                                                          
                                                                    which means tile ID is strange after 0x3f, or maybe it isn't that bad	                                                                
	                                                                in other words, if tile ID = abcdefgh, then
	                                                                  BB = cdefgh(c2ee here)
	                                                                    cdefgh loops every 0x3F		                                                        
		                                                        de = (ID<<2) + (tilecorner), how nice.
		                                                        max = (FF<<2) + 3 = 3FF
		                                                        min = 0
hl = 0x4EF1 + de                                            (ranges from 0x4EF1 to 52F0)
                                                                       (or )
(C2EF) = (hl)                              and of course (hl) is in the "tile effect land", so c2ef stores that effect
                                                        (note that there are many repeated effects, so just because ID or Corner changes, that doesn't necessarily mean the effect must change)
                                                           (though actually i guess this means the storage of the data is much easier to imagine than i had thought, like 4EF1 is bigtile 00 subtile 00, 4EF2 is bigtile 00 subtile 01, maybe i could have guessed this since well then... ez haxx0ring !)

----------
10B2: (c2ee related stuff)
push (7FFF)                  (current chunk num, will be the level's bigtile/collision chunk 01, 02, ...)
load chunk (C2EF)       (contains the number of the chunk that contains the level's shape. 0a, 0b, ...)
b = (c21f)                                                 (c21f is hz location)
c = (c220)                                                 (c220 is direction-adjacent, says me)
e = ((c2d1) AND 0x0F) + c + 0x10            (c2d1 related to vertical location)
																	(AND 0x0f would chop the larger nibble)
																	(+ c + 10 adds some stuff to it, so it isn't just dependent on vertical location like b is on hz loc)
(c2ee) = 0                                                    (start it off with bits 0 and 1 as zeros!)
if bit 3, e != z
    set 1, (c2ee)                                            (if bit 3 of e is 1, bit 1 of c2ee is 1)
if bit 3, b != z
    set 0, (c2ee)                                            (if bit 3 of b is 1, bit 0 of c2ee is 1)
e = e AND F0
ld a, b
swap a
and a, 0f
or e
ld e, a
e += (c2e7)                                                  (?????)
d = (c2e8) adc 00     (idk how adc works, but the c flag would be active if (c2e7) + e overflows)
                                                                    (c2e8 is also ????????????????)
(c2ed) = (de)                                                (c2ed = tile id, well i found copper, or is it gold?)
pop and reload the old chunk
return                                                      (to 5:4495 perhaps? that's one of many options)


what kind of bit manip chaos is this, what is happening  !!!!!!!!!!


"is e's 3rd bit set" is a bit confusing but:
counter's right nibble + "direction?" + 0x10

"is horizontal location's 3rd bit set" asks if you're on the right(?) side of a tile? (it'd be 4 on, 4 off, but i dunno if it starts counting on the leftmost pixel)
c2ee seems to be 2 bits:         "" , "left or right side of a tile = 0 or 1"(?)

----------
1:4823 (c220 examination, for toboggan) (happens during a left turn) (right calls from 4843)
hl = 4cb7 + (c225) + (c225) 
if c flag overflow
    inc h
b = (c21f) + (hl)
inc hl
c = (c220) + (hl)
(c225) -= 1
jr 4861
a = (c225) + (c225)
push af
hl = 4cb7
l += a
if c flag overflow
    inc h
(c21f) = b - (hl)
(c220) = c - (hl)                                    (c220) = (A) - (B), where
                                                             A = (c220) + (   4cb7 + (c225) + (c225)   ),
                                                             B = (   4cb7 + (c225) + (c225)   )
                                                             (note that (c225) is one less in B)
                                                             (but where does c220 come from originally? load-in code, 4048)
                                                             
pop af
hl = 4c3a
l += a
if c flag overflow
    inc h
a = (hl)
hl = c228
add (hl)
ld (c227), a
cp (c226), 0x12
if zero
    (c221) = 1
(c21a) = 3
hl = 1e5e
l += (c221)
if c flag overflow
    inc h
(c21c) = (hl)
ret                              (to 41b9?)

--------------------
1:41b9
if NOT 2 > (c225)
    jp 422b (i will do that)



-------
1:422b
ld a, (ff8b)
bit 7, a

-----
1:4048
sets (c220) to be 6c on startup, and other things are near as well but i wont document now

--------
![[Pasted image 20231023003904.png]]

------
2:4559 (when on a bumper tile, checks bumper value)
if bumper == 40
    jp 4567
if bumper == 80
    jp 4576
jp 45e4

-------
14f1 (related to time generation
if 9 is larger than (c287)
    jr 14ee (call 159d)

---------------
159d: 
push current chunk
load chunk 1e
(c286) = 0
push hl     (stores the vram address where the current image-a number or colon score tile-will go)
hl = c268
l += (c287)
if overflow:
    inc h
(c271) = (hl)
if (hl) = 0
    (c2c4) = (c287)
    (c286) = 50
pop hl
inc (c287)
a = (c287)
call 1a9d
    add a, 30
    call 1068
        push bc
        push de
        sub a, 20
        push hl
        a += (c286)
        pop hl
        bc = 6a1e
        c += a
        if overflow
            inc b
        push current chunk
        load chunk 11
        e = (bc)                                (11:6a32 was one i saw)
        pop af
		load old chunk
		ld a, (ff41)            ( ** )
		bit 1, a
		while not zero
		    head back to stars
		(hl) = e                                 (this adds the thing into vram) (my example of hl is 9900)
		ld a, (ff41)
		bit 1, a
		while not zero
		    head back to stars
		inc hl
		ld a, e
		pop de
		pop bc
		ret (to a112)
	ret (to 15d3)
inc hl
if (c286) is zero
    e = 0
    if (c2c2) is not zero
        if (c2c2) < 3
            e = 8
    a = (c271) + 3 + e
    jr 15f4        ( the & )
ld a, (c2c0)
add a                      (&)
push hl
hl = 4a69
l += a
if overflow
    inc h
ldi e, (hl)                    (4a83 for me)
ld d, (hl)
pop hl
call 1a85
    push current chunk
    load chunk 1e
    ld a, (de)          (@)                      (this loads bear names from 1E)
    inc de                                           (inc bear name char pointer thing)
    if a != 0                                        (if not at the end of a name)
        call 1068       (gwuuuhgh i dont wanna look at branches.sss.ssm,m,mfjg) (oh it's already done)
        jr 1a8e           (goto the @)
    pop af
    load old chunk
    ret (to 1606)
l = (l and e0) or 0d
bc = c230
if (c272) is not zero
    bc = c2f2
e = (c271)
c += (e + e + e)
if overflow
    inc b
a = (bc)
inc bc
if a == 0
    inc hl
    jr 162f          (follow the $)
call 1a9d                (done earlier)
ld a, (bc)                             ($)
inc bc
call (1a9d)          (done earlier)
ld a, 3a
call 1068           (i'm done widdit)
ld a, (bc)
inc bc
call 1a9d           (wooooo! what have i really done by writing this out though, i still dunno how the 
                           times are generated lol)

uh where's the exit condition? is it just an inf loop or
one thing, ff41 relates to the state, so those while loops are just checking if the vram is in the correct state (otherwise it'd write to some unrelated vram chunk)


ok so: e comes from (bc) comes from:
    c230 + (c271) * 3 + 1                  (if c272 is zero)
    c2f2 + (c271) * 3 + 1                   (if c272 isn't zero)

----------------
1:449f
2:44af
3:44d2
4:44e7
5:4ef1
6:5031
are all the effect starting offset instructions (start at 44something, and add ...)

-----
1:44b2 starts collision effect detection for toboggan (i think) (the ANDs and jumps are bit checks, so like AND C0 checks if either bit 6/7 are set, then AND 03 checks if bits 0/1 are set, etc. it just splits cases up i think)

1:4641 starts collision effect detection for toboggan while in air (i also think)

-----------------------
2:4b6b is insta-loaded into sled beginner's horizontal location memory byte
2:4b6c is insta-loaded into sled intermediate's horizontal location memory byte
(guessing that the pattern continues, so the 8b6X-ish range is that)

---
6:43D6
call 18E6
	0:18E6
	ld e, a
	ld d, 00
	push de (00(a))
	push bc
	ld b 00
	call 1905
		0:1905
		ld a, 8
		ld hl, 0000
		shift right logically c **
		if bit 0 of c was 1 hl += de
		shift left arithmetically e
		rotate left d (combined with above, this shifts de left one, putting 0 in the new rightmost bit and putting the old leftmost bit into c)
		dec a (a = 7)
		jr (notz, 190A)
			0:190A **
			(so basically do this stuff 8 times, then return)
		return
	pop bc, de
	xor a (a = 0, so stays 0 and sets z true)
	or b (a = b)
	ret z (true)
bc = hl
ld hl, c2d1 (y value)
ldi a, (hl) (a = c2d1 val, hl = c2d2)
ldd (hl), a (put c2d1 val into c2d2, and dec hl to c2d1)
dec hl (to c2d0)
sub c from a
ldi (hl), a (c2d0 = c2d1 val - c)
ld a, hl (c2d1 val)
sbc b (sub b and carry from a)
ldi a, (hl) (c2d1 -= (b + carry, which was set with sub c))
xor (hl) (a ^= val of c2d2)
and a F0 (is the top nibble of a set? if no z = true)
if not z, call 0B4D
	0:0B4D
	ld a, (7FFF) (chunk 2 in memory's id number)
	push af (store that id)
	ld a, (C2EB)
	ld (2000), a (load level data)
	ld a, (c2e5) *??*
	ld e, a
	ld a, (c2e6)
	ld d, a
	ld a, (de)
	call 04D7
		0:04D7
		ld hl, 1C56
		add a
		if carry activaed, inc h
		add l
		ld l, a
		if carry avticated, inc h
		ldi a, (hl)
		
jp 449D
	


--
6:4BF7 and near are for updating a buncha high ram values or whatever theyre called, e.g. ly, ldc, or x position of window, probably only for dirtboard though?


6:44C7 another collision checker, for dirtboard
load C2ED (current tile id) into de
multiply de by 4 (via left shifts), then add C2EE (the current tile quadrant location) to de
then hl = 0x5031 + de (will be at the correct collision data byte)
load (hl) into C2EF
ld a, C279 (jump phase, 0 1 2 or 3)
and a; if not zero (in air), jp 460B
load C280's val into c (is effect tile a small or big jump? if yes nonzero) "were we on a jump effect tile since last time?"
load C2EF into a, and AND it by 0C. then put it into C280. if it was zero (not currently on a jump), jr 453E
otherwise check if c is zero (implies a jump is starting - C280 is not yet changed). if not jr 453E
oetkerwise load C280, floor divide by four, subtract one, and multiply by two. (if 8, it becomes 2. if C, it becomes 4)
then take that 2 or 4, and hl = 0x502B + (2 or 4) (if there could be overflow, add it to h.)
check if C221 (speed) is zero. if yes, increase it by one
set C278 (for C277, jump rise/fall timer) to be (the value pointed to by hl + C221's val aka speed)
increase hl by 1
set C276 (the jump apex timer) to be (the value pointed to by hl + C221's val aka speed)
set C279 to be 1 (starting a jump)
ld a, 0B
call 490E (the big one!? )
	


so, for some reason this code may not run correctly when you turn into a ramp at the right time, which leads to the non-wallclippy ramp clip. maybe other collision types can be messed up with frame perfect turns? not sure if the error happens here or earlier, but by logging and breaking when seeing new, it doesn't reach the latter half of this code? C2EF never changes to 08, wonder why?
---
6:4525 updates C279 (jump phase) to 1, 6:4629 to 2, 6:4639 to 3, and 6:464B to 0, for dirtboard

---
0:19AA
push hl
put $C201 in $C289 (yuh huh im using $ now, how long will it last)
call 1BB4
	ww
if $FF8C AND 0F isn't zero, jr 19C4

FILLLLLLLLLLL !! please !

pop hl
return

----
6:4000
call 18A8
	oooo
C29A = 01
loop until LCD break thing, and jump to 32F
	0:0ACD
	ld some address (in my case, offset 19431 or 6:5431 when loading dirtboard), and put it in $C29D
	go forwards 2 addresses, and put it in $C2A0
	forwards 1 and put it in $C2A1
	forwards 1 and put it in $C29E
	forwards 1 and put it in $C29F
	forwards 1 (e = val), forwards another (d = val)
	push hl, put de in hl, and call 0496
		0:0496
		i don't want to bye
	forwards 1 and put it in $C2A2
	forwards 1 and put it in $C2A3
	return

----

0:12A6
ld a (C2B8)
then make hl the sum of (that + 1E80, with l carry)
then compare \[that] with \[C2B9]
if not zero
	push bc, and load 4472 into bc
	then call 046F
		0:046F
		load bank 1F and call 1F:4018
			1F:4018
				push all registers
				(LOOP POINT @)
				load (bc) into a (in this case, first is (4472))
				inc bc
				if a is 1,
					hl = FF10
					de = 0511
					jump to 1F:404E
						(~)
				else if a is 2,
					hl = FF16
					de = 0422
					jump to 1F:404E
						(~)\
				else if a is 3,
					hl = FF1A
					(and make (FF1A) 0)
					de = 0504
					jump to 1F:404E
						(~)
				else if a is 4,
					hl = FF28
					de = 0488
					now we are at 1F:404E
						(~)
				else
					jump to 1F:405D
						(&)
				(~)
				until d is zero,
					ld (bc) into (hl) and increase bc and hl by 1
					dec d by 1
				or (FF25) by e
				head back to LOOP POINT @
				..
				(&)
				pop all registers and return
		reload current bank and return
	pop bc
	ld a (C2B8)
	then make hl the sum of (that + C2BF, with l carry)
	ld (C2B9) into (hl)
	if (C2B8) + 1 >= 5,  (*** may be wrong about this inequality, it compares the two and has a nc jump)
		jump to 0:131B (\%\%)
	else (C2B8)++, and if it isn't 3 OR if (C2C1) isn't zero,
		jump to 0:1318 (\%)
	else
		(C2B8) = 4
		(C2C2) = 1
		hl = C2F6
		b = 36
		do
			(hl++) = 0
			b -= 1
			while b isn't zero
		(%)
		jump to 0:1199
			0:1199
			(later :])
				call 0:A66
					elsewhere
				call 0:69F
					elsewhere
	(\%\%)
	c = 3
	if (C2C1) isn't zero,
		c--
	(C2B8) = c
	call 0:A66
		elsewhere
	...
	hl = 1F9D + (C2B8)
	a = (hl++)
	push af
	a = (hl)
	h = a
	pop af
	l = a
	(C2B4) = (hl++)
	(C2B5) = (hl++)
	(C2B6) = (hl++)
	(C2BA) = l
	(C2BB) = h
	e = (hl++)
	d = (hl++)
	if e = d = 0, jump to 0:11FA
	b = (hl++)
	c = 0
	a = 2^(hl++)
	push hl
	hl = 9800 + a
	h = h adc c
	l = l or b
	b = (C2B4)
	c = (C2B5)
	call 0:0515
		0:0515
		aaa no more
	
	
	
else
	

----

0:A66
call 0:0003
	0:0003
	make (DD80) to (DDBF) 0
	inf loop until audio jump? (on ly = 8F there's an interrupt that goes to 0048 and then 032f)
		0:032F
	to exit the loop we need a = 0, which happens at some point on the way back maybe
	(C29C) = 0
	return
call 0:001D
	0:001D
	c = 0
	LOOP START
	if (FF41)'s bit 1 isn't zero, inf? LOOP until it is          (lcd stat)
	(FF6A) = c          (obj pal sel)
	(FF6B) = 0          (obj pal data)
	if (FF41)'s bit 1 isn't zero, inf? LOOP until it is
	if c++'s 6th bit isn't one, LOOP until it is
		(in theory this should happen 0x40 times, unless FF41 is zero in which case uh oh)
	return
return

---

0:069F
hl = 9800
bc = 1413
(FF41) = 1
call 0:06B6
(FF41) = 0
call 0:06B6
return

---

0:06B6
push bc lh bc lh
(FF41) bit 1 = 0 to pass loop, no idea when it changes but can watch it as 'stat' in the TR corner. maybe related to count idk
(hl) = 0
inc hl
dec b
if not zero then back to the loop
pop hl and add 0020
pop bc
oh god it's a mess, c-- and if that isn't zero, push hl bc and loop again
...
pop bc
pop hl
return


---

SCOREBOARD BASE TIME LOADER F'N (18E6 is quite important will need to document how it works) 
0:165B
a = (C2C3)
bc = 0120
call 0:18E6
	0:18E6
	...
push hl
a = (C2C2)
bc = 0030
call 0:18E6
	0:18E6
	...
pop bc
bc += hl + 208E
hl = C236
do
	(hl++) = (bc++)
	until l = 66


the 18E6 things should eventually lead to C holding some multiple of 0x30, which lets a group of 8 times be chosen.
idk how it works, but it's def related to which course is chosen
yet also seems to be called a bunch of other times

what i'm thinking is that it's a kind of multiplication function?
a * bc or something
(where C2C3 is the sport diff, and C2C2 is the sport type)

---

0:18E6
d,e = 00,a
push de, bc
b = 00
call 0:1905
	0:1905
	a = 8
	hl = 0000
	($) (do this 8 times)
	srl c
	if bit 0 was 1, add de to hl
	sla e
	rl d
	dec a
	jump nz ($)
	ret
pop bc, de
if b = 0, return
push hl
bc = 00b
call 0:1905
	0:1905
	a = 8
	hl = 0000
	($) (do this 8 times)
	srl c
	if bit 0 was 1, add de to hl
	sla e
	rl d
	dec a
	jump nz ($)
	ret	
pop de
bc = 00d
hl += bc
a = h
hl = le
ret


take inputs (a) and (c)
	then multiply them together and put the product into S1 (gets pushed as hl and popped as de)
then take inputs (a) and (b)
(unless b is zero, then no need.)
	then multiply them together and put the sum into S2 (the last stretch's hl)
and eventually return those as a 3 byte number
	(bit complicated to imagine maybe, but by adding 00d to hl it's like adding something shifted left 8 times, even though d is on the left register, because we're gonna shift a bunch of registers anyways.)
	like hl = bc + d is 8 shifts too right, but then hle becomes ahl yknow?
(ahl)


---

0:1905
	hl = 0000
	($) (do this 8 times)
	shift c right
	if bit 0 was 1, add de to hl
	shift de left

i.e.
load some 8-bit val into c
from right to left, for eaach 1 seen, add de to hl


----

gbc fail (c200 not 11)
0:1FE
... load bank 1E and jump to 1E:4000
1E:4000
hl = 9CA1
de = 40CF
call 400E
	1E:400E
	(C2D7) = A1 and 1F = 01
	(@)
	ret if (de++) == 0
	call 401D
		1E:401D
		if a = FF (linebreak) jr 4025
			1E:4025
			hl += 20
			l and= E0
			l or= (C2D7)
			c = a
			ret (back to the 401D call)
		else
			call 109C
				0:109C
				push de
				e = a - 20
				inf loop until (FF41)'s bit 1 is 0
				(hl) = e
				inf loop until (FF41)'s bit 1 is 0
				hl += 1
				a = e
				pop de
				ret
			ret
	loop (@)
call 0A51
	0:0A51
	(DDC0) = 63
	(DDC1) = 1C
	(DDC2) = 2C
	(C29B) = 01
	ret
inf loop, except for the occasional 032F

BUT this doesn't seem to work right, maybe they forgot to make the palette work but everything is 00 in colour so it's just a black screen.

---

SCOREBOARD TIME WOBBLER F'N
0:175E
hl = c265
~~~~
hl--
e = 00
call 0:1956
	0:1956
	bc = C206
	c += (C216)
	(C216) = (C216) + 1 & 0F
	a = (bc)
	ret
push af
c = a & 7
a = (hl) + c
if a >= 0A, a -= 0A
(hl--) = a
pop af
swap a
c = a & 0F
a = (hl) + c + e
while a >= 0A
	a -= 0A
	e++
(hl--) = a
a = (hl) + e
e = 0
if a >= 6
	a -= 6
	e++
(hl--) = a
a = (hl) + e
(hl--) = a
hl--
~~~~
8 times (for each non-berenstain time)
return

overall, for each time:
ignore the 1/100 seconds
take one of the c206-c215 random values 'R' (depends on what c216 is at.)
	take the last 3 bits and add em to the 1/10 seconds, but truncate for 4 bits
	take the first 4 bits and add em to the seconds, and any overflow can go into the 10 seconds and minutes.

---

(hl = 50E1, from 3:4057)
0:0ACD
(C29D) = (hl++)
hl++
(C2A0) = (hl++)
(C2A1) = (hl++)
(C29E) = (hl++)
(C29F) = (hl++)
d, e = (hl++), (hl++)
push hl
hl = de
call 0496
	0:0496
pop hl
(C2A2) = (hl++)
(C2A3) = (hl)
ret


(3:40BC overwrites those last 2 later). they seem to be palette addr, but idk why it isn't in with the rest)

---

supercalled by 3:4091 lol
0:0BF4
store cur chunk and load chunk with sport course shape data
(loop point &)
d, e = (C2E6), (C2E5)
a = (de) - 6A
if a == 0 AND (C22E) == 0
	(C22E), (C22D) = hl - 20
call 0D47
	0:0D47
	hl = 1C56
	if 2a > FF
		h++
	hl += 2a
	a = (hl++)
	push af
	a = (hl)
	h = a
	pop af
	l = a
	de = (C29F) (C29E) + hl
	bc = (C2A1) (C2A0) + hl
	hl = (C2E2) (C2E1)
	store cur chunk and load chunk with sport graphics data
				(by slope point, im imagining falling back down to that chechpoint when the stat check fails. prob a less weird term but idk)
				also let me simplify rq, this next block of code will be labeled WW
											vram bank (FF4F) = 1
													(slope point)
											wait for stat (FF41) = C0
											(hl) = (bc)
											wait for stat (FF41) = C0
											vram bank (FF4F) = 0
													(slope point)
											wait for stat (FF41) = C0
											(hl) = (de)
											wait for stat (FF41) = C0
											inc hl, bc, de
	WW
	WW
	hl += 1E
	de += 1E
	bc += 1E
	WW
	WW
	(C2E2) (C2E1) += 2
	(C2E6) (C2E5) += 1
	reload old chunk, return
if (C2E1) AND 1F != 0, go back to loop point (&)
(C2E1) = (C2E3) - 40
(C2E4) (C2E3) = (C2E3) - 40
if (C2E4) < 98, (C2E4) += 4
(C2E2) = (C2E4)
(C2E8) (C2E7) = (C2E7) - 10
(C2E5) = (C2E7)
(C2E6) = (C2E8)
(C2EA) (C2E9) -= 1
reload orig chunk and return




(what is going on?)
(i would guess there's a lot of 2 byte pointers involved)
from e1 to ea we have...
e1 e2
e3 e4
e5 e6
e7 e8
e9 ea remainder of course length before done


----

3:4000

---

0:032F
load chunk (C203)
jump to (C205) (C204)

0:347
if (C32E) is nonzero,
	load chunk 1F
	call 1F:40DF
	load chunk 1
(C201) += 1
if (C267) is nonzero,
	(C235) += 1
	if (C235) != 6, break out of this if
	else
		(C266) = 1
		(C235) = 0
		if ++(C234) != 0A, break out of these ifs
		else
			(C234) = 0
			if ++(C233) != 0A, break out of these ifs
			else
				(C233) = 0
				if ++(C232) != 06, break out of these ifs
				else
					(C232) = 0
					if ++(C231) != 0A, break out of these ifs
					else
						(C231) = 0
						if ++(C230) != 0A, break out of these ifs
						else
							(C230) = 0, break out of these ifs
if (C29B) != 0,
	d

---

4:4452
theres obvs more function before here, but this is the "did you collide"? and then the "are you in the air? is it a wall? is it a wipeout?" logic

------------
# memory addresses (no $, since lazy)

    0000-3FFF: set ROM (chunk 00/FF)

0B7E: in a big function, activates every time c2d1 needs to loop back from 00 to ff? dunno if it's what makes 00 into ff or if it's just some other cause, prob a cause tbh since it might as well just underflow into ff right?

1270: related to loading a direction into C2BC

1E5(x) , x in {1 2 4 5 6 8 9 A}: directions to load into C2BC


    4000-7FFF: switchable ROM (any chunk ya want)

C200: GBC game checker thing (needs to be 11?)
C201: 
C202: increase every frame which an input happens (as long as 1BBD-1BC1 can happen) (increases nonstop during end times board)
C203: 

C206-C215: are changed every time a button is pressed (one by one: 06 changes, then 07, then 08, ... ,15, 06, 07, ...)
i think they have something to do with random values:? e.g. in the scoreboard time wobbler

C216: only time i've seen it move is in 0:1956, where it's a short that increases by one each time the function is called.

C217: every time a button is pressed (when it does something, e.g. no arrow keys in a cutscene), increments by 1 (goes back to 0 after 0f) (i think related to which of the adresses from C206-C2 are modified? 0xc206 + (c217) = the byte that will be written to (0:193f)

C21F: hz location

C220: direction-adjacent, but not completely
  also decreases during a collision, and increases during recovery
C221: speed
C222: kinda trails speed? (but doesn't work in bike/dirt)

C225: direction of bear

C230 to C235: clock stuff (0 is for the tens place in minutes, 1 is for the ones place in minutes, 2 is for the tens place in seconds, etc.)
C236 to C23B: bruin/freddy time
C23C to C241: mcbear/honey time
C242 to C247: grizzly/lizzy time
C248 to C24D: honeypot/queenie time
C24E to C253: chubb/too-tall time
C254 to C259: broom/ellen time
C25A to C25F: grizzmeyer/marsha time
C260 to C265: brown/tuffy time

C276: jump apex timer. based on speed and the four base ramp jump values
C277: jump ascending/descending timer. based on C278
C278: value to which C277 should rise before apex timer starts ticking, & val at which descent starts at. based on speed and the four base ramp jump values

C279: jump stage checker/memory? 00 is on ground, 01 is ascending, 02 is neither ascending nor descending, 03 is descending

C27F: related to bumper cars (00 when loading in and after ramp, 40 when forced left, 80 when forced right, and c0 (post collision) functions like 00? unrelated but i want hot chocolate, idk why im saying it here but it's a fact jack)

C280: "are we on a jump effect subtile? (if zero, no. otherwise, yes)" equals (C2EF (aka effect val) AND 0C), so throw away all bits except for xxxxXXxx. is only nonzero when effect is 08 (small jump) or 0C (big jump)

C281/C282: x and y position of some object adjacent? they change when you move the box in course select (diff vals from c2b2/c2b3)

C284: stores chunk related number (i've seen bear sprite numbers (07 and 08 only, but theres def more) 1E)

C289: counter-ish? imitates C201 when some button is pressed (and is used in a "compare" infinite loops for LCD i think)

C2B2 and C2B3: x and y position of some object adjacent? they also change when you move the box in course select, though vals are different from c281/c282

C2B8: current menu screen's number (00 is language, 01 is bear, ...)
C2B9: current menu option # selected (e.g. english is 00, spanish 01, ... , brobear is 00, ...)

C2BC: current direction button pressed? (00 is up, 01 is upleft, 02 is right, 03 downright, 04 down, 05 downleft, 06 left, 07 upleft)\

C2BF - C2C3: current long term chosen language, bear, gamemode, sport, and difficulty respectivetly. all are chosen on the menu screen and only update on screen change.

C2CF: screen's x coord? (takes some data form c21f, e.g. 2:4472, though it modifies it a bit)

C2D1: screen's y coord? (loops back to ff when it passes 00) (i think it's related to drawing a new line of tiles? but it might rely on some other y coord variable)
related to vertical location (decreases once per movement, and loops back to FF when under 00) (also does some stuff in the intro sequence (increases once per movement of the TDK intro, to 70) (i'm thinking it's the vertical location of the screen box? like in bgb VRAM viewer, that box's top border)
C2D2: folows C2D1 when in a sport, but lags behind a bit (updated around once every 0.167ms ish? around every 2 increments of C235, or about after C2D1 has changed 5 times. it still lags a bit behind) (5:43af/43b5 and stuff around shows how it changes in bike)


C2E1 and a few after?: i'm thinking pointers to VRAM, since c2e1 changes by 0x40 every 2 vertical tiles traversed, and it changes at the same time that the tiles are updated (plus c2e2 is in the 90s which is very VRAMmy i think, and since 0b7e adds 4 to (c2e2) when the screen value goes from 00 to ff, i think that this is a kind of "go back to the bottom of alotted vram memory" instruction)

C2E5-C2E6: 

C2E9-C2EA: related to the length of the course before it ends (little endian value, when 0A it's ovah, and at 00 bear stops moving)
C2EB: sport/difficulty, in terms of which chunk stores that level data (e.g. tob begin is 0A, tob intermed is 0B, ..., sled begin is 0D, ...)
C2EC: current sport's graphics chunk number (01 02 03 04 05 06)
C2ED: ID of the tile you're on (e.g. for sled, 0x10 is the white snow, 0x20 is the left ramp, ...)
C2EE: a value from 00 to 03 which says which quadrant (or tile/subtile) of a bigtile you're on ((the 0th bit checks whether you're on the left or right of a tile, while the 1st bit is related to being on the top/bottom half of a tile, but idk how to prove it other than with observation) (makes tile effects more intricate) (i also suppose that this paints a good picture of where clips would be available? if i could convert all the tile images to collision tile images, but i dunno how i'd automate that. but like proof of concept, if you see any free subtile diagonals then that's clip potential, as long as you can get there w/o bumping/skidding) (on that idea what in the code does that activate? and why do ramps deactivate it?) 
C2EF: effect of the tile you're on?
C2F0: collisions/wipeouts/nothings? (bumper carsy) (effect and C0)

C32E: kind of a song id thing, which is written to when a song starts/loops/ends (or when the null 0th begins?) silence = 0, title = , menu = 82, trick = 3, crash = 4, finishline = 5, results = 86, medal = 87, courseintro = 8 (same order as data is stored, though the 7th bit has some other purpose in 1F:4079) (not too sure when all the reads happen though) (speaking of writes, the 00 writes either happen in a different spot than the others (1F--4293), or with the rest in 1F--f(4079)'S 40D8) (and for some reason, 4079 gets called twice for a crash)

C330: 
C331-C332: big endian counter for the location in the music?
C333-C334: little endian something for channel 1, updates when audio is output
C335-C336: channel 2 
C337-C338: channel 3 
C339-C33A: channel 4 

C33B: 

DD80-DDBF: reserved for the current palette?

FF26: related to channel 3 output

FF40: LCDC

FF41: STAT
	related to graphics (07D0 uses it when writing each new row of timer pixels)

FF44: LY

FF4B: WIN X

FF68: BG PAL SEL

FF69: BG PAL DATA







c201, c289, 
c2b8, c2b9, c2c1, c29b
c28f, c290, c11f, c297, c28d
c2cc, c2c9, c282, c2cb, c281, c121, c120, c122
c204, c205, c32e, 




clip ability bumper cars potential memory
c227 c221 c27c c21c c28a c289 c224 c27c c21a c21f c2d2 c2d0 c2d1 c2cf

________
which chunks have machine code (tricky things, not pointers and stuff)
FF
01
02
03
04
05
06

1E
1F

3D