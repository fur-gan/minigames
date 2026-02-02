import pygame
from random import random, randint

class Rectangle:
    def __init__(self, x: float, y: float, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = random() * 3
        self.vy = random() * 3

    @property
    def topLeft(self):
        return self.x, self.y
    
    @property
    def topRight(self):
        return self.x + self.w, self.y
    
    @property
    def bottomLeft(self):
        return self.x, self.y + self.h
    
    @property
    def bottomRight(self):
        return self.x + self.w, self.y + self.h

def isBump():
    if r.x <= w.x or\
       r.x + r.w >= w.x + w.w or\
       r.y <= w.y or\
       r.y + r.h >= w.y + w.h:
        return True
    return False

def bump():
    # floor or ceiling
    if r.y <= w.y or r.y + r.h >= w.y + w.h:
        # flip vy
        r.vy = -r.vy
        return True
    # wall
    if r.x <= w.x or r.x + w.x >= w.x - w.w:
        # flip vx
        r.vx = -r.vx
        return True
    return False

def passTime():
    r.x += r.vx
    r.y += r.vy

def getRandomColor():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    width = 500
    height = 500
    running = True
    fps = 60
    display = pygame.display.set_mode((width, height))

    w = Rectangle(0, 0, width, height)
    r = Rectangle(200, 50, 110, 70)
    color = getRandomColor()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    running = False
                if event.key == ord('r'):
                    running = False

        display.fill((255, 255, 255))
        pygame.draw.rect(display, color, (r.x, r.y, r.w, r.h))

        passTime()

        if isBump():
            color = getRandomColor()
            bump()

        pygame.display.flip()
        clock.tick(fps)
