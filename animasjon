import pygame
import random
pygame.init()

clock = pygame.time.Clock()
SCREEN_WITH = 500
SCREEN_HEIGTH = 500

screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGTH))

pygame.display.set_caption('Spritescheets')

BG = (50, 50, 50)
sprite_sheet_image = pygame.image.load("char_blue.png")
br = 56

def get_image(sheet, xcor, ycor):
    image = pygame.Surface((56, 56)).convert_alpha()
    image.blit(sheet, (0, 0), ((xcor-1)*br, (ycor-1)*br, 56, 56))
    return image

def running(sheet, ycor, a):

    image = pygame.Surface((56,56)).convert_alpha()
    image.blit(sheet, (0, 0), ((a-1)*br, (ycor-1) * br, 56, 56))
    return image



frame_0 = get_image(sprite_sheet_image, 6, 6)
frame_1 = get_image(sprite_sheet_image, 1, 1)
frame_running = get_image(sprite_sheet_image,random.randint(1,8) ,3 )
#frame_running = running(sprite_sheet_image)
a = pygame.transform.flip(frame_1, True, False)
time_elapsed_since_last_action = 0
counter = 1
b = running(sprite_sheet_image, 3,counter)
c = running(sprite_sheet_image, 2, counter)

run = True
while run:
    #Update background
    screen.fill(BG)

    #temporarily

    screen.blit(frame_0, (56, 56))
    screen.blit(a,(200, 200))
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    dt = clock.tick()

    time_elapsed_since_last_action += dt
    # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
    if time_elapsed_since_last_action > 100:
        b = running(sprite_sheet_image, 3,counter)
        c = running(sprite_sheet_image, 2, counter)
        time_elapsed_since_last_action = 0
        if counter ==8:
            counter = 1
        else:
            counter+=1
    screen.blit(b, (150, 150))
    screen.blit(c, (150, 350))
    pygame.display.update()

pygame.quit()
