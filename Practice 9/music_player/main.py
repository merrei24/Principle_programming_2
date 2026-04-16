import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Music Player")

app = MusicPlayer(screen)
app.run()

pygame.quit()