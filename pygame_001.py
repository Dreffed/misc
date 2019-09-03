import pygame, sys, time
from pygame.locals import *

pygame.init()
WINDOWWIDTH = 200
WINDOWHEIGHT = 300
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

MOVESPEED = 1

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


b1 = {'rect':pygame.Rect(0, 50, 25, 25), 'color':RED, 'dir':DOWNRIGHT}
b2 = {'rect':pygame.Rect(0, 100, 25, 25), 'color':GREEN, 'dir':DOWNRIGHT}
b3 = {'rect':pygame.Rect(0, 150, 25, 25), 'color':BLUE, 'dir':DOWNRIGHT}
blocks = [b1, b2, b3]


while True:
# check for the closing of the 'x' button
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLACK)
    pygame.draw.line(screen,BLUE,(150,0),(150,150),5)


    for b in blocks:
    #moves the blocks
        if b['dir'] == DOWNLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top += MOVESPEED
        if b['dir'] == DOWNRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top += MOVESPEED
        if b['dir'] == UPLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top -= MOVESPEED
        if b['dir'] == UPRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top -= MOVESPEED

    # check if the block has move out of the window
        if b['rect'].top < 0:
        # block has moved past the top
            if b['dir'] == UPLEFT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = DOWNRIGHT
        if b['rect'].bottom > WINDOWHEIGHT:
        # block has moved past the bottom
            if b['dir'] == DOWNLEFT:
                b['dir'] = UPLEFT
            if b['dir'] == DOWNRIGHT:
                b['dir'] = UPRIGHT
        if b['rect'].left < 0:
        # block has moved past the left side
            if b['dir'] == DOWNLEFT:
                b['dir'] = DOWNRIGHT
            if b['dir'] == UPLEFT:
                b['dir'] = UPRIGHT
        if b['rect'].right > WINDOWWIDTH:
        # block has moved past the right side
            if b['dir'] == DOWNRIGHT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = UPLEFT
        if b['dir'] == UPLEFT or b['dir'] == DOWNLEFT: # In this case it's rather easy to check for the exact conditions when direction changes should be made. Being the movement speed is only 1, at some point the b['rect'].right/left will be exactly 150. It's easier to check for that than deal with greater than less than problems which tend to only work for one way. If movement was higher than one you'd have to switch to short ranges instead.
            if b['rect'].left == 150 and b['rect'].top > 0 and b['rect'].top < 150:
                if b['dir'] == DOWNLEFT:
                    b['dir'] = DOWNRIGHT
                if b['dir'] == UPLEFT:
                    b['dir'] = UPRIGHT

        if b['dir'] == DOWNRIGHT or b['dir'] == UPRIGHT:
            if b['rect'].right == 150 and b['rect'].top < 150:
                if b['dir'] == DOWNRIGHT:
                    b['dir'] = DOWNLEFT
                if b['dir'] == UPRIGHT:
                    b['dir'] = UPLEFT
        print(b['rect'].right)
        pygame.draw.rect(screen, b['color'], b['rect'])

    pygame.display.update()
    time.sleep(0.00001)