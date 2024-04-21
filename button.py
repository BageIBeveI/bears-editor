# heavily based off of Coding With Russ' videos

import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.action = False

    def draw(self, surface):
        self.action = False
        #find mouse position
        position = pygame.mouse.get_pos()
        #if pygame.mouse.get_pressed()[0]:
            #print(position)

        if self.rect.collidepoint(position) == 1:
            if pygame.mouse.get_pressed()[0]: # and not self.clicked:
                self.action = True
            #elif ygame.mouse.get_pressed()[0] and not self.clicked:
            """
                if self.clicked == False:
                    print(1)
                    self.clicked = True
                    action = True
            elif not pygame.mouse.get_pressed()[0]:
                print(2)
                self.clicked = False
            """

        #if pygame.mouse.get_pressed()[0] == 0:# and self.clicked == True:
            #self.clicked = False
            #print(2)


        #draw button to screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return self.action

    def slowDraw(self, surface):
        self.action = False
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position) == 1:
            if pygame.mouse.get_pressed()[0]: # and not self.clicked:
                self.action = True
                pygame.time.wait(40) # lazy solution so effects and grid don't freak out. increase if too small (or long) a wait
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return self.action