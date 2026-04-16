import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.x = 400
        self.y = 300
        self.r = 25
        self.step = 20

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.x - self.step >= self.r:
                            self.x -= self.step
                    elif event.key == pygame.K_RIGHT:
                        if self.x + self.step <= 800 - self.r:
                            self.x += self.step
                    elif event.key == pygame.K_UP:
                        if self.y - self.step >= self.r:
                            self.y -= self.step
                    elif event.key == pygame.K_DOWN:
                        if self.y + self.step <= 600 - self.r:
                            self.y += self.step

            self.screen.fill((255, 255, 255))
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.r)

            pygame.display.flip()
            self.clock.tick(60)