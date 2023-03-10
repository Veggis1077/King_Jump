import pygame
import time as t
from pygame import *
from pygame.locals import *

SCREEN_SIZE = pygame.Rect((0, 0, 960, 720))
TILE_SIZE = 32
GRAVITY = (0, 0.3)

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
            self.cam += ((x, y) - self.cam) * 0.05
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
        "                              ",
        "          E                   ",
        "       pppppppppppppppp       ",
        "       p              p       ",
        "       p              p       ",
        "       ppppppppppppppppppp    ",
        "                              ",
        "                              ",
        "            pp                ",
        "               pp             ",
        "                  pp          ",
        "    pppp                      ",
        "                              ",
        "                              ",
        "                              ",
        "                           ppp",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "   ppppp           pppp       ",
        "       p           p          ",
        "       p           p          ",
        "       p                      ",
        "       p                      ",
        "       p                      ",
        "       pppp            ppppp  ",
        "       p  p            p      ",
        "       p  p            p      ",
        "       p  p            p      ",
        "       p  p            p      ",
        "       pppp         pppp      ",
        "                    p         ",
        "                    p         ",
        "                    p         ",
        "       pppp       ppp         ",
        "                              ",
        "ppp                           ",
        "                              ",
        "                              ",
        "       pppp                   ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "ppp                           ",
        "                              ",
        "       pppp                   ",
        "                              ",
        "                              ",
        "                              ",
        "                ppp           ",
        "        ppppppppp p           ",
        "        p         p           ",
        "        ppppppppppp        pppp",
        "                              ",
        "                              ",
        "       ppppp  pppppppp        ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "PPPPP                         ",
        "       PPPPP                  ",
        "                              ",
        "                              ",
        "              PPPP        PPPP",
        "                              ",
        "                              ",
        "                    PPPP      ",
        "                              ",
        "                              ",
        "                              ",
        "             PPPPPP           ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "PPPPPPPPPP           PPPPPPPPP",
        "         P           P        ",
        "         P           P        ",
        "         P           P        ",
        "         P           P        ",
        "         P           P        ",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    
    x = y = 0

    for row in level:
        y += TILE_SIZE
    
    platforms = pygame.sprite.Group()
    player = Player(platforms, (SCREEN_SIZE.width/2, y-300), (24, 34)) #andre argument er startposisjon, (0, 0) er ??verst i venstre krok, tredje argument er hitbox, x og y st??rrelse
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))
    
    pygame.mixer.init()
    mixer.music.load("menuStart.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play()
    startMenu(screen, timer)
    mixer.music.stop()
    mixer.music.load("gameMusic.mp3")
    mixer.music.play()

    x = y = 0
    
    # build the level
    for row in level:
        for col in row:
            if col.lower() == "p":
                Platform((x, y), (TILE_SIZE, TILE_SIZE), platforms, entities)
            if col.lower() == "e":
                ExitBlock((x, y), (TILE_SIZE, TILE_SIZE), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    startTime = pygame.time.get_ticks()
    
    background = pygame.image.load("newBackground.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_SIZE.width, background.get_height()))

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT: 
                return

        entities.update()
        
        screen.blit(background, (0, -625 - player.rect.bottom/10))

        entities.draw(screen)
        
        elapsedTime = (pygame.time.get_ticks() - startTime)/1000
        time = FONT.render(f"{convert(elapsedTime)}", True, (255, 255, 255))
        screen.blit(time, (level_width/50, level_height/200))
        height = FONT.render(f"Height: {round((level_height - 32 - player.rect.bottom)/26)}", True, (255, 255, 255))
        screen.blit(height, (level_width*8/10, 25)) 
        jumps = FONT.render(f"Jumps: {player.jumps}", True, (255, 255, 255))
        screen.blit(jumps, (level_width*8/10, 60))

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
    def __init__(self, platforms, pos, hitbox, *groups):
        super().__init__(Color("#0000FF"), pos, hitbox)
        self.image = pygame.image.load("newPlayer.png").convert()
        self.vel = pygame.Vector2((0, 0))
        self.onGround = True
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 12
        self.jumps = 0
        self.fails = 0
        
    def update(self):
        for platform in self.platforms:
            if isinstance(platform, ExitBlock):
                image = pygame.image.load("door.png").convert()
                image = pygame.transform.scale(image, (66, 50))
                platform.image = image
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
                    endMenu()
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

def startMenu(screen, timer):
    currentMenu = "start"
    menuStart = pygame.image.load("menuStart.png").convert()
    menuQuit = pygame.image.load("menuQuit.png").convert()
    viewingMenu = True
    while viewingMenu:
        for event in pygame.event.get():
            if event.type == QUIT: 
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if currentMenu == "start":
                        viewingMenu = False
                    elif currentMenu == "quit":
                        exit()
                elif event.key == pygame.K_DOWN:
                    currentMenu = "quit"
                elif event.key == pygame.K_UP:
                    currentMenu = "start"
            else:
                if currentMenu == "start":
                    screen.blit(menuStart, (0, 0))
                elif currentMenu == "quit":
                    screen.blit(menuQuit, (0, 0))
                pygame.display.update()
                timer.tick(60)

def endMenu():
    FONT = pygame.font.Font("freesansbold.ttf", 32)
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    timer = pygame.time.Clock()
    startTime = pygame.time.get_ticks()
    viewingMenu = True
    while viewingMenu:
        if (pygame.time.get_ticks() - startTime)/1000 > 5:
            viewingMenu = False
        for event in pygame.event.get():
            if event.type == QUIT: 
                exit()
            screen.fill((0, 0, 0))
            endMessage1 = FONT.render("Congratulations! You escaped the simulation.", True, (255, 255, 255))
            screen.blit(endMessage1, (120, SCREEN_SIZE.height/2))
            endMessage2 = FONT.render("The next one is more challenging. Good luck.", True, (255, 255, 255))
            screen.blit(endMessage2, (120, SCREEN_SIZE.height/2 + 30))
            pygame.display.update()
            timer.tick(60)

def convert(seconds):
    return t.strftime("%H:%M:%S", t.gmtime(seconds))

main()