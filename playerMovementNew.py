import pygame
import time as t
from pygame import *
from pygame.locals import *

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
TILE_SIZE = 32 
GRAVITY = pygame.Vector2((0, 0.3))

level_width = 0
level_height = 0

class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for sprite in self.sprites():
            rec = spritedict[sprite]
            newrect = surface_blit(sprite.image, sprite.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[sprite] = newrect
        return dirty            
            
def main():
    global level_width, level_height
    pygame.init()
    FONT = pygame.font.Font("freesansbold.ttf", 32)
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("King Jump")
    timer = pygame.time.Clock()

    level = [
        "                         ",
        "                  ppppppp",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        " PPPPP                   ",
        "                         ",
        "                         ",
        "                         ",
        "                     PPPP",
        "                         ",
        "                         ",
        "                         ",
        "     PPPPPPPP            ",
        "                         ",
        "                         ",
        "                  PPPPPPP",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "    PPPPPPPPPPP          ",
        "                         ",
        "                         ",
        "                         ",
        "            PPPP         ",
        "              PP         ",
        "               P         ",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",]

    
    platforms = pygame.sprite.Group()
    player = Player(platforms, (25, 1020), (12, 27)) #andre argument er startposisjon, (0, 0) er øverst i venstre krok, tredje argument er hitbox, x og y størrelse
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))
    
    # build the level
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), (TILE_SIZE, TILE_SIZE), platforms, entities)
            if col == "E":
                ExitBlock((x, y), (TILE_SIZE, TILE_SIZE), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0
    
    startTime = pygame.time.get_ticks()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT: 
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        entities.update()

        screen.blit(pygame.image.load("newBackground.jpg").convert(), (0, -875 - player.rect.bottom/10))

        entities.draw(screen)
        
        elapsedTime = (pygame.time.get_ticks() - startTime)/1000
        time = FONT.render(f"{convert(elapsedTime)}", True, (255, 255, 255))
        screen.blit(time, (level_width/50, level_height/50))
        height = FONT.render(f"Height: {round((level_height - 32 - player.rect.bottom)/26)}", True, (255, 255, 255))
        screen.blit(height, (level_width*7/10, 25))
        jumps = FONT.render(f"Jumps: {player.jumps}", True, (255, 255, 255))
        screen.blit(jumps, (level_width*7/10, 60))

        pygame.display.update()
        timer.tick(60)

class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, hitbox, *groups):
        super().__init__(*groups)
        self.image = Surface((hitbox))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    oldHeight = 0
    newHeight = 0
    global level_width, level_height
    def __init__(self, platforms, pos, hitbox, jumps = 0, fails = 0, *groups):
        super().__init__(Color("#0000FF"), pos, hitbox)
        self.image = pygame.image.load("player.png").convert()
        self.vel = pygame.Vector2((0, 0))
        self.onGround = True
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 12
        self.jumps = jumps
        self.fails = fails
        
    def update(self):
        for platform in self.platforms:
            if platform.rect[1] < 500:
                platform.image = pygame.image.load("grass.png").convert()
        pressed = pygame.key.get_pressed()
        
        up = pressed[K_SPACE]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]

        if up and left and self.onGround:
            self.vel.y = -self.jump_strength
            self.vel.x = -self.speed*0.5
            self.jumps += 1
            self.oldHeight = self.rect.bottom
        elif up and right and self.onGround:
            self.vel.y = -self.jump_strength
            self.vel.x = self.speed*0.5
            self.jumps += 1
            self.oldHeight = self.rect.bottom
        elif up and self.onGround:
            self.vel.y = -self.jump_strength
            self.jumps += 1
            self.oldHeight = self.rect.bottom
        if not up and left and self.onGround:
            self.vel.x = -self.speed*0.25
        if not up and right and self.onGround:
            self.vel.x = self.speed*0.25
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.vel += GRAVITY
            # max falling speed
            if self.vel.y > 100:
                self.vel.y = 100
        elif not(left or right):
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        # do x-axis collisions
        self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += self.vel.y
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.vel.y, self.platforms)

        if self.rect.left/2 < 0:
            self.rect.right = level_width
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self, platform):
                    self.rect.left = 0
            
        if self.rect.right > level_width:
            self.rect.left = 0
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self, platform):
                    self.rect.right = level_width

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if isinstance(platform, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = platform.rect.left
                    self.vel.x = 0
                if xvel < 0:
                    self.rect.left = platform.rect.right
                    self.vel.x = 0
                if yvel > 0:
                    self.rect.bottom = platform.rect.top
                    self.onGround = True
                    self.vel.y = 0
                    self.newHeight = self.rect.bottom
                if yvel < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel.y = 0
                #if self.oldHeight - self.newHeight < 0:
                #    print("Fail")

class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)

class ExitBlock(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)

def convert(seconds):
    return t.strftime("%H:%M:%S", t.gmtime(seconds))

main()