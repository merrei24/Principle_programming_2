import pygame
from ball import Game

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ball")

game = Game(screen)
game.run()

pygame.quit()