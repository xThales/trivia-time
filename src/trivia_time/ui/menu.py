import pygame


class MainMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        self.title_font = pygame.font.Font(None, 80)
        self.menu_font = pygame.font.Font(None, 48)

        self.title_surface = self.title_font.render(
            "Trivia Time", True, (255, 255, 255)
        )
        self.play_surface = self.menu_font.render("Play", True, (255, 255, 255))

        screen_rect = self.screen.get_rect()
        self.title_rect = self.title_surface.get_rect(
            center=(screen_rect.centerx, screen_rect.top - 80)
        )
        self.play_rect = self.play_surface.get_rect(
            center=(screen_rect.centerx, screen_rect.top + 40)
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN

    def draw(self) -> None:
        self.screen.blit(self.title_surface, self.title_rect)
        self.screen.blit(self.play_surface, self.play_rect)
