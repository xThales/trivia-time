import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60


def run() -> None:

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Trivia Time")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
