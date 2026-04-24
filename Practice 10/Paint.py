import pygame
import sys

pygame.init()

# -------------------
# Screen settings
# -------------------
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# -------------------
# Colors
# -------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

colors = [
    (BLACK, pygame.Rect(20, 20, 50, 50)),
    (RED, pygame.Rect(80, 20, 50, 50)),
    (GREEN, pygame.Rect(140, 20, 50, 50)),
    (BLUE, pygame.Rect(200, 20, 50, 50)),
    (YELLOW, pygame.Rect(260, 20, 50, 50)),
]

# -------------------
# Canvas
# -------------------
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# -------------------
# Tools
# -------------------
tool = "line"   # line / rect / circle / eraser
selected_color = BLACK
drawing = False
start_pos = (0, 0)

font = pygame.font.SysFont("Arial", 22)


def draw_ui():
    screen.fill((240, 240, 240))

    # draw saved canvas
    screen.blit(canvas, (0, 0))

    # top panel background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 90))

    # color palette
    for color, rect in colors:
        pygame.draw.rect(screen, color, rect)

        if color == selected_color:
            pygame.draw.rect(screen, BLACK, rect, 3)

    # tool text
    text = font.render(
        f"Tool: {tool} | Keys: R-Rect  C-Circle  L-Line  E-Eraser",
        True,
        BLACK
    )
    screen.blit(text, (350, 35))


running = True
while running:
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------------------
        # Keyboard controls
        # -------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key == pygame.K_e:
                tool = "eraser"

        # -------------------
        # Mouse pressed
        # -------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # color selection
            clicked_color = False
            for color, rect in colors:
                if rect.collidepoint(x, y):
                    selected_color = color
                    clicked_color = True
                    break

            if not clicked_color:
                drawing = True
                start_pos = event.pos

        # -------------------
        # Mouse released
        # -------------------
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if tool == "line":
                    pygame.draw.line(
                        canvas,
                        selected_color,
                        start_pos,
                        end_pos,
                        4
                    )

                elif tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(end_pos[0] - start_pos[0])
                    h = abs(end_pos[1] - start_pos[1])

                    pygame.draw.rect(
                        canvas,
                        selected_color,
                        (x, y, w, h),
                        3
                    )

                elif tool == "circle":
                    radius = int(
                        ((end_pos[0] - start_pos[0]) ** 2 +
                         (end_pos[1] - start_pos[1]) ** 2) ** 0.5
                    )

                    pygame.draw.circle(
                        canvas,
                        selected_color,
                        start_pos,
                        radius,
                        3
                    )

                drawing = False

        # -------------------
        # Eraser while moving
        # -------------------
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "eraser":
                pygame.draw.circle(
                    canvas,
                    WHITE,
                    event.pos,
                    15
                )

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
