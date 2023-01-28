import pygame
pygame.init()
karakterer = "char_blue.png"
class Game:
    def __init__(self):
        self.SCREEN_WITH = 500
        self.SCREEN_HEIGTH = 500
        self.BG = (50, 50, 50)
        self.screen = pygame.display.set_mode((self.SCREEN_WITH, self.SCREEN_HEIGTH))
        pygame.display.set_caption('Spritescheets')  # Navn
        self.sprite_sheet_image = pygame.image.load(karakterer) #Importerer inn karakteren
        self.br = 56
        self.counter = 1 #Counter for løpe hoppe og slå animasjon
        self.clock = pygame.time.Clock() #Lager klokke som skal tikke
        self.hopp = False
        self.lope = False
        self.hoyre = True
        self.sla = False

    def running(self, sheet, rad, a):  # Velger riktig del av char_blue.png og returnerer den delen
        image = pygame.Surface((56, 56)).convert_alpha()
        image.blit(sheet, (0, 0), ((a) * self.br, (rad - 1) * self.br, 56, 56))

        return image

    def game_loop(self):
        time_elapsed_since_last_action = 0  # For å få riktig animasjon
        spacbar_down_time = 0
        run = True
        x_pos = 150 #Bare startverdier for å ha no å gjøre
        y_pos = 150
        while run:
            # Update background
            self.screen.fill(self.BG)

            # temporarily

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        spacbar_down_time = pygame.time.get_ticks()
                        lope = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        spacbar_down_time = (pygame.time.get_ticks() - spacbar_down_time) / 1000
                        print("Spacebar held down for", spacbar_down_time, "seconds")
                elif event.type == pygame.K_Delete:
                    sla = True

            keys = pygame.key.get_pressed()
            x_pos += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 1.5

            if x_pos > self.SCREEN_WITH:
                x_pos -= (self.SCREEN_WITH + 40)
            elif x_pos < -40:
                x_pos += self.SCREEN_WITH

            if keys[pygame.K_LEFT] and not self.hopp:
                self.lope = True
                self.hoyre = False
            elif keys[pygame.K_RIGHT]:
                self.lope = True
                self.hoyre = True
            else:
                self.lope = False
                self.hoyre = True

            dt = self.clock.tick()

            time_elapsed_since_last_action += dt
            # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
            if time_elapsed_since_last_action > 100:
                if self.lope:
                    b = self.running(self.sprite_sheet_image, 3, self.counter % 8)
                else:
                    b = self.running(self.sprite_sheet_image, 1, self.counter % 6)

                c = self.running(self.sprite_sheet_image, 2, self.counter % 6)
                time_elapsed_since_last_action = 0

                self.counter += 1

            if self.hoyre:
                self.screen.blit(b, (x_pos, y_pos))
            else:
                self.screen.blit(pygame.transform.flip(b, True, False), (x_pos, y_pos))
            pygame.display.update()

        pygame.quit()


prove = Game()
prove.game_loop()
