import pygame
import os

class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.folder = "sample_tracks"
        self.playlist = [f for f in os.listdir(self.folder)]
        self.index = 0

        self.font = pygame.font.SysFont(None, 30)

    def play(self):
        if self.playlist:
            path = os.path.join(self.folder, self.playlist[self.index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play()
                    elif event.key == pygame.K_s:
                        self.stop()
                    elif event.key == pygame.K_n:
                        self.next()
                    elif event.key == pygame.K_b:
                        self.prev()
                    elif event.key == pygame.K_q:
                        self.running = False

            self.screen.fill((255, 255, 255))

            if self.playlist:
                text = self.font.render(self.playlist[self.index], True, (0, 0, 0))
                self.screen.blit(text, (50, 50))

            pygame.display.flip()
            self.clock.tick(30)