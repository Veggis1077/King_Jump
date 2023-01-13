import pygame as pg
from pygame.locals import *

pg.init()

vec = pg.math.Vector2
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
ACC = 0.5
FPS = 60
FONT = pg.font.Font("freesansbold.ttf", 32)
FramePerSec = pg.time.Clock()
window = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pg.display.set_caption("King Jump")

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()
        
        self.pos = vec((100, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def move(self):
        keysPressed = pg.key.get_pressed()

        collisions = pg.sprite.spritecollide(P1, platforms, False)
        if collisions:
            self.vel.y = 0
            self.vel.x = 0
            if keysPressed[K_SPACE] and keysPressed[K_LEFT]:
                self.vel.y = -23
                self.vel.x = -7
            if keysPressed[K_SPACE] and keysPressed[K_RIGHT]:
                self.vel.y = -23
                self.vel.x = 7
            if keysPressed[K_SPACE]:
                self.vel.y = -23
            if keysPressed[K_LEFT]:
                self.pos.x -= 3
            if keysPressed[K_RIGHT]:
                self.pos.x += 3
        else:
            self.acc.y = ACC
                
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
                
        if self.pos.x > window.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = window.get_width()
            
        self.rect.midbottom = self.pos
                
    def distance(self, obj2):
        xDistance = (self.x - obj2.x)**2
        yDistance = (self.y - obj2.y)**2
        totalDistance = (xDistance + yDistance)**(1/2) - self.radius - obj2.radius
        return totalDistance
    
    def update(self):
        collisions = pg.sprite.spritecollide(P1, platforms, False)
        if collisions:
            self.pos.y = collisions[0].rect.top + 1
            self.vel.y = 0
    
class Platform(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pg.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (width/2, WINDOW_HEIGHT - height/2))
        
platform1 = Platform(WINDOW_WIDTH, 20)

P1 = Player()

platforms = pg.sprite.Group()
platforms.add(platform1)

startTime = pg.time.get_ticks()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    window.fill((255, 255, 255))
    
    P1.move()
    P1.update()
    window.blit(P1.surf, P1.rect)
    
    for platform in platforms:
        window.blit(platform.surf, platform.rect)
    
    elapsedTime = (pg.time.get_ticks() - startTime)/1000
    
    text = FONT.render(f"{round(elapsedTime, 1)}", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (WINDOW_WIDTH*19/20, WINDOW_HEIGHT*19/20)
    
    window.blit(text, textRect)
    
    FramePerSec.tick(FPS)
    
    pg.display.update()

pg.quit()