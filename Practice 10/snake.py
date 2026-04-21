import pygame
import time
import random

pygame.init()

# Түстер
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Экран өлшемі
WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# FPS бақылаушы
FPS = pygame.time.Clock()

block = 10
speed = 10

# Шрифттер
font_lose = pygame.font.SysFont("None", 25)
font_score = pygame.font.SysFont("None", 35)

# Баллды көрсету функциясы
def score(score):
    value = font_score.render("Score: " + str(score), True, YELLOW)
    screen.blit(value, [0, 0])

# Змейктың көрінісі
def snake(block, list):
    for x in list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block, block])

# Хабарлама шығару
def message(msg, color):
    mesg = font_lose.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Ойынның негізгі логикасы
def gameLoop():
    game_over = False
    game_close = False

    # Бастапқы орын
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Тамақтың бастапқы орны
    foodx = round(random.randrange(0, WIDTH - block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            screen.fill(BLUE)
            message("GAME OVER! Press R to Restart or Q to Quit", RED)
            score(Length_of_snake - 1)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # R басқанда ойынды қайта бастау
                        gameLoop()  # Ойынды қайта бастау
                    if event.key == pygame.K_q:  # Q басқанда шығып кету
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    x1_change = -block
                    y1_change = 0
                elif event.key in  [pygame.K_RIGHT, pygame.K_d]:
                    x1_change = block
                    y1_change = 0
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    y1_change = -block
                    x1_change = 0
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    y1_change = block
                    x1_change = 0

        # Шектен шыққан жағдайда ойын аяқталады
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)
        pygame.draw.rect(screen, RED, [foodx, foody, block, block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Змейк өзінің денесімен соқтығысса, ойын аяқталады
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake(block, snake_List)
        score(Length_of_snake - 1)

        # Тамақты жеу жағдайы
        if x1 == foodx and y1 == foody:
            # Тамақ қайта орналасады
            foodx = round(random.randrange(0, WIDTH - block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - block) / 10.0) * 10.0
            Length_of_snake += 1

        pygame.display.flip()

        # FPS бақылау
        FPS.tick(speed)

    pygame.quit()
    quit()

# Ойынды бастау
gameLoop()