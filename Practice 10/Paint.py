import pygame
import sys

# Pygame-ды бастау
pygame.init()

# Түстер
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Экран өлшемі
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# FPS бақылаушы
FPS = pygame.time.Clock()

# Бастапқы конфигурациялар
drawing = False
draw_color = BLACK
shape = "line"  # "line", "rect", "circle"
start_x = 0
start_y = 0

# Құралдарды көрсету үшін шрифт
font = pygame.font.SysFont("Arial", 20)

# Түстер палитрасы
color_palette = [(BLACK, (10, 10)), (RED, (60, 10)), (GREEN, (110, 10)), (BLUE, (160, 10)), (YELLOW, (210, 10))]
selected_color = BLACK

# Өшіруші (eraser)
eraser_mode = False

# Функциялар
def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))

def draw_circle(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_line(x, y, x2, y2, color, width):
    pygame.draw.line(screen, color, (x, y), (x2, y2), width)

def draw_color_palette():
    # Түстер палитрасын сызу
    for color, pos in color_palette:
        pygame.draw.rect(screen, color, (pos[0], pos[1], 40, 40))
    # Ағымдағы таңдалған түс
    pygame.draw.rect(screen, selected_color, (50, 300, 40, 40), 3)  # Сәйкестік жиегі

def handle_color_selection(x, y):
    global selected_color
    for color, pos in color_palette:
        if pos[0] <= x <= pos[0] + 40 and pos[1] <= y <= pos[1] + 40:
            selected_color = color
            break

def handle_shape_selection(x, y):
    global shape
    if 50 <= x <= 150 and 50 <= y <= 100:
        shape = "line"
    elif 50 <= x <= 150 and 120 <= y <= 170:
        shape = "rect"
    elif 50 <= x <= 150 and 190 <= y <= 240:
        shape = "circle"
    elif 50 <= x <= 150 and 260 <= y <= 310:
        global eraser_mode
        eraser_mode = not eraser_mode

# Негізгі ойын циклі
while True:
    screen.fill(WHITE)

    # Пайдаланушының оқиғаларын өңдеу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_x, start_y = event.pos
            # Пайдаланушы түстерді таңдаса
            if 10 <= start_x <= 50 and 10 <= start_y <= 50:
                handle_color_selection(start_x, start_y)
            # Фигураны немесе құралды таңдау
            if 10 <= start_x <= 50 and 50 <= start_y <= 100:
                handle_shape_selection(start_x, start_y)
            if 10 <= start_x <= 50 and 120 <= start_y <= 170:
                handle_shape_selection(start_x, start_y)
            if 10 <= start_x <= 50 and 190 <= start_y <= 240:
                handle_shape_selection(start_x, start_y)
            if 10 <= start_x <= 50 and 260 <= start_y <= 310:
                handle_shape_selection(start_x, start_y)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            end_x, end_y = event.pos
            if shape == "line":
                draw_line(start_x, start_y, end_x, end_y, selected_color, 3)
            elif shape == "rect":
                draw_rect(start_x, start_y, end_x - start_x, end_y - start_y, selected_color)
            elif shape == "circle":
                radius = int(((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5)
                draw_circle(start_x, start_y, radius, selected_color)
            if eraser_mode:
                draw_rect(start_x - 10, start_y - 10, 20, 20, WHITE)

    draw_color_palette()
    
    pygame.display.flip()
    FPS.tick(60)