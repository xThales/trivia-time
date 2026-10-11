import pygame

from trivia_time.game.question import Question

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (245, 245, 245)
BUTTON_COLOR = (55, 65, 81)
BUTTON_HOVER_COLOR = (75, 95, 125)
CORRECT_COLOR = (34, 139, 94)
INCORRECT_COLOR = (190, 65, 65)


class QuizScreen:
    def __init__(self, screen: pygame.Surface, question: Question) -> None:
        self.screen = screen

        self.title_font = pygame.font.Font(None, 48)
        self.answer_font = pygame.font.Font(None, 32)
        self.feedback_font = pygame.font.Font(None, 30)

        self.selected_answer_index: int | None = None
        self.answer_was_correct: bool | None = None

        self.set_question(question)

    def set_question(self, question: Question) -> None:
        """Update the question and reset answer feedback."""

        self.question = question
        self.selected_answer_index = None
        self.answer_was_correct = None

        self.question_surface = self.title_font.render(question.text, True, TEXT_COLOR)
        screen_rect = self.screen.get_rect()
        self.question_rect = self.question_surface.get_rect(
            center=(screen_rect.centerx, 150)
        )

        button_width = 500
        button_height = 65
        gap = 20
        total_height = (
            len(question.answers) * button_height + (len(question.answers) - 1) * gap
        )
        start_y = (screen_rect.height - total_height) // 2 + 100

        self.answer_rects: list[pygame.Rect] = []

        for index in range(len(question.answers)):
            rect = pygame.Rect(
                0, start_y + index * (button_height + gap), button_width, button_height
            )
            rect.centerx = screen_rect.centerx
            self.answer_rects.append(rect)

    def show_feedback(self, selected_index: int, is_correct: bool) -> None:
        """Display the result of the player's answer."""

        self.selected_answer_index = selected_index
        self.answer_was_correct = is_correct

    def handle_event(self, event: pygame.event.Event) -> int | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(self.answer_rects):
                if rect.collidepoint(event.pos):
                    return index

        return None

    def draw(self) -> None:
        self.screen.blit(self.question_surface, self.question_rect)

        mouse_pos = pygame.mouse.get_pos()

        for index, rect in enumerate(self.answer_rects):
            is_hovered = rect.collidepoint(mouse_pos)

            # Set answer boxes/buttons colors.
            if index == self.selected_answer_index:
                color = CORRECT_COLOR if self.answer_was_correct else INCORRECT_COLOR
            elif (
                self.answer_was_correct is False
                and index == self.question.correct_answer
            ):
                color = CORRECT_COLOR
            elif is_hovered and self.selected_answer_index is None:
                color = BUTTON_HOVER_COLOR
            else:
                color = BUTTON_COLOR

            pygame.draw.rect(self.screen, color, rect, border_radius=10)

            answer_surface = self.answer_font.render(
                self.question.answers[index], True, TEXT_COLOR
            )
            answer_rect = answer_surface.get_rect(center=rect.center)
            self.screen.blit(answer_surface, answer_rect)

        if self.answer_was_correct is not None:
            message = "Correct" if self.answer_was_correct else "Incorrect"
            feedback_surface = self.feedback_font.render(message, True, TEXT_COLOR)
            feedback_rect = feedback_surface.get_rect(
                center=(self.screen.get_rect().centerx, 650)
            )
            self.screen.blit(feedback_surface, feedback_rect)
